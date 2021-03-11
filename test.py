import os
from flask import Flask, flash, request, redirect, url_for, send_from_directory, jsonify
from werkzeug.utils import secure_filename
import pickle
import joblib
from model import *
import cv2

filename = 'Static/img/Beyonce.jpg'
image = createimage(filename)
userdata = jsonify(dominantColors(image))
rbg = userdata[0][1]

userdata
