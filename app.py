import openai
from flask import Flask, jsonify, request, make_response
from flask_cors import CORS
from DataBaseCreator import add_user  # Assuming this is correctly adjusted

import os
import bleach

app = Flask(__name__)
CORS(app)

@app.route('/api/v1/submit-form', methods=['POST', 'OPTIONS'])
def submit_form():
    if request.method == 'OPTIONS':
        # Handle CORS preflight request
        response = make_response()
        response.headers.add("Access-Control-Allow-Origin", "*")
        response.headers.add("Access-Control-Allow-Headers", "Content-Type")
        response.headers.add("Access-Control-Allow-Methods", "POST, OPTIONS")
        return response

    # Process the POST request
    try:
        data = request.get_json()

        # Sanitize inputs
        username = bleach.clean(data.get('username', ''))
        email = bleach.clean(data.get('email', ''))

        # Collect dietary preferences only if marked as True
        diet_info = []
        if data.get('kosher', False):
            diet_info.append('kosher')
        if data.get('vegan', False):
            diet_info.append('vegan')
        if data.get('vegetarian', False):
            diet_info.append('vegetarian')
        if data.get('halal', False):
            diet_info.append('halal')
        diet_info = ', '.join(diet_info) if diet_info else None  # Convert list to string or None if empty

        # Process allergens and preferences
        allergens = ', '.join([bleach.clean(a) for a in data.get('allergens', [])])
        preferences = bleach.clean(data.get('preferences', ''))

        # Store data in database
        add_user(username, email, diet_info, allergens, preferences)

        # Return a success response
        return jsonify({
            "message": "Form submitted successfully!",
            "data": {
                "username": username,
                "email": email,
                "diet_info": diet_info,
                "allergens": allergens,
                "preferences": preferences
            }
        }), 200

    except Exception as e:
        print(f"Error processing form submission: {e}")
        # Return an error response
        return jsonify({
            "message": "An error occurred while processing the form.",
            "error": str(e)
        }), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8001)