async function newUser() {
  let csrftoken = Cookies.get("csrftoken");
  let config = {
    headers: {
      "X-CSRFToken": csrftoken,
    },
  };

  const topBar = document.querySelector(".top-bar ");
  let rightSide = document.querySelector(".right-side");
  let rightSideNewUser = document.querySelector(".right-side-new-user");


  const createUser = () => {
    // extract user data from user html
    const nameInput = userFieldsDiv.querySelector("#name");
    const lastnameInput = userFieldsDiv.querySelector("#lastname");
    const emailInput = userFieldsDiv.querySelector("#email");
    const passwordInput = userFieldsDiv.querySelector("#newuser-password");

    // update user data
    const userUpdated = {
      username: nameInput.value,
      lastname: lastnameInput.value,
      password: passwordInput.value || "",
      email: emailInput.value,
    };

    axios
      .post(`/api/admin-users/`, userUpdated, config)
      .then((response) => {
        console.log("response=>", response);
      });
  };

  const cancelCreateUser = () => {
    const oldRightSideNewUser = document.querySelector(".right-side-new-user");
    console.log("oldRightSideNewUser=>", oldRightSideNewUser);
    oldRightSideNewUser.remove();

    const userFieldsDiv = document.querySelector(".container-form__group");
    userFieldsDiv.style.display = "none";
  };

  if (!rightSideNewUser) {
    rightSideNewUser = createRightSideNewUser(topBar, createUser, cancelCreateUser);
  }

  if (rightSide) {
    rightSide.remove();
  }

  let newUserObject = {
    username: "",
    lastname: "",
    email: ""
  };


  const userFieldsDiv = document.querySelector(".container-form__group");

  setUserFieldsDiv(
    userFieldsDiv, newUserObject, true
  );
}

function createRightSideNewUser(topBar, createUserFn, cancelCreateUserFn) {
  let rightSide = document.createElement("div");
  rightSide.classList.add("right-side-new-user");

  let updateButton = document.createElement("button");
  updateButton.textContent = "Crear";
  updateButton.onclick = createUserFn;

  updateButton.classList.add("add-user-button");
  rightSide.appendChild(updateButton);

  let deleteButton = document.createElement("button");
  deleteButton.textContent = "Cancelar";
  deleteButton.onclick = cancelCreateUserFn;
  deleteButton.classList.add("cancel-add-user-button");
  rightSide.appendChild(deleteButton);

  topBar.appendChild(rightSide);
  return rightSide;
}

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
    const passwordInput = userFieldsDiv.querySelector("#newuser-password");

    // update user data
    const userUpdated = {
      username: nameInput.value,
      lastname: lastnameInput.value,
      password: passwordInput.value || "",
      email: emailInput.value,
    };

    axios
      .put(`/api/admin-users/${userID.id}/`, userUpdated, config)
      .then((response) => {
        console.log("response=>", response);
      });
  };

  const deleteUser = () => {
    axios.delete(`/api/admin-users/${userID.id}/`, config).then((response) => {
      console.log("response=>", response);

      const btnId = `#user-card-${userID.id}`;
      const btn = document.querySelector(btnId);
      btn.remove();
    });
  };

  if (!rightSide) {
    rightSide = createRightSide(topBar);
  }

  const updateButton = rightSide.querySelector(".update-button");
  updateButton.onclick = updateUser;

  const deleteButton = rightSide.querySelector(".delete-button");
  deleteButton.onclick = deleteUser;

  const userFieldsDiv = document.querySelector(".container-form__group");

  setUserFieldsDiv(userFieldsDiv, user, false);
}

function createRightSide(topBar) {
  const rightSideNewUser = document.querySelector(".right-side-new-user");
  if (rightSideNewUser) {
    rightSideNewUser.remove();
  }

  let rightSide = document.createElement("div");
  rightSide.classList.add("right-side");

  let updateButton = document.createElement("button");
  updateButton.textContent = "Actualizar";
  //updateButton.onclick = onUpdate;

  updateButton.classList.add("update-button");
  rightSide.appendChild(updateButton);

  let deleteButton = document.createElement("button");
  deleteButton.textContent = "Borrar";
  //deleteButton.onclick = onDelete;
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
