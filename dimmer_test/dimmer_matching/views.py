from django.shortcuts import render, get_object_or_404, redirect
from .models import Luminaire, Dimmer,  DimmerTest
from .forms import LuminaireForm, DimmerTestForm
from django.db import IntegrityError
from django.http import JsonResponse, HttpResponseBadRequest
from django.contrib import messages

from datetime import datetime

# Main page displaying the list of luminaires and form for adding new luminaires
def main_page(request):
    luminaires = Luminaire.objects.all()
    form = LuminaireForm(request.POST or None)

    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect('main_page')

    return render(request, 'main_page.html', {'luminaires': luminaires, 'form': form})


def to_int(value, default=0):
    try:
        return int(value)
    except (ValueError, TypeError):
        return default

def to_float(value, default=0.0):
    try:
        return float(value)
    except (ValueError, TypeError):
        return default

# def add_compatibility(request, luminaire_id):
#     # Retrieve the Luminaire object based on the provided id
#     luminaire = get_object_or_404(Luminaire, id=luminaire_id)
#
#     # Filter Dimmer objects based on Luminaire's dimming protocol
#     compatible_dimmers = Dimmer.objects.filter(dimming_protocol=luminaire.dimming_protocol)
#
#     # Get existing tests for this luminaire
#     existing_tests = DimmerTest.objects.filter(luminaire=luminaire)
#
#     if request.method == 'POST':
#         for dimmer in compatible_dimmers:
#             # Try to get an existing test for this combination
#             dimmer_test = existing_tests.filter(dimmer=dimmer).first()
#
#             # Determine compatibility status
#             compatibility_status = dimmer_test.compatibility_status if dimmer_test else False
#
#             # Create or update the DimmerTest entry
#             compatibility, created = DimmerTest.objects.get_or_create(
#                 luminaire=luminaire,
#                 dimmer=dimmer
#             )
#
#             # Populate fields from POST data
#             compatibility.min_luminaires = to_int(request.POST.get(f"min_luminaires_{dimmer.id}"))
#             compatibility.max_luminaires = to_int(request.POST.get(f"max_luminaires_{dimmer.id}"))
#             compatibility.min_dimming_percentage = to_float(request.POST.get(f"min_dimming_percentage_{dimmer.id}"))
#             compatibility.max_dimming_percentage = to_float(request.POST.get(f"max_dimming_percentage_{dimmer.id}"))
#             compatibility.low_end_start_time = to_float(request.POST.get(f"low_end_start_time_{dimmer.id}"))
#             compatibility.visual_test = request.POST.get(f"visual_test_{dimmer.id}") == 'on'
#
#             # Use compatibility status from earlier (based on existing test)
#             compatibility.compatibility_status = compatibility_status
#
#             # Save to DB
#             compatibility.save()
#
#         # Optional user message
#         messages.success(request, "Compatibility information has been saved.")
#
#         return redirect('luminaire_dimmers', luminaire_id=luminaire.id)
#
#     # Render template with data
#     return render(request, 'add_compatibility.html', {
#         'luminaire': luminaire,
#         'compatible_dimmers': compatible_dimmers,
#         'existing_tests': existing_tests,
#     })

def add_compatibility(request, luminaire_id):
    luminaire = get_object_or_404(Luminaire, id=luminaire_id)
    compatible_dimmers = list(Dimmer.objects.filter(dimming_protocol=luminaire.dimming_protocol))

    # Determine which dimmer we're editing (via ?step=)
    step = int(request.GET.get('step', 0))
    if step >= len(compatible_dimmers):
        return redirect('luminaire_dimmers', luminaire_id=luminaire.id)

    current_dimmer = compatible_dimmers[step]

    # Try to find existing test
    dimmer_test, _ = DimmerTest.objects.get_or_create(
        luminaire=luminaire,
        dimmer=current_dimmer
    )

    if request.method == 'POST':
        dimmer_test.min_luminaires = request.POST.get("min_luminaires", 0)
        dimmer_test.max_luminaires = request.POST.get("max_luminaires", 0)
        dimmer_test.min_dimming_percentage = request.POST.get("min_dimming_percentage", 0)
        dimmer_test.max_dimming_percentage = request.POST.get("max_dimming_percentage", 100)
        dimmer_test.low_end_start_time = request.POST.get("low_end_start_time", 0)
        dimmer_test.visual_test = request.POST.get("visual_test") == 'on'
        dimmer_test.comments = request.POST.get("comments", "")
        dimmer_test.save()

        # Go to next step
        return redirect(f"{request.path}?step={step + 1}")

    return render(request, 'add_compatibility_step.html', {
        'luminaire': luminaire,
        'dimmer': current_dimmer,
        'step': step,
        'total': len(compatible_dimmers),
        'dimmer_test': dimmer_test,
    })



# Display all compatibility records
def compatibility_list(request):
    compatibilities = DimmerTest.objects.select_related('luminaire', 'dimmer').all()
    return render(request, 'compatibility_list.html', {'compatibilities': compatibilities})


# Run a test for luminaire-dimmer compatibility
def test_compatibility(request, luminaire_id):
    luminaire = get_object_or_404(Luminaire, id=luminaire_id)

    # Simulate testing process (this can be expanded for real tests)
    luminaire.status = 'Tested'
    luminaire.save()

    return redirect('compatibility_result', luminaire_id=luminaire.id)


# Show test results for a luminaire
def compatibility_result(request, luminaire_id):
    luminaire = get_object_or_404(Luminaire, id=luminaire_id)
    compatibility_results = DimmerTest.objects.filter(luminaire=luminaire)

    return render(request, 'compatibility_result.html', {
        'luminaire': luminaire,
        'compatibility_results': compatibility_results
    })


# List dimmers compatible with a specific luminaire
def luminaire_dimmers(request, luminaire_id):
    luminaire = get_object_or_404(Luminaire, id=luminaire_id)
    compatible_dimmers = Dimmer.objects.filter(dimming_protocol=luminaire.dimming_protocol)

    return render(request, 'luminaire_dimmers.html', {
        'luminaire': luminaire,
        'compatible_dimmers': compatible_dimmers
    })


# Display luminaires with links to compatible dimmers or add compatibility
def luminaire_list_with_dimmers(request):
    luminaires = Luminaire.objects.all()

    luminaire_data = [
        {
            'luminaire': luminaire,
            'dimmer_link': (
                f"/luminaire/{luminaire.id}/dimmers/"
                if Dimmer.objects.filter(dimming_protocol=luminaire.dimming_protocol).exists()
                else f"/luminaire/{luminaire.id}/add-compatibility/"
            )
        }
        for luminaire in luminaires
    ]

    return render(request, 'luminaire_list_with_dimmers.html', {
        'luminaire_data': luminaire_data
    })



from django.shortcuts import render, redirect, get_object_or_404
from .models import Luminaire, Dimmer, DimmerTest

def create_dimmer_test(request):
    luminaires = Luminaire.objects.all()
    dimmers = Dimmer.objects.all()

    if request.method == "POST":
        # Get the selected luminaire and dimmer
        luminaire_id = request.POST.get("luminaire")
        dimmer_model = request.POST.get("dimmer")
        luminaire = get_object_or_404(Luminaire, id=luminaire_id)
        dimmer = get_object_or_404(Dimmer, model=dimmer_model)

        # Get other form data (assuming these fields exist in the form)
        luminaire_production_date = request.POST.get("luminaire_production_date")
        light_level = int(request.POST.get("light_level"))
        number_of_luminaries = int(request.POST.get("number_of_luminaries"))
        max_lux = int(request.POST.get("max_lux"))
        min_lux = int(request.POST.get("min_lux"))

        print("Form submitted")
        # Check if data is correctly passed to the view
        print(request.POST)
        # Create or update the test record
        test, created = DimmerTest.objects.get_or_create(
            luminaire=luminaire,
            dimmer=dimmer,
            luminaire_production_date=luminaire_production_date,
            defaults={
                "light_level": light_level,
                "number_of_luminaries": number_of_luminaries,
                "max_lux": max_lux,
                "min_lux": min_lux,
            }
        )

        # Update test fields if it already exists
        if not created:
            test.light_level = light_level
            test.number_of_luminaries = number_of_luminaries
            test.max_lux = max_lux
            test.min_lux = min_lux
            test.save()

        # Redirect to the success page after the test is saved
        return redirect('success_page')

    return render(request, "dimmer_test.html", {
        "luminaires": luminaires,
        "dimmers": dimmers,
    })




def dimmer_test_view(request):
    luminaires = Luminaire.objects.all()  # Get all luminaires for selection
    selected_luminaire = None
    selected_dimmer_number = None
    tests = None
    completed_tests = []  # Store completed test dimmer numbers

    if request.method == "POST":
        if "select_dimmer" in request.POST:
            selected_dimmer_number = request.POST.get("selected_dimmer")

        elif "submit_test" in request.POST:
            luminaire_id = request.POST.get("luminaire")
            production_date = request.POST.get("luminaire_production_date")
            selected_dimmer_number = request.POST.get("selected_dimmer")
            light_level = request.POST.get("light_level")

            # Get number_of_luminaries from the POST data
            number_of_luminaries = int(request.POST.get("number_of_luminaries", 0))  # Default to 0 if not provided

            selected_luminaire = get_object_or_404(Luminaire, id=luminaire_id)
            dimmer = get_object_or_404(Dimmer, model=selected_dimmer_number)

            test, created = DimmerTest.objects.get_or_create(
                luminaire=selected_luminaire,
                dimmer=dimmer,
                luminaire_production_date=production_date,
                defaults={"light_level": light_level, "number_of_luminaries": number_of_luminaries}
            )

            # Update test fields
            test.number_of_luminaries = number_of_luminaries
            test.max_lux = int(request.POST.get("max_lux", test.max_lux))
            test.min_lux = int(request.POST.get("min_lux", test.min_lux))

            test.visual_flicker = "visual_flicker" in request.POST
            test.ghosting = "ghosting" in request.POST
            test.turnon_time = "turnon_time" in request.POST
            test.popon_light = "popon_light" in request.POST
            test.popcorn = "popcorn" in request.POST
            test.dimmer_noise = "dimmer_noise" in request.POST
            test.fixture_noise = "fixture_noise" in request.POST
            test.breaker_noise = "breaker_noise" in request.POST

            test.save()

            completed_tests.append(selected_dimmer_number)
            selected_dimmer_number = None  # Reset after submission

    # Fetch completed tests
    existing_tests = DimmerTest.objects.all()
    completed_tests = [test.dimmer.model for test in existing_tests]

    # If a luminaire is selected, filter dimmers based on its dimming protocol
    if selected_luminaire:
        # Only show dimmers that have the same dimming protocol as the selected luminaire
        dimmers = Dimmer.objects.filter(dimming_protocol=selected_luminaire.dimming_protocol)
    else:
        # Show all dimmers if no luminaire is selected
        dimmers = Dimmer.objects.all()

    return render(request, "dimmer_test.html", {
        "luminaires": luminaires,
        "dimmers": dimmers,
        "selected_luminaire": selected_luminaire,
        "selected_dimmer_number": selected_dimmer_number,
        "completed_tests": completed_tests,
        "tests": existing_tests if "generate_test" in request.POST else None,
    })
def dimmer_list(request):
    dimmers = Dimmer.objects.all()  # Fetch all dimmers
    return render(request, 'all_dimmers.html', {'dimmers': dimmers})