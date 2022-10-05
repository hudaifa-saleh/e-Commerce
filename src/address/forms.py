from django import forms
from address.models import Address


class AddressForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = [
            # "billing_profile",
            # "address_type",
            "address_1",
            "address_2",
            "city",
            "country",
            "state",
            "postal_code",
        ]
