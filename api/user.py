import models
import os
import sys
import secrets
from PIL import Image


from flask import Blueprint, request, jsonify
from flask_bcrypt import generate_password_hash, check_password_hash
from flask_login import login_user, current_user, logout_user, login_required
from playhouse.shortcuts import model_to_dict

user = Blueprint('users', 'user', url_prefix='/user/v1')

#function to save the picture to a local directory
def save_picture(form_picture):
     #create random hex to use in name
     random_hex = secrets.token_hex(8)

    #split filename from form_picture to find extension
     f_name, f_ext = os.path.splitext(form_picture.filename)
    #make new name by adding hex to extension 
     picture_name = random_hex + f_ext
     #create filepath, grab current working directory, add static/profile_pics/ and add picture_name
     file_path_for_avatar = os.path.join("/static/profile_pics/" + picture_name)
    #using Pillow
     output_size = (125, 175) #set size of picture as tuple
     i = Image.open(form_picture) #open picture
     i.thumbnail(output_size)#set size of thumbnail - method accepts tuple as argument
     i.save(file_path_for_avatar) #save it to filepath from line 20

     return picture_name

@user.route('/', methods=['GET'])
@login_required
def get_all_users():
    try:
        users = [model_to_dict(user) for user in models.Users.select()]
        return jsonify(data=users, status={'code': 200, 'message': 'Success'})
    except models.DoesNotExist:
        return jsonify(data={}, status={'code': 401, 'message': 'There was an error getting the resource'})

@user.route('/login', methods=['POST'])
def login():
    # print(request.form)
    payload = request.get_json()
    # print(request.json, "<---request data")
    print(payload, "<---payload")
    payload['email'].lower()
    # try:
    user = models.Users.get(models.Users.email == payload['email'])
    user_dict = model_to_dict(user)
    print(user_dict, "user_dict")
    if (check_password_hash(user_dict['password'], payload['password'])):
        del user_dict['password']
        login_user(user)
        print(user, 'this is the user')
        print('user logged in')
        print(current_user, 'current_user')
        # if user.password == payload['password']:

    # users = [model_to_dict(user) for user in models.Users.select().where(
    #     (models.Users.email == payload['email']) and 
    #     (models.Users.password == payload['password']))]
    # user = users[0]
    # print(users, "<---users")
    return jsonify(data=user_dict, status={'code': 200, 'message': 'User successfully retrieved'})
    # except models.DoesNotExist:
        
    #     return jsonify(data={}, status={'code': 401, 'message': 'There was an error in finding the user.'})

@user.route('/register', methods=['POST'])
def register():
    img_file = request.files #grab image file
    payload = request.form.to_dict()
    img_file_dict = img_file.to_dict()
    print(img_file_dict, "img_file_dict")
    print(payload, "payload", type(payload), "type")

    payload["email"].lower() #make emails lowercase
    try:
        models.Users.get(models.Users.email == payload["email"])#query to see if user exists via email
        return jsonify(data={}, status={'code': 401, 'message': 'A user with that name or email already exists'})
    except models.DoesNotExist: #boolean property of the model
        #if no user with that email, make one

        #hash password using bcrypt
        payload["password"] = generate_password_hash(payload["password"])
        file_picture_path = save_picture(img_file_dict["image"]) #save picture path

        #add the image property to the form dictionary
        payload["image"] = file_picture_path

        #makes the user (1 row in the sql table)
        user = models.Users.create(**payload)
        login_user(user) #from flask_login - sets userid in session
    
        current_user.image = file_picture_path #current_user comes from login_user(), and we're grabbing the picture path

        user_dict = model_to_dict(user)

        print(user_dict, "user dictionary", type(user_dict), "type")
        del user_dict["password"] #user doesn't need password

        return jsonify(data = user_dict, status={'code': 201, 'message': 'Success'})

@user.route('/<name>/history', methods=['GET'])
def get_history(name):
    user = models.Users.get(models.Users.username == name)
    history = [model_to_dict(movie) for movie in user.history]
    # print(history, "<------------------------movie history-------------------------")
    # print(user_dict['history'])
    return jsonify(data=history, status={'code': 200, 'message':'Success'})

@user.route('/search/<name>', methods=['GET'])
def search_user(name):
    try:
        users = [model_to_dict(user) for user in models.Users.select().where(models.Users.username.contains(name))]
        return jsonify(data=users, status={'code': 200, 'message': 'Success'}) 
    except models.DoesNotExist:
        return jsonify(data={}, status={'code': 401, 'message': 'There was an error retrieving the resource'})

@user.route('/<name>', methods=['GET'])
def get_one_user(name):
    user = models.Users.get(models.Users.username == name)

    return jsonify(data=model_to_dict(user), status={'code': 200, 'message': 'Success'})

@user.route('/<name>', methods=['PUT'])
def update_user(name):
    #grab image file from request
    img_file = request.files
    #grab form data and turn into dictionary
    payload = request.form.to_dict()
    #turn image file into dictionary
    img_file_dict = img_file.to_dict()
    #save image and create path
    file_picture_path = save_picture(img_file_dict["image"])
    #set payload['image'] to path
    payload["image"] = file_picture_path

    #query to upate users whose ids match argument id - pass in payload
    query = models.Users.update(**payload).where(models.Users.username == name)
    #execute query
    query.execute()


    updated_user = models.Users.get(models.Users.username == name)
    return jsonify(data=model_to_dict(updated_user), status={'code': 200, 'message': 'Success'})


@user.route('/<name>', methods=['Delete'])
# @login_required
def delete_user(name):
    if current_user.username == name:
        user = models.Users.get_by_id(current_user.id)
        user.delete_instance()
        return jsonify(data='resources successfully deleted', status={'code': 200, 'message': 'Resource deleted'})
    else:
        flask.flash('You must be logged in as this user to delete this account')
        return jsonify(data={}, status={'code': 401, 'message':'Error deleting resource'})

@user.route('/logout', methods=['GET'])
@login_required
def logout():
    logout_user()
    # print(current_user)
    return jsonify(data={}, status={'code': 200, 'message':'Successfully logged out user'})
