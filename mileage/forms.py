from django import forms

from .models import Profile, SparePart, Review, CarModel, CarBrand

BLANK_CHOICE_DASH = [("", "Сделайте выбор")]


class AddCarBrandForm(forms.ModelForm):
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

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['model_name'].queryset = CarModel.objects.none()

        if 'car_brand_id' in self.data:
            print('yes-------------------------------------------------')
            try:
                brand_id = int(self.data.get('car_brand_id'))
                # self.fields['model_name'].queryset = CarModel.objects.filter(brand_id=brand_id).order_by('model_name')
                self.fields['model_name'].queryset = CarModel.objects.filter(brand_id=self.data['car_brand_id'])
            except (ValueError, TypeError):
                pass  # invalid input from the client; ignore and fallback to empty City queryset
        elif self.instance.pk:
            print('no---------------------------------------------------')
            self.fields['model_name'].queryset = self.instance.brand.model_name_set
        else:
            print('else--------------------------------------------------')


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
    class Meta:
        model = Review
        fields = ['spare_part', 'mileage', 'car_brand', 'car_model', 'rating', 'review', 'owner']
        widgets = {
            'spare_part': forms.Select(attrs={'class': 'form-select'}),
            'mileage': forms.NumberInput(attrs={'class': 'form-control'}),
            'car_brand': forms.Select(attrs={'class': 'form-select', 'id': 'id_brand'}),
            'car_model': forms.Select(attrs={'class': 'form-select', 'id': 'id_model_name'}),
            'rating': forms.Select(attrs={'class': 'form-select'}),
            'review': forms.Textarea(attrs={'class': 'form-control', 'rows': '5'}),
            'owner': forms.Select(attrs={'class': 'form-select'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['car_model'].queryset = CarModel.objects.none()


class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = '__all__'
        widgets = {
            'user': forms.Select(attrs={'class': 'form-select'}),
            'drive2_link': forms.URLInput(attrs={'class': 'form-control'}),
            'cars': forms.SelectMultiple(),
        }
