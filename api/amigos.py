from flask import Blueprint, request, jsonify
import models
from flask_login import login_user, current_user
from playhouse.shortcuts import model_to_dict

amigos = Blueprint('amigos', 'amigos', url_prefix='/amigos/v1')

@amigos.route('/', methods=['GET'])
def get_amigos():
    try:
        amigos = [model_to_dict(amigo) for amigo in models.Amigos.select().where(
            (models.Amigos.user1_id == current_user.id) or
            (models.Amigos.user2_id == current_user.id))]
        # print(amigos, "<--amigos",type(amigos),"<--amigos type")
        # for amigo in amigos:
        #     print(amigo['user1']['username'], "<--user1 username")
        return jsonify(data=amigos, status={'code': 200, 'message': 'Success'})
    except models.DoesNotExist:
        return jsonify(data={}, status={'code': 401, 'message':'There was an error getting the resource'})


@amigos.route('/<id>', methods=['POST'])
def make_amigos(id):
    try:
        # amigos = current_user.following.execute()
        # amigos = current_user.following
        print(models.Users.select(models.Users.id == current_user), "current_user")
        amigos = [model_to_dict(amigo) for amigo in current_user.following]
        for amigo in amigos:
            print(amigo.user2_id, 'row in amigos, col user2_id')
            if amigo.user2.id == id:
                print(amigo.user2_id, "row in amigos, col user2_id")
                return jsonify(data={}, status={'code': 401, 'message': 'Users are already amigos'})
        print(amigos, '<-------amigos')
        link = models.Amigos.create(user1 = current_user.id, user2=id)
        link_dict = model_to_dict(link)
        return jsonify(data=link_dict, status={'code': 201, 'message': 'Resource successfully created'})
        # amigos = [model_to_dict(amigo) for amigo in current_user.following]
        
        
        # print(amigos, 'current_user.following')
        # # models.Amigos.get((models.Amigos.user1_id == id and models.Amigos.user2_id == current_user.id) or (models.Amigos.user2_id == id and models.Amigos.user1_id == current_user.id)
        # #     (models.Amigos.user1_id == current_user.id) or 
        # #     (models.Amigos.user2_id == current_user.id))]
        # # print(amigos, "<----------------amigos")
        
    except :
        amigos = models.Amigos.create(user1 = current_user.id, user2=id)
        amigos_dict = model_to_dict(amigos)
        return jsonify(data=amigos_dict, status={'code': 201, 'message': 'Resource successfully created'})

@amigos.route('/<id>', methods=['DELETE'])
def delete_amigo(id):
    count = 0
    for amigo in models.Amigos.select().where(
    (models.Amigos.user1_id == id) or
    (models.Amigos.user2_id == id)):
        amigo.delete_instance()
        count += 1
    
    return jsonify(data=count, status={'code': 200, 'message':'Resource(s) deleted'})


