const apiRequest = (endpoint, params) => {
  return axios.get(`/${endpoint}`, {
    params: params,
  });
};

const createSpotifyWidget = (
  track_id,
  container,
  className = "img-center",
  width = 300,
  height = 380
) => {
  container.innerHTML = `
  <iframe class="${className}" src="https://open.spotify.com/embed/track/${track_id}" 
  width="${width}" height="${height}" frameborder="0" allowtransparency="true" allow="encrypted-media">
  </iframe>
  `;
};
