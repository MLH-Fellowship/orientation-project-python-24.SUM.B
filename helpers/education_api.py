from flask import jsonify, Response, abort
from models import Education

def handle_education_get_request(data, index = None):
    # Here if user pass in index, we return the educational details for that index
    if index is not None:
        try:
            index = int(index)
            # If index is in the range of the list of education objects, we return the education corresponding to that index in the list.
            if 0 <= index < len(data["education"]):
                edu = data["education"][index]
                return jsonify({
                    "course": edu.course,
                    "school": edu.school,
                    "start_date": edu.start_date,
                    "end_date": edu.end_date,
                    "grade": edu.grade,
                    "logo": edu.logo,
                })
            else:
                return jsonify({"error": "Education not found"})
        except ValueError:
            return jsonify({"error": "Invalid index. Must be an integer."})
        except Exception as e:
            return jsonify({"error": f"Server Error: {str(e)}"})
    else:
        # Returns all the education data present in the database. If there are none, returns an empty list
        return jsonify(data.get('education', []))
    

def handle_education_post_request(data, new_education_data):
    if new_education_data:
        # Create a new Education object and append it to the list of education objects
        edu = Education(
            course=new_education_data.get('course'),
            school=new_education_data.get('school'),
            start_date=new_education_data.get('start_date'),
            end_date=new_education_data.get('end_date'),
            grade=new_education_data.get('grade'),
            logo=new_education_data.get('logo')
        )
        data["education"].append(edu)
        return (data, jsonify({"id": len(data["education"]) - 1}))
    else:
        return (data, Response(status=400, description="Bad Request"))
    

def handle_education_put_request(data, index, new_education_data):
    try:
        index = int(index)
        if 0 <= index < len(data["education"]):
            # Update the education object at the given index
            edu = data["education"][index]
            edu.course = new_education_data.get('course', edu.course)
            edu.school = new_education_data.get('school', edu.school)
            edu.start_date = new_education_data.get('start_date', edu.start_date)
            edu.end_date = new_education_data.get('end_date', edu.end_date)
            edu.grade = new_education_data.get('grade', edu.grade)
            edu.logo = new_education_data.get('logo', edu.logo)
            return (data, jsonify(edu.__dict__))
        else:
            return (data, jsonify({"error": "Education not found"}))
    except ValueError:
        return (data, jsonify({"error": "Invalid index. Must be an integer."}))
    except Exception as e:
        return (data, jsonify({"error": f"Server Error: {str(e)}"}))