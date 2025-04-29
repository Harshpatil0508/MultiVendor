from django import forms
from .models import User,UserProfile
from .validators import allow_only_images

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    confirm_password = forms.CharField(widget=forms.PasswordInput())
    class Meta:
        model = User
        fields = ['first_name','last_name','username','email','phone_number','password']

    def clean(self):
        cleaned_data = super(UserForm,self).clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')
        if password != confirm_password:
            raise forms.ValidationError("Password and Confirm Password do not match")
        return cleaned_data
    
class UserProfileForm(forms.ModelForm):
    address = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'start typing...','required': 'required'}))
    profile_picture = forms.FileField(widget=forms.FileInput(attrs={'class': 'btn btn-info'}),validators=[allow_only_images])
    cover_photo = forms.FileField(widget=forms.FileInput(attrs={'class': 'btn btn-info'}),validators=[allow_only_images])

    # longitude = forms.CharField(widget=forms.TextInput(attrs={'readonly': 'readonly'}))
    # latitude = forms.CharField(widget=forms.TextInput(attrs={'readonly': 'readonly'}))

    def __init__(self, *args, **kwargs):  # sourcery skip: merge-comparisons
        super(UserProfileForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            if field == 'longitude' or field == 'latitude':
                self.fields[field].widget.attrs['readonly'] = 'readonly'
    class Meta:
        model = UserProfile
        fields = ['profile_picture','cover_photo','address','city','state','country','pincode','longitude','latitude']