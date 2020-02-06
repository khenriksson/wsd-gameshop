from django.shortcuts import render, redirect, get_object_or_404, get_list_or_404
from django.http import HttpResponse, Http404, HttpResponseNotFound
from django.template import loader
from django.contrib import messages
from django.contrib.auth import login, authenticate, get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import BadHeaderError, send_mail
from django.core import serializers
from django.db import transaction
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from django.db import connection


from .tokens import account_activation_token
from hashlib import md5
from urllib.parse import urlencode
import json

from .models import Game, UserProfile, Transaction, User, GameData
from .forms import SignUpForm, AddGameForm, EditProfileForm, EditGame




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
    except Game.DoesNotExist:
        raise Http404("Game does not exist")
    return render(request, 'webshop/detail.html', {'game': game})

def signup(request):
    if request.user.is_authenticated:
        return redirect('index')
    else: 
        if request.method == 'POST':
                form = SignUpForm(request.POST)
                if form.is_valid():
                    user = form.save(commit=False)
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
                    return HttpResponse('Please confirm your email address to complete the registration')
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
        gameData = GameData.objects.get(game = game, user = user)
        gameState = gameData.gameInfo
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
	
			
		pelit=Game.objects.filter(developer_id=request.user.pk)#get_object_or_404(Game,developer_id=request.user.pk) 
			
			
		##Adding all of the games data (i.e title...) that user in developer into dictionary
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
				
		data2={'data':data}
		return render(request,"webshop/your_games.html",data2)
		#pass
	
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
			raise Http404
	raise Http404
	
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
        login(request, user)
        return HttpResponse('Thank you for your email confirmation. Now you can login your account.')
    else:
        return HttpResponse('Activation link is invalid!')

#PAYMENT METHODS DOWN HERE

# def payment(request):
#     return render(request, 'webshop/payment.html')

@transaction.atomic
def payment(request):
    # This code executes inside a transaction.
    #game = get_object_or_404(Game, pk=request.game.id)
    #price = game.price
    # buyer = get_object_or_404(User, pk=request.user)

    sid = "l1YLtkV4YW1wbGU="
    pid = "payment1"
    amount = "9.95"
    secret = "1f08IXzzUNKUSye_5LTWy78t83wA"
    checksumstr = "pid={pid:s}&sid={sid:s}&amount={amount:.2f}&token={secret:s}"
    checksum = md5(checksumstr.encode('utf-8')).hexdigest()
    bankapi = 'https://tilkkutakki.cs.aalto.fi/payments/pay'
    print(checksum)
    query = urlencode({
        'pid': pid, 'sid': sid, 'amount': amount,
        'checksum': checksum,
        'success_url': 'http://localhost:8000/payment/success',
        'cancel_url': 'http://localhost:8000/payment/cancel',
        'error_url': 'http://localhost:8000/payment/error'})

    return redirect(bankapi + '?' + query)
