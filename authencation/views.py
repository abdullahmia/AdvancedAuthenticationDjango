from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, logout, login
from django.contrib.sessions.models import Session
from django.core.mail import EmailMessage

# To Activate Account Import Thoose Module
from django.urls import reverse
from django.utils.encoding import force_bytes, force_text, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.sites.shortcuts import get_current_site

# other File for advanced_login
from .utils import token_ganetor

# Create your views here.
def user_login(request):
    if request.session.has_key('is_logged'):
        return redirect('dashboard')
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        print(email)
        print(password)

        user_logins = authenticate(username=email, password=password)

        if user_logins is not None:
            login(request, user_logins)
            request.session['is_logged'] = True
            messages.add_message(request, messages.INFO, 'Account Login Successfully')
            return redirect('dashboard')
        else:
            messages.add_message(request, messages.INFO, 'No Such User')


    return render(request, 'login.html')


def user_signup(request):
    if request.method == "POST":
        if '@bsdi-bd.org' in request.POST['email']:
            if request.POST['password'] == request.POST['cpassword']:
                name = request.POST.get('name')
                email = request.POST.get('email')
                password = request.POST.get('password')

                user_check = User.objects.filter(username=email)
                if user_check:
                    messages.error(request, 'The Email is allready Taken, Try something New')
                    return redirect('user_signup')

                user_creation = User.objects.create_user(first_name=name, username=email, password=password)
                user_creation.is_active = False
                user_creation.save()

                # Path to View
                # --getting domain we are on
                # -- relative url to varification
                # --encode uid
                # --token


                uidb64 = urlsafe_base64_encode(force_bytes(user_creation.pk))
                domain = get_current_site(request).domain
                link = reverse('activate_account', kwargs={'uidb64': uidb64, 'token': token_ganetor.make_token(user_creation)})
                activate_link = "http://" + domain + link


                email_subject = 'Activae Your Account'
                email_body = 'Hi ' + user_creation.first_name + " " + "Please use this link to activate your Account\n" + activate_link
                email = EmailMessage(
                    email_subject,
                    email_body,
                    'kabirsing23423323@gmail.com',
                    [email],
                )
                email.send(fail_silently=False)
                messages.add_message(request, messages.INFO, 'Account Create Successfully')


            else:
                messages.error(request, "Your Password was don't match")
                return redirect('user_signup')
        else:
            messages.add_message(request, messages.ERROR, 'Try with Bsdi Email Address...😃😃😃😃😃')

    return render(request, 'signup.html')

#

def VarificationView(request, uidb64, token):

    try:
        id = force_text(urlsafe_base64_decode(uidb64))
        # To check User
        user = User.objects.get(pk=id)

        if not token_ganetor.check_token(user, token):
            messages.add_message(request, messages.INFO, "Account already Activcated")
            return redirect('user_login')

        if user.is_active:
            return redirect('user_login')
        user.is_active = True
        user.save()
        messages.add_message(request, messages.SUCCESS, 'Account Activated... Try to login')
        return redirect('user_login')

    except Exception as e:
        pass

# class VarificationView(view):
#     def get(self, request, uidb64, token):
#         return redirect('user_login')


def user_logout(request):
    logout(request)
    return redirect('user_login')


def dashboard(request):
    if request.session.has_key('is_logged'):
        return render(request, 'admin_dashboard.html')
    else:
        return redirect('user_login')

