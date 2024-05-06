function submitBook() {
    // Get the form element
    const form = document.querySelector("#book-form");

    // Serialize the form data into JSON
    const formData = new FormData(form);
    const jsonData = {};
    for (let [key, value] of formData.entries()) {
        jsonData[key] = value;
    }

    //category book_id
    // TODO: Add the category and book_id to the JSON data
    jsonData["category"] = "Unknown"
    jsonData["book_id"] = "Unknown"
    /*
    // Send the JSON data to the server using Axios
    axios.post('/api/books', jsonData)
        .then(response => {
            // Handle the response from the server
            console.log(response.data);
        })
        .catch(error => {
            // Handle any errors that occurred during the request
            console.error(error);
        });
        */
    console.log(jsonData);
}