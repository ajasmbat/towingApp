from django import forms
from .models  import MyUser, Location

class MyUserForm(forms.ModelForm):
    class Meta:
        model = MyUser
        fields = ['phoneNumber', 'firstName', 'lastName', 'password']

        labels = {
            'phoneNumber': "Phone Number", 
            'firstName': "First Name", 
            'lastName': "Last Name", 
            'password' : "Password"

        }

    
    
        widgets = {

            
            
            "phoneNumber":forms.TextInput(attrs={'onkeydown': "phoneNumberFormatter(this, event)"}),
            'password': forms.PasswordInput()
        }

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user    









class LoginUserForm(forms.Form):
    
    phoneNumber = forms.IntegerField(label='Phone Number',widget=forms.TextInput(attrs={'onkeydown': "phoneNumberFormatter(this, event)"}))
    password = forms.CharField(label='Password', widget=forms.PasswordInput())

