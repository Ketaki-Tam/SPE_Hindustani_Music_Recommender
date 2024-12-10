import pytest
import pandas as pd
import os
from backend.rec_app.utils import artist_map, get_audio_similarities, get_audio_file_names, load_scores
import json

@pytest.fixture
def mock_artist_map_file():
    test_file = "test_artist_map.csv"
    data = {
        "artist_id": ["1", "2", "3"],
        "artist_name": ["Artist A", "Artist B", "Artist C"]
    }
    df = pd.DataFrame(data)
    df.to_csv(test_file, index=False)
    yield test_file
    os.remove(test_file)

def test_artist_map(mock_artist_map_file):
    result = artist_map(mock_artist_map_file)
    expected = {"1": "Artist A", "2": "Artist B", "3": "Artist C"}
    assert result == expected



@pytest.fixture
def mock_audio_sim_file():
    test_file = "test_audio_similarities.json"
    data = {"('song1', 'song2')": 0.85, "('song2', 'song3')": 0.65}
    with open(test_file, 'w') as f:
        json.dump(data, f)
    yield test_file
    os.remove(test_file)

def test_get_audio_similarities(mock_audio_sim_file):
    result = get_audio_similarities(mock_audio_sim_file)
    expected = {"('song1', 'song2')": 0.85, "('song2', 'song3')": 0.65}
    assert result == expected



@pytest.fixture
def mock_audio_files():
    test_dir = "test_audio_files"
    os.makedirs(test_dir)
    with open(os.path.join(test_dir, "song1.mp3"), "w") as f:
        f.write("dummy content")
    with open(os.path.join(test_dir, "song2.wav"), "w") as f:
        f.write("dummy content")
    yield test_dir
    for file in os.listdir(test_dir):
        os.remove(os.path.join(test_dir, file))
    os.rmdir(test_dir)

def test_get_audio_file_names(mock_audio_files):
    result = get_audio_file_names(mock_audio_files)
    expected = ["song1", "song2"]
    assert sorted(result) == sorted(expected)


@pytest.fixture
def mock_scores_file():
    test_file = "test_scores.json"
    data = {"('song1', 'song2')": 0.95}
    with open(test_file, 'w') as f:
        json.dump(data, f)
    yield test_file
    os.remove(test_file)

def test_load_scores(mock_scores_file):
    result = load_scores(mock_scores_file)
    expected = {"('song1', 'song2')": 0.95}
    assert result == expected


# from django.test import TestCase
# import pandas as pd
# import os
# from backend.rec_app.utils import artist_map, get_audio_similarities, get_audio_file_names
# import json

# class ArtistMapTests(TestCase):
#     def setUp(self):
#         self.test_file = "test_artist_map.csv"
#         data = {
#             "artist_id": ["1", "2", "3"],
#             "artist_name": ["Artist A", "Artist B", "Artist C"]
#         }
#         df = pd.DataFrame(data)
#         df.to_csv(self.test_file, index=False)

#     def tearDown(self):
#         os.remove(self.test_file)

#     def test_artist_map(self):
#         result = artist_map(self.test_file)
#         expected = {"1": "Artist A", "2": "Artist B", "3": "Artist C"}
#         self.assertEqual(result, expected)




# class AudioSimilaritiesTests(TestCase):
#     def setUp(self):
#         self.test_file = "test_audio_similarities.json"
#         data = {"('song1', 'song2')": 0.85, "('song2', 'song3')": 0.65}
#         with open(self.test_file, 'w') as f:
#             json.dump(data, f)

#     def tearDown(self):
#         os.remove(self.test_file)

#     def test_get_audio_similarities(self):
#         result = get_audio_similarities(self.test_file)
#         expected = {"('song1', 'song2')": 0.85, "('song2', 'song3')": 0.65}
#         self.assertEqual(result, expected)



# class AudioFileNamesTests(TestCase):
#     def setUp(self):
#         self.test_dir = "test_audio_files"
#         os.makedirs(self.test_dir)
#         with open(os.path.join(self.test_dir, "song1.mp3"), "w") as f:
#             f.write("dummy content")
#         with open(os.path.join(self.test_dir, "song2.wav"), "w") as f:
#             f.write("dummy content")

#     def tearDown(self):
#         for file in os.listdir(self.test_dir):
#             os.remove(os.path.join(self.test_dir, file))
#         os.rmdir(self.test_dir)

#     def test_get_audio_file_names(self):
#         result = get_audio_file_names(self.test_dir)
#         expected = ["song1", "song2"]
#         self.assertEqual(sorted(result), sorted(expected))

# class LoadScoresTests(TestCase):
#     def setUp(self):
#         self.test_file = "test_scores.json"
#         data = {"('song1', 'song2')": 0.95}
#         with open(self.test_file, 'w') as f:
#             json.dump(data, f)

#     def tearDown(self):
#         os.remove(self.test_file)

#     def test_load_scores(self):
#         from backend.rec_app.utils import load_scores
#         result = load_scores(self.test_file)
#         expected = {"('song1', 'song2')": 0.95}
#         self.assertEqual(result, expected)


# class AudioSimilarityTests(TestCase):
#     def setUp(self):
#         # Mocking meta_dataset and simA
#         from backend.rec_app.utils import meta_dataset, simA
#         self.meta_dataset = meta_dataset
#         self.simA = simA

#     def test_get_audio_similarity(self):
#         from backend.rec_app.utils import getAudioSimilarity
#         # Assuming test setup has proper mock data
#         similarity = getAudioSimilarity(1, 2)
#         self.assertTrue(0 <= similarity <= 1)

# class AudioDetailsTests(TestCase):
#     def test_get_audio_details(self):
#         from backend.rec_app.utils import getAudioDetails
#         details = getAudioDetails(1)  # Assuming metadata exists for metaID = 1
#         self.assertIsInstance(details, dict)
#         self.assertIn("Artist", details)

