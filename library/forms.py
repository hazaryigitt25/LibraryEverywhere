from django import forms

class LibLoginForm(forms.Form):
    lib_name = forms.CharField(label="Library Name")
    lib_password = forms.CharField(label="Library Password",widget=forms.PasswordInput)
    username = forms.CharField(label="Username")
    password = forms.CharField(label="Password",widget=forms.PasswordInput)
    
class SellBookForm(forms.Form):
    buyer_name = forms.CharField(label="Buyer Name")
    buyer_phone = forms.CharField(label="Buyer Phone")
    buyer_email = forms.EmailField(label="Buyer Email")
    
class AddBookForm(forms.Form):
    book_name = forms.CharField(label="Book Name")
    book_author = forms.CharField(label="Book Author")
    
class LibRegisterForm(forms.Form):
    lib_name = forms.CharField(label="Library Name")
    lib_password = forms.CharField(label="Library Password",widget=forms.PasswordInput)
    username = forms.CharField(label="Username")
    user_email = forms.EmailField(label="User Email")
    password = forms.CharField(label="Password",widget=forms.PasswordInput)
    confirm = forms.CharField(label="Confirm Password",widget=forms.PasswordInput)
    
    def clean(self):
        lib_name = self.cleaned_data.get('lib_name')
        lib_password = self.cleaned_data.get('lib_password')
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        confirm = self.cleaned_data.get('confirm')
        
        if password and confirm and password != confirm:
            raise forms.ValidationError('Passwords Does Not Match!')
        
        values = {
            'lib_name' : lib_name,
            'lib_password' : lib_password,
            'username' : username,
            'password' : password
        }
        return values
    