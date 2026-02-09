from django import forms
from django.contrib.auth import get_user_model

User = get_user_model()


class LoginForm(forms.Form):
    username = forms.CharField(max_length=150)
    password = forms.CharField(widget=forms.PasswordInput)


class RegisterForm(forms.ModelForm):
    username = forms.CharField(max_length=150, )
    email = forms.EmailField(max_length=150, label='Введите Email')
    password1 = forms.CharField(widget=forms.PasswordInput, label='Пороль')
    password2 = forms.CharField(widget=forms.PasswordInput, label='Повторите пороль')


    class Meta:
        model = User
        fields = ('username', 'email')

    def clean(self):
        cleaned_data = super().clean()
        p1 = cleaned_data.get('password1')
        p2 = cleaned_data.get('password2')
        email= cleaned_data.get('email')

        if not email:
            raise forms.ValidationError('Вы должны ввести Email')


        if p1 and p2 and p1 != p2:
            raise forms.ValidationError('Пароли не совпадают')

        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()
        return user