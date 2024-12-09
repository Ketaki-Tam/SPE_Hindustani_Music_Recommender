import pandas as pd
import numpy as np
import heapq
import pickle
import sys
import ast
import json
import os
import math

id_dataset = pd.read_csv("backend/data/id_vectors.csv")
meta_dataset = pd.read_csv("backend/data/metadata.csv")
dummy_metaID = len(id_dataset)

simR = np.load('backend/data/raag-similarity-matrix-mean.npy')
simM = np.load('backend/data/meta-similarity-matrix.npy')

zero_row = np.zeros((1, simM.shape[1]))  # One row with same number of columns as sim_meta
zero_col = np.zeros((simM.shape[0]+1, 1))  # One column with same number of rows as sim_meta

simM = np.concatenate([simM, zero_row], axis=0)  # Add row
simM = np.concatenate([simM, zero_col], axis=1)  # Add column


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

def get_audio_similarities(audio_sim_json):
    # Load JSON data from file
    with open(audio_sim_json, 'r') as f:   #'/kaggle/input/song-similarities/normalized_similarity_dict (1).json'
        simA = json.load(f)
    return simA

simA = get_audio_similarities("backend/data/scores.json")

def get_audio_file_names(directory):
    """
    Get the names of audio files (without extensions) from the specified directory.

    Args:
    - directory (str): Path to the directory containing audio files.

    Returns:
    - file_names (list): List of audio file names (without extensions) in the directory.
    """
    file_names = []
    # Iterate over all files in the directory
    for file_name in os.listdir(directory):
        # Check if the file is an audio file
        if file_name.endswith('.mp3') or file_name.endswith('.wav'):
            # Remove the extension and add the file name to the list
            file_names.append(os.path.splitext(file_name)[0])
    return file_names

def load_scores(path):
    # Load the JSON file
    with open(path, 'r') as json_file:   #'/kaggle/input/model-song-score/scores.json'
        sim = json.load(json_file)
    return sim

def compute_best_fits(sim, audio_files):   #define a dictionary to store this retruned dict

    global best_fit
    for i in range(len(audio_files)):
        max_obs = -float('inf')
        file_name = audio_files[i]
        for j in range(len(audio_files)):
            if i != j:
                other_file_name = audio_files[j]
                try:
                    score_diff = sim[f'(\'{file_name}\', \'{other_file_name}\')']
                    if score_diff > max_obs:
                        max_obs = score_diff                        
                except KeyError:
                    continue
        best_fit[file_name]=max_obs


def getAudioSimilarity(songID1,songID2): 
    coeff = 1/1000000
    try:
        rec1 = meta_dataset.loc[int(songID1),'Name'] + 'mp'
        rec2 = meta_dataset.loc[int(songID2),'Name'] + 'mp'
        global best_fit
        sim12 = (-2 / math.pi * math.atan(math.pi * coeff *abs(simA[f'(\'{rec1}\', \'{rec2}\')']) / 2) + 1)
        sim21 = (-2 / math.pi * math.atan(math.pi * coeff *abs(simA[f'(\'{rec2}\', \'{rec1}\')']) / 2) + 1)
        return (sim12+sim21)/2
    except:
        return 0
    
def rec_sim(rec1,rec2,user):

    rec1_split = ""
    user_split = ""
    rec2_split = ""
    
    
    if rec1 != "":
        rec1_split = rec1.split('|')
    if user[2] != "":
        user_split = user[0].split('|')
    if rec2 != "":
        rec2_split = rec2.split('|')
    
    sim = 0
    
    length = (len(rec1_split)+len(user_split)) * len(rec2_split)
    if length == 0:
        return 0
    
    for recID in rec1_split:
        for recID2 in rec2_split:
            sim += getAudioSimilarity(recID,recID2)

    for recID in user_split:
        for recID2 in rec2_split:
            sim +=getAudioSimilarity(recID,recID2)/5
    return sim/length



