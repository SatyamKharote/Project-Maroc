from django.core.mail import send_mail
from maroc import settings

def send_forgot_password_mail(email,username,token):
    subject = 'Your Forgot Password Link'
    message = f'Hi, click on linmk to reset your password http://127.0.0.1:8000/changepassword/{token}/{username}'
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [email]
    send_mail(subject,message,email_from,recipient_list)
    return True