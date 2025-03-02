import pytest
import numpy as np
import os
from get_features import extract_features  # Import your function

# Path to the directory containing test audio files
AUDIO_DIR = "mytest"

# Find all .wav files in the directory
audio_files = [os.path.join(AUDIO_DIR, f) for f in os.listdir(AUDIO_DIR) if f.endswith(".wav")]

@pytest.fixture(scope="module", params=audio_files)
def extracted_features(request):
    """Run extract_features **only once** per file and return results."""
    audio_file = request.param
    results = extract_features(audio_file)
    return audio_file, results

@pytest.mark.parametrize("feature", [
    "bpm", "rms", "centroid", "rolloff", "flux", "bandwidth", "contrast", "dynamic_range"
])
def test_feature_comparison(extracted_features, feature):
    """Compare our featurizer against Librosa for all features across multiple files."""
    
    audio_file, results = extracted_features

    # Define allowed tolerance for floating point comparison
    tolerance = 1  # Adjust if needed

    # Compare our feature against Librosa’s feature
    ours = results[f"{feature}_ours"]
    librosa = results[f"{feature}_librosa"]

    assert np.isclose(ours, librosa, atol=tolerance), (
        f"Feature {feature} mismatch in {audio_file}: Ours={ours}, Librosa={librosa}"
    )
