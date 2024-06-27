'''
Tests in Pytest
'''
from app import app


def test_client():
    '''
    Makes a request and checks the message received is the same
    '''
    response = app.test_client().get('/test')
    assert response.status_code == 200
    assert response.json['message'] == "Hello, World!"


def test_experience():
    '''
    Add a new experience and then get all experiences. 
    
    Check that it returns the new experience in that list
    '''
    example_experience = {
        "title": "Software Developer",
        "company": "A Cooler Company",
        "start_date": "October 2022",
        "end_date": "Present",
        "description": "Writing JavaScript Code",
        "logo": "example-logo.png"
    }

    item_id = app.test_client().post('/resume/experience',
                                     json=example_experience).json['id']
    response = app.test_client().get('/resume/experience')
    assert response.json[item_id] == example_experience


def test_education():
    '''
    Add a new education and then get all educations. 
    
    Check that it returns the new education in that list
    '''
    example_education = {
        "course": "Engineering",
        "school": "NYU",
        "start_date": "October 2022",
        "end_date": "August 2024",
        "grade": "86%",
        "logo": "example-logo.png"
    }
    item_id = app.test_client().post('/resume/education',
                                     json=example_education).json['id']

    response = app.test_client().get('/resume/education')
    assert response.json[item_id] == example_education

def test_getting_education_by_id():
    
    '''
    Fetch Education details by its ID.
    
    Check that the returned education matches the added education.
    '''
    example_education = {
        "course": "Engineering",
        "school": "NYU",
        "start_date": "October 2022",
        "end_date": "August 2024",
        "grade": "86%",
        "logo": "example-logo.png"
    }

    # Add the new education entry
    response = app.test_client().post('/resume/education', json=example_education)
    item_id = response.json['id']

    # Get the education entry by its ID
    response = app.test_client().get(f'/resume/education/?id={item_id}')
    retrieved_education = response.json

    # Assert that the retrieved education matches the added education
    assert retrieved_education['course'] == example_education['course']
    assert retrieved_education['school'] == example_education['school']
    assert retrieved_education['start_date'] == example_education['start_date']
    assert retrieved_education['end_date'] == example_education['end_date']
    assert retrieved_education['grade'] == example_education['grade']
    assert retrieved_education['logo'] == example_education['logo']


def test_getting_every_education():
    '''
    Fetch all educations and check the response structure.
    '''
    # First, let's add a couple of education entries to ensure we have multiple items
    example_educations = [
        {
            "course": "Computer Science",
            "school": "MIT",
            "start_date": "September 2022",
            "end_date": "June 2026",
            "grade": "95%",
            "logo": "mit-logo.png"
        },
        {
            "course": "Data Science",
            "school": "Stanford",
            "start_date": "August 2023",
            "end_date": "May 2025",
            "grade": "92%",
            "logo": "stanford-logo.png"
        }
    ]
    
    for edu in example_educations:
        response = app.test_client().post('/resume/education/', json=edu)
        assert response.status_code == 200  # Assuming POST returns 200 OK

    # Now, let's fetch all educations
    response = app.test_client().get('/resume/education/')
    assert response.status_code == 200
    assert isinstance(response.json, list)
    
    # Check if we have at least as many entries as we just added
    assert len(response.json) >= len(example_educations)

    # Check the structure of each education entry
    for edu in response.json:
        assert 'course' in edu
        assert 'school' in edu
        assert 'start_date' in edu
        assert 'end_date' in edu
        assert 'grade' in edu
        assert 'logo' in edu

    # Verifying that our added education are in the response
    added_courses = set(edu['course'] for edu in example_educations)
    response_courses = set(edu['course'] for edu in response.json)
    assert added_courses.issubset(response_courses)

    # Optional: We could also check for the exact match of the added educations
    for example_edu in example_educations:
        assert any(
            all(item in edu.items() for item in example_edu.items())
            for edu in response.json
        )

def test_skill():
    '''
    Add a new skill and then get all skills. 
    
    Check that it returns the new skill in that list
    '''
    example_skill = {
        "name": "JavaScript",
        "proficiency": "2-4 years",
        "logo": "example-logo.png"
    }

    item_id = app.test_client().post('/resume/skill',
                                     json=example_skill).json['id']

    response = app.test_client().get('/resume/skill')
    assert response.json[item_id] == example_skill

def test_experience_deletion():
    '''
    Remove the first experience from the list.
    
    Check if the experience has been removed from the list
    '''
    id = 0
    response = app.test_client().delete(f'/resume/experience?id={id}')
    assert response.status_code == 204
    
def test_experience_retrieval():
    '''
    Add an experience to the empty experience list.
    Get the first experience from the list.
    
    Check if the retrieved experience is correct.
    '''
    new_experience = {
        'title': 'Software Developer',
        'company': 'A Cool Company',
        'start_date': 'October 2022',
        'end_date': 'Present',
        'description': 'Writing Python Code',
        'logo': 'example-logo.png'
    }
    id = app.test_client().post('/resume/experience', json = new_experience).json['id']
    response = app.test_client().get(f'/resume/experience?id={id}')
    assert response.status_code == 200
    assert response.json['title'] == 'Software Developer'
    assert response.json['company'] == 'A Cool Company'
    assert response.json['description'] == 'Writing Python Code'

def test_update_skill():
    new_skill = {
        "name": "Haskell",
        "proficiency": "0 years",
        "logo": "example-logo.png"
    }

    skill_id = app.test_client().post('/resume/skill', json=new_skill).json['id']
    
    updated_skill = {
        "name": "C++",
        "proficiency": "4 years",
        "logo": "updated-logo.png"
    }
    
    response = app.test_client().put(f'/resume/skill/{skill_id}', json=updated_skill)
    assert response.status_code == 200
    assert response.json['name'] == updated_skill['name']
    assert response.json['proficiency'] == updated_skill['proficiency']
    assert response.json['logo'] == updated_skill['logo']

def test_delete_skill():
    new_skill = {
        "name": "C++",
        "proficiency": "4 years",
        "logo": "example-logo.png"
    }

    skill_id = app.test_client().post('/resume/skill', json=new_skill).json['id']
    
    response = app.test_client().delete(f'/resume/skill/{skill_id}')
    assert response.status_code == 200
    assert response.json['name'] == new_skill['name']
    
    get_response = app.test_client().get('/resume/skill')
    assert skill_id not in get_response.json
