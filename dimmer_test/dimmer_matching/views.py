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


def test_compatibility(request, luminaire_id):
    luminaire = get_object_or_404(Luminaire, id=luminaire_id)

    # If the luminaire status is "Not Tested", we can proceed to the compatibility testing
    if luminaire.status == 'Not Tested':
        # Perform compatibility testing for all dimmers
        dimmers = Dimmer.objects.all()
        for dimmer in dimmers:
            # Create DimmerCompatibility entries
            DimmerCompatibility.objects.create(
                luminaire=luminaire,
                dimmer=dimmer,
                min_luminaires=1,
                max_luminaires=10,
                min_dimming_percentage=0.1,
                max_dimming_percentage=100.0,
                low_end_start_time=0.0,
                visual_test=True,
                comments="Tested"
            )

        # After testing, update the luminaire's status to "Tested"
        luminaire.status = 'Tested'
        luminaire.save()

        return redirect('compatibility_result', luminaire_id=luminaire.id)

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