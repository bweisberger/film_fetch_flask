from flask import Blueprint, request, jsonify
import models
from flask_login import login_user, current_user, login_required, logout_user
from playhouse.shortcuts import model_to_dict

fellows = Blueprint('fellows', 'fellows', url_prefix='/fellows/v1')

@fellows.route('/', methods=['GET'])
def get_fellows():
    try:
        fellows = [model_to_dict(fellow) for fellow in models.Fellows.select().where(
            (models.Fellows.user1_id == current_user.id) or
            (models.Fellows.user2_id == current_user.id))]
        # print(fellows, "<--fellows",type(fellows),"<--fellows type")
        # for follow in fellows:
        #     print(fellow['user1']['username'], "<--user1 username")
        return jsonify(data=fellows, status={'code': 200, 'message': 'Success'})
    except models.DoesNotExist:
        return jsonify(data={}, status={'code': 401, 'message':'There was an error getting the resource'})


@fellows.route('/<id>', methods=['POST'])
def make_fellows(id):
    try:
        # fellows = current_user.following.execute()
        # fellows = current_user.following
        # print(current_user, "<---current_user")
        if current_user.is_authenticated:
            print(models.Users.select(models.Users.id == current_user), "current_user")
            fellows = [model_to_dict(fellow) for fellow in models.Fellows.select().where(user_id == current_user.id)]
            for fellow in fellows:
                print(fellow.user2_id, 'row in fellows, col user2_id')
                if fellow.user2_id == id:
                    return jsonify(data={}, status={'code': 401, 'message': 'Users are already fellows'})
        print(fellows, '<-------fellows')
        link = models.Fellows.create(user1 = current_user.id, user2=id)
        link_dict = model_to_dict(link)
        return jsonify(data=link_dict, status={'code': 201, 'message': 'Resource successfully created'})
        # fellows = [model_to_dict(fellow) for fellow in current_user.following]
        
        
        # print(fellows, 'current_user.following')
        # # models.Fellows.get((models.Fellows.user1_id == id and models.Fellows.user2_id == current_user.id) or (models.Fellows.user2_id == id and models.Fellows.user1_id == current_user.id)
        # #     (models.Fellows.user1_id == current_user.id) or 
        # #     (models.Fellows.user2_id == current_user.id))]
        # # print(fellows, "<----------------fellows")
        
    except :
        fellows = models.Fellows.create(user1 = current_user.id, user2=id)
        fellows_dict = model_to_dict(fellows)
        return jsonify(data=fellows_dict, status={'code': 201, 'message': 'Resource successfully created'})

@fellows.route('/<id>', methods=['DELETE'])

def delete_fellow(id):
    count = 0
    for fellow in models.Fellows.select().where(
    (models.Fellows.user1_id == id) or
    (models.Fellows.user2_id == id)):
        fellow.delete_instance()
        count += 1
    
    return jsonify(data=count, status={'code': 200, 'message':'Resource(s) deleted'})


