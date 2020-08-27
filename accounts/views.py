from django.shortcuts import render,redirect
from django.contrib import messages,auth
from django.contrib.auth.models import User
from contacts.models import Contact

def register(request):
    if request.method == 'POST':
        #get values
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']

        if password == password2:
            #check user
            if User.objects.filter(username=username).exists():
                messages.error(request,'that user is exist')
                return redirect('register')
            else:
                if User.objects.filter(email=email).exists():
                    messages.error(request,'that email already in use')
                    return redirect('register')
                else:
                    user=User.objects.create_user(username=username,password=password,email=email,
                                                  first_name=first_name,last_name=last_name)
                    #login after register without message
                    # auth.login(request,user)
                    # messages.success(request,'you are log in')
                    # return redirect('index')
                    user.save()
                    messages.success(request,'your are register now you can login')
                    return redirect('login')

        else:
            messages.error(request, 'passwords do not match')
            return redirect('register')
    else:
        return render(request,'accounts/register.html')

def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username,password=password)

        if user is not None:
            auth.login(request,user)
            messages.success(request,'your are now logged in')
            return redirect('dashboard')
        else:
            messages.error(request,'invalid credentials')
            return redirect('login')
    else:
        return render(request, 'accounts/login.html')

def logout(request):
    if request.method == 'POST':
        auth.logout(request)
        messages.success(request,'you are now logout')
        return redirect('index')

def dashboard(request):
    user_contacts = Contact.objects.order_by('-contact_date').filter(user_id=request.user.id)

    context = {
        'contacts' : user_contacts
    }
    return render(request,'accounts/dashboard.html', context)