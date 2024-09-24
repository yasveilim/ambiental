async function selectUser(event, userID) {
  let csrftoken = Cookies.get("csrftoken");
  let config = {
    headers: {
      "X-CSRFToken": csrftoken,
    },
  };

  console.log("Selecting user: ", userID);
  let responseData = await axios.get(
    `/api/admin-users/${userID.id}/`,
    null,
    config
  );
  user = responseData.data;

  const topBar = document.querySelector(".top-bar ");

  let rightSide = document.querySelector(".right-side");

  const updateUser = () => {
    // extract user data from user html
    const nameInput = userFieldsDiv.querySelector("#name");
    const lastnameInput = userFieldsDiv.querySelector("#lastname");
    const emailInput = userFieldsDiv.querySelector("#email");

    // update user data
    const userUpdated = {
      username: nameInput.value,
      lastname: lastnameInput.value,
      email: emailInput.value,
    };

    axios
      .put(`/api/admin-users/${userID.id}/`, userUpdated, config)
      .then((response) => {
        console.log("response=>", response);
      });
  };

  const deleteUser = () => {
    console.log("Deleting user: ", userID, config);

    axios.delete(`/api/admin-users/${userID.id}/`, config);
  };

  if (!rightSide) {
    rightSide = createRightSide(topBar, updateUser, deleteUser);
  }

  const userFieldsDiv = document.querySelector(".container-form__group");

  setUserFieldsDiv(userFieldsDiv, user);
}

function createRightSide(topBar, onUpdate, onDelete) {
  let rightSide = document.createElement("div");
  rightSide.classList.add("right-side");

  let updateButton = document.createElement("button");
  updateButton.textContent = "Actualizar";
  updateButton.onclick = onUpdate;
  updateButton.classList.add("update-button");
  rightSide.appendChild(updateButton);

  let deleteButton = document.createElement("button");
  deleteButton.textContent = "Borrar";
  deleteButton.onclick = onDelete;
  deleteButton.classList.add("delete-button");
  rightSide.appendChild(deleteButton);

  topBar.appendChild(rightSide);
  return rightSide;
}

function setUserFieldsDiv(userFieldsDiv, user) {
  userFieldsDiv.style.display = "flex";
  userFieldsDiv.style["flex-direction"] = "column";
  userFieldsDiv.style.gap = "20px";

  const nameInput = userFieldsDiv.querySelector("#name");
  nameInput.value = user.username;

  const lastnameInput = userFieldsDiv.querySelector("#lastname");
  lastnameInput.value = user.lastname;

  const emailInput = userFieldsDiv.querySelector("#email");
  emailInput.value = user.email;
}
