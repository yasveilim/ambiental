function isLetter(str) {
  return str.length === 1 && str.match(/[a-z]/i);
}
function submitBook() {
  // Get the form element
  const form = document.querySelector("#document_pic");

  // Serialize the form data into JSON
  const formData = new FormData();

  // console.log("File data: ", form.files[0]);
  // console.log("Book ID: ", globalBookSelect.name);
  let shortName = globalBookSelect.name.split(" ").slice(0, 3).join(" ");
  shortName = shortName
    .split("")
    .map((x) => (isLetter(x) ? x : ""))
    .join("");

  let ctx = getCtx();
  let targetUserDump = JSON.stringify(ctx.targetUser);
  formData.append("book_id", globalBookSelect.doc_number);
  formData.append("document_name", shortName);
  formData.append("category", sectionName);
  formData.append("document", form.files[0], form.files[0].name);
  formData.append("targetUser", targetUserDump);
  //
  console.log(globalBookSelect, [...formData.entries()]);

  let csrftoken = Cookies.get("csrftoken");
  let config = {
    headers: {
      "X-CSRFToken": csrftoken,
    },
  };

  axios
    .post("/api/save-material-book/", formData, config)
    .then((response) => {
      closeModal();
      console.log(response.data);
    })
    .catch((error) => {
      console.error(error);
    });
}

/// Path: static/js/submitbook.js

const selectElement = document.querySelector("#users-list");

selectElement.addEventListener("click", () => {
  selectElement.classList.toggle("open");
});

selectElement.addEventListener("blur", () => {
  selectElement.classList.remove("open");
});
