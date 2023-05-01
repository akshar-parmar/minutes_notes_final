// Wait for the page to finish loading
document.addEventListener("DOMContentLoaded", function() {

    // Get the "Upload Another File" link
    var uploadLink = document.querySelector("a");
  
    // Add a click event listener to the link
    uploadLink.addEventListener("click", function(event) {
      event.preventDefault(); // Prevent the default link behavior
      window.location.href = "/"; // Redirect the user to the index page
    });
  
  });
  