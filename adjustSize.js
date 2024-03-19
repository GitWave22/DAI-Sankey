fetch('output.txt')
  .then(response => response.text())
  .then(data => {
    // This is the text from output.txt
    let textFromFile = data;

    // Find the textarea by its ID (replace 'flows_in' with your textarea's ID)
    let myTextarea = document.getElementById('flows_in');

    // Replace the text within the textarea
    myTextarea.value = textFromFile;

    // Create a new 'change' event
    var event = new Event('change');

    // Dispatch it.
    myTextarea.dispatchEvent(event);
  })
  .catch(error => console.error(error));