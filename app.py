'''
Flask Application
'''
from flask import Flask, jsonify, request, abort, Response
from models import Experience, Education, Skill
from helpers.education_api import *

app = Flask(__name__)

data = {
    "experience": [
        Experience("Software Developer",
                   "A Cool Company",
                   "October 2022",
                   "Present",
                   "Writing Python Code",
                   "example-logo.png")
    ],
    "education": [
        Education("Computer Science",
                  "University of Tech",
                  "September 2019",
                  "July 2022",
                  "80%",
                  "example-logo.png")
    ],
    "skill": [
        Skill("Python",
              "1-2 Years",
              "example-logo.png")
    ]
}


@app.route('/test')
def hello_world():
    '''
    Returns a JSON test message
    '''
    return jsonify({"message": "Hello, World!"})


@app.route('/resume/experience', methods=['GET', 'POST', 'DELETE'])
def experience():
    '''
    Handle experience requests
    '''
    # This method return us a JSON object representing the data associated with the ID passed as query parameter
    # It can be None or an integer. If None it returns empty json object.
    if request.method == 'GET':
        return jsonify({})

    if request.method == 'POST':
        return jsonify({})
    
    if request.method == 'DELETE':
        index = request.args.get("id")
        index = int(index)
        if 0 <= index < len(data["experience"]) and len(data["experience"]) > 0:
            data["experience"].pop(index)
            return Response(status=204) # Return no content body, since it's not necessary for DELETE requests
        else:
            abort(404, description="Experience not found")
        
    return jsonify({})

@app.route('/resume/education/', methods=['GET', 'POST', 'DELETE', 'PUT'])
def education():
    '''
    Handles education requests
    '''
    # This method return us a JSON object representing the data associated with the ID passed as query parameter
    # It can be None or an integer. If None it returns empty json object.
    if request.method == 'GET':
        index = request.args.get("id")
        return handle_education_get_request(data, index)

    if request.method == 'POST':
        new_education_data = request.json
        data, response = handle_education_post_request(data, new_education_data)
        return response
    
    if request.method == 'DELETE':
        index = request.args.get("id")
        index = int(index)
        if 0 <= index < len(data["education"]) and len(data["education"]) > 0:
            data["education"].pop(index)
            return Response(status=204)
        else:
            abort(404, description="Education not found")
    
    if request.method == 'PUT':
        index = request.args.get("id")
        index = int(index)
        new_education_data = request.json
        data, response = handle_education_put_request(data, new_education_data, index)
        return response

    return jsonify({})


@app.route('/resume/skill', methods=['GET', 'POST', 'DELETE', 'PUT'])
def skill():
    '''
    Handles Skill requests
    '''
    if request.method == 'GET':
        return jsonify({})

    if request.method == 'POST':
        return jsonify({})
    if request.method == 'PUT':

        return jsonify({})
    if request.method == 'DELETE':
        return jsonify({})
    return jsonify({})


#Delete Existing Skill by Index
@app.route('/resume/skill/<int:skill_id>', methods=['DELETE'])

def delete_skill(skill_id):

    if 0 <= skill_id < len(data["skill"]):
        deleted_skill = data["skill"].pop(skill_id)
        return jsonify(deleted_skill.__dict__), 200
    else:
        abort(404, description="Skill not found")


#Update Exisitng Skill by Index
@app.route('/resume/skill/<int:skill_id>', methods=['PUT'])
def edit_skill(skill_id):

    if 0 <= skill_id < len(data["skill"]):
        skill_data = request.json
        new_skill = data["skill"](skill_id)
        new_skill.name = skill_data.get('name', new_skill.name)
        new_skill.proficiency = skill_data.get('proficiency', new_skill.proficiency)
        new_skill.logo = skill_data.get('logo', new_skill.logo)
        return jsonify(new_skill.__dict__), 200
    else:
        abort(404, description="Skill not found")
