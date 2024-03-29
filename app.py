from flask import Flask, g
from flask_cors import CORS
from flask_login import LoginManager
from whitenoise import WhiteNoise
import models

#import the blueprint       
from api.user import user
from api.fellows import fellows
from api.utelly import utelly

DEBUG = True
PORT = 8000

login_manager = LoginManager() #sets up the ability to start a session

#Initialize the Flask Class
#Start the website
app = Flask(__name__, static_url_path="", static_folder='static')
app.wsgi_app = WhiteNoise(app.wsgi_app, root='static/')
app.wsgi_app.add_files('static/profile_pics/')


#analogous to const app = express()
app.secret_key = "Vader is Luke's dad" #analogy: app.use(session({secret_key: 'blah'}))
login_manager.init_app(app) #sets up the session on the app

@login_manager.user_loader
def load_user(user_id):
    try:
        return models.Users.get(models.Users.id == user_id)
    except models.DoesNotExist:
        return None

CORS(user, origins=['http://localhost:3000', 'https://filmfetch.herokuapp.com', 'http://filmfetch.herokuapp.com'], supports_credentials=True)
CORS(fellows, origins=['http://localhost:3000', 'https://filmfetch.herokuapp.com', 'http://filmfetch.herokuapp.com'], supports_credentials=True)
CORS(utelly, origins=['http://localhost:3000', 'https://filmfetch.herokuapp.com', 'http://filmfetch.herokuapp.com'], supports_credentials=True)

app.register_blueprint(user)
app.register_blueprint(fellows)
app.register_blueprint(utelly)

@app.before_request #built in by flask
def before_request():
    """Connect to the database before each request"""
    #global database = models.DATABASE
    g.db = models.DATABASE
    g.db.connect()

@app.after_request
def after_request(response):
    g.db.close()
    return response

# The default URL ends in / ('my-website.com/').
@app.route('/')
def index(): #method called immediately, name it anything
    return 'hi' #analogous to res.send() in express

import os
## import os at the top of your file 

if 'ON_HEROKU' in os.environ:
    print('hitting ')
    models.initialize()
# Run the app when the program starts
if __name__ == '__main__':
    models.initialize()
    app.run(debug=DEBUG, port=PORT) #app.listen in express