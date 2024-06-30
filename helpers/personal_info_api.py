from flask import jsonify, Response, abort
import json
from models import PersonalInfo
def load_country_data():
    with open("countries.json", 'r', encoding='utf-8') as f:
        countries_data = json.load(f)
    return countries_data

def validate_phone_number(phone_number):
    countries_data = load_country_data()
    valid_country_codes = [country['dial_code'] for country in countries_data]
    for code in valid_country_codes:
        if phone_number.startswith(code):
            return True
    return False

def get_personal_data(data):
    try:
      personal_info = data["personal_info"]
      return jsonify({
        "name": personal_info.name,
        "email": personal_info.email,
        "phone": personal_info.phone
      })

    except Exception as e:
      return jsonify({"error": f"Server Error: {str(e)}"})

def add_personal_data(data,new_personal_data):
    try:
      if new_personal_data:
        phone = new_personal_data.get('phone')
        if not phone.startswith("+"):
          phone = "+" + phone
        if not validate_phone_number(phone):
          abort(400, description="Invalid phone number, you must enter country code.")

        personal_info = PersonalInfo(
          name=new_personal_data.get('name'),
          email=new_personal_data.get('email'),
          phone=phone
        )
        data["personal_info"] = personal_info
        return (data, jsonify(personal_info.__dict__))
      else:
        abort(400, description="Bad Request")

    except Exception as e:
      return (data, jsonify({"error": f"Server Error: {str(e)}"}))

def update_personal_data(data, updated_personal_data):
    try:
      if updated_personal_data:
        phone = updated_personal_data.get('phone')
        if not phone.startswith("+"):
          phone = "+" + phone
        if not validate_phone_number(phone):
          abort(400, description="Invalid phone number, you must enter country code.")

        personal_info = data["personal_info"]
        personal_info.name = updated_personal_data.get('name', personal_info.name)
        personal_info.email = updated_personal_data.get('email', personal_info.email)
        personal_info.phone = phone
        return (data, jsonify(personal_info.__dict__))
      else:
        abort(400, description="Bad Request")

    except Exception as e:
      return (data, jsonify({"error": f"Server Error: {str(e)}"}))