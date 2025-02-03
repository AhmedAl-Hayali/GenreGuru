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

// Function to fetch preview URL from iTunes using ISRC code
const getiTunesPreview = async (isrc) => {
  try {
    const response = await axios.get('https://itunes.apple.com/lookup', {
      params: {
        isrc: isrc,
      },
    });

    if (response.data.results.length > 0) {
      return response.data.results[0].previewUrl; // iTunes preview URL
    }
  } catch (error) {
    console.error('iTunes API search failed:', error);
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
          const itunesPreview = await getiTunesPreview(track.external_ids.isrc);
          if (itunesPreview) {
            return { ...track, preview_url: itunesPreview }; // Add iTunes preview URL
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
  
  
  
  
  
