import json
import http.server
import joblib  # Use joblib for loading the model
import numpy as np

# Load your trained model (make sure to use the correct path to your model)
model = joblib.load('lasso_model.pkl')  # Use joblib.load() to load the model

# Debugging: Print the type of the loaded model
print(f"Loaded model type: {type(model)}")

# Define the handler for HTTP requests
class SimpleHTTPRequestHandler(http.server.BaseHTTPRequestHandler):

    def _send_response(self, response_data):
        """Helper function to send a JSON response."""
        self.send_response(200)
        self.send_header("Content-type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps(response_data).encode('utf-8'))

    def do_OPTIONS(self):
        """Handle OPTIONS request for CORS."""
        self.send_response(200)
        self.send_header("Access-Control-Allow-Origin", "*")  # Allow any origin (for testing purposes)
        self.send_header("Access-Control-Allow-Methods", "POST, GET, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()


    def do_POST(self):
        """Handle POST request for prediction."""
        # Read the content length to know how much data to read
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)  # Read the POST data

        # Convert POST data to JSON
        data = json.loads(post_data)

        # Extract features from the JSON request
        country = data.get("country")
        form = data.get("form")
        played_in_ipl_2022 = data.get("playedInIpl2022")
        reserve_price = data.get("reservePrice")
        played_in_ipl = data.get("playedInIpl")
        t20_cap = data.get("t20Cap")
        odi_cap = data.get("odiCap")

        # Ensure all values are numeric (convert to float or int where needed)
        try:
            country = int(country)  # Assuming country is numeric (modify if categorical)
            form = int(form)
            played_in_ipl_2022 = int(played_in_ipl_2022)
            reserve_price = int(reserve_price)
            played_in_ipl = int(played_in_ipl)
            t20_cap = int(t20_cap)
            odi_cap = int(odi_cap)
        except ValueError as e:
            response_data = {'error': f"Invalid input data: {str(e)}"}
            self._send_response(response_data)
            return

        # Create a feature array (make sure it's numeric)
        features = np.array([[country, form, played_in_ipl_2022, reserve_price, played_in_ipl, t20_cap, odi_cap]])

        # Debugging: Print the features being passed to the model
        print(f"Features being passed to model: {features}")

        # Predict using the model
        try:
            predicted_price = model.predict(features)
            # Round the predicted price to 2 decimal places
            predicted_price_rounded = round(predicted_price[0], 2)
            response_data = {
                'predictedPrice': predicted_price_rounded
            }
        except Exception as e:
            response_data = {'error': f"Model prediction failed: {str(e)}"}

        # Send CORS headers along with the response
        self.send_response(200)
        self.send_header("Content-type", "application/json")
        self.send_header("Access-Control-Allow-Origin", "*")  # Allow the frontend origin
        self.end_headers()

        # Send response back to the client
        self.wfile.write(json.dumps(response_data).encode('utf-8'))



    def do_GET(self):
        """Handle GET request."""
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(b"Welcome to the Auction Price Predictor!")

# Set up the server
def run(server_class=http.server.HTTPServer, handler_class=SimpleHTTPRequestHandler):
    server_address = ('', 8080)  # Listen on port 8080
    httpd = server_class(server_address, handler_class)
    print("Server running on http://localhost:8080")
    httpd.serve_forever()

# Run the server
if __name__ == "__main__":
    run()
