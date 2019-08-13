from django import forms
from django.contrib.auth import get_user_model

User = get_user_model()


class ContactForm(forms.Form):
    fullname = forms.CharField(
        widget=forms.TextInput(
            attrs={'class': 'form-control',
                   'placeholder': 'Ваше имя',
                   }

        ))
    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={'class': 'form-control',
                   'placeholder': 'Ваш емейл',
                   }
        )

    )
    content = forms.CharField(
        widget=forms.TextInput(
            attrs={'class': 'form-control',
                   'placeholder': 'Ваш вопрос',
                   }

        ))

    # choice_field = forms.BooleanField(
    #     label='Accept conditions',
    #     widget=forms.CheckboxInput(
    #         attrs={
    #             'class': 'form-check-label',
    #         }
    #     )
    # )


class LoginForm(forms.Form):
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Имя пользователя'
            }
        )
    )
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Пароль'
            }
        )
    )

class RegisterForm(forms.Form):
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Имя пользователя'
            }
        )
    )
    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={'class': 'form-control',
                   'placeholder': 'Ваш емейл',
                   }
        )

    )
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Пароль'
            }
        )
    )
    password2 = forms.CharField(
        label='Подтвердите пароль',
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Пароль'
            }
        )
    )

    # name1 = 'one'
    # name2 = 'two'
    # name3 = 'three'
    # name4 = 'four'
    #
    # names = [name1, name2, name3, name4]
    # for i, n in enumerate(names):
    #     n[i] = forms.CharField()


    def clean_username(self):
        username = self.cleaned_data.get('username')
        qs = User.objects.filter(username=username)
        if qs.exists():
            raise forms.ValidationError("Это имя пользователя занято!")
        return username

    def clean_email(self):
        email = self.cleaned_data.get('email')
        qs = User.objects.filter(email=email)
        if qs.exists():
            raise forms.ValidationError("Этот адрес электронной почты занят!")
        return username

    def clean(self):
        data = self.cleaned_data
        password = self.cleaned_data.get('password')
        password2 = self.cleaned_data.get('password2')
        if password2 != password:
            raise forms.ValidationError('Пароли не совпадают! Попробуйте еще раз.')
        else:
            return data


