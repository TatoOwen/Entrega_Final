from django import forms
from django.contrib.auth.forms import UserCreationForm
from account.models import Account
from django.contrib.auth import authenticate

class RegistrationForm(UserCreationForm):
    email = forms.EmailField(max_length=60,help_text='Inserte un email')

    class Meta:
        model = Account
        fields = ("email","username","password1","password2")

class AccountAuthenticationForm(forms.ModelForm):

    password = forms.CharField(label='Password',widget=forms.PasswordInput)

    class Meta:
        model = Account
        fields = ('email','password')

        def clean(self):
            email = self.cleaned_data['email']
            password = self.cleaned_data['password']
            if not authenticate(email=email, password=password):
                raise forms.ValidationError("Formato Inválido")

class AccountUpdateForm(forms.ModelForm):

    class Meta:
        model = Account
        fields = ('email','username')
    
    def clean_email(self):
        if self.is_valid():
            email = self.cleaned_data['email']
            try:
                account = Account.objects.exclude(pk=self.instance.pk).get(email=email)
            except Account.DoesNotExist:
                return email
            raise forms.ValidationError('Email "%s" ya se encuentra en uso.' % account)

    def clean_username(self):
            username = self.cleaned_data['username']
            try:
                account = Account.objects.exclude(pk=self.instance.pk).get(username=username)
            except Account.DoesNotExist:
                return username
            raise forms.ValidationError('Usuario "%s" ya se encuentra en uso.' % username)
