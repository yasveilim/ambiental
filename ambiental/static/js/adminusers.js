function selectUser(event, user) {
  console.log(event, "user=> ", user);

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

    console.log("Updating user: ", user.id);
    let csrftoken = Cookies.get('csrftoken');
    let config = {
        headers:  {
            'X-CSRFToken': csrftoken
        },
    };
    
    axios.put(`/api/admin-users/${user.id}/`, userUpdated, config).then((response) => { 
      console.log("response=>", response);
    });
  };

  if (!rightSide) {
    rightSide = createRightSide(topBar, updateUser);
  }

  const userFieldsDiv = document.querySelector(".container-form__group");

  setUserFieldsDiv(userFieldsDiv, user);
}

function createRightSide(topBar, onUpdate) {
  let rightSide = document.createElement("div");
  rightSide.classList.add("right-side");

  let updateButton = document.createElement("button");
  updateButton.textContent = "Actualizar";
  updateButton.onclick = onUpdate;
  updateButton.classList.add("update-button");
  rightSide.appendChild(updateButton);

  let deleteButton = document.createElement("button");
  deleteButton.textContent = "Borrar";
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
