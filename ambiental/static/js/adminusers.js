async function loadUsers() {
  const container = document.querySelector(".flex-container");

  // 1. Eliminar todos los nodos hijos de "flex-container"
  while (container.firstChild) {
    console.log("container.firstChild=>", container.firstChild);
    container.removeChild(container.firstChild);
  }

  console.log("container=>", container.chh);

  try {
    /*
    let csrftoken = Cookies.get("csrftoken");
  let config = {
    headers: {
      "X-CSRFToken": csrftoken,
    },
  };
  */
    // 2. Hacer la solicitud a la API
    const response = await axios.get("/api/admin-users/");
    if (response.status != 200) {
      throw new Error("Error al obtener los usuarios");
    }
    const usersList = response.data.users; // Asumiendo que la API devuelve un JSON con la lista de usuarios

    // 3. Crear y agregar los nuevos elementos de usuario
    usersList.forEach((user) => {
      // Crear el botón de usuario
      const button = document.createElement("button");
      button.classList.add("button-select-user");
      button.setAttribute(
        "onclick",
        `selectUser(event, { "id": "${user.id}" })`
      );
      button.id = `user-card-${user.id}`;

      // Crear la estructura interna del botón
      const userCard = document.createElement("div");
      userCard.classList.add("user-card");

      const userImageDiv = document.createElement("div");
      userImageDiv.classList.add("user-image-div");

      const img = document.createElement("img");
      img.src = "/static/alejandro.jpeg"; // Puedes cambiar esta línea según la lógica de la imagen
      img.alt = "User Image";
      img.classList.add("user-image");

      const userInfo = document.createElement("div");
      userInfo.classList.add("user-info");

      const userName = document.createElement("h3");
      userName.classList.add("user-name");
      userName.textContent = user.username;

      const userEmail = document.createElement("p");
      userEmail.classList.add("user-lastname");
      userEmail.textContent = user.email;

      // Añadir todo a su lugar
      userImageDiv.appendChild(img);
      userInfo.appendChild(userName);
      userInfo.appendChild(userEmail);
      userCard.appendChild(userImageDiv);
      userCard.appendChild(userInfo);
      button.appendChild(userCard);
      container.appendChild(button);
    });
  } catch (error) {
    console.error("Error al cargar los usuarios:", error);
  }
}

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
      .then(async (response) => {
        console.log("response=>", response);
        await loadUsers();

        setUserFieldsDiv(userFieldsDiv, {
          username: "",
          lastname: "",
          email: "",
        });
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
    rightSideNewUser = createRightSideNewUser(
      topBar,
      createUser,
      cancelCreateUser
    );
  }

  if (rightSide) {
    rightSide.remove();
  }

  let newUserObject = {
    username: "",
    lastname: "",
    email: "",
  };

  const userFieldsDiv = document.querySelector(".container-form__group");

  setUserFieldsDiv(userFieldsDiv, newUserObject);
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

  const passwordInput = userFieldsDiv.querySelector("#newuser-password");
  if (user.password) {
    passwordInput.value = user.password;
  } else {
    passwordInput.value = "";
  }
}
