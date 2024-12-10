from django.urls import path
from . import views

urlpatterns = [
    path('give-recs-for-new-vec/', views.give_recs_for_new_vec, name='give_recs_for_new_vec'),
    path('give-recs-for-chosen-vec/', views.give_recs_for_chosen_vec, name='give_recs_for_chosen_vec'), 
    path('get-raag-rec/', views.get_raag_rec, name='get_raag_rec'),
    path('get-artist-rec/', views.get_artist_rec, name='get_artist_rec'),
    # path('get-audio-details/', views.get_audio_details, name='get_audio_details'),
]