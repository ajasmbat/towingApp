from django.shortcuts import render, redirect, HttpResponse
from .forms import MyUserForm, LoginUserForm
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .models import Location, MyUser
from webpush import send_user_notification
from django.views.decorators.http import require_GET
from django.http.response import JsonResponse, HttpResponse
from django.views.decorators.http import require_GET, require_POST
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from webpush import send_user_notification
import json
from django.conf import settings
from django.contrib.auth import authenticate, login as log, logout
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator



def register(request):
    if request.method == 'POST':
        form = MyUserForm(request.POST)
        
        if form.is_valid():
            cleaned_data = form.cleaned_data
            
            phoneNumber = cleaned_data['phoneNumber']
            password = cleaned_data['password']
            phone_validator = RegexValidator(r'^\d{10}$', 'Phone number must have exactly 10 digits.')
            try:
                validate_password(password, user=phoneNumber)  # Validate the password
            except ValidationError as validation_errors:
                form.add_error('password', validation_errors)
            
            
            
            try:
                phone_validator(phoneNumber)
            except ValidationError as validation_error:
                form.add_error('phoneNumber', validation_error.message)
                
            if form.errors:
                return render(request, 'myApp/register.html', {'form': form})
            
            form.save()
            
            user = authenticate(request, phoneNumber=phoneNumber, password=password)
            if user is not None:
                log(request, user)
                return redirect('home')  # Redirect to the home page after successful registration
        
        
    else:
        form = MyUserForm()
        
    return render(request, 'myApp/register.html', {'form': form})

def login(request):
    if request.method =="POST":
        form = LoginUserForm(request.POST)

        

        if form.is_valid():
            clean = form.cleaned_data
            
            user = authenticate(phoneNumber = clean['phoneNumber'],password=clean['password'])

        

            if user:
                
                if user.is_active:
                    
                    log(request,user)

                    return redirect('home')
                
            else:

                error = "Wrong UserName Or Password"

                return render(request, 'myApp/login.html',{'form':form,'error':error})

            


            
    
    else:
        form = LoginUserForm()
        

    return render(request, 'myApp/login.html',{'form':form})


def signout(request):
    logout(request)
    return redirect('home')

@login_required(login_url='/')
def requestHelp(request):
    if request.method == "POST":
        data = json.loads(request.body)
        location = Location()

        location.user = request.user
        location.long = data.get('long')
        location.lat = data.get('lat')

        location.alert()

        location.save()
        

        
        
        
      
        response_data = {
            "message": "Location received successfully",
            
        }
        return JsonResponse(response_data)
    else:
        return render(request,"myApp/request.html")



@login_required(login_url='/')
def superUserManagerTerminal(request):
    webpush_settings = getattr(settings, 'WEBPUSH_SETTINGS', {})
    vapid_key = webpush_settings.get('VAPID_PUBLIC_KEY')
    user = request.user

    if request.user.is_superuser:

        objects = Location.objects.all()
        
        
        return render(request,'myApp/manager.html',{user: user, 'vapid_key': vapid_key, 'objects': objects})

    else:
        return redirect('Home')

        

def home(request):
   if request.user.is_superuser:
       return redirect("manager")

   elif request.user.is_authenticated:
       return redirect("requestHelp")
   else:
       return render(request, "myApp/home.html")




@require_POST
@csrf_exempt
def send_push(request):
    try:
        body = request.body
        data = json.loads(body)

        if 'head' not in data or 'body' not in data or 'id' not in data:
            return JsonResponse(status=400, data={"message": "Invalid data format"})

        user_id = data['id']
        user = get_object_or_404(MyUser, pk=user_id)
        print(user)
        payload = {'head': data['head'], 'body': data['body']}
        send_user_notification(user=user, payload=payload, ttl=1000)

        return JsonResponse(status=200, data={"message": "Web push successful"})
    except TypeError:
        return JsonResponse(status=500, data={"message": "An error occurred"})
    


def view_help(request,pk):
    if request.user.is_superuser:

        data = get_object_or_404(Location,id=pk)

        context = {'data':data}

        
        



        return render(request,'myApp/managerView.html',context)
       

  
    else:
       return HttpResponse("Not Allowed")

    

    





