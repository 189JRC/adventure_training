import markdown
import os
from flask import Flask, render_template, jsonify, request, flash, redirect, url_for
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func

# define base directory as current directory
basedir = os.path.abspath(os.path.dirname(__file__))

# instantiate flask application instance as variable 'app'
app = Flask(__name__)

# update application constantly
app.config.from_object(__name__)

# 8080 is default port for vue
# This configuration allows resource sharing between flask and vue.
CORS(app, resources={r"/*": {'origins': '*',  # 'http://localhost:8080',
                             "allow_headers": "Access-Control-Allow-Origin"}})

# Connect application with SQLAlchemy
# join database file with route dir
app.config['SQLALCHEMY_DATABASE_URI'] =\
    'sqlite:///' + os.path.join(basedir, 'database.db')

#Disabled tracking apparantly saves memory, to be changed to TRUE if records of migrations is required
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# instantiate instance of SQLAlchemy for ORM
db = SQLAlchemy(app)

# FUNCTIONS FOR URL ROUTING TO STATIC HTML FILES

@app.route('/')
def index():
    f = open("README.md", "r")
    md = markdown.markdown(f.read())
    return render_template('index.html', content=md)

# provides queryset for html rendering

@app.route('/providers')
def show_providers():
    providers = Provider.query.all()
    return render_template('providers.html', providers=providers)

# FUNCTIONS FOR HTTP ENDPOINT

# allows 'GET' request of json data of all providers
@app.route('/providers_data', methods=['GET'])
def providers_data():
    providers = Provider.query.all()
    #make a list of dicts for each provider, to convert into json
    providers_list = []
    for provider in providers:
        provider_dict = {
            'id': provider.id,
            'name': provider.company_name,
        }
        providers_list.append(provider_dict)
    return jsonify(json_list=providers_list)

# DECLARATION OF DB MODELS

class Provider(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    company_name = db.Column(db.String(100), nullable=False)
    contact_email = db.Column(db.String(80), unique=True, nullable=False)
    created_at = db.Column(db.DateTime(timezone=True),
                           server_default=func.now())
    bio = db.Column(db.Text)

    def __repr__(self):
        return f'<Provider {self.company_name}>'

#LAUNCH FLASK APP

if __name__ == "__main__":
    app.run(debug=True)
