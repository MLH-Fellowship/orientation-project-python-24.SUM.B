from flask import jsonify, Response, abort
from models import PersonalInfo

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
        personal_info = PersonalInfo(
          name=new_personal_data.get('name'),
          email=new_personal_data.get('email'),
          phone=new_personal_data.get('phone')
        )
        data["personal_info"] = personal_info
        return (data, jsonify({"personal_info": data["personal_info"]}))
      else:
        return (data, Response(status=400, description="Bad Request"))

    except Exception as e:
      return (data, jsonify({"error": f"Server Error: {str(e)}"}))

def update_personal_data(data, updated_personal_data):
    try:
      if updated_personal_data:
        personal_info = data["personal_info"]
        personal_info.name = updated_personal_data.get('name', personal_info.name)
        personal_info.email = updated_personal_data.get('email', personal_info.email)
        personal_info.phone = updated_personal_data.get('phone', personal_info.phone)
        return (data, jsonify(personal_info.__dict__))
      else:
        return (data, Response(status=400, description="Bad Request"))

    except Exception as e:
      return (data, jsonify({"error": f"Server Error: {str(e)}"}))