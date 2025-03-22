
from django.contrib import admin
from .models import Dimmer, Luminaire, DimmerTest

# Register the model in Django admin
admin.site.register(Dimmer)
admin.site.register(Luminaire)
admin.site.register(DimmerTest)
