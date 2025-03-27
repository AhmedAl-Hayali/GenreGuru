import axios from 'axios';

const getSpotifyToken = async () => {
  try {
    const response = await fetch("http://localhost:5000/get_spotify_token");
    const data = await response.json();
    return data.access_token;
  } catch (error) {
    console.error("Error fetching token from Flask server:", error);
    throw error;
  }
};


// Function to fetch preview URL from Deezer using ISRC code
export const getDeezerPreview = async (isrc) => {
  try {
    const response = await axios.get(`https://cors-anywhere.herokuapp.com/http://api.deezer.com/track/isrc:${isrc}`);

    if (response.data && response.data.preview) {
      return response.data.preview; // Deezer preview URL (30s mp3)
    }
  } catch (error) {
    console.error('Deezer API search failed:', error);
  }

  return null; // Return null if no preview found
};

// Search for a song using the Spotify API
export const searchSong = async (query) => {
  try {
    const token = await getSpotifyToken();
    const response = await axios.get(`https://api.spotify.com/v1/search`, {
      headers: {
        Authorization: `Bearer ${token}`,
      },
      params: {
        q: query,
        type: 'track',
        limit: 10,
      },
    });

    let tracks = response.data.tracks.items;

    // Enrich tracks with iTunes preview URLs if Spotify preview_url is null
    const updatedTracks = await Promise.all(
      tracks.map(async (track) => {
        if (!track.preview_url && track.external_ids?.isrc) {
          console.log(track.external_ids.isrc)
          const deezerPreview = await getDeezerPreview(track.external_ids.isrc);
          if (deezerPreview) {
            return { ...track, preview_url: deezerPreview }; // Add iTunes preview URL
          }
        }
        return track;
      })
    );

    return updatedTracks;
  } catch (error) {
    console.error('Spotify search failed:', error);
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
    console.error('Upload failed:', error);
    throw error;
  }
};

// Fetch track details from Spotify
export const fetchTrackDetails = async (spotifyIds) => {
    try {
      const token = await getSpotifyToken(); // Ensure authentication
      const trackRequests = spotifyIds.map((spotifyId) =>
        axios.get(`https://api.spotify.com/v1/tracks/${spotifyId}`, {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        })
      );
  
      const trackResponses = await Promise.all(trackRequests);
      return trackResponses.map((res) => res.data);
    } catch (error) {
      console.error("Error fetching track details:", error);
      throw error;
    }
  };
  
  
  
  
  
