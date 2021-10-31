from django import forms

from .models import Profile, SparePart, Review, CarModel, CarBrand

BLANK_CHOICE_DASH = [("", "Сделайте выбор")]


class AddCarForm(forms.ModelForm):

    class Meta:
        model = CarBrand
        fields = ['brand']
        choice_field = forms.ChoiceField(choices=())
        widgets = {
            'brand': forms.Select(attrs={'class': 'form-select'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        choices = [(pt.id, pt) for pt in CarBrand.objects.all()]
        choices = BLANK_CHOICE_DASH + choices
        self.fields['brand'].choices = choices


class AddCarModelForm(forms.ModelForm):
    class Meta:
        model = CarModel
        fields = ['model_name']
        widgets = {
            'model_name': forms.Select(attrs={'class': 'form-select'}),
        }

    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     self.fields['model_name'].queryset = CarModel.objects.none()

        # if 'country' in self.data:
        #     try:
        #         country_id = int(self.data.get('country'))
        #         self.fields['city'].queryset = City.objects.filter(country_id=country_id).order_by('name')
        #     except (ValueError, TypeError):
        #         pass  # invalid input from the client; ignore and fallback to empty City queryset
        # elif self.instance.pk:
        #     self.fields['city'].queryset = self.instance.country.city_set.order_by('name')


class AddSparePartForm(forms.ModelForm):
    class Meta:
        model = SparePart
        fields = '__all__'
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'id': 'sp_name'}),
            'brand': forms.TextInput(attrs={'class': 'form-control', 'id': 'sp_brand'}),
            'number': forms.TextInput(attrs={'class': 'form-control'}),
        }


class AddReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = '__all__'
        widgets = {
            'spare_part': forms.Select(attrs={'class': 'form-select'}),
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
