import axios from 'axios';

// Function to get Spotify API token
const getSpotifyToken = async () => {
  const clientId = process.env.REACT_APP_SPOTIFY_CLIENT_ID;
  const clientSecret = process.env.REACT_APP_SPOTIFY_CLIENT_SECRET;

  const response = await axios.post('https://accounts.spotify.com/api/token', 
    new URLSearchParams({
      grant_type: 'client_credentials'
    }), 
    {
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Authorization': `Basic ${btoa(`${clientId}:${clientSecret}`)}`
      }
    }
  );

  return response.data.access_token;
};

// Search for a song using the Spotify API
export const searchSong = async (query) => {
  try {
    const token = await getSpotifyToken();
    const response = await axios.get(`https://api.spotify.com/v1/search`, {
      headers: {
        Authorization: `Bearer ${token}`
      },
      params: {
        q: query,
        type: 'track',
        limit: 10
      }
    });
    
    return response.data.tracks.items;
  } catch (error) {
    console.error("Spotify search failed:", error);
    throw error;
  }
};

// Upload File (placeholder, will integrate backend later)
export const uploadFile = async (file) => {
  const formData = new FormData();
  formData.append('file', file);

  try {
    return await axios.post('/api/upload', formData);
  } catch (error) {
    console.error("Upload failed:", error);
    throw error;
  }
};
