from django.core.mail import send_mail


def anc_send_email(email, message):
    
    send_mail(
        subject="ANC Track Notification", 
        message=message, 
        recipient_list=[email], 
        from_email=None, 
        fail_silently=False
        )


# EMAIL PASSWORD = zdia cpwp dvlz esvv