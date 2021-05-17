const input = document.querySelector("input");
const button = document.querySelector("button");
const widgetContainer = document.querySelector("#spotifyWidget");
const lyricsContainer = document.querySelector("#lyrics");
const allAboutThatTrack = document.querySelector("#allAboutThatTrack");
const artistBanner = document.querySelector("#artistBanner");
const artistBio = document.querySelector("#artistBio");
const specifics = document.querySelector("#specifics");
const info = document.querySelector("#info");
const errorContainer = document.querySelector("#all_about_that_track_error");
const discography = document.querySelector("#discography");

const createLyrics = (lyrics, container) => {
  let splitLyrics = lyrics.split("\n");
  for (let line of splitLyrics) {
    const p = document.createElement("p");
    p.classList.add("verse");
    p.innerText = line;
    container.appendChild(p);
  }
};

const addContent = (content, container) => {
  let index = 0;
  for (let element of content) {
    if (element.text && element.type === "album") {
      const album = document.createElement("div");
      album.classList.add("album");
      album.innerHTML = `
      <div class="card" style="min-width: 18rem; max-width: 22rem;">
          <img class="card-img-top" src="${element.text.strAlbumThumb}" alt="Cover img not found">
          <div class="card-body">
            <h5 class="card-title">${element.text.strAlbum}</h5>
              <a class="submit" data-bs-toggle="collapse" href="#album${index}" role="button" aria-expanded="false" aria-controls="album${index}">
                  description
              </a>
          
              <div class="collapse" id="album${index}">
                  <div class="card card-body">${element.text.strDescriptionEN}</div>
              </div>
            <p class="card-text"><small class="text-muted">Year: ${element.text.intYearReleased}</small></p>
          </div>
      </div>
      `;
      container.append(album);
      index++;
    } else if (element.text) {
      //other cases
      const paragraph = document.createElement(element.type);
      paragraph.innerText = element.name + element.text;
      container.append(paragraph);
    }
  }
};

const createChart = ({
  energy,
  speechiness,
  acousticness,
  instrumentalness,
  liveness,
  valence,
}) => {
  console.log(energy);
  new Chartist.Bar(
    ".ct-chart",
    {
      labels: [
        "energy",
        "speechiness",
        "acousticness",
        "instrumentalness",
        "liveness",
        "valence",
      ],
      series: [
        [
          energy,
          speechiness,
          acousticness,
          instrumentalness,
          liveness,
          valence,
        ],
      ],
    },
    {
      seriesBarDistance: 10,
      reverseData: true,
      horizontalBars: true,
      axisY: {
        offset: 150,
      },
    }
  );
};

button.addEventListener("click", () => {
  if (input.value) {
    errorContainer.innerText = "";
    let audioFeatures = {};
    let trackInfo = {};
    let artistInfo = {};
    Promise.all([
      apiRequest("get_audio_features", { track_id: input.value }),
      apiRequest("get_track_info", { track_id: input.value }),
    ])
      .then(([audioFeaturesResponse, trackInfoResponse]) => {
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

            addContent(
              //specifics
              [
                { name: "mood: ", text: artistInfo.mood, type: "p" },
                { name: "genre: ", text: artistInfo.genre, type: "p" },
                { name: "style: ", text: artistInfo.style, type: "p" },
              ],
              specifics
            );

            addContent(
              //info
              [
                {
                  name: "formed year: ",
                  text: artistInfo.formed_year,
                  type: "p",
                },
                {
                  name: "number of members: ",
                  text: artistInfo.number_of_members,
                  type: "p",
                },
                { name: "country: ", text: artistInfo.country, type: "p" },
                { name: "website: ", text: artistInfo.website, type: "a" },
              ],
              info
            );
            const albums = artistInfo.discography.map((album) => {
              return { text: album, type: "album" };
            });
            console.log(albums);
            addContent(
              //discography
              albums,
              discography
            );

            artistBio.innerText = artistInfo.artist_bio;
            createChart(audioFeatures.audio_features);

            allAboutThatTrack.classList.toggle("invisible"); //make whole div visible
          }
        );
      })
      .catch((error) => {
        errorContainer.innerText =
          "Something went wrong. Maybe you pasted an artist uri instead of track uri?";
      });
  }
});
