function selectUser(event) {
    console.log(event);

    let topBar  = document.querySelector(".top-bar ")

    let rightSide = document.querySelector(".right-side")
    if (!rightSide) {
        rightSide = createRightSide(topBar);
    }


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