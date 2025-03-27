import axios from "axios";

// Backend API base URL
// DuckDNS Domain
const API_BASE_URL = "http://mygenre.duckdns.org:5000";
// For local testing, you can temporarily change it back to:
// const API_BASE_URL = "http://localhost:5000";

// Upload a WAV file for recommendations
export const uploadWavFile = async (file) => {
  try {
    const reader = new FileReader();

    return new Promise((resolve, reject) => {
      reader.onload = async () => {
        try {
          const base64Wav = reader.result.split(",")[1]; // Extract base64 string
          const response = await axios.post(`${API_BASE_URL}/process`, {
            is_wav_file: true,
            file: base64Wav,
          });

          resolve(response.data.spotify_ids);
        } catch (err) {
          console.error("API error during WAV upload:", err);
          reject(err);
        }
      };

      reader.onerror = (error) => {
        console.error("File reading error:", error);
        reject(error);
      };

      reader.readAsDataURL(file);
    });
  } catch (error) {
    console.error("Unexpected error during file upload:", error);
    throw error;
  }
};

// Submit a Spotify track ID for recommendations
export const fetchRecommendations = async (spotifyId) => {
  try {
    const response = await axios.post(`${API_BASE_URL}/process`, {
      is_wav_file: false,
      spotify_id: spotifyId,
    });

    return response.data.spotify_ids;
  } catch (error) {
    console.error("API error during Spotify ID request:", error);
    throw error;
  }
};
