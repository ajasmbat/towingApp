from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.utils.translation import gettext_lazy as _
from django.db import models
from django.views.decorators.csrf import csrf_exempt
from webpush import send_user_notification
from django.core.validators import RegexValidator


class MyUserManager(BaseUserManager):

    def create_user(self, phoneNumber, firstName,lastName, password=None):
        if not phoneNumber:
            raise ValueError("Phone Number Required")

        user = self.model(
            phoneNumber = phoneNumber,
            firstName = firstName,
            lastName = lastName,
        )


        user.set_password(password)
        
        user.save(using=self._db)
        return user
    
    
    
    def create_superuser(self, phoneNumber, firstName,lastName, password=None):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """

       
        user = self.create_user(
            phoneNumber,
            password=password,
            firstName = firstName,
            lastName = lastName,
        )
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)
        return user
    



class MyUser(AbstractBaseUser,PermissionsMixin):

    phoneNumber = models.DecimalField(unique= True,max_digits=10,decimal_places=0)

    firstName = models.CharField(max_length=30,blank=False)
    lastName = models.CharField(max_length=30,blank=False)

    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)



    



    objects = MyUserManager()

    USERNAME_FIELD = "phoneNumber" 

    REQUIRED_FIELDS = ["firstName","lastName"]


    
        

    

    def __str__(self):
        return self.firstName
    



   


class Location(models.Model):
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE)
    long = models.FloatField()
    lat = models.FloatField()
    created_time = models.DateTimeField(auto_now_add=True)

    

    
    def alert(self):


        
        head = "Towing Service Request"
        body = "{} is requesting assistance".format(self.user)

        payload = {'head': head, 'body': body,"url": "/manager"}

        superUser = MyUser.objects.filter(is_superuser=True)

        for user in superUser:
            send_user_notification(user = user, payload=payload,ttl=1000)

        
        
        


       

        return None

    
    def __str__(self):
        
        return "{} Is Requesting Towing".format(self.user)
    




   

    