def artist_sim(artist1,artist2,user):

    artist1_split = ""
    user_split = ""
    artist2_split = ""
    
    
    if artist1 != "":
        artist1_split = artist1.split('|')
    if user[1] != "":
        user_split = user[1].split('|')
    if artist2 != "":
        artist2_split = artist2.split('|')
    
    sim = 0
    length1 = len(artist1_split)*len(artist2_split)
    length2 = (len(user_split))*len(artist2_split)
   
    try:
        for artistID in artist1_split:
            for artistID2 in artist2_split:
                artist1_name = artist_dict[artistID]
                artist2_name = artist_dict[artistID2]
                if artist1_name == artist2_name:
                    sim+=1
                else:
                    sim+= simA[f'(\'{artist1_name}\', \'{artist2_name}\')']/length1
    
    except:
        sim =0
    
    try:
        for artistID in user_split:
            for artistID2 in artist2_split:
                artist1_name = artist_dict[artistID]
                artist2_name = artist_dict[artistID2]
                if artist1_name == artist2_name:
                    sim+=1
                else:
                    sim+= simA[f'(\'{artist1_name}\', \'{artist2_name}\')'] / (5*length2)
    except:
        sim+=sim
    return sim/4



def raag_sim(raga1,raga2,user):
    raga1_split = ""
    user_split = ""
    raga2_split = ""
    
    if raga1 != "":
        raga1_split = raga1.split('|')
    if raga2 != "":
        raga2_split = raga2.split('|')
    if user[2] != "":
        user_split = user[2].split('|')
    
    sim = 0
    
    length1 = len(raga1_split)*len(raga2_split)
    length2 = (len(user_split))*len(raga2_split)
    
    for ragaID in raga1_split:
        for ragaID2 in raga2_split:
            sim += simR[int(ragaID),int(ragaID2)]/length1
    for ragaID in user_split:
        for ragaID2 in raga2_split:
            sim += simR[int(ragaID),int(ragaID2)] / (5*length2)
            
    return sim/2


def meta_sim(meta1,meta2,user):
    try:
        meta1_split = ""
        user_split = ""
        meta2_split = ""
    
        if meta1 != "":
            meta1_split = meta1.split('|')
        if user[0] != "":
            user_split = user[0].split('|')
        if meta2 != "":
            meta2_split = meta2.split('|')
        sim=0
        
        length1 = len(meta1_split)*len(meta2_split)
        length2 = (len(user_split))*len(meta2_split)
        
    
        for metaID in meta1_split:
            for metaID2 in meta2_split:
                sim += simM[int(metaID),int(metaID2)]/length1
        for metaID in user_split:
            for metaID2 in meta2_split:
                sim += simM[int(metaID), int(metaID2)] /(5*length2)
            
        return sim/2
    except:
        return 0
    


class User:
    
    def __init__(self, user_id):
        self.user_id = user_id
        #self.liked_recs = []
        self.liked_recs = ["","",""]
    
    def like_rec(self, rec):
        for i in range(len(self.liked_recs)):
            if self.liked_recs[i] == "":
                self.liked_recs[i]+=str(rec[i])
            else:
                self.liked_recs[i] +="|"+str(rec[i])        #if rec not in self.liked_recs:
         #   self.liked_recs.append(rec)


        
    def get_liked_recs(self):
        return self.liked_recs

    
    def user_rep(self,artistID,ragaID):
        user_rep = []
        user_rep.append(str(dummy_metaID))
        user_rep.append(str(artistID))
        user_rep.append(str(ragaID))
        
        self.like_rec(user_rep)


def giveRecsForNewVec(vec,user_rep):
    
        
    priority_queue = []
    
    for index,rec in id_dataset.iterrows():
            
        score =(rec_sim(str(vec[0]),str(rec['meta_id']),user_rep) + meta_sim(str(vec[0]),str(rec['meta_id']),user_rep)+artist_sim(str(vec[1]),str(rec['artist_id']),user_rep) +raag_sim(str(vec[2]),str(rec['raag_id']),user_rep))/4
        
        heapq.heappush(priority_queue, (-score,rec['meta_id']))  #max-heap
    
    #Display in descending order, using audio player allow the user to play the rec.
    recs = []

    for i in range(min(len(priority_queue),10)):
        recs.append(heapq.heappop(priority_queue))
    return recs


