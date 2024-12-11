# from django.shortcuts import render

# Create your views here.

import os
import pandas as pd
import json
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.http import FileResponse, JsonResponse
from django.conf import settings
from .utils import (
    giveRecsForNewVec as give_recs,
    getRaagRec as raag_rec,
    getArtistRec as artist_rec,
    getAudioDetails as audio_details,
    User
)
# import librosa


# map needed for intial recommendations
def artist_map(artist_map_file_name):
    # Read the CSV file into a pandas DataFrame
    df = pd.read_csv(artist_map_file_name)   #'/kaggle/input/artist-map/artist-map-3.csv'
    artist_dict = {}
    # Convert the DataFrame to a dictionary
    for _,row in df.iterrows():
        try:
            artist_id = row['artist_id']
            artist_name = row['artist_name']

            artist_dict[str(artist_id) ] = artist_name.strip()
        except:
            continue
    return artist_dict

artist_dict = artist_map("backend/data/artist-map.csv")

revartist_dict = {value: key for key, value in artist_dict.items()}

#raag dataset
def create_row_map(file_name, key_column_name):
    """
    Reads a CSV file and creates a dictionary where the keys are the values
    of the specified column and the values are the row numbers (1-based index).

    Args:
        file_name (str): Path to the CSV file.
        key_column_name (str): The column whose values will serve as keys.

    Returns:
        dict: A dictionary mapping column values to row numbers.
    """
    # Read the CSV file into a pandas DataFrame
    df = pd.read_csv(file_name)

    # Initialize an empty dictionary
    row_map = {}

    # Iterate through the DataFrame rows
    for index, row in df.iterrows():
        try:
            key_value = row[key_column_name].strip()  # Ensure the key is stripped of whitespace
            row_number = index  
            row_map[key_value] = row_number
        except Exception as e:
            print(f"Error processing row {index}: {e}")
            continue

    return row_map

# Example usage
file_name = "backend/data/raag-dataset.csv"  # Replace with your file path
key_column_name = "raag"   # Replace with the column name you want as keys

try:
    raag_row_map = create_row_map(file_name, key_column_name)
    # print("Raag Row Map:", raag_row_map)
except Exception as e:
    print("Error:", str(e))

id_dataset = pd.read_csv("backend/data/id_vectors.csv")


# Global variable to hold similarity data in memory
metadata = None
user_id = 1
user = User(user_id)


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
import json
from django.http import JsonResponse

def give_recs_for_new_vec(request):
    # Get the 'data' parameter from the query string
    data = request.GET.get('data')
    if not data:
        return JsonResponse({'error': 'No data provided'}, status=400)

    try:
        parsed_data = json.loads(data)
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid data format'}, status=400)

    # Assuming `revartist_dict` is defined elsewhere
    global user_id
    global user
    user.user_rep(
        revartist_dict[parsed_data["artist_id"].strip()],
        raag_row_map[parsed_data["raga_id"].strip()]
    )

    user_liked = user.get_liked_recs()
    recommendations = give_recs(['', '', ''], user_liked)
    rec_list = [audio_details(tuple[1]) for tuple in recommendations]

    return JsonResponse({'recommendations': rec_list})


from django.http import JsonResponse
import json

def give_recs_for_chosen_vec(request):
    # Get 'data' from query parameters
    data = request.GET.get('data')  # Expecting JSON string
    if not data:
        return JsonResponse({'error': 'No data provided'}, status=400)

    try:
        parsed_data = json.loads(data)  # Parse the JSON string into a dictionary
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON format'}, status=400)

    # Ensure 'Id' exists in parsed data
    if " Id" not in parsed_data:
        return JsonResponse({'error': '" Id" field is missing'}, status=400)

    # Process the data
    print("Will try now")
    print(parsed_data)
    print(id_dataset)
    try:
        vec1 = id_dataset.loc[id_dataset["meta_id"].astype(str) == parsed_data[" Id"]].values.tolist()

        print(vec1)
        global user
        user.like_rec(vec1[0])
        user_liked = user.get_liked_recs()
        recommendations = give_recs(vec1[0], user_liked)
        
        rec_list = []
        for tuple in recommendations:
            rec_list.append(audio_details(tuple[1]))
        return JsonResponse({'recommendations': rec_list})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


# Expose 'getRaagRec' as a view
def get_raag_rec(request):
    raag_name = request.GET.get('raag_name')
    if not raag_name:
        return JsonResponse({'error': 'No raag_name provided'}, status=400)
    
    global user

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

    global user
    user_liked = user.get_liked_recs()
    recommendations = artist_rec(artist_name,user_liked)
    rec_list = []
    for tuple in recommendations:
        rec_list.append(audio_details(tuple[1]))
    return JsonResponse({'recommendations': rec_list})

def generate_signed_url(request):
    file_name = request.GET.get('file')
    if not file_name:
        return JsonResponse({"error": "File name is required"}, status=400)

    # Retrieve the bucket name and API key from environment variables
    storj_bucket_name = os.getenv("STORJ_BUCKET_NAME")
    storj_api_key = os.getenv("STORJ_API_KEY")

    if not storj_bucket_name or not storj_api_key:
        return JsonResponse({"error": "Missing Storj credentials"}, status=500)

    # Construct the API endpoint to generate a signed URL
    url = f"https://api.storj.io/v1/buckets/{storj_bucket_name}/objects/{file_name}/download"

    # Define the headers with the API key
    headers = {
        "Authorization": f"Bearer {storj_api_key}",
    }

    # Prepare the expiration time (1 hour)
    expiration_time = 3600

    # Request signed URL from Storj
    params = {"expires": expiration_time}
    response = requests.get(url, headers=headers, params=params)

    if response.status_code == 200:
        signed_url = response.json().get("url")
        return JsonResponse({"signedUrl": signed_url})
    else:
        return JsonResponse({"error": "Failed to generate signed URL", "details": response.text}, status=500)

# # Expose 'getAudioDetails' as a view
# def get_audio_details(request):
#     audio_id = request.GET.get('audio_id')
#     if not audio_id:
#         return JsonResponse({'error': 'No audio_id provided'}, status=400)
#     details = audio_details(audio_id)
#     return JsonResponse({'audio_details': details})

AUDIO_DIR = '/app/audio_files'

def stream_audio_file(request):
    file_name = request.GET.get('file_name')
    file_path = os.path.join(AUDIO_DIR, file_name)
    if os.path.exists(file_path):
        return FileResponse(open(file_path, 'rb'), content_type='audio/mpeg')
    return JsonResponse({"error": "File not found"}, status=404)