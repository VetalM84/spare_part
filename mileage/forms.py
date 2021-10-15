from django import forms
from .models import Profile, Car, SparePart, Mileage


class AddCarForm(forms.ModelForm):

    class Meta:
        model = Car
        fields = '__all__'


class AddSparePartForm(forms.ModelForm):

    class Meta:
        model = SparePart
        fields = '__all__'


class AddMileageForm(forms.ModelForm):

    class Meta:
        model = Mileage
        fields = '__all__'
