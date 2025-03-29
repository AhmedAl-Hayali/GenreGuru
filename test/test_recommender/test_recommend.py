import pytest
import pandas as pd
import numpy as np
from src.recommendation.recommend import Recommendation

# ✅ Create Mock Data (Simulating the CSV File)
MOCK_DATA = pd.DataFrame({
    'track_name': ['Song1', 'Song2', 'Song3'],
    'collapsed_rolloff_1': [10000, 9000, 8000],
    'collapsed_rolloff_2': [11000, 9500, 8500],
    'collapsed_centroid_1': [3000, 2500, 2000],
    'collapsed_bandwidth_1': [4000, 3500, 3000],
    'collapsed_contrast_1': [50, 45, 40],
    'collapsed_rms_1': [-5, -6, -7],
    'collapsed_dynamic_range_1': [5, 6, 7],
    'collapsed_instrumentalness_1': [0.9, 0.8, 0.7],
    'major': ['C Major', 'D Major', 'E Major'],
    'minor': ['A Minor', 'B Minor', 'C Minor'],
    'bpm': [120, 110, 100]
})

@pytest.fixture
def recommendation():
    """Fixture to create a Recommendation instance using mock data."""
    return Recommendation(data=MOCK_DATA)

def test_init(recommendation):
    """Test initialization and data encoding."""
    assert recommendation.df.shape == MOCK_DATA.shape  # Ensure same number of rows/columns
    assert 'major' in recommendation.df_encoded.columns
    assert 'minor' in recommendation.df_encoded.columns

def test_data_encoding(recommendation):
    """Test major/minor encoding."""
    assert set(recommendation.df_encoded['major']) == {0, 1, 2}
    assert set(recommendation.df_encoded['minor']) == {0, 1, 2}

def test_feature_extraction(recommendation):
    """Test feature extraction."""
    assert len(recommendation.feature_cols) == len(MOCK_DATA.columns) - 1  # Excludes 'track_name'

def test_similarity_matrix(recommendation):
    """Test similarity matrix computation."""
    assert recommendation.similarity_df.shape == (3, 3)  # Should match number of tracks

def test_get_similar_songs(recommendation):
    """Test retrieval of similar songs."""
    similar_songs = recommendation.get_similar_songs('Song1', top_n=2)
    assert len(similar_songs) == 2  # Should return 2 similar songs
    assert 'Song1' not in similar_songs.index  # Should not include itself

def test_get_similar_songs_not_found(recommendation):
    """Test case when reference track is missing."""
    result = recommendation.get_similar_songs('UnknownSong')
    assert isinstance(result, str)
    assert "not found in dataset" in result
