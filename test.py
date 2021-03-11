import os
from flask import Flask, flash, request, redirect, url_for, send_from_directory, jsonify
from werkzeug.utils import secure_filename
import pickle
import joblib
from model import *
import cv2
from flask import Flask, render_template, redirect, jsonify
from flask_pymongo import PyMongo

app = Flask(__name__, template_folder='templates')
mongo = PyMongo(app, uri="mongodb://localhost:27017/foundation_db")

# Function to convert   
def listToString(s):  
    
    # initialize an empty string 
    str1 = ""  
    
    # traverse in the string   
    for ele in s:  
        str1 += ele   
    
    # return string   
    return str1  
        
        
# Driver code     
route = mongo.db.img.distinct("route")
print(listToString(route))