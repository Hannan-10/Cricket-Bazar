function predictPrice() {
    // Get user input
    const formData = {
        country: document.getElementById("country").value,
        form: document.getElementById("form").value,
        playedInIpl2022: document.getElementById("playedInIpl2022").value,
        reservePrice: document.getElementById("reservePrice").value,
        playedInIpl: document.getElementById("playedInIpl").value,
        t20Cap: document.getElementById("t20Cap").value,
        odiCap: document.getElementById("odiCap").value
    };

    // Send a POST request to the backend
    fetch('http://localhost:8080/predict', { // Ensure the correct endpoint for prediction
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(formData)
    })
    .then(response => response.json())
    .then(data => {
        // Display the result
        document.getElementById("predictedPrice").textContent = `₹ ${data.predictedPrice} Lacs`;
        console.log(data.predictPrice);
    })
    .catch(error => {
        console.error("Error:", error);
    });
}