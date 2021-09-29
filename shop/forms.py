from django import forms

from home.models import User, City
from models.models import Model, Variant

from .models import SellCar, BuyCar

class SellCarModelForm(forms.ModelForm):
    fullname = forms.CharField(max_length= 100, widget=forms.TextInput())
    email = forms.EmailField(widget=forms.EmailInput())

    year = forms.CharField(max_length=4, widget=forms.TextInput())
    kilometer = forms.CharField(max_length=10, widget=forms.TextInput())
    reg_no = forms.CharField(max_length=10, widget=forms.TextInput())
    price = forms.CharField(max_length= 10, widget=forms.TextInput())

    class Meta:
        model = SellCar
        fields = '__all__'
        exclude = ('status',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['city'].queryset = City.objects.none()
        self.fields['model'].queryset = Model.objects.none()
        self.fields['variant'].queryset = Variant.objects.none()

        if 'state' in self.data:
            try:
                state_id = int(self.data.get('state'))
                self.fields['city'].queryset = City.objects.filter(state_id=state_id).order_by('name')
            except (ValueError, TypeError):
                pass  # invalid input from the client; ignore and fallback to empty City queryset
        elif self.instance.pk:
            self.fields['city'].queryset = self.instance.state.city_set.order_by('name')

        if 'make' in self.data:
            try:
                make_id = int(self.data.get('make'))
                self.fields['model'].queryset = Model.objects.filter(make_id=make_id).order_by('name')
            except (ValueError, TypeError):
                pass  # invalid input from the client; ignore and fallback to empty Model queryset
        elif self.instance.pk:
            self.fields['model'].queryset = self.instance.make.model_set.order_by('name')

        if 'model' in self.data:
            try:
                model_id = int(self.data.get('model'))
                self.fields['variant'].queryset = Variant.objects.filter(model_id=model_id).order_by('name')
            except (ValueError, TypeError):
                pass  # invalid input from the client; ignore and fallback to empty Variant queryset
        elif self.instance.pk:
            self.fields['variant'].queryset = self.instance.model.variant_set.order_by('name')

    def clean_fullname(self):
        fullname = self.cleaned_data.get('fullname')
        if len(fullname) < 3:
            raise forms.ValidationError("Name cannot be less than 3 characters")
        return fullname

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if not email.endswith('@gmail.com'):
            raise forms.ValidationError("Email should end with @gmail.com")
        account = False
        for instance in User.objects.all():
            if instance.email == email:
                account = True
                break
        if not account:
            raise forms.ValidationError("An account doesn't exist with the given email")
        return email
    
    def clean_mobile(self):
        mobile = self.cleaned_data.get('mobile')
        if not mobile.isnumeric():
            raise forms.ValidationError("Mobile number should be a number")
        if len(mobile)<10:
            raise forms.ValidationError("Mobile cannot be less than 10-digits")
        return mobile

    def clean_year(self):
        year = int(self.cleaned_data.get('year'))
        if len(str(year))!=4 or year<0:
            raise forms.ValidationError("Year is invalid")
        return year

    def clean_kilometer(self):
        kilometer = float(self.cleaned_data.get('kilometer'))
        if kilometer<0:
            raise forms.ValidationError("Length cannot be negative")
        return kilometer

    def clean_reg_no(self):
        reg_no = int(self.cleaned_data.get('reg_no'))
        if len(str(reg_no)) < 5:
            raise forms.ValidationError("Cannot be less than 5 digits")
        if reg_no<0:
            raise forms.ValidationError("Registration number cannot be negative")
        for instance in SellCar.objects.all():
            if int(instance.reg_no) == int(reg_no):
                raise forms.ValidationError('This car with reg_no '+str(reg_no)+' is already on sale!')
        return reg_no
        
class BuyCarModelForm(forms.ModelForm):
    class Meta:
        model = BuyCar
        fields = '__all__'