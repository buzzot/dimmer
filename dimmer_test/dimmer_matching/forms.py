from django import forms
from .models import DimmerCompatibility
from .models import Luminaire

class DimmerCompatibilityForm(forms.ModelForm):
    class Meta:
        model = DimmerCompatibility
        fields = [
            'luminaire', 'dimmer', 'min_luminaires', 'max_luminaires',
            'min_dimming_percentage', 'max_dimming_percentage',
            'low_end_start_time', 'visual_test', 'comments'
        ]



class LuminaireForm(forms.ModelForm):
    class Meta:
        model = Luminaire
        fields = ['product_name', 'dimming_protocol', 'manufacturer_url', 'max_power']