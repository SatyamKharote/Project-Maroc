import uuid
import math
from base64 import urlsafe_b64decode
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib import messages
from maroc import settings
from django.core.mail import send_mail, EmailMessage
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes, force_str
from .helper import send_forgot_password_mail
from .models import Profile,Contact_table
# from .wl import wl

# Create your views here.


def index(request):
    return render(request, 'index.html')


def service(request):
    return render(request, 'service.html')


def about(request):
    return render(request, 'about.html')


def contact(request):
    if request.method == 'POST':
        user = request.POST['name']
        email = request.POST['email']
        problem = request.POST['problem']
        desc = request.POST['desc']

        con_obj = Contact_table.objects.create(user=user,email=email,problem=problem,desc=desc)
        con_obj.save()
        messages.success(request,"Your Problem is sended to admin. Please wait 2-3 days for furture communication !")
        return render(request, 'index.html')

    return render(request, 'contact.html')

def notavailable(request):
    return render(request, 'notavailable.html')

def signin(request):
    if 'username' in request.session:
        return redirect('home')
    if (request.method == "POST"):
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            request.session['username'] = username
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, "Wrong Credentials !")
            return redirect('signin')
    return render(request, 'signin.html')


def signup(request):
    if request.method == "POST":
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        # username=email.split("@", 1)[0]
        confirmpassword = request.POST['confirmpassword']

        if User.objects.filter(username=username):
            messages.error(request, "Username already exists!")
            return redirect('signin')

        if User.objects.filter(email=email):
            messages.error(request, "Email Account already exists!")
            return redirect('signin')

        if password != confirmpassword:
            messages.error(request, "Password didn't match !")

        if not username.isalnum():
            messages.error(request, "Username must be Alpha-Numeric !")
            return redirect('signin')

        myuser = User.objects.create_user(username, email, password)
        myuser.is_active = False
        myuser.save()
        # messages.success(request,"Your Account has been successfully created. Please Login Here :)")

        # Welcome Email

        subject = "Welcome to Maroc : A Health Application"
        message = "Hello " + myuser.username + ",\n\n" + "Welcome to Maroc, a nutrition consulting website based in India that aims to help clients manage chronic health issues such as weight gain, diabetes, PCOS, and thyroid through personalized diet protocols.\n\nThank you for visiting our website.\n\nWe have also sent you a confidential email, please confirm your email address in order to activate your account.\n\n"
        from_email = settings.EMAIL_HOST_USER
        to_list = [myuser.email]
        send_mail(subject, message, from_email, to_list, fail_silently=True)

        # return redirect('signin')

        # Email Confimation

        current_site = get_current_site(request)
        email_subject = "Confirm your email @ Maroc - A Health Application"
        message2 = render_to_string('email_confirmation.html', {
            'name': myuser.username,
            'domain': current_site.domain
        })
        email = EmailMessage(
            email_subject,
            message2,
            settings.EMAIL_HOST_USER,
            [myuser.email],
        )
        email.fail_silently = True
        email.send()

        return redirect('signin')

    return render(request, 'signup.html')


def home(request):
    if 'username' in request.session:
        context = {
            'username': request.session['username']
        }
        return render(request, 'home.html', context)
    return redirect(signin)


def logout(request):
    if 'username' in request.session:
        request.session.flush()
    return redirect('signin')


def activate(request, uname):

    try:
        myuser = User.objects.get(username=uname)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        myuser = None

    if myuser is not None:
        myuser.is_active = True
        myuser.save()
        login(request, myuser)
        return redirect('home')
    else:
        return render(request, 'activation_failed.html')


def forgot(request):
    try:
        if request.method == 'POST':
            username = request.POST.get('username')
            # print(username)
            if not User.objects.filter(username=username).first():
                messages.success(request, 'Not User found with this Username!')
                return redirect(forgot)

            user_obj = User.objects.get(username=username)
            # print(username)
            token = str(uuid.uuid4())
            # print(username)
            profile_obj = Profile.objects.create(user=user_obj)
            # print(username)
            profile_obj.forget_password_token = token
            # print(username)
            profile_obj.save()
            # print(username)
            send_forgot_password_mail(user_obj.email, user_obj.username, token)

            # print(username)

            messages.success(request, 'An email is sent')
            return redirect(forgot)
    except Exception as e:
        print(e)
    return render(request, 'forgot.html')


