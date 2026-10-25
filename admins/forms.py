
from django import forms
from folder.models import Product,UserProfile,ProductRequest,ProductRequestAdmin,ProductRequestSystem

class adminForm(forms.Form):
    username = forms.CharField(
        max_length=65,
        widget=forms.TextInput(attrs={'class': 'form-control', 'id': 'id_username'})
    )
    password = forms.CharField(
        max_length=65,
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'id': 'id_password'})
    )

class createProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name','info','price']

class editProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = '__all__'

class CreateUserForm(forms.ModelForm):
    username = forms.CharField(max_length=30)
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model =UserProfile
        fields = ['role', 'raiting','phonenumber']

class editUserForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['role', 'raiting','phonenumber']

class ProductRequestForm(forms.ModelForm):
    class Meta:
        model = ProductRequest
        fields = [ 'ism','malumot','narx','soni','rasm','ulchov']


class ProductRequestAdminForm(forms.ModelForm):
    class Meta:
        model = ProductRequestAdmin
        fields = [ 'admin_comment', 'tekshirgan', 'tekshirilganvaqt']


class ProductRequestSystemForm(forms.ModelForm):
    class Meta:
        model = ProductRequestSystem
        fields = ['status','sotuvchi']

