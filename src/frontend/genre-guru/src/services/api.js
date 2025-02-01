import axios from 'axios';

export const searchSong = async (query) => {
  return axios.get(`/api/search?q=${query}`);
};

export const uploadFile = async (file) => {
  const formData = new FormData();
  formData.append('file', file);
  return axios.post('/api/upload', formData);
};
