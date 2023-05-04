#!flask/bin/python
################################################################################################################################
# ------------------------------------------------------------------------------------------------------------------------------
# This file implements the REST layer. It uses flask micro framework for server implementation. Calls from front end reaches 
# here as json and being branched out to each projects. Basic level of validation is also being done in this file. #                                                                                                                                  	       
# -------------------------------------------------------------------------------------------------------------------------------
################################################################################################################################
from flask import Flask, jsonify, request, redirect, render_template, Response
from flask_httpauth import HTTPBasicAuth
from flask_cors import *
from werkzeug.utils import secure_filename
import os
import shutil
import numpy as np
from search import recommend
from tensorflow.python.platform import gfile

UPLOAD_FOLDER = './uploads'
RESULT_FOLDER = './result'
DATABASE_TAGS = './database/tags'
DATABASE_IMGS = './database/dataset'
FEATURES_FILE = './saved_features_recom.txt'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])


app = Flask(__name__,
            static_folder='./front-end-vue/dist',  # 设置静态文件夹目录
            template_folder="./front-end-vue/dist",
            static_url_path="")
CORS(app, supports_credentials=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['RESULT_FOLDER'] = RESULT_FOLDER
app.config['DATABASE_TAGS'] = DATABASE_TAGS
app.config['DATABASE_IMGS'] = DATABASE_IMGS
app.config['FEATURES_FILE'] = FEATURES_FILE
if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])
if not os.path.exists(app.config['RESULT_FOLDER']):
    os.makedirs(app.config['RESULT_FOLDER'])
auth = HTTPBasicAuth()


# Loading the extracted feature vectors for image retrieval
extracted_features = np.zeros((2955, 2048), dtype=np.float32)

with open(app.config['FEATURES_FILE']) as f:
    for i, line in enumerate(f):
        extracted_features[i, :] = line.split()
        
tags = ['animals', 'baby', 'bird', 'car', 'clouds', 'dog', 'female', 'flower', 'food', 'indoor', 'lake', 'male', 'night', 'people', 'plant_life', 'portrait', 'river', 'sea', 'structures', 'sunset', 'transport', 'tree', 'water']
def getTagsOfImages():
    imageTags = {}
    for i in tags:
        imageTags[i] = []
        with open(os.path.join(app.config['DATABASE_TAGS'], f"{i}.txt"), 'r') as fp:
            for j in fp.readlines():
                imageTags[i].append(j.strip())
    return imageTags
imageTags = getTagsOfImages()


@app.route('/image', methods=['GET'])
def getImage():
    imageId = request.values.get('id')
    with open(os.path.join(app.config['DATABASE_IMGS'], f"im{imageId}.jpg"), mode='rb') as f:
        byte_data = f.read()

    return Response(byte_data, mimetype='image/jpeg')


@app.route('/collect/all', methods=['GET'])
def getCollects():
    res = []
    with open('./database/favorites.txt', mode='r') as f:
        for i in f.readlines():
            res.append(i.strip())
    return jsonify(res)


@app.route('/collect', methods=['GET'])
def modifyCollectState():
    imageId = request.values.get('id')

    with open('./database/favorites.txt', mode='r') as f:
        s = f.readlines()

    p = []
    isCollected = False
    for i in s:
        if i.strip() == imageId:
            isCollected = True
        else:
            p.append(i.strip())

    if not isCollected:
        p.append(imageId)

    with open('./database/favorites.txt', mode='w') as f:
        for index, item in enumerate(p):
            if index != len(p) - 1:
                f.write(item + '\n')
            else:
                f.write(item)

    return jsonify({'status': True})


@app.route("/tags", methods=['GET'])
def getTags():
    res = [{'label': i, 'size': len(imageTags[i])} for i in imageTags.keys()]
    res.sort(key=lambda x: x['size'], reverse=True)
    return jsonify(res)


@app.route('/info', methods=['GET'])
def getImageInfo():
    imageId = request.values.get('id')

    with open('./database/favorites.txt', mode='r') as f:
        isCollected = False
        for i in f.readlines():
            if i.strip() == imageId:
                isCollected = True
                break
            
    tags = [i for i in imageTags.keys() if imageId in imageTags[i]]

    return jsonify({
        'isCollected': isCollected,
        'tags': tags,
    })


@app.route('/imgUpload', methods=['GET', 'POST'])
def upload_img():
    shutil.rmtree(app.config['RESULT_FOLDER'])
    os.makedirs(app.config['RESULT_FOLDER'])
    if request.method in ['POST', 'GET']:
        if 'file' not in request.files:
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            return redirect(request.url)
        if file:  # and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            inputloc = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            image_list = recommend(inputloc, extracted_features)
            return jsonify(image_list)



@app.route('/')
def main():
    return render_template('index.html', name='index')  # 使用模板插件，引入index.html。此处会自动Flask模板文件目录寻找index.html文件


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8081)
