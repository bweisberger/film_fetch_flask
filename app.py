from flask import Flask, g
from flask_cors import CORS
from flask_login import LoginManager
import models

#import the blueprint       
from api.user import user

DEBUG = True
PORT = 8000

login_manager = LoginManager() #sets up the ability to start a session

#Initialize the Flask Class
#Start the website
app = Flask(__name__, static_url_path="", static_folder='static')
#analogous to const app = express()
app.secret_key = 'AS;LDFAJLKWE STRING' #analogy: app.use(session({secret_key: 'blah'}))
login_manager.init_app(app) #sets up the session on the app

@login_manager.user_loader
def load_user(user_id):
    try:
        return models.Users.get(models.Users.id == user_id)
    except models.DoesNotExist:
        return None

CORS(user, origins=['http://localhost:3000'], supports_credentials=True)

app.register_blueprint(user)

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


# Run the app when the program starts
if __name__ == '__main__':
    models.initialize()
    app.run(debug=DEBUG, port=PORT) #app.listen in express