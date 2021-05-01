const validateInput = (checkbox, checkboxes) => {
  const numberOfChecked = [...checkboxes].filter((box) => box.checked).length;
  if (numberOfChecked > 5 && numberOfChecked) {
    checkbox.checked = false;
    return false;
  } else if (numberOfChecked < 1) {
    //One checkbox has to be checked
    checkbox.checked = true;
    return false;
  }
  return true;
};

const toggleCheckedClass = (checkbox) => {
  //   checkbox.parentNode.classList.toggle("checked");
  if (checkbox.checked) {
    checkbox.parentNode.classList.remove("unchecked");
    checkbox.parentNode.classList.add("checked");
  } else {
    checkbox.parentNode.classList.remove("checked");
    checkbox.parentNode.classList.add("unchecked");
  }
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

//TODO dodaj automatyczne zaznaczanie jednego pola.

const addCheckbox = (
  checkboxContainer,
  id,
  label,
  className,
  isChecked = False
) => {
  if (isChecked) {
    checkboxContainer.classList.add(className, "checked");
    checkboxContainer.innerHTML = `<input type="checkbox" class="track-checkbox" value=${id} id=${id} name="seed" checked>
                                  <label for=${id}>${label}</label>`;
  } else {
    checkboxContainer.classList.add(className, "unchecked");
    checkboxContainer.innerHTML = `<input type="checkbox" class="track-checkbox" value=${id} id=${id} name="seed">
                                  <label for=${id}>${label}</label>`;
  }
};

playlistSelect.addEventListener("change", function (evt) {
  const tracks = playlists[this.value];
  container.innerHTML = ""; //clear tracks from previous event
  for (let i = 0; i < tracks.length; i++) {
    const checkboxContainer = document.createElement("div");
    isChecked = i === 0 ? true : false; //at least one check box should be checked by default
    addCheckbox(
      checkboxContainer,
      tracks[i].id,
      tracks[i].name,
      "checkbox-container",
      isChecked
    );
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
