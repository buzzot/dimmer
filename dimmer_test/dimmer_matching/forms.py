from django import forms
# from .models import DimmerCompatibility
from .models import Luminaire, DimmerTest


# class DimmerCompatibilityForm(forms.ModelForm):
#     class Meta:
#         model = DimmerCompatibility
#         fields = [
#             'luminaire', 'dimmer', 'min_luminaires', 'max_luminaires',
#             'min_dimming_percentage', 'max_dimming_percentage',
#             'low_end_start_time', 'visual_test', 'comments'
#         ]

# class DimmerCompatibilityForm(forms.ModelForm):
#     class Meta:
#         model = DimmerCompatibility
#         fields = [
#
#             'luminaire_min_luminaires',
#             'luminaire_max_luminaires',
#             'luminaire_min_dimming_percentage',
#             'luminaire_max_dimming_percentage',
#             'luminaire_low_end_start_time',
#             'luminaire_visual_test',
#         ]

class LuminaireForm(forms.ModelForm):
    class Meta:
        model = Luminaire
        fields = ['product_name', 'dimming_protocol', 'manufacturer_url', 'max_power']

        from django import forms
        from .models import DimmerTest

from django import forms
from .models import DimmerTest

class DimmerTestForm(forms.ModelForm):
    class Meta:
        model = DimmerTest
        fields = ['luminaire', 'dimmer', 'luminaire_production_date', 'light_level',
                  'number_of_luminaries', 'max_lux', 'min_lux', 'visual_flicker',
                  'ghosting', 'turnon_time', 'popon_light', 'popcorn',
                  'dimmer_noise', 'fixture_noise', 'breaker_noise']