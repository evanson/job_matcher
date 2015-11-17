from django import forms


class LoginForm(forms.Form):
    username = forms.CharField(error_messages={'required': 'Please enter your username.',
                                               'invalid': 'Please enter a valid username.'})
    password = forms.CharField(widget=forms.PasswordInput,
                               error_messages={'required': 'Please enter your password.',
                                               'invalid': 'Please enter a valid password.'})
    def clean_username(self):
        username = self.cleaned_data['username']
        if not username:
            raise forms.ValidationError("Please enter your username.")
        return username

    def clean_password(self):
        password = self.cleaned_data['password']
        if not password:
            raise forms.ValidationError("Please enter your password.")
        return password
