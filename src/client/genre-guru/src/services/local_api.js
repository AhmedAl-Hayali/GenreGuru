import axios from "axios";

// Send uploaded WAV file
export const uploadWavFile = async (file) => {
  try {
    const reader = new FileReader();
    return new Promise((resolve, reject) => {
      reader.onload = async () => {
        const base64Wav = reader.result.split(",")[1]; // Extract Base64 content

        const response = await axios.post("http://localhost:5000/process", {
          is_wav_file: true,
          file: base64Wav,
        });

        resolve(response.data.spotify_ids);
      };

      reader.onerror = (error) => reject(error);
      reader.readAsDataURL(file);
    });
  } catch (error) {
    console.error("Error uploading WAV file:", error);
    throw error;
  }
};

// Send Spotify ID for recommendations
export const fetchRecommendations = async (spotifyId) => {
  try {
    const response = await axios.post("http://localhost:5000/process", {
      is_wav_file: false,
      spotify_id: spotifyId,
    });

    return response.data.spotify_ids;
  } catch (error) {
    console.error("Error fetching recommendations:", error);
    throw error;
  }
};
