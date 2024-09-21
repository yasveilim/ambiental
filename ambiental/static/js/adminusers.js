function selectUser(event, user) {
    console.log(event, "user=> ", user);

    const topBar  = document.querySelector(".top-bar ")

    let rightSide = document.querySelector(".right-side")
    if (!rightSide) {
        rightSide = createRightSide(topBar);
    }

    const userFieldsDiv = document.querySelector(".container-form__group");

    setUserFieldsDiv(userFieldsDiv, user);
    

    console.log(topBar);
}

function createRightSide(topBar) {
    let rightSide = document.createElement("div");
    rightSide.classList.add("right-side");

    let updateButton = document.createElement("button");
    updateButton.textContent = "Actualizar";
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

    // ids name lastname email

    const nameInput = userFieldsDiv.querySelector("#name");
    nameInput.value = user.username;
    
    const lastnameInput = userFieldsDiv.querySelector("#lastname");
    lastnameInput.value = user.lastname;

    const emailInput = userFieldsDiv.querySelector("#email");
    emailInput.value = user.email;

    console.log(nameInput);
}