console.log("run")

fetch('output.txt')
  .then(response => response.text())
  .then(data => {
    // This is the text from output.txt
    let textFromFile = data;
    console.log(textFromFile)

    // Find the div by its ID (replace 'myDiv' with your div's ID)
    let myDiv = document.getElementById('flows_in');

    // Replace the text within the div
    myDiv.innerHTML = textFromFile;
  })
  .catch(error => console.error(error));


