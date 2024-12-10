# from django.shortcuts import render

# Create your views here.

import os
import pandas as pd
import json
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.http import JsonResponse
from .utils import (
    giveRecsForNewVec as give_recs,
    getRaagRec as raag_rec,
    getArtistRec as artist_rec,
    getAudioDetails as audio_details,
    User
)
# import librosa

# Global variable to hold similarity data in memory
metadata = None
user_id = 1


@api_view(['POST'])
def load_data(request):
    """
    Endpoint to load similarity data from a CSV file.
    This should be called once before making any recommendations.
    """
    global similarity_data
    data_path = os.path.join(os.path.dirname(__file__), '../data/metadata.csv')
    
    try:
        # Load similarity data
        similarity_data = pd.read_csv(data_path)
        return Response({"message": "Similarity data loaded successfully", "columns": similarity_data.columns.tolist()})
    
    except FileNotFoundError:
        return Response({"error": "File not found. Please ensure the CSV is in the data directory."}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# Expose 'giveRecsForNewVec' as a view
def give_recs_for_new_vec(request):
    # Example: Use request.GET or request.POST to get user input
    data = request.GET.get('data')  # Assume data is passed as a GET parameter
    if data:
        parsed_data = json.loads(data)
    else:
        return JsonResponse({'error': 'No data provided'}, status=400)

    global user_id
    user = User(user_id)
    user.user_rep(parsed_data["artist_id"],parsed_data["raga_id"])

    #giveRecsForNewVec(user_rep,vec,raag,artist)
    user_liked = user.get_liked_recs()
    recommendations = give_recs(['','',''],user_liked)
    rec_list = []
    for tuple in recommendations:
        rec_list.append(audio_details(tuple[1]))
    return JsonResponse({'recommendations': rec_list})

# Expose 'getRaagRec' as a view
def get_raag_rec(request):
    raag_name = request.GET.get('raag_name')
    if not raag_name:
        return JsonResponse({'error': 'No raag_name provided'}, status=400)
    
    global user_id
    user = User(user_id)
    user_liked = user.get_liked_recs()
    recommendations = raag_rec(raag_name,user_liked)
    rec_list = []
    for tuple in recommendations:
        rec_list.append(audio_details(tuple[1]))
    return JsonResponse({'recommendations': rec_list})

# Expose 'getArtistRec' as a view
def get_artist_rec(request):
    artist_name = request.GET.get('artist_name')
    if not artist_name:
        return JsonResponse({'error': 'No artist_name provided'}, status=400)
    global user_id
    user = User(user_id)
    user_liked = user.get_liked_recs()
    recommendations = artist_rec(artist_name,user_liked)
    rec_list = []
    for tuple in recommendations:
        rec_list.append(audio_details(tuple[1]))
    return JsonResponse({'recommendations': rec_list})

# # Expose 'getAudioDetails' as a view
# def get_audio_details(request):
#     audio_id = request.GET.get('audio_id')
#     if not audio_id:
#         return JsonResponse({'error': 'No audio_id provided'}, status=400)
#     details = audio_details(audio_id)
#     return JsonResponse({'audio_details': details})