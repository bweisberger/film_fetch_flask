from flask import Blueprint, request, jsonify
from flask_login import login_required, login_fresh, current_user
from playhouse.shortcuts import model_to_dict
import requests
import models
from PIL import Image


utelly = Blueprint('utelly', 'utelly', url_prefix='/watch/v1')

@utelly.route('/search/<title>', methods=['GET'])
def search_movies(title):
    words = title.split("+")
    title = " ".join(words)
    print(title, "<---title")
    url = "https://utelly-tv-shows-and-movies-availability-v1.p.rapidapi.com/lookup"

    querystring = {"term":title, "country":'us'}
    

    headers = {
        'access-control-allow-origin': 'true',
        'x-rapidapi-host': "utelly-tv-shows-and-movies-availability-v1.p.rapidapi.com",
        'x-rapidapi-key': "1426a716c5msh793d351a44eb06cp1e7045jsnf2035438b817"
        }

    response = requests.request("GET", url, headers=headers, params=querystring)
    # response.headers['Access-Control-Allow-Origin'] = 'True'
    # print(response.headers, "<--headers")
    # print(response.json(), "response json object")
    response_json = response.json()
    # print(response_json['headers'], "<---headers")
    results = response_json['results']
    key_info = []
    # for result in results:

    print(results)
    return jsonify(data=response_json, status={'code': 200, 'message': 'Successfully retrieved movies'})

@utelly.route('/<title>/<country>/<id>', methods=['GET'])
@login_required
def add_movie(title, country, id):
    url = "https://utelly-tv-shows-and-movies-availability-v1.p.rapidapi.com/lookup"

    querystring = {"term":title, "country":country}
    

    headers = {
        'x-rapidapi-host': "utelly-tv-shows-and-movies-availability-v1.p.rapidapi.com",
        'x-rapidapi-key': "1426a716c5msh793d351a44eb06cp1e7045jsnf2035438b817"
        }

    response = requests.request("GET", url, headers=headers, params=querystring)
    response_json = response.json()
    results = response_json['results']
    print(results, "<---results")
    for result in results:
        print(result, "<---result")
        locations = result['locations']
        print(locations, "<--locations")
        for location in locations:
            print(location, "<--location")
            if location['id'] == id:
                movie_data = {'movie_id':id,'user':current_user.id, 'title':title, 'country':country}
                movie = models.History.create(**movie_data)
    return(jsonify(data=model_to_dict(movie), status={'code': 201, 'message': 'Resource successfully created'}))

