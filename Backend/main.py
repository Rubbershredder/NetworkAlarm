from flask import Flask, request, jsonify, redirect, url_for
from flask_cors import CORS
import psycopg2

# Initialize Flask app and configure CORS
app = Flask(__name__)
CORS(app, origins=["http://localhost:5173"])  # Allowing only your frontend's origin

# Database connection
def get_db_connection():
    conn = psycopg2.connect(
        host="localhost",
        database="NetworkAlarmDB",
        user="postgres",
        password="postgres"
    )
    return conn

# User registration route
@app.route('/api/logins', methods=['POST'])
def register_user():
    # Get data from request
    data = request.get_json()

    # Extract user data from the request
    name = data.get("name")
    college_name = data.get("collegeName")
    email = data.get("email")
    phone = data.get("phone")
    college_id = data.get("collegeId")
    username = data.get("username")
    password = data.get("password")
    confirm_password = data.get("confirmPassword")
    year_of_study = data.get("yearOfStudy")
    address = data.get("address")

    # Basic validation
    if not name or not college_name or not email or not phone or not college_id or not username or not password:
        return jsonify({"message": "All fields are required"}), 400
    if password != confirm_password:
        return jsonify({"message": "Passwords do not match"}), 400

    # Create a new user in the database
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        # Insert user data into the users table
        cursor.execute("""
            INSERT INTO users (name, college_name, email, phone, college_id, username, password, year_of_study, address)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (name, college_name, email, phone, college_id, username, password, year_of_study, address))
        
        # Commit the transaction and close the connection
        conn.commit()
        cursor.close()
        conn.close()

        return jsonify({"message": "User registered successfully"}), 201
    except Exception as e:
        return jsonify({"message": f"An error occurred: {str(e)}"}), 500

# User login route (for later use)
@app.route('/api/logins/login', methods=['POST'])
def login_user():
    data = request.get_json()

    email = data.get("email")
    password = data.get("password")

    if not email or not password:
        return jsonify({"message": "Username and password are required"}), 400

    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        # Check if the user exists in the database
        cursor.execute("""
            SELECT * FROM users WHERE email = %s AND password = %s
        """, (email, password))

        user = cursor.fetchone()

        if user:
            # Redirect to the home page
            return redirect("http://localhost:5173/home")
        else:
            return jsonify({"message": "Invalid credentials"}), 401
    except Exception as e:
        return jsonify({"message": f"An error occurred: {str(e)}"}), 500
    finally:
        cursor.close()
        conn.close()

if __name__ == "__main__":
    app.run(debug=True)
