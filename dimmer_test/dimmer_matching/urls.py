from django.urls import path
from . import views

urlpatterns = [
    path('', views.main_page, name='main_page'),  # Main page URL
    path('add_compatibility/<int:luminaire_id>/', views.add_compatibility, name='add_compatibility'),
    path('compatibility_list/', views.compatibility_list, name='compatibility_list'),
    path('test_compatibility/<int:luminaire_id>/', views.test_compatibility, name='test_compatibility'),
    path('add_compatibility/<int:luminaire_id>/', views.add_compatibility, name='add_compatibility'),
    path('compatibility_result/<int:luminaire_id>/', views.compatibility_result, name='compatibility_result'),
    path('add_compatibility/<int:luminaire_id>/', views.add_compatibility, name='add_compatibility'),
    path('luminaire/<int:luminaire_id>/dimmers/', views.luminaire_dimmers, name='luminaire_dimmers'),
    path('luminaires/', views.luminaire_list_with_dimmers, name='luminaire_list_with_dimmers'),
    path('dimmer-test/', views.dimmer_test_view, name='dimmer_test_view'),
    # Add this line
]
