from django.db import models
from django import forms
from django.shortcuts import render, get_object_or_404, redirect


class Luminaire(models.Model):
    STATUS_CHOICES = [
        ('Not Tested', 'Not Tested'),
        ('Tested', 'Tested')
    ]

    creation_date = models.DateTimeField(auto_now_add=True)
    product_name = models.CharField(max_length=255)
    max_power = models.FloatField()  # Added max_power field to store the maximum power (in watts)

    dimming_protocol = models.CharField(max_length=100, choices=[
        ('ELV', 'ELV'),
        ('Triac', 'Triac'),
        ('0-10V', '0-10V')
    ])
    manufacturer_url = models.URLField(blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Not Tested')  # Add status field

    def __str__(self):
        return self.product_name


class Dimmer(models.Model):
    dim_number = models.IntegerField(blank=True, null=True)
    brand = models.CharField(max_length=255)
    series = models.CharField(max_length=255)
    model = models.CharField(max_length=255)
    dimming_protocol = models.CharField(max_length=200, choices=[
        ('ELV', 'ELV'),
        ('Triac', 'Triac'),
        ('0-10V', '0-10V')
    ])
    manufacturer_url = models.URLField(blank=True, null=True)
    max_power = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return f"{self.brand} {self.model} ({self.dimming_protocol})"


class DimmerCompatibility(models.Model):
    luminaire = models.ForeignKey(Luminaire, on_delete=models.CASCADE)
    dimmer = models.ForeignKey(Dimmer, on_delete=models.CASCADE)
    min_luminaires = models.IntegerField()
    max_luminaires = models.IntegerField()
    min_dimming_percentage = models.FloatField()
    max_dimming_percentage = models.FloatField()
    low_end_start_time = models.FloatField()
    visual_test = models.BooleanField()
    comments = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.luminaire} - {self.dimmer} Compatibility"


class DimmerCompatibilityForm(forms.ModelForm):
    class Meta:
        model = DimmerCompatibility
        fields = ['luminaire', 'dimmer', 'min_luminaires', 'max_luminaires', 'min_dimming_percentage',
                  'max_dimming_percentage', 'low_end_start_time', 'visual_test', 'comments']


def add_compatibility(request, luminaire_id):
    luminaire = get_object_or_404(Luminaire, id=luminaire_id)
    dimmers = Dimmer.objects.all()

    if request.method == 'POST':
        form = DimmerCompatibilityForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('compatibility_list')  # Redirect to compatibility listing
    else:
        form = DimmerCompatibilityForm(initial={'luminaire': luminaire})

    return render(request, 'add_compatibility.html', {'form': form, 'luminaire': luminaire, 'dimmers': dimmers})
