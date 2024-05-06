function submitBook() {
    // Get the form element
    const form = document.querySelector("#book-form");

    // Serialize the form data into JSON
    const formData = new FormData(form);
    const jsonData = {};
    for (let [key, value] of formData.entries()) {
        jsonData[key] = value;
    }

    console.log(globalBookSelect);
    //category book_id
    // TODO: Add the category and book_id to the JSON data
    jsonData["category"] = sectionName;
    jsonData["book_id"] = globalBookSelect.doc_number;

    let csrftoken = Cookies.get('csrftoken');
    let config = {
        headers: {
            'X-CSRFToken': csrftoken
        },
    };

    // Send the JSON data to the server using Axios
    axios.post('/api/save-material-book/', jsonData, config)
        .then(response => {
            // Handle the response from the server
            console.log(response.data);
        })
        .catch(error => {
            // Handle any errors that occurred during the request
            console.error(error);
        });

    console.log(jsonData);
}