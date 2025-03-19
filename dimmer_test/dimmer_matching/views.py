from django.shortcuts import render, get_object_or_404
from .models import Luminaire, DimmerCompatibility, DimmerCompatibilityForm, Dimmer
from django.shortcuts import render, redirect
from .models import Luminaire
from .forms import LuminaireForm


# Main page displaying the list of luminaires and form for adding new luminaires
def main_page(request):
    luminaires = Luminaire.objects.all()

    if request.method == 'POST':
        form = LuminaireForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('main_page')  # Reload the page after adding a luminaire
    else:
        form = LuminaireForm()

    return render(request, 'main_page.html', {'luminaires': luminaires, 'form': form})

# def add_compatibility(request, luminaire_id):
#     luminaire = get_object_or_404(Luminaire, id=luminaire_id)
#     dimmers = Dimmer.objects.all()
#
#     if request.method == 'POST':
#         form = DimmerCompatibilityForm(request.POST)
#         if form.is_valid():
#             form.save()
#             return redirect('compatibility_list')  # Redirect to compatibility listing
#     else:
#         form = DimmerCompatibilityForm(initial={'luminaire': luminaire})
#
#     return render(request, 'add_compatibility.html', {'form': form, 'luminaire': luminaire, 'dimmers': dimmers})


def add_compatibility(request, luminaire_id):
    luminaire = get_object_or_404(Luminaire, id=luminaire_id)
    compatible_dimmers = Dimmer.objects.filter(dimming_protocol=luminaire.dimming_protocol)

    if request.method == 'POST':
        for dimmer in compatible_dimmers:
            # Here, we need to check if a DimmerCompatibility record already exists for this dimmer and luminaire.
            compatibility, created = DimmerCompatibility.objects.get_or_create(luminaire=luminaire, dimmer=dimmer)

            # We update the compatibility flags based on the form submission (passed or failed)
            compatibility.min_luminaires_passed = request.POST.get(f"min_luminaires_passed_{dimmer.id}") == 'on'
            compatibility.max_luminaires_passed = request.POST.get(f"max_luminaires_passed_{dimmer.id}") == 'on'
            compatibility.min_dimming_percentage_passed = request.POST.get(f"min_dimming_percentage_passed_{dimmer.id}") == 'on'
            compatibility.max_dimming_percentage_passed = request.POST.get(f"max_dimming_percentage_passed_{dimmer.id}") == 'on'
            compatibility.low_end_start_time_passed = request.POST.get(f"low_end_start_time_passed_{dimmer.id}") == 'on'
            compatibility.visual_test_passed = request.POST.get(f"visual_test_passed_{dimmer.id}") == 'on'
            compatibility.save()

        return redirect('luminaire_dimmers', luminaire_id=luminaire.id)

    return render(request, 'add_compatibility.html', {
        'luminaire': luminaire,
        'compatible_dimmers': compatible_dimmers
    })
    # Display the form for each dimmer
    form_list = []
    for dimmer in dimmers:
        form = DimmerCompatibilityForm(prefix=f'dimmer_{dimmer.id}')
        form_list.append((dimmer, form))

    return render(request, 'add_compatibility.html', {
        'luminaire': luminaire,
        'form_list': form_list
    })

def compatibility_list(request):
    # Fetch all compatibility records
    compatibilities = DimmerCompatibility.objects.all()

    # Render the template with the compatibility data
    return render(request, 'compatibility_list.html', {'compatibilities': compatibilities})

def test_compatibility(request, luminaire_id):
    luminaire = get_object_or_404(Luminaire, id=luminaire_id)

    # Simulate compatibility testing (this can be more complex depending on your requirements)
    # After testing, update the luminaire's status to 'Tested'
    luminaire.status = 'Tested'
    luminaire.save()

    return redirect('main_page')  # Redirect back to the main page after testing


# def test_compatibility(request, luminaire_id):
#     luminaire = get_object_or_404(Luminaire, id=luminaire_id)
#
#     # If the luminaire status is "Not Tested", we can proceed to the compatibility testing
#     if luminaire.status == 'Not Tested':
#         # Perform compatibility testing for all dimmers
#         dimmers = Dimmer.objects.all()
#         for dimmer in dimmers:
#             # Create DimmerCompatibility entries
#             DimmerCompatibility.objects.create(
#                 luminaire=luminaire,
#                 dimmer=dimmer,
#                 min_luminaires=1,
#                 max_luminaires=10,
#                 min_dimming_percentage=0.1,
#                 max_dimming_percentage=100.0,
#                 low_end_start_time=0.0,
#                 visual_test=True,
#                 comments="Tested"
#             )
#
#         # After testing, update the luminaire's status to "Tested"
#         luminaire.status = 'Tested'
#         luminaire.save()
#
#         return redirect('compatibility_result', luminaire_id=luminaire.id)

    # If the luminaire is already tested, just redirect to the compatibility results
    return redirect('compatibility_result', luminaire_id=luminaire.id)


def compatibility_result(request, luminaire_id):
    luminaire = get_object_or_404(Luminaire, id=luminaire_id)

    # Fetch the compatibility results for the luminaire
    compatibility_results = DimmerCompatibility.objects.filter(luminaire=luminaire)

    return render(request, 'compatibility_result.html', {
        'luminaire': luminaire,
        'compatibility_results': compatibility_results,
    })


def luminaire_dimmers(request, luminaire_id):
    # Get the luminaire by its ID
    luminaire = get_object_or_404(Luminaire, id=luminaire_id)

    # Get compatible dimmers based on the luminaire's dimming protocol
    compatible_dimmers = Dimmer.objects.filter(dimming_protocol=luminaire.dimming_protocol)

    # Render the luminaire_dimmers.html template with the luminaire and compatible dimmers
    return render(request, 'luminaire_dimmers.html', {
        'luminaire': luminaire,
        'compatible_dimmers': compatible_dimmers
    })


def luminaire_list_with_dimmers(request):
    # Get all luminaires
    luminaires = Luminaire.objects.all()

    # For each luminaire, check if compatible dimmers exist
    luminaire_data = []
    for luminaire in luminaires:
        # Get compatible dimmers (those matching the dimming protocol)
        compatible_dimmers = Dimmer.objects.filter(dimming_protocol=luminaire.dimming_protocol)

        if compatible_dimmers.exists():
            # If there are compatible dimmers, add a link to the compatible dimmers page
            dimmer_link = f"/luminaire/{luminaire.id}/dimmers/"
        else:
            # If no compatible dimmers, provide a link to the page to create compatibility
            dimmer_link = f"/luminaire/{luminaire.id}/add-compatibility/"

        # Add the luminaire and its corresponding link to the list
        luminaire_data.append({
            'luminaire': luminaire,
            'dimmer_link': dimmer_link
        })

    # Pass the data to the template
    return render(request, 'luminaire_list_with_dimmers.html', {
        'luminaire_data': luminaire_data
    })


def test_compatibility(request, luminaire_id):
    luminaire = get_object_or_404(Luminaire, id=luminaire_id)

    # Form handling logic here to add compatibility

    return render(request, 'test_compatibility.html', {'luminaire': luminaire})

