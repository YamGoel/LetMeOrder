from django import forms

PRODUCT_CATEGORIES = [
    ('', 'Select one category'),
    ('Snacks', 'Snacks'),
    ('Drinks', 'Drinks'),
    ('Sweet', 'Sweet'),
    ('Bread', 'Bread'),
    ('Burgers', 'Burgers'),
    ('Pizzas', 'Pizzas'),
    ('Shakes', 'Shakes'),
]

class AddProductForm(forms.Form):
    storeid = None
    product_name = forms.CharField(widget=forms.TextInput(attrs={'autofocus': 'True', 'class': 'form-control'}))
    product_price = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    product_category = forms.ChoiceField(choices=PRODUCT_CATEGORIES, widget=forms.Select(attrs={'class': 'form-control'}), initial='')
    product_image = forms.ImageField(widget=forms.FileInput(attrs={'class': 'form-control'}))

class AddStoreForm(forms.Form):
    storeid = forms.CharField(widget=forms.TextInput(attrs={'autofocus': 'True', 'class': 'form-control'}))
    store_username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    store_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    store_city = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    category = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))

class EditProductForm(forms.Form):
    product_name = forms.CharField(required=False, widget=forms.TextInput(attrs={'autofocus': 'True', 'class': 'form-control'}))
    product_price = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))
    product_category = forms.ChoiceField(required=False, choices=PRODUCT_CATEGORIES, widget=forms.Select(attrs={'class': 'form-control'}), initial='')
    product_image = forms.ImageField(required=False, widget=forms.FileInput(attrs={'class': 'form-control'}))


class SetupStoreForm(forms.Form):
    key_id = forms.CharField(widget=forms.TextInput(attrs={'autofocus': 'True', 'class': 'form-control'}))
    key_secret = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))

class LoginForm(forms.Form):
    storeid = forms.CharField(widget=forms.TextInput(attrs={'autofocus': 'True', 'class': 'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'autocomplete':'current-password', 'class':'form-control'}))

class MyPasswordResetForm(forms.Form):
    storeid = forms.CharField(widget=forms.TextInput(attrs={'autofocus': 'True', 'class': 'form-control'}))
    oldpassword = forms.CharField(widget=forms.PasswordInput(attrs={'autocomplete':'current-password', 'class':'form-control'}))
    newpassword = forms.CharField(widget=forms.PasswordInput(attrs={'autocomplete':'current-password', 'class':'form-control'}))