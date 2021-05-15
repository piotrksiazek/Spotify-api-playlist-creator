const input = document.querySelector("input");
const button = document.querySelector("button");
const widgetContainer = document.querySelector("#spotifyWidget");
const lyricsContainer = document.querySelector("#lyrics");
const allAboutThatTrack = document.querySelector("#allAboutThatTrack");
const artistBanner = document.querySelector("#artistBanner");
const artistBio = document.querySelector("#artistBio");
const specifics = document.querySelector("#specifics");
const info = document.querySelector("#info");

const createLyrics = (lyrics, container) => {
  let splitLyrics = lyrics.split("\n");
  for (let line of splitLyrics) {
    const p = document.createElement("p");
    p.classList.add("verse");
    p.innerText = line;
    container.appendChild(p);
  }
};

button.addEventListener("click", () => {
  if (input.value) {
    let audioFeatures = {};
    let trackInfo = {};
    let artistInfo = {};
    Promise.all([
      apiRequest("get_audio_features", { track_id: input.value }),
      apiRequest("get_track_info", { track_id: input.value }),
    ]).then(([audioFeaturesResponse, trackInfoResponse]) => {
      audioFeatures = audioFeaturesResponse.data;
      trackInfo = trackInfoResponse.data;
      apiRequest("get_artist_info", { artist_name: trackInfo.artist }).then(
        (response) => {
          artistInfo = response.data;
          createSpotifyWidget(trackInfo.id, widgetContainer);
          createLyrics(trackInfo.lyrics, lyricsContainer);
          artistBanner.src = artistInfo.artist_banner;
          //if banner not found, placeholder should be hidden
          if (artistBanner.getAttribute("src") === "null")
            artistBanner.classList.toggle("invisible");

          artistBio.innerText = artistInfo.artist_bio;
          allAboutThatTrack.classList.toggle("invisible"); //make whole div visible
        }
      );
    });
  }
});