def changepassword(request, token, username):
    # context = {}
    try:
        # profile_obj = Profile.objects.get(forget_password_token = token)
        # # print(profile_obj)
        # context = {'username' : {username}}

        # print(profile_obj)

        if request.method == 'POST':
            new_pass = request.POST.get('password')
            con_new_pass = request.POST.get('con_password')
            # username = request.POST.get('username')

            if username is None:
                messages.success(request, 'No User Found!!!')
                # return redirect(f'changepassword/{token}/{username}')

            if new_pass != con_new_pass:
                messages.success(request, 'Both Password should be same')
                # return redirect(f'changepassword/{token}/{username}')

            user_obj = User.objects.get(username=username)
            user_obj.set_password(new_pass)
            user_obj.save()
            return redirect('signin')

    except Exception as e:
        print(e)
    context = {
        username: username
    }
    return render(request, 'changepassword.html', context)


def pcos(request):
    return render(request, 'pcos.html')


def weightloss(request):
    if request.method == 'POST':
        weight = float(request.POST.get('weight'))
        height = float(request.POST.get('height'))
        age = request.POST.get('age')

        weight = weight*2.2046

        height = height/2.54

        ans = weightpredict(height, weight)

        ans = int(ans/2.2046)
        
        
        diet = {
                "general": {
                "breakfast": "poha with vegetables/2 egg white(boiled) + 1 toast multigrain/fresh fruit juice/toned milk(1 glass)",
                "lunch": "1-2 chapatis(mixed grains),vegetables+dal+curd/butter milk bhuna jeera/pepper +salad",
                "Dinner": "low fat panner tikka/soya  uggets + saulted vegetables or roasted /grill/ chicken or fish vegetables with a piece of bread/chapatti",
                "Snakes": "green tea + veg cracker /nuts/1 bowl murmura/apple /green moong /sprouts"
            },
            "0-10": {
                "breakfast": "idli sambar, oatmeal boal,poha /Healthy smoothie/bread - omelette",
                "lunch": "brown rice dal / multigrain chapati and chicken curry /vegetable bowl with chickpeas/chicken sandwich/veggies/rice",
                "Dinner": "vegetable wrap/chicken noodle soup/chapati and soya curry/scrambled eggs/paratha/ raita",
                "Snakes": "Green tea/rusk /whole fruits /nuts/hardboiled Eggs/protein bars"
            },
            "10-20": {
                "breakfast": "cup of milk/green tea,2 almonds with cup of vegetables, 1cup vegetable oats,2walnuts/almods with green tea",
                "lunch": "3 pulka with 1 cup vegetables/1 cup lentils /beans , cup salad and cup curd || 2 serving white rice , 1 cup rajma,1 roti , cup salad and curd. ",
                "Dinner": "3 pulka with dal, 1 cup vegetable,salad || 1 roti , 1 brown rice,cup boiled vegetables, 1 cup dal/mushroom",
                "Snakes": " fresh fruit juice , green tea,coconut water, 1 multigrain biscuit"
            },
            "20-30": {
                "breakfast": "Green tea 1 cup, crunchy oats with skimmed milk or Greek yogurt",
                "lunch": "1 chapati with vegetable/chicken curry",
                "Dinner": "Roasted chicken with veggies or crunchy oats with skimmed milk"
            },
            "30-40": {
                "breakfast": ''' Parathas (plain, paneer, tofu, broccoli and flaxseeds), without any butter or oil
        Upma/ Oats Upma ,Homemade peanut butter (devoid of oil, salt and sugar) slathered on multi-grain bread
        Idli, sambhar with coconut chutney,Oatmeal,Muesli (no sugar) with yoghur ''',
                "lunch": "Traditional Indian meal with chapatis/ bhakris with dal/beans/tofu/paneer, green vegetables, salad and curd",
                "Dinner": "Grilled chicken or roasted fish with vegetables and a bowl of rice"
            }
        }

        weight = weight/2.2046

        loss = ans - weight

        if loss>0:
            diet = "You do not need to lose weight because you are at a healthy weight."
        elif loss<=-10 and loss>=0:
            diet = diet['0-10']
        elif loss<=-20 and loss>=-10:
            diet = diet['10-20']
        elif loss<=-30 and loss>=-20:
           diet =  diet['20-30']
        elif loss<=-40 and loss>=-30:
            diet = diet['30-40']
        else:
           diet =  diet['general']

        import operator

        from_weight = ans -  3
        to_weight = ans + 3

        context = {
            'from':from_weight,
            'to':to_weight,
            'ans': ans,
            'loss' : loss,
            'diet' : diet
        }

        return render(request, 'temp.html', context)


    return render(request, 'weightloss.html')


import joblib
def weightpredict(height, weight):
    val = [[height]]
    cls = joblib.load(
        'D:\\Projects\\Project Maroc\\Maroc\\maroc-env\\projects\\maroc\\app\\weightloss.sav')
    ans = cls.predict(val)
    return ans

def temp(request):
    return render(request, 'temp.html')
