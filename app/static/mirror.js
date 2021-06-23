const playlistSelect = document.querySelector(".playlists-select");
console.log("hello there");
axios
  .get("/get_user_playlists")
  .then(function ({ data }) {
    for (let playlist of data) {
      const option = document.createElement("option");
      option.value = playlist.id;
      option.innerText = playlist.name;
      playlistSelect.append(option);
    }
  })
  .catch((error) => console.log(error));
