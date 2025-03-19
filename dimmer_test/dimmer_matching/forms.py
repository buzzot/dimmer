from django import forms
from .models import DimmerCompatibility
from .models import Luminaire

# class DimmerCompatibilityForm(forms.ModelForm):
#     class Meta:
#         model = DimmerCompatibility
#         fields = [
#             'luminaire', 'dimmer', 'min_luminaires', 'max_luminaires',
#             'min_dimming_percentage', 'max_dimming_percentage',
#             'low_end_start_time', 'visual_test', 'comments'
#         ]

class DimmerCompatibilityForm(forms.ModelForm):
    class Meta:
        model = DimmerCompatibility
        fields = [
            'min_luminaires_passed',
            'max_luminaires_passed',
            'min_dimming_percentage_passed',
            'max_dimming_percentage_passed',
            'low_end_start_time_passed',
            'visual_test_passed',
            'comments',
            'luminaire_min_luminaires',
            'luminaire_max_luminaires',
            'luminaire_min_dimming_percentage',
            'luminaire_max_dimming_percentage',
            'luminaire_low_end_start_time',
            'luminaire_visual_test',
        ]

class LuminaireForm(forms.ModelForm):
    class Meta:
        model = Luminaire
        fields = ['product_name', 'dimming_protocol', 'manufacturer_url', 'max_power']