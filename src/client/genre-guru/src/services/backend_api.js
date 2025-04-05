import axios from "axios";

let cachedBaseUrl = null;
let lastFetched = 0;
const TTL = 60 * 1000; // 1 minute in milliseconds

export const getBaseURL = async () => {
  const now = Date.now();

  // Only use cached URL if it's fresh
  if (cachedBaseUrl && now - lastFetched < TTL) {
    return cachedBaseUrl;
  }

  try {
    const response = await axios.get("https://genreguru.onrender.com/get-url");
    const url = response.data.url;

    if (!url) {
      throw new Error("No URL available from backend URL store.");
    }

    cachedBaseUrl = url;
    lastFetched = now;
    return url;
  } catch (error) {
    console.error("Error fetching backend URL from URL store:", error);
    throw error;
  }
};

// ✅ Upload a WAV file using FormData instead of base64
export const uploadWavFile = async (formData) => {
  try {
    const API_BASE_URL = await getBaseURL();
    const response = await axios.post(`${API_BASE_URL}/process`, formData, {
      headers: {
        "Content-Type": "multipart/form-data",
      },
    });

    return response.data.track_ids || []; // Expecting track_ids from backend
  } catch (err) {
    console.error("Upload failed:", err);
    throw err;
  }
};

// ✅ Submit a Deezer track for recommendations
export const fetchRecommendations = async (deezerTrack) => {
  try {
    const API_BASE_URL = await getBaseURL();
    const response = await axios.post(`${API_BASE_URL}/process`, {
      is_wav_file: false,
      deezer_track: deezerTrack,
    });

    return response.data.track_ids || [];
  } catch (error) {
    console.error("API error during recommendation request:", error);
    throw error;
  }
};
