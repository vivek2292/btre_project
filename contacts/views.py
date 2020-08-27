from django.shortcuts import render,redirect
from .models import Contact
from django.core.mail import send_mail
from django.contrib import messages

def contact(request):
    if request.method=="POST":
        listing_id = request.POST['listing_id']
        listing = request.POST['listing']
        name = request.POST['name']
        email = request.POST['email']
        phone = request.POST['phone']
        message = request.POST['message']
        user_id = request.POST['user_id']
        realtor_email = request.POST['realtor_email']

        #check if user had alredy entered the form
        if request.user.is_authenticated:
            user_id = request.user.id
            has_contacted = Contact.objects.all().filter(listing_id=listing_id,user_id=user_id)
            if has_contacted:
                messages.error(request,'you have already made an request')
                return redirect('/listings/' + listing_id)

        contact =Contact(listing=listing,listing_id=listing_id,name=name,email=email,phone=phone,message=message
                    ,user_id=user_id)

        contact.save()

        #send email
        send_mail(
            'property listing inquery',
            'There has been inquery for'+listing+'. Sign into the admin panel for more info',
            'vivekthakurkbl@gmail.com',
            [realtor_email,'vivekthakurkbl@gmail.com'],
            fail_silently = False
        )

        messages.success(request,'your from has been submited an realtor will get back to you')
        return redirect('/listings/'+listing_id)