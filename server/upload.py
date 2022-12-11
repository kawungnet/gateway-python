import pyrebase
import time

config = {
  "apiKey": "AIzaSyCDIgZdIGqw7DTlad_b6O4Y5S9PP54IYCI",
  "authDomain": "kawungnet.firebaseapp.com",
  "databaseURL": "https://kawungnet-default-rtdb.firebaseio.com",
  "projectId" : "kawungnet",
  "storageBucket" : "kawungnet.appspot.com",
  "messagingSenderId" : "443771470605",
  "appId" : "1:443771470605:web:61b813f36a86e1d940e644"
};

firebase = pyrebase.initialize_app(config)


def up_server(node_id, data_name, up_data):
    # upload to database
    db = firebase.database()
    timestamp = str(int(time.time()))
    
    db.child("users").child(node_id).child(timestamp).child(data_name).push(up_data)
