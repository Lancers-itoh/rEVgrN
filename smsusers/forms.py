from django import forms

from .models import CustomUser, AdEmail

class CustomUserForm(forms.ModelForm):

    class Meta:
        model = CustomUser
        fields = ('username', 'password')

class AdEmailForm(forms.ModelForm):

	class Meta:
		model = AdEmail
		fields = ('email',)