from django import forms
from django.contrib.auth import get_user_model

User = get_user_model()


class LoginForm(forms.Form):
    username = forms.CharField(max_length=150)
    password = forms.CharField(widget=forms.PasswordInput)


class RegisterForm(forms.ModelForm):
    username = forms.CharField(max_length=150, )
    password1 = forms.CharField(widget=forms.PasswordInput, label='Пороль')
    password2 = forms.CharField(widget=forms.PasswordInput, label='Повторите пороль')
    phone = forms.CharField(widget=forms.TextInput, required=False, label='Номер телефона')
    email = forms.EmailField(required=False, label='Email')

    class Meta:
        model = User
        fields = ('username', 'email', 'phone')

    def clean(self):
        cleaned_data = super().clean()
        p1 = cleaned_data.get('password1')
        p2 = cleaned_data.get('password2')
        email = cleaned_data.get('email')
        phone = cleaned_data.get('phone')

        if not email and not phone:
            raise forms.ValidationError('Вы должны ввести либо номер телефона или Email')


        if p1 and p2 and p1 != p2:
            raise forms.ValidationError('Пароли не совпадают')

        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()
        return user