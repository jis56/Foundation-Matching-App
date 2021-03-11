import os
from flask import Flask, flash, request, redirect, url_for, send_from_directory, jsonify
from werkzeug.utils import secure_filename
import pickle
import joblib
from model import *
import cv2
from flask import Flask, render_template, redirect, jsonify
from flask_pymongo import PyMongo

UPLOAD_FOLDER = 'static/img'
ALLOWED_EXTENSIONS = {'png', 'jpg'}

app = Flask(__name__, template_folder='templates')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

mongo = PyMongo(app, uri="mongodb://localhost:27017/foundation_db")

def listToString(s):  
    str1 = ""  
    for ele in s:  
        str1 += ele   
    return str1  

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('uploaded_file',
                                    filename=filename))
    return render_template("home.html")

@app.route('/<filename>')
def uploaded_file(filename):
    baseimage = 'static/img/' + filename
    #image = createimage(baseimage)
    #print(jsonify(dominantColors(image)))
    send_from_directory(app.config['UPLOAD_FOLDER'],
                        filename)
    mongo.db.img.delete_many({})                    
    mongo.db.img.insert_one( { "route": baseimage } )
    return render_template("home.html", filename = filename)

@app.route('/predictcolor')
def predictcolor():

    route = mongo.db.img.distinct("route")
    image = createimage(listToString(route))
    return jsonify(dominantColors(image))

@app.route('/exactmatch')
def findcolor():
    foundation_data = []
    r = 92  
    g = 68
    b = 51
    #Find data from the mongo database
    for data in mongo.db.foundation.find( {
        "red": { "$gte": r-2, "$lte": r+2 },
        "blue": { "$gte": b-2, "$lte": b+2 },
        "green": { "$gte": g-2, "$lte": g+2 }
        },{"_id":False} ):
        foundation_data.append(data)
    
    return jsonify(foundation_data) 

@app.route('/closestmatch')
def closestmatch():
    foundation_data = []
    r = 92  
    g = 68
    b = 51
    for data in mongo.db.foundation.find( {
        "red": { "$gte": r-10, "$lte": r+10 },
        "blue": { "$gte": b-10, "$lte": b+10 },
        "green": { "$gte": g-10, "$lte": g+10 }
        },{"_id":False} ):
        foundation_data.append(data)
    
    return jsonify(foundation_data) 

if __name__ == "__main__":
        app.run()