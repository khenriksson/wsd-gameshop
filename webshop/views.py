from django.shortcuts import render, redirect, get_object_or_404, get_list_or_404
from django.http import HttpResponse, Http404, HttpResponseNotFound
from django.template import loader
from django.contrib import messages
from django.contrib.auth import login, authenticate, get_user_model
from django.contrib.auth.models import Group
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import BadHeaderError, send_mail
from django.core import serializers
from django.db import transaction, IntegrityError
from django.core.exceptions import ValidationError
from django.utils import timezone
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from django.db import connection

from urllib.parse import urlencode
import json
from hashlib import md5
from uuid import uuid4

from .models import Game, UserProfile, Transaction, User, GameData
from .forms import SignUpForm, AddGameForm, EditProfileForm, EditGame
from .tokens import account_activation_token



# Rendering front page
def webshop(request):
    all_games = Game.objects.all()
    template = loader.get_template('webshop/index.html')
    context = {
        'all_games': all_games,
    }
    return HttpResponse(template.render(context, request))

# Rendering games filtered based on a search from the navbar
def search_games(request, search_text):
    filtered_games = []
    for game in Game.objects.all():
        if search_text in game.game_title:
            filtered_games.append(game)
    template = loader.get_template('webshop/search.html')
    context = {
        'filtered_games': filtered_games,
    }
    if not filtered_games:
        return render(request, 'webshop/wronggame.html', {'search_text': search_text})
    else:
        return HttpResponse(template.render(context, request))
    

#
def detail(request, game_id):
    try:
        game = Game.objects.get(pk=game_id)
        if request.user.is_authenticated:
            owned = Transaction.objects.filter(buyer=request.user, game=game, state='Confirmed').exists()
            own = Game.objects.filter(developer=request.user).exists()
            test = 'no'
            if owned or own:
                test ='yes'
            return render(request, 'webshop/detail.html', {'game': game, 'test': test })
    except Game.DoesNotExist:
        raise Http404("Game does not exist")
    return render(request, 'webshop/detail.html', {'game': game })

def signup(request):
    # Quick check for making sure that the user is authenticated when 
    # clicking the signup button, and if case they're already logged in
    # it will redirect to the front page
    if request.user.is_authenticated:
        return redirect('index')
    else: 
        # If the user isn't logged in then redirecting to the signup form
        if request.method == 'POST':
                form = SignUpForm(request.POST)
                if form.is_valid():
                    user = form.save(commit=False)
                    user.is_active = False
                    user.save()
                    # Adding user to group Developers based on form selection
                    is_dev = form.cleaned_data.get('is_dev')
                    if is_dev == 'Developer':
                        my_group, created = Group.objects.get_or_create(name='Developers') 
                        my_group.user_set.add(user)
                    # Sending the confirmation email
                    # The email backend can be changed in the 
                    current_site = get_current_site(request)
                    subject = 'Activate your account.'
                    message = render_to_string('webshop/activate_email.html', {
                        'user': user,
                        'domain': current_site.domain,
                        'uid':urlsafe_base64_encode(force_bytes(user.id)),
                        'token':account_activation_token.make_token(user),
                    })
                    
                    send_email(request, user.email, subject, message)
                    messages.success(request, ('Please Confirm your email to complete registration.'))
                    return render(request, 'webshop/activation.html', {'text': 'Please confirm your email address to complete the registration'})
                    #redirect('index') 
        else:
            form = SignUpForm()
        return render(request, 'webshop/signup.html', {'form': form})
    

def addgame(request):
    ## Checking if player is logged in and has developers status
    if request.user.is_authenticated and request.user.groups.filter(name__in=['Developers']).exists():
        game = Game()
        user = request.user
        ## checking if form is posted and is valid.
        if request.method == 'POST':
            form = AddGameForm(request.POST)
            if form.is_valid():
                game = form.save(commit = False)
                game.developer = user
                game.save()
                return redirect('index')   
        else:
            ##Sending form to be filled.
            form = AddGameForm()
        return render(request, 'webshop/addgame.html', {'form': form})
    else: return redirect('index')

# Handling the request to save a gamestate 
def savegame(request):
    if request.method == 'POST':
        game = request.POST['gameID']
        user = request.user
        gameInfo = request.POST['gameState']
        try:
            # If a previous gamestate is saved for the user in the game, overwrite it
            gameData = GameData.objects.get(game = game,
            user = user)
            gameData.gameInfo = gameInfo
            gameData.save()
        except:
            # If no previous saved gamestate exists, creating a new GameData object and saving it
            gameData = GameData(game = game, user = user,
            gameInfo = gameInfo)
            gameData.save()
    return HttpResponse("data saved")

