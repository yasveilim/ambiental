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

  formData.append("book_id", globalBookSelect.doc_number);
  formData.append("document_name", shortName);
  formData.append("category", sectionName);
  formData.append("document", form.files[0], form.files[0].name);
  //
  console.log(globalBookSelect, [...formData.entries()]);

  let csrftoken = Cookies.get("csrftoken");
  let config = {
    headers: {
      "X-CSRFToken": csrftoken,
    },
  };

  // Send the JSON data to the server using Axios
  axios
    .post("/api/save-material-book/", formData, config)
    .then((response) => {
      // Handle the response from the server
      closeModal();
      console.log(response.data);
    })
    .catch((error) => {
      // Handle any errors that occurred during the request
      console.error(error);
    });
}
