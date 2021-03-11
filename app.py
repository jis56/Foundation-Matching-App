import os
from flask import Flask, flash, request, redirect, url_for, send_from_directory, jsonify
from werkzeug.utils import secure_filename
import pickle
import joblib
from model import *
import cv2
from flask import Flask, render_template, redirect, jsonify
from flask_pymongo import PyMongo

UPLOAD_FOLDER = 'Static/img'
ALLOWED_EXTENSIONS = {'png', 'jpg'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

mongo = PyMongo(app, uri="mongodb://localhost:27017/foundation_db")

filename = 'Static/img/Beyonce.jpg'

rbg = []

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
    return '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form method=post enctype=multipart/form-data>
      <input type=file name=file>
      <input type=submit value=Upload>
    </form>
    '''
@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'],
                          filename)

@app.route('/predictcolor')
def predictcolor():

    filename = 'Static/img/Beyonce.jpg'
    image = createimage(filename)
    return jsonify(dominantColors(image))

@app.route('/findcolor')
def findcolor():
    foundation_data = []
    r = 243  
    g = 181
    b = 132
    #Find data from the mongo database
    for data in mongo.db.foundation.find( {
        "red": { "$gt": r-2, "$lt": r+2 },
        "blue": { "$gt": b-2, "$lt": b+2 },
        "green": { "$gt": g-2, "$lt": g+2 }
        },{"_id":False} ):
        foundation_data.append(data)
    
    return jsonify(foundation_data) 

if __name__ == "__main__":
        app.run()