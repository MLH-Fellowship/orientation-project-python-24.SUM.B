from flask import jsonify, Response, abort

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
    
def handle_education_delete_request(data, index):
    index = int(index)
    if 0 <= index < len(data["education"]) and len(data["education"]) > 0:
        data["education"].pop(index)
        return Response(status=204)
    else:
        abort(404, description="Education not found")

