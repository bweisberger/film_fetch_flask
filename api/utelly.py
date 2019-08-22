from flask import Blueprint, request, jsonify
from flask_login import login_required, login_fresh, current_user
import models
from playhouse.shortcuts import model_to_dict

import models
from PIL import Image


utelly = Blueprint('utelly', 'utelly', url_prefix='/watch/v1')

@utelly.route('/search', methods=['GET'])
def get_movies():
    url = "https://utelly-tv-shows-and-movies-availability-v1.p.rapidapi.com/lookup"

    querystring = {"term":"bojack","country":"uk"}

    headers = {
        'x-rapidapi-host': "utelly-tv-shows-and-movies-availability-v1.p.rapidapi.com",
        'x-rapidapi-key': "1426a716c5msh793d351a44eb06cp1e7045jsnf2035438b817"
        }

    response = requests.request("GET", url, headers=headers, params=querystring)

    print(response.text)
    return jsonify(data={}, status={'code': 200, 'message': 'Successfully retrieved movies'})