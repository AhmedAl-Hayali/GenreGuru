import axios from 'axios';

// Function to get Spotify API token
const getSpotifyToken = async () => {
  const clientId = process.env.REACT_APP_SPOTIFY_CLIENT_ID;
  const clientSecret = process.env.REACT_APP_SPOTIFY_CLIENT_SECRET;

  const response = await axios.post(
    'https://accounts.spotify.com/api/token',
    new URLSearchParams({
      grant_type: 'client_credentials',
    }),
    {
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded',
        Authorization: `Basic ${btoa(`${clientId}:${clientSecret}`)}`,
      },
    }
  );

  return response.data.access_token;
};

// Function to fetch preview URL from Deezer using ISRC code
export const getDeezerPreview = async (isrc) => {
  try {
    const track = await getDeezerTrackFromISRC(isrc);
    return track?.preview || null;
  } catch (error) {
    console.error("Deezer preview fetch failed:", error);
    return null;
  }
};

export const getDeezerTrackFromISRC = async (isrc) => {
  try {
    const response = await axios.get(`https://genreguru.onrender.com/proxy/deezer?isrc=${isrc}`);
    return response.data;
  } catch (err) {
    console.error("Failed to fetch Deezer track from ISRC:", err);
    throw err;
  }
};





export const getSpotifyTrackFromISRC = async (isrc) => {
  const accessToken = await getSpotifyToken();
  const response = await axios.get(`https://api.spotify.com/v1/search`, {
    headers: {
      Authorization: `Bearer ${accessToken}`,
    },
    params: {
      q: `isrc:${isrc}`,
      type: "track",
      limit: 1,
    },
  });

  return response.data.tracks.items[0]; // null if not found
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

    // Enrich tracks with preview URLs if Spotify preview_url is null
    const updatedTracks = await Promise.all(
      tracks.map(async (track) => {
        if (!track.preview_url && track.external_ids?.isrc) {
          console.log(track.external_ids.isrc)
          const deezerPreview = await getDeezerPreview(track.external_ids.isrc);
          if (deezerPreview) {
            return { ...track, preview_url: deezerPreview }; // Add preview URL
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
  

  
  
  
  
