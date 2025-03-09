document.addEventListener("DOMContentLoaded", function () {
    const form = document.getElementById("uploadForm");
    const fileInput = document.getElementById("fileInput");
    const ingredientsDisplay = document.getElementById("ingredients");
    const recipesDisplay = document.getElementById("recipes");
    const uploadedImage = document.getElementById("uploadedImage");

    form.addEventListener("submit", function (event) {
        event.preventDefault();
        
        const formData = new FormData(form);
        
        fetch("/upload", {
            method: "POST",
            body: formData
        })
        .then(response => response.json())
        .then(data => {
            if (data.error) {
                alert(data.error);
                return;
            }

            // Show the uploaded image
            uploadedImage.src = data.image_url;
            uploadedImage.style.display = "block";

            // Display detected ingredients
            ingredientsDisplay.textContent = data.ingredients;

            // Display recipes
            recipesDisplay.innerHTML = "";
            data.recipes.forEach(recipe => {
                let li = document.createElement("li");
                li.textContent = recipe;
                recipesDisplay.appendChild(li);
            });
        })
        .catch(error => console.error("Error:", error));
    });
});
