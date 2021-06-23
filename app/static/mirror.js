const playlistSelect = document.querySelector(".playlists-select");

axios.get("/get_user_playlists").then(function ({ data }) {
  for (let playlist of data) {
    const option = document.createElement("option");
    option.value = playlist.id;
    option.innerText = playlist.name;
    playlistSelect.append(option);
  }
});
