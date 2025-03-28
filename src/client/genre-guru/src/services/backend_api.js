import axios from "axios";

let cachedBaseUrl = null;

// Fetch the dynamic backend URL from the URL store
export const getBaseURL = async () => {
  if (cachedBaseUrl) return cachedBaseUrl;

  try {
    const response = await axios.get("https://genreguru.onrender.com/get-url");
    const url = response.data.url;

    if (!url) {
      throw new Error("No URL available from backend URL store.");
    }

    cachedBaseUrl = url;
    return url;
  } catch (error) {
    console.error("Error fetching backend URL from URL store:", error);
    throw error;
  }
};

// Upload a WAV file for recommendations
export const uploadWavFile = async (file) => {
  try {
    const reader = new FileReader();

    return new Promise((resolve, reject) => {
      reader.onload = async () => {
        try {
          const base64Wav = reader.result.split(",")[1]; // Extract base64 string
          const API_BASE_URL = await getBaseURL();

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

// Submit a Deezer track for recommendations
export const fetchRecommendations = async (deezerTrack) => {
  try {
    const API_BASE_URL = await getBaseURL();

    const response = await axios.post(`${API_BASE_URL}/process`, {
      is_wav_file: false,
      deezer_track: deezerTrack,
    });

    return response.data.deezer_tracks;
  } catch (error) {
    console.error("API error during recommendation request:", error);
    throw error;
  }
};



