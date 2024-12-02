from flask import Blueprint, request, jsonify
from app.db import get_db_connection

registration_bp = Blueprint('registration', __name__)

@registration_bp.route('/register', methods=['POST'])
def create_registration():
    data = request.json
    name = data.get('name')
    email = data.get('email')
    date_of_birth = data.get('date_of_birth')
    phone_number = data.get('phone_number', None)

    connection = get_db_connection()
    cursor = connection.cursor()
    try:
        query = "INSERT INTO Registration (Name, Email, DateOfBirth, PhoneNumber) VALUES (%s, %s, %s, %s)"
        cursor.execute(query, (name, email, date_of_birth, phone_number))
        connection.commit()
        return jsonify({"message": "Registration created successfully"}), 201
    except Exception as e:
        connection.rollback()
        return jsonify({"error": str(e)}), 400
    finally:
        cursor.close()
        connection.close()

@registration_bp.route('/registrations', methods=['GET'])
def get_registrations():
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT * FROM Registration")
    registrations = cursor.fetchall()
    cursor.close()
    connection.close()
    return jsonify(registrations)

@registration_bp.route('/register/<int:id>', methods=['PUT'])
def update_registration(id):
    data = request.json
    name = data.get('name')
    email = data.get('email')
    date_of_birth = data.get('date_of_birth')
    phone_number = data.get('phone_number')

    connection = get_db_connection()
    cursor = connection.cursor()
    try:
        query = """UPDATE Registration 
                   SET Name=%s, Email=%s, DateOfBirth=%s, PhoneNumber=%s 
                   WHERE ID=%s"""
        cursor.execute(query, (name, email, date_of_birth, phone_number, id))
        connection.commit()
        return jsonify({"message": "Registration updated successfully"})
    except Exception as e:
        connection.rollback()
        return jsonify({"error": str(e)}), 400
    finally:
        cursor.close()
        connection.close()

@registration_bp.route('/register/<int:id>', methods=['DELETE'])
def delete_registration(id):
    connection = get_db_connection()
    cursor = connection.cursor()
    try:
        cursor.execute("DELETE FROM Registration WHERE ID=%s", (id,))
        connection.commit()
        return jsonify({"message": "Registration deleted successfully"})
    except Exception as e:
        connection.rollback()
        return jsonify({"error": str(e)}), 400
    finally:
        cursor.close()
        connection.close()