# Handling the request to load a previously saved gamestate
def loadgame(request):
    if request.method == 'POST':
        game = request.POST['gameID']
        user = request.user
        try:
            # If a gamestate can be found
            gameData = GameData.objects.get(game = game, user = user)
            gameState = gameData.gameInfo
        except:
            # If no saved gamestate exists
            gameState = ''
    return HttpResponse(gameState)

# Handling the request to save a score from a game
def savescore(request):
    if request.method == 'POST':
        game = request.POST['gameID']
        score = request.POST['score']
        user = request.user
        try:
            # If a previous score exists for the user, check if the current score is higher
            gameData = GameData.objects.get(game = game,
            user = user)
            if (int(score) > gameData.score):
                gameData.score = score
                gameData.save()
        except:
            # If no previous score exists, saving a new GameData object
            gameData = GameData(game = game, user = user, score = score)
            gameData.save()
    return HttpResponse("score saved")

# Retreiving the top 10 scores from GameData objects
def highscore(request):
    if request.method == 'GET':
        game = request.GET['gameID']
        filtered = GameData.objects.filter(game=game).order_by('-score')[:10]
        top10 = serializers.serialize("json", filtered, fields = ('user', 'score'))
    return HttpResponse(json.dumps(top10), content_type="application/json")


def get_user(user):
    try:
        user = UserProfile.objects.get(user=user)
    except UserProfile.DoesNotExist:
        user = None
    

def profile(request):
    return render(request, 'webshop/profile.html')


def your_games(request):
    if request.user.is_authenticated:
        data={}
        own_games={}	
        #Getting all developers games and all games    
        devgames=Game.objects.filter(developer_id=request.user.pk)#get_object_or_404(Game,developer_id=request.user.pk) 
        allgames = Game.objects.all()
        # Does user own the game? if so add it to own_games
        for i in range(0, len(allgames)):
            if ( Transaction.objects.filter(buyer=request.user, game=i, state='Confirmed')):
            
                own_games[str(allgames[i].id)]={
                    'own_games':
                    {
                    'id':str(allgames[i].id),
                    'title':allgames[i].game_title,
                    'description': allgames[i].description,
                    'bought':str(allgames[i].times_bought),
                    'url':allgames[i].game_url,
                    'picurl':allgames[i].picture_url,
                    'price':str(allgames[i].price),
                    },
                }
        #Adding all of the games data (i.e title...) that user in developer into dictionary
        for x in range(0,len(devgames)):
            data[str(devgames[x].id)]={
                'data':
                {
                'id':str(devgames[x].id),
                'title':devgames[x].game_title,
                'description': devgames[x].description,
                'bought':str(devgames[x].times_bought),
                'url':devgames[x].game_url,
                'picurl':devgames[x].picture_url,
                'price':str(devgames[x].price),
                
                },
                }

        
                

        return render(request,"webshop/your_games.html",{'data': data, 'own_games':own_games})
    else:
        return Http404
	
def remove_game(request,value):
	
	if request.user.is_authenticated:
		##Checking if user owns the game.
		
		peli=get_object_or_404(Game,pk=value, developer_id=request.user.pk)
		##Remove the game
		Game.objects.filter(id=peli.pk).delete()
		
		
		##Return to your_games
		return redirect('/webshop/your_games')
	else:
		return Http404
	'''
	with connection.cursor() as cs:
		cs.execute("REMOVE * From webshop_game")
	'''	

	
def game(request,value):
	##Modify the game
	## Note to self: Using Pk as a game value sounds like a bad idea.
	if request.user.is_authenticated:
		# Checking: Does user own this game
		'''
		with connection.cursor() as cs:	
			cs.execute("SELECT * FROM webshop_game WHERE developer_id=="+str(request.user.pk))
			games={'data': cs.fetchall()}
		if bool(games['data']):
		'''	
		#Game excists
		##Checking if user really has the game.
		##Getting games that user owns.
		game=get_object_or_404(Game,pk=value, developer_id=str(request.user.pk)) 
		
		form = EditGame(request.POST or None,initial={'game_title':peli.game_title,'description':peli.description,'price':peli.price,'game_url':peli.game_url,'picture_url':peli.picture_url})
		if request.method=='POST':
				
			## Form is valid and is posted. -Compiling the data to proper format.
			if form.is_valid():
				game.game_title = request.POST['game_title']
				game.description = request.POST['description']
				game.price = request.POST['price']
				game.game_url = request.POST['game_url']
				game.picture_url = request.POST['picture_url']
				game.save()
				return redirect('/webshop/your_games')
				
			
			context = {
				"game": form,
				"val": value
				}
						
			return render(request, "webshop/game.html",context)	
		else:
			return Http404
	return Http404
	
##Custom 404 page	
def chandler404(request,exception,template='webshop/404.html'):
	response= render(request,template)
	response.status_code=404
	return response