def getRaagRec(raag,user_rep):
    
    # Filter rows where the value in the "Raga" column equals the given raag
    raag_rows = meta_dataset[meta_dataset['Raga'] == raag]
    
    # Get the indexes of the filtered rows
    indexes = raag_rows.index.tolist()
    
    priority_queue = []
    
    customdf = []
    
    for meta_id in indexes:
        row =id_dataset.loc[meta_id].tolist()
        customdf.append(row)
    
    #print(customdf)
    id_data = pd.DataFrame(customdf, columns=['meta_id','artist_id','raag_id'])
    for index,rec in id_data.iterrows():
            
        score =(rec_sim('',str(rec['meta_id']),user_rep) + meta_sim('',str(rec['meta_id']),user_rep)+artist_sim('',str(rec['artist_id']),user_rep) +raag_sim('',str(rec['raag_id']),user_rep))/4
        #score =(artist_sim('',str(rec['artist_id']),user_rep)+meta_sim('',str(rec['meta_id']),user_rep) + rec_sim('',str(rec['meta_id']),user_rep))/3
        heapq.heappush(priority_queue, (-score,rec['meta_id']))  #max-heap
    
    #Display in descending order, using audio player allow the user to play the rec.
    recs = []
    for i in range(min(10,len(priority_queue))):
        recs.append(heapq.heappop(priority_queue))
    
    
    return recs

def getArtistRec(artist,user_rep):
    
    # Filter rows where the value in the "Raga" column equals the given raag
    raag_rows = meta_dataset[meta_dataset['Artist'] == artist]
    
    # Get the indexes of the filtered rows
    indexes = raag_rows.index.tolist()
    
    priority_queue = []
    
    customdf = []
    for meta_id in indexes:
        row =id_dataset.loc[meta_id].tolist()
        customdf.append(row)
    
    id_data = pd.DataFrame(customdf, columns=['meta_id','artist_id','raag_id'])
    for index,rec in id_data.iterrows():
            
        score =(rec_sim('',str(rec['meta_id']),user_rep) + meta_sim('',str(rec['meta_id']),user_rep)+artist_sim('',str(rec['artist_id']),user_rep) +raag_sim('',str(rec['raag_id']),user_rep))/4
        
        heapq.heappush(priority_queue, (-score,rec['meta_id']))  #max-heap
    
    
    #Display in descending order, using audio player allow the user to play the rec.
    recs = []
    for i in range(min(10,len(priority_queue))):
        recs.append(heapq.heappop(priority_queue))

    
    return recs



def get_file_path(audio_name, folder_path):
    # Concatenate ".mp3" to the audio name
    audio_file = audio_name+"mp.mp3"
    # Construct the full path to the file
    file_path = os.path.join(folder_path, audio_file)

    # Check if the file exists
    if os.path.isfile(file_path):
        return file_path
    

def getAudioDetails(metaID):
    row = meta_dataset.loc[metaID]
    
    artists = str(row['Artist']).split('|')
    row_artists = ""
    for artist in artists:
        row_artists +=artist
    
    instruments = str(row['Instrument']).split('|')
    row_instruments = ""
    for instrument in instruments:
        row_instruments +=instrument
        
    ragas = str(row['Raga']).split('|')
    row_ragas = ""
    for raga in ragas:
        row_ragas +=raga
    
    taals = str(row['Taal']).split('|')
    row_taals = ""
    for taal in taals:
        row_taals += taal
    
    layas = str(row['Laya']).split('|')
    row_layas = ""
    for laya in layas:
        row_layas += laya
    
    acc_instruments = str(row['Instruments']).split('|')
    row_acc_instruments = ""
    for acc_instrument in acc_instruments:
        row_acc_instruments += acc_instrument
        
        
    return {" Id":str(metaID),"Artist":row_artists,"Main Instrument":row_instruments,"Raga":row_ragas,"Taal":row_taals,"Laya":row_layas}


def getAudio(metaID):
    audio_path= meta_dataset.loc[metaID,'AudioPath']
    print(audio_path)
    audio,sr = librosa.core.load(audio_path, sr=44100, mono=True)   #need to use the full path for this
    try:
        with open(audio_path, 'rb') as f:
            audio_data = f.read()
            player(audio_data,sr)
    except OSError as e:
        print(f"Error playing audio: {e}")
    

revartist_dict = {value: key for key, value in artist_dict.items()}

