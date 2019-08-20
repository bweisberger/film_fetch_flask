import models

from flask import Blueprint, request, jsonify
from flask_bcrypt import generate_password_hash, check_password_hash
from flask_login import login_user, current_user
from playhouse.shortcuts import model_to_dict

user = Blueprint('users', 'user', url_prefix='/user/v1')

#function to save the picture to a local directory
def save_picture(form_picture):
     #create random hex to use in name
     random_hex = secrects.token_hex(8)

    #split filename from form_picture to find extension
     f_name, f_ext = os.path.splitext(form_picture.filename)
    #make new name by adding hex to extension 
     picture_name = random_hex + f_ext
     #create filepath, grab current working directory, add static/profile_pics/ and add picture_name
     file_path_for_avatar = os.path.join(os.getcwd(), 'static/profile_pics/' + picture_name)

    #using Pillow
     output_size = (125, 175) #set size of picture as tuple
     i = Image.open(form_picture) #open picture
     i.thumbnail(output_size)#set size of thumbnail - method accepts tuple as argument
     i.save(file_path_for_avatar) #save it to filepath from line 20

     return file_path_for_avatar

@user.route('/', methods=['GET'])
def get_all_users():
    try:
        users = [model_to_dict(user) for user in models.Users.select()]
        return jsonify(data=users, status={'code': 200, 'message': 'Success'})
    except models.DoesNotExist:
        return jsonify(data={}, status={'code': 401, 'message': 'There was an error getting the resource'})

@user.route('/register', methods=['POST'])
def register():
    img_file = request.files #grab image file
    payload = request.form.to_dict()
    img_file_dict = img_file.to_dict()
    print(payload, "payload", type(payload), "type")

    payload['email'].lower() #make emails lowercase
    try:
        models.Users.get(models.Users.email == payload['email'])#query to see if user exists via email
        return jsonify(data={}, status={'code': 401, 'message': 'A user with that name or email already exists'})
    except models.DoesNotExist: #boolean property of the model
        #if no user with that email, make one

        #hash password using bcrypt
        payload['password'] = generate_password_hash(payload['password'])
        file_picture_path = save_picture(img_file_dict['file']) #save picture path

        #add the image property to the form dictionary
        payload['image'] = file_picture_path

        #makes the user (1 row in the sql table)
        user = models.Users.create(**payload)
        login_user(user) #from flask_login - sets userid in session
    
        current_user.image = file_picture_path #current_user comes from login_user(), and we're grabbing the picture path

        user_dict = model_to_dict(user)

        print(user_dict, "user dictionary", type(user_dict), "type")
        del user_dict['password'] #user doesn't need password

        return jsonify(data = user_dict, status={'code': 201, 'message': 'Success'})
    user = models.Users.create(**payload)

    print(user.__dict__, 'seeing inside user')
    user_dict = model_to_dit(user)

    return jsonify(data=user_dict, status={'code': 201, 'message': 'Success'})

@user.route('/<id>', methods=['GET'])
def get_one_user(id):
    user = models.Users.get_by_id(id)

    return jsonify(data=model_to_dict(user), status={'code': 200, 'message': 'Success'})

@user.route('/<id>', methods=['PUT'])
def update_user(id):
    #grab image file from request
    img_file = request.files
    #grab form data and turn into dictionary
    payload = request.form.to_dict()
    #turn image file into dictionary
    img_file_dict = img_file.to_dict()
    #save image and create path
    file_picture_path = save_picture(img_file_dict['file'])
    #set payload['image'] to path
    payload['image'] = file_picture_path

    #query to upate users whose ids match argument id - pass in payload
    query = models.Users.update(**payload).where(models.Users.id == id)
    #execute query
    query.execute()


    updated_user = models.Users.get_by_id(id)
    return jsonify(data=model_to_dict(updated_user), status={'code': 200, 'message': 'Success'})


@user.route('/<id>', methods=['Delete'])
def delete_user(id):
    user = models.Users.get_by_id(id)
    user.delete_instance()

    return jsonify(data='resources successfully deleted', status={'code': 200, 'message': 'Resource deleted'})
