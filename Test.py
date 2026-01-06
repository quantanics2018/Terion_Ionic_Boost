from flask import Flask, jsonify, request
import mysql.connector

app = Flask(__name__)

# ---- DB Connection Helper ----
def get_db_connection():
    try:
        conn = mysql.connector.connect(
            host="localhost",      # XAMPP usually localhost
            user="root",           # default user
            password="",           # default is empty in XAMPP
            database="ionic_boost" # your db name
        )
        return conn
    except mysql.connector.Error as e:
        print("Database connection error:", e)
        return None

# ---- Fetch User Details ----
def fetch_user_from_db(user_id):
    conn = get_db_connection()
    if not conn:
        return {"error": "Database connection failed"}

    try:
        cursor = conn.cursor(dictionary=True)
        query = "SELECT id, name, whatsapp_number, email, address, city, state, pincode FROM users WHERE id = %s"
        cursor.execute(query, (user_id,))
        row = cursor.fetchone()
        cursor.close()
        conn.close()

        if not row:
            return {"error": f"No user found with id {user_id}"}
        return row
    except mysql.connector.Error as e:
        return {"error": f"MySQL error: {e}"}


# ---- Flask Route ----
@app.route("/user/<int:user_id>")
def get_user(user_id):
    """API to fetch user details directly from DB"""
    user_data = fetch_user_from_db(user_id)
    print("User Data:", user_data)  # Debug log
    return jsonify(user_data)


if __name__ == "__main__":
    app.run(debug=True)
