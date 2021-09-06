from pymongo import MongoClient
import json
import bcrypt

client = MongoClient('localhost:27017')

db = client.videoDB
def video_metadata_insert(data=None):

    print(data)
    db.videoinfo.insert(data)
    return "Done"
def user_verified(data=None):
    # print(data)
    login_user = db.user.find_one({'Login_Id' : data['Login_Id']})
    print(login_user)
    if login_user['Login_Id'] == data['Login_Id']:
        if bcrypt.checkpw(data['Password'].encode('utf-8'), login_user['Password']) == True:
            print('Done')
            return 'success',200
        else:
            return 'Invalid password combination'
    else:
        return 'Invalid username/password combination'
