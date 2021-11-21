from django import forms
from django.core.exceptions import ValidationError

from dal import autocomplete

from .models import Profile, SparePart, Review, CarModel, CarBrand


class AddCarBrandForm(forms.ModelForm):
    class Meta:
        model = CarBrand
        fields = ['brand']
        choice_field = forms.ChoiceField(choices=())
        widgets = {
            'brand': forms.Select(attrs={'class': 'uk-select'}),
        }


class AddCarModelForm(forms.ModelForm):
    class Meta:
        model = CarModel
        fields = ['model_name']
        widgets = {
            'model_name': forms.Select(attrs={'class': 'uk-select'}),
        }


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

    class Meta:
        model = Review
        fields = ['spare_part', 'mileage', 'car_brand', 'car_model', 'rating', 'testimonial']
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


class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = '__all__'
        widgets = {
            'user': forms.Select(attrs={'class': 'form-select'}),
            'drive2_link': forms.URLInput(attrs={'class': 'uk-input'}),
            'cars': forms.SelectMultiple(),
        }

    def clean_drive2_link(self):
        drive2_link = self.cleaned_data['drive2_link']
        if not drive2_link.startswith('https://www.drive2.ru/users/'):
            raise ValidationError('Ссылка должна выглядеть так: https://www.drive2.ru/users/имя_пользователя')
        return drive2_link
