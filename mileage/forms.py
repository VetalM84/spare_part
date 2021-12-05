from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UserChangeForm
from django.contrib.auth.models import User

from dal import autocomplete
from captcha.fields import ReCaptchaField

from .models import Profile, SparePart, Review, CarModel, CarBrand


class UserLoginForm(AuthenticationForm):
    username = forms.CharField(label='Логин', widget=forms.TextInput(attrs={'class': 'uk-input'}))
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'uk-input'}))


class UserRegisterForm(UserCreationForm):
    username = forms.CharField(label='Логин', widget=forms.TextInput(attrs={'class': 'uk-input'}))
    email = forms.EmailField(label='Email', widget=forms.EmailInput(attrs={'class': 'uk-input'}))
    password1 = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'uk-input'}))
    password2 = forms.CharField(label='Подтвердите пароль', widget=forms.PasswordInput(attrs={'class': 'uk-input'}))

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')


class AddSparePartForm(forms.ModelForm):
    class Meta:
        model = SparePart
        fields = '__all__'
        widgets = {
            'name': forms.TextInput(attrs={'class': 'uk-input', 'id': 'sp_name'}),
            'brand': forms.TextInput(attrs={'class': 'uk-input', 'id': 'sp_brand'}),
            'number': forms.TextInput(attrs={'class': 'uk-input'}),
            'category': forms.Select(attrs={'class': 'uk-select'}),
        }


class AddReviewForm(forms.ModelForm):
    car_brand = forms.ModelChoiceField(queryset=CarBrand.objects.all(), label='Марка', empty_label='Выберите марку',
                                       widget=forms.Select(attrs={'class': 'uk-select'}))
    car_model = forms.ModelChoiceField(queryset=CarModel.objects.all(), label='Модель',
                                       empty_label='Сначала выберите марку',
                                       widget=forms.Select(attrs={'class': 'uk-select'}))
    jpeg = forms.ImageField(label='Фото', required=False, widget=forms.FileInput)
    # captcha = CaptchaField(label='Антибот')
    captcha = ReCaptchaField(label='Антибот')

    class Meta:
        model = Review
        fields = ['spare_part', 'mileage', 'car_brand', 'car_model', 'rating', 'testimonial', 'jpeg']
        widgets = {
            'spare_part': autocomplete.ModelSelect2(url='spare_part_autocomplete', attrs={'class': 'uk-select'}),
            # 'spare_part': forms.Select(attrs={'class': 'uk-select'}),
            # 'car_brand': autocomplete.ModelSelect2(url='car_brand_autocomplete', attrs={'class': 'uk-select'}),
            # 'car_model': autocomplete.ModelSelect2(url='ajax_get_chained_car_models', attrs={'class': 'uk-select'}),
            'mileage': forms.NumberInput(attrs={'class': 'uk-input'}),
            'rating': forms.Select(attrs={'class': 'uk-select'}),
            'testimonial': forms.Textarea(attrs={'class': 'uk-textarea', 'rows': '5'}),
        }

    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     self.fields['car_model'].queryset = CarModel.objects.none()


class UserEditForm(UserChangeForm):
    first_name = forms.CharField(label='Имя', widget=forms.TextInput(attrs={'class': 'uk-input'}))
    last_name = forms.CharField(label='Фамилия', widget=forms.TextInput(attrs={'class': 'uk-input'}))
    username = forms.CharField(label='Логин', widget=forms.TextInput(attrs={'class': 'uk-input'}))
    email = forms.EmailField(label='Email', widget=forms.EmailInput(attrs={'class': 'uk-input'}))

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'email',)
        exclude = ('password',)


# TODO реализовать редактирование профиля
class ProfileEditForm(forms.ModelForm):

    class Meta:
        model = Profile
        fields = ['drive2_link', 'avatar']
        widgets = {
            'drive2_link': forms.URLInput(attrs={'class': 'uk-input'}),
        }

    def clean_drive2_link(self):
        drive2_link = self.cleaned_data['drive2_link']
        if not drive2_link.startswith('https://www.drive2.ru/users/'):
            raise ValidationError('Ссылка должна выглядеть так: https://www.drive2.ru/users/имя_пользователя')
        return drive2_link
