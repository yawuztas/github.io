// Select the button element
const tiklaBtn = document.getElementById("tiklaBtn");

// Add an event listener for the button click
tiklaBtn.addEventListener("click", function () {
    // Display an alert message
    alert("Butona tıkladın! 🎉");

    // Change the button text after clicking
    tiklaBtn.textContent = "Tekrar Tıkla!";

    // Create a new paragraph element dynamically
    const newParagraph = document.createElement("p");
    newParagraph.textContent = "Tebrikler, butona başarıyla tıkladınız!";
    newParagraph.style.color = "green";
    newParagraph.style.fontWeight = "bold";

    // Append the new paragraph to the body
    document.body.appendChild(newParagraph);

    // Change the background color of the page for fun
    document.body.style.backgroundColor = getRandomColor();
});

// Function to generate a random color
function getRandomColor() {
    const letters = "0123456789ABCDEF";
    let color = "#";
    for (let i = 0; i < 6; i++) {
        color += letters[Math.floor(Math.random() * 16)];
    }
    return color;
}