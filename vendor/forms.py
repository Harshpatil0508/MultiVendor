from django import forms
from vendor.models import Vendor
from accounts.validators import allow_only_images

class VendorForm(forms.ModelForm):
    vendor_license = forms.FileField(widget=forms.FileInput(attrs={'class': 'btn btn-info'}),validators=[allow_only_images])
    class Meta:
        model = Vendor
        fields = ['vendor_name','vendor_license']
   