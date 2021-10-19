from django import forms
from .models import Profile, Car, SparePart, Mileage


class AddCarForm(forms.ModelForm):
    class Meta:
        model = Car
        fields = '__all__'
        labels = {'model_variant': 'Поколение модели (например: 2, B6, F15, IV)'}
        widgets = {
            'brand': forms.TextInput(attrs={'class': 'form-control'}),
            'model_name': forms.TextInput(attrs={'class': 'form-control'}),
            'model_variant': forms.TextInput(attrs={'class': 'form-control'}),
            'age': forms.NumberInput(attrs={'class': 'form-control'}),
        }


class AddSparePartForm(forms.ModelForm):
    class Meta:
        model = SparePart
        fields = '__all__'
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'brand': forms.TextInput(attrs={'class': 'form-control'}),
            'number': forms.TextInput(attrs={'class': 'form-control'}),
        }


class AddMileageForm(forms.ModelForm):
    class Meta:
        model = Mileage
        fields = '__all__'
        widgets = {
            'spare_part': forms.Select(attrs={'class': 'form-control'}),
            'car': forms.Select(attrs={'class': 'form-select'}),
            'mileage': forms.NumberInput(attrs={'class': 'form-control'}),
            'rating': forms.Select(attrs={'class': 'form-select'}),
            'owner': forms.Select(attrs={'class': 'form-select'}),
        }


class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = '__all__'
        widgets = {
            'user': forms.Select(attrs={'class': 'form-select'}),
            'drive2_link': forms.URLInput(attrs={'class': 'form-control'}),
            'cars': forms.SelectMultiple(),
        }
