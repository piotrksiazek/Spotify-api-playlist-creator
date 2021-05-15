const button = document.querySelector("button");
const input = document.querySelector("input");
const width = 300;
const height = 380;
const validPlaceholder = "Spotify artist uri";
const invalidPlaceholder = "You must fill this field";

button.addEventListener("click", () => {
  if (input.value) {
    input.placeholder = validPlaceholder;
    axios
      .get("/get_least_popular_track", { params: { artist_id: input.value } })
      .then((response) => {
        const widget = document.querySelector("#spotifyWidget");
        widget.innerHTML = `
        <iframe src="https://open.spotify.com/embed/track/${response.data.track_id}"
        width="${width}" height="${height}" frameborder="0" allowtransparency="true" allow="encrypted-media"></iframe>
        `;
      });
  } else {
    input.placeholder = invalidPlaceholder;
  }
});

input.addEventListener("input", function () {
  this.placeholder = validPlaceholder;
});
