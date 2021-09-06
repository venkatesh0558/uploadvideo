from functools import wraps
from flask import *
import jwt
import videoDB
import json
import media_meatadata
import datetime
import os
app = Flask(__name__)

def authorize(f):
    @wraps(f)
    def decorated(*args, **kwargs):

        token = None
        clientdata=request.json
        # jwt is passed in the request header
        if 'Authorization' in request.headers:
            token = request.headers['Authorization']
        if not token:
            return jsonify({'message' : 'Token is missing !!'}), 401

        try:
            # print(token)
            token_apikey = token.split(' ')
            data = jwt.decode(token_apikey[1], "secret", algorithm="HS256")
            # print(data)
            current_user  = videoDB.user_verified(data=data)
            print(current_user)
        except:
            return jsonify({
                'message' : 'Token is invalid !!'
            }), 401
        #
        return f(current_user,clientdata, *args, **kwargs)
    return decorated

@app.route('/uploadvideo', methods=['GET','POST'])
# @authorize
def upload():
    if request.method == 'GET':
        return render_template("index.html")
    elif request.method == 'POST':
        print("hello")
        print(request.form)
        f = request.files['filename']
        print(f)
        file_name = f.filename
        print(file_name)
        f.save(f.filename)
        timestamp=datetime.datetime.now()
        # samplefile = 'sample_videos/file_example_OGG_480_1_7mg.ogg'
        res_meatadata = media_meatadata.metadatainfo(str(file_name))
        current_user="Rao"
        data={
            "UserName":current_user,
            "Video_ID":current_user+'_1',
            "Timestamp":str(timestamp),
            "Video_Status":"Active",
            "Video_Path":str(os.getcwd()+"\saved_videos/"+file_name),
            "Video_Metadata":res_meatadata
        }
        # print(res_meatadata[2])
        res=videoDB.video_metadata_insert(data)
        print(res)
        return "Video MetaData Stored into DB"
@app.route('/video/active', methods=['GET'])
@authorize
def useractive(urrent_user,clientdata, *args, **kwargs):
    if request.method == 'GET':
        res_data = {"respond": True}
        return res_data


@app.route('/video/deactive', methods=['GET'])
@authorize
def userdeactive(urrent_user,clientdata, *args, **kwargs):
    if request.method == 'GET':
        res_data = {"respond": False}
        return res_data

if __name__ == '__main__':

    app.run(debug=True,port=50011)