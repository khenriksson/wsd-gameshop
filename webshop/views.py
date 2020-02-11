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




def webshop(request):
    all_games = Game.objects.all()
    template = loader.get_template('webshop/index.html')
    context = {
        'all_games': all_games,
    }
    return HttpResponse(template.render(context, request))

def search_games(request, search_text):
    filtered_games = []
    '''search_text = "test"'''
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
    if request.user.is_authenticated:
        return redirect('index')
    else: 
        if request.method == 'POST':
                form = SignUpForm(request.POST)
                if form.is_valid():
                    user = form.save(commit=False)
                    group = request.POST.get('group')
                    if group == 'Developers':
                        my_group = Group.objects.get(name='Developers') 
                        my_group.user_set.add(user)
                    # username = form.cleaned_data.get('username')
                    #login(request, user, backend='django.contrib.auth.backends.ModelBackend')
                    user.is_active = False
                    user.save()
                    current_site = get_current_site(request)
                    # Sending the confirmation email
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
    
    if request.user.is_authenticated:

        game = Game()
        user = request.user
        if request.method == 'POST':
            form = AddGameForm(request.POST)
            if form.is_valid():
                game = form.save(commit = False)
                game.developer = user
                #game.picture_url='https://store-images.s-microsoft.com/image/apps.58949.14571142807322667.df9fc94b-3bd3-4ec2-b7a2-423331d84b17.5883e11e-8555-4114-83b7-72d1cb12cd6e?mode=scale&q=90&h=1080&w=1920'
                
                game.save()
                return redirect('index')   
        else:
            form = AddGameForm()
        return render(request, 'webshop/addgame.html', {'form': form})
    else: return redirect('index')

def savegame(request):
    if request.method == 'POST':
        game = request.POST['gameID']
        user = request.user
        gameInfo = request.POST['gameState']
        try:
            gameData = GameData.objects.get(game = game,
            user = user)
            gameData.gameInfo = gameInfo
            gameData.save()
        except:
            gameData = GameData(game = game, user = user,
            gameInfo = gameInfo)
            gameData.save()
    return HttpResponse("data saved")

def loadgame(request):
    if request.method == 'POST':
        game = request.POST['gameID']
        user = request.user
        #Need to add: checking if loaded state exists
        try:
            gameData = GameData.objects.get(game = game, user = user)
            gameState = gameData.gameInfo
        except:
            gameState = ''
    return HttpResponse(gameState)

def savescore(request):
    if request.method == 'POST':
        game = request.POST['gameID']
        score = request.POST['score']
        user = request.user
        try:
            gameData = GameData.objects.get(game = game,
            user = user)
            if (int(score) > gameData.score):
                gameData.score = score
                gameData.save()
        except:
            gameData = GameData(game = game, user = user, score = score)
            gameData.save()
    return HttpResponse("score saved")

def highscore(request):
    if request.method == 'GET':
        game = request.GET['gameID']
        #testing with only top1
        filtered = GameData.objects.filter(game=game).order_by('-score')[:3]
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
            
        pelit =Game.objects.filter(developer_id=request.user.pk)#get_object_or_404(Game,developer_id=request.user.pk) 
        allgames = Game.objects.all()
        # own =  Transaction.objects.filter(buyer=request.user, state='Confirmed')
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
        for x in range(0,len(pelit)):
            data[str(pelit[x].id)]={
                'data':
                {
                'id':str(pelit[x].id),
                'title':pelit[x].game_title,
                'description': pelit[x].description,
                'bought':str(pelit[x].times_bought),
                'url':pelit[x].game_url,
                'picurl':pelit[x].picture_url,
                'price':str(pelit[x].price),
                
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
	
	## Note to self: Using Pk as a game value sounds like a bad idea.
	if request.user.is_authenticated:
		
		with connection.cursor() as cs:	
			cs.execute("SELECT * FROM webshop_game WHERE developer_id=="+str(request.user.pk))
			games={'data': cs.fetchall()}
		if bool(games['data']):
			print(bool(games['data']))
			#Game excists
			##Checking if user really has the game.
			print("Value: ",value)
			peli=get_object_or_404(Game,pk=value) 
		
			form = EditGame(request.POST or None,initial={'game_title':peli.game_title,'description':peli.description,'price':peli.price,'game_url':peli.game_url,'picture_url':peli.picture_url})
			if request.method=='POST':
				
				
				if form.is_valid():
					
					for i in ('game_title','description','price','game_url','picture_url'):
						print(request.POST[i])
					
					peli.game_title = request.POST['game_title']
					peli.description = request.POST['description']
					peli.price = request.POST['price']
					peli.game_url = request.POST['game_url']
					peli.picture_url = request.POST['picture_url']
					peli.save()
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

#                    domain = 'http://' + str(get_current_site(request))

                    print(domain)
                    query = urlencode({
                    'pid': pid, 'sid': sid, 'amount': amount,
                    'checksum': checksum,
                    'success_url':  domain + '/payment/success',

                    'cancel_url': domain + '/payment/cancel',
                    'error_url': domain + '/payment/error'})

#                    'cancel_url':  domain + '/payment/cancel',
#                    'error_url':  domain + '/payment/error'})


            except IntegrityError:
                return render(request, 'payment/error.html',{'error':"You already own the game."})
    else:
        return render(request, 'payment/error.html', {'error':"You already own the game."})

    #checksumstr = f"pid={pid:s}&sid={sid:s}&amount={amount:.2f}&token={secret:s}"
    

    

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

