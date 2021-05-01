const validateInput = (checkbox, checkboxes) => {
  const numberOfChecked = [...checkboxes].filter((box) => box.checked).length;
  console.log(numberOfChecked);
  if (numberOfChecked > 5) {
    checkbox.checked = false;
    return false;
  }
  return true;
};

const toggleCheckedClass = (checkbox) => {
  checkbox.parentNode.classList.toggle("checked");
};

const toggleCheckbox = (checkbox) => {
  checkbox.checked = !checkbox.checked;
};

const playlistSelect = document.querySelector(".playlists-select");
const container = document.querySelector("#recommendations");
const playlists = {};
let checkboxes = [];
axios.get("/get_user_playlists").then(function ({ data }) {
  for (let playlist of data) {
    const option = document.createElement("option");
    option.value = playlist.id;
    option.innerText = playlist.name;
    playlists[playlist.id] = playlist.tracks;
    playlistSelect.append(option);
  }
});

playlistSelect.addEventListener("change", function (evt) {
  const tracks = playlists[this.value];
  container.innerHTML = ""; //clear tracks from previous event
  for (let i = 0; i < tracks.length; i++) {
    const checkboxContainer = document.createElement("div");
    checkboxContainer.classList.add("checkbox-container");
    checkboxContainer.innerHTML = `<input type="checkbox" class="track-checkbox" value=${tracks[i].id} id=track${i} name=${tracks[i].name}>
                            <label for=${tracks[i].name}>${tracks[i].name}</label>`;
    container.append(checkboxContainer);
  }
  checkboxes = document.querySelectorAll(".track-checkbox");
  checkboxes.forEach((checkbox) => {
    checkbox.parentNode.addEventListener("click", function (evt) {
      toggleCheckbox(checkbox);
      if (validateInput(checkbox, checkboxes)) {
        toggleCheckedClass(checkbox);
      }
    });
  });
});
