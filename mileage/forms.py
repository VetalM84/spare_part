from django import forms

from .models import Profile, SparePart, Review, CarModel, CarBrand


class AddCarBrandForm(forms.ModelForm):
    class Meta:
        model = CarBrand
        fields = ['brand']
        choice_field = forms.ChoiceField(choices=())
        widgets = {
            'brand': forms.Select(attrs={'class': 'form-select'}),
        }


class AddCarModelForm(forms.ModelForm):
    class Meta:
        model = CarModel
        fields = ['model_name']
        widgets = {
            'model_name': forms.Select(attrs={'class': 'form-select'}),
        }


class AddSparePartForm(forms.ModelForm):
    class Meta:
        model = SparePart
        fields = '__all__'
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'id': 'sp_name'}),
            'brand': forms.TextInput(attrs={'class': 'form-control', 'id': 'sp_brand'}),
            'number': forms.TextInput(attrs={'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-select'}),

        }


class AddReviewForm(forms.ModelForm):
    car_brand = forms.ModelChoiceField(queryset=CarBrand.objects.all(), label='Марка', empty_label='Выберите марку',
                                       widget=forms.Select(attrs={'class': 'form-select'}))
    car_model = forms.ModelChoiceField(queryset=CarModel.objects.all(), label='Модель',
                                       empty_label='Сначала выберите марку',
                                       widget=forms.Select(attrs={'class': 'form-select'}))

    class Meta:
        model = Review
        fields = ['spare_part', 'mileage', 'car_brand', 'car_model', 'rating', 'testimonial', 'owner']
        widgets = {
            'spare_part': forms.Select(attrs={'class': 'form-select'}),
            'mileage': forms.NumberInput(attrs={'class': 'form-control'}),
            'rating': forms.Select(attrs={'class': 'form-select'}),
            'testimonial': forms.Textarea(attrs={'class': 'form-control', 'rows': '5'}),
            'owner': forms.Select(attrs={'class': 'form-select'}),
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
            'drive2_link': forms.URLInput(attrs={'class': 'form-control'}),
            'cars': forms.SelectMultiple(),
        }