# Updating a user's status by adding them to the Group 'Developers'
def update_dev(request):
    my_group, created = Group.objects.get_or_create(name='Developers') 
    my_group.user_set.add(request.user)
    return redirect('profile')

# Handling the request to edit a user's personal information sent through an EditProfileForm
def edit_profile(request):
    if request.user.is_authenticated:
        user = request.user
        form = EditProfileForm(request.POST or None, initial={'first_name':user.first_name, 'last_name':user.last_name, 'email':user.email})
        if request.method == 'POST':
            if form.is_valid():
                user.first_name = request.POST['first_name']
                user.last_name = request.POST['last_name']
                user.email = request.POST['email']
                user.save()
                return redirect('profile')
        context = {
        "form": form
        }
        return render(request, 'webshop/edit_profile.html', context)
    else:
        return redirect('index')


# A secure way of sending the registered emails
def send_email(request, user_email, subject, message):
    try:
        # No way to do header injections
        subject = request.POST.get('subject', subject)
        message = request.POST.get('message', message)
        from_email = request.POST.get('from_email', 'noreply@kuubatiimi.com')
        if subject and message and from_email:
            try:
                send_mail(subject, message, from_email, [user_email])
            except BadHeaderError:
                return HttpResponse('Invalid header found.')
            return redirect('index')
        else:
            return HttpResponse('Make sure all fields are entered and valid.')
    except UserProfile.DoesNotExist:
        raise Http404("User does not exist")
    


def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = get_object_or_404(User, pk=uid)
    except(TypeError, ValueError, OverflowError, UserProfile.DoesNotExist):
        raise Http404("No user found")
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user, backend='django.contrib.auth.backends.ModelBackend')
        return render(request, 'webshop/activation.html', {'text': 'Thank you for your email confirmation. Now you can login your account.'}) 
    else:
        return render(request, 'webshop/activation.html', {'text': 'Link is inactive!'})

#PAYMENT METHODS DOWN HERE

@login_required
@transaction.atomic()
def payment(request, game_id):
    # This code executes inside a transaction.
    user = request.user.id
    buyer = get_object_or_404(User, pk=user)
    game = get_object_or_404(Game, pk=game_id)
    amount = game.price

    pid = str(uuid4()) # Generate this everytime
    sid = "tb6AYmthc3Blcg==" #Constant 
    secret = "hzTsouE5tl3Zrp7CvofAtMnxLEEA" #Constant
 
    owned = Transaction.objects.filter(buyer=buyer, game=game, state='Confirmed').exists()
    own = Game.objects.filter(developer=buyer).exists()

    if not owned:
        if own:
            return render(request, 'payment/error.html', {'error':"You cannot buy your own game."})
        else: 
            try:
                with transaction.atomic():
                    payment = Transaction(buyer=buyer,  game=game, pid=pid)
                    checksumstr = "pid={}&sid={}&amount={}&token={}".format(pid,
                                                                    sid,
                                                                    amount,
                                                                    secret)
                    checksum = md5(checksumstr.encode('utf-8')).hexdigest()
                    payment.save()
                    bankapi = 'https://tilkkutakki.cs.aalto.fi/payments/pay'
                    domain ='https://' + str(get_current_site(request))
                    print(domain)
                    query = urlencode({
                    'pid': pid, 'sid': sid, 'amount': amount,
                    'checksum': checksum,
                    'success_url':  domain + '/payment/success',
                    'cancel_url': domain + '/payment/cancel',
                    'error_url': domain + '/payment/error'})

            except IntegrityError:
                return render(request, 'payment/error.html',{'error':"You already own the game."})
    else:
        return render(request, 'payment/error.html', {'error':"You already own the game."})

    return redirect(bankapi + '?' + query)


def error(request):
    pid = request.GET['pid']
    data = get_object_or_404(Transaction, pid=pid)
    if data.state == 'Pending':
        data.state ='Rejected'
        data.save()
        return render(request, 'payment/error.html')
    return render(request, 'payment/error.html')

    
def cancel(request):
    pid = request.GET['pid']
    data = get_object_or_404(Transaction, pid=pid)
    if data.state == 'Pending':
        data.state ='Rejected'
        data.save()
        return render(request, 'payment/cancel.html')
    return render(request, 'payment/cancel.html')


def success(request):
    if request.GET.get('result') == 'success':
        pid = request.GET['pid']
        data = get_object_or_404(Transaction, pid=pid)
        game = get_object_or_404(Game, pk=data.game.id)
        if data.state == 'Pending':
            print(data.state)
            data.state ='Confirmed'
            data.buy_completed = timezone.now()
            data.save()
            game.times_bought += 1
            game.save() 
            return render(request, 'payment/success.html')
        elif data.state == 'Confirmed':
            return render(request, 'payment/owned.html')
    return render(request, 'payment/error.html')

