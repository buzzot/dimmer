from django.db import models
from django import forms
from django.shortcuts import render, get_object_or_404, redirect
from django.core.exceptions import ValidationError
from django.utils.timezone import now


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



class DimmerTest(models.Model):
    report_date = models.DateTimeField(auto_now_add=True)  # Auto-set current date
    luminaire = models.ForeignKey(Luminaire, on_delete=models.CASCADE)
    luminaire_production_date = models.DateTimeField()
    light_level = models.IntegerField()
    dimmer = models.ForeignKey(Dimmer, on_delete=models.CASCADE)

    compatibility_status = models.BooleanField(default=False)
    number_of_luminaries = models.IntegerField()
    max_lux = models.IntegerField()
    min_lux = models.IntegerField()

    # Issue Tests
    visual_flicker = models.BooleanField(default=False)
    ghosting = models.BooleanField(default=False)
    turnon_time = models.BooleanField(default=False)
    popon_light = models.BooleanField(default=False)
    popcorn = models.BooleanField(default=False)
    dimmer_noise = models.BooleanField(default=False)
    fixture_noise = models.BooleanField(default=False)
    breaker_noise = models.BooleanField(default=False)

    class Meta:
        unique_together = ('luminaire', 'dimmer', 'luminaire_production_date')  # Prevent duplicate compatibility records
        ordering = ['luminaire', 'dimmer']

    @property
    def min_dimming_level(self):
        """Calculate the minimum dimming level as a percentage."""
        return round((self.min_lux / self.max_lux) * 100, 2) if self.max_lux else 0

    @property
    def high_dimming_level(self):
        """Calculate the high dimming level as a percentage."""
        return round((self.max_lux / self.light_level) * 100, 2) if self.light_level else 0

    @property
    def low_dimming_level(self):
        """Calculate the low dimming level as a percentage."""
        return round((self.min_lux / self.light_level) * 100, 2) if self.light_level else 0

    def calculate_compatibility(self):
        """Determine compatibility based on issue tests."""

        # Check the additional dimming level conditions
        dimming_level_check = self.low_dimming_level > 10 and self.high_dimming_level > 80

        self.compatibility_status = all([
            self.visual_flicker, self.ghosting, self.turnon_time,
            self.popon_light, self.popcorn, self.dimmer_noise,
            self.fixture_noise, self.breaker_noise
        ])

    def save(self, *args, **kwargs):
        """Auto-set compatibility status before saving."""
        self.calculate_compatibility()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Test Report ({self.report_date}): {self.luminaire.product_name} - {self.dimmer.model}"

