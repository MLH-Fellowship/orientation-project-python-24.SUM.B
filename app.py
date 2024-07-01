'''
Flask Application
'''
from spellchecker import SpellChecker
from flask import Flask, jsonify, request, abort, Response
from models import Experience, Education, Skill, PersonalInfo
from helpers.education_api import *
from helpers.personal_info_api import *

app = Flask(__name__)
spell = SpellChecker(distance=2)

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
    ],
    "pesronal_info": PersonalInfo("Zeyad Tarek","zeyad.ta01@gmail.com","+201111111111")
    
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
    '''
    Returns a JSON object from a GET request for a specific experience ID.
    If the ID is not found/is out of bounds, raises a 404.
    '''
    if request.method == 'GET':
        index = request.args.get("id")
        index = int(index)
        if 0 <= index < len(data["experience"]) and len(data["experience"]) > 0:
            exp = data["experience"][index]
            return jsonify({
                "title": exp.title,
                "company": exp.company,
                "start_date": exp.start_date,
                "end_date": exp.end_date,
                "description": exp.description,
                "logo": exp.logo,
                })
        abort(404, description="Experience not found") # 404 if ID isn't valid

    if request.method == 'POST':
        experience_data = request.json
        new_experience = Experience(experience_data["title"],
                                    experience_data["company"],
                                    experience_data["start_date"],
                                    experience_data["end_date"],
                                    experience_data["description"],
                                    experience_data["logo"])
        data["experience"].append(new_experience)
        return jsonify({"id": len(data["experience"])-1})
    
    if request.method == 'DELETE':
        index = request.args.get("id")
        index = int(index)
        if 0 <= index < len(data["experience"]) and len(data["experience"]) > 0:
            data["experience"].pop(index)
            return Response(status=204) # Return no content body, not necessary for DELETE
        abort(404, description="Experience not found")
        
    return jsonify({})

@app.route('/resume/education/', methods=['GET', 'POST', 'PUT'])
def education():
    '''
    Handles education requests
    '''
    if request.method == 'GET':
        index = request.args.get("id")
        return handle_education_get_request(data, index)
    if request.method == 'POST':
        new_education_data = request.json
        data, response = handle_education_post_request(data, new_education_data)
        return response
    if request.method == 'PUT':
        index = request.args.get("id")
        index = int(index)
        new_education_data = request.json
        data, response = handle_education_put_request(data, new_education_data, index)
        return response
    if request.method == 'DELETE':
        index = request.args.get("id")
        data, response = handle_education_delete_request(data, index)
        return response

    return jsonify({})

# To Get, Add, and update personal info
@app.route('/resume/personal-info/', methods=['GET', 'POST', 'PUT'])
def personal_info():
    '''
    Handles personal info requests
    '''
    if request.method == 'GET':
        return get_personal_data(data)
    if request.method == 'POST':
        new_personal_data = request.json
        data, response = add_personal_data(data, new_personal_data)
        return response
    if request.method == 'PUT':
        updated_personal_data = request.json
        data, response = update_personal_data(data, updated_personal_data)
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

@app.route('/resume/spell-check', methods=['POST'])
def spell_check():
    '''
    Handle spell checking on phrases.
    Note that since the spell checker is based on a simple Levenshtein Distance algorithm,
    some spell checking results may not be exactly correct.
    
    Returns a JSON format equivalent to the one suggested in issue #11.
    '''
    if request.method == 'POST':
        phrase = request.args.get("phrase")
        word_list = phrase.split()
        correct_phrase = ""
        corrections = spell.unknown(word_list)
        for word in word_list:
            if word.lower() not in corrections:
                correct_phrase = correct_phrase + " " + word
            else:
                correct_phrase = correct_phrase + " " + spell.correction(word)
        # Remove the first space added by the loop
        correct_phrase = correct_phrase[1:]
        return jsonify([{"before": phrase, "after": correct_phrase.capitalize()}])
