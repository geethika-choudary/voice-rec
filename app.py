"""
The flask application package.
"""
from flask import Flask

app = Flask(__name__)
wsgi_app = app.wsgi_app #Registering with IIS

#import views
import Speaker_Enrollment
import Speaker_Authentication