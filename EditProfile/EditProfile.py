from flask import Blueprint, jsonify, request

from .EditProfile_pb2 import InputMessage
from .EditProfile_pb2_grpc import EditProfileStub

import os
import grpc

from google.protobuf.json_format import MessageToDict



mod = Blueprint('EditProfile', __name__)



# connecting to my own service
EditProfile_host = os.getenv('EDITUSERPROFILE_HOST', "localhost")
EditProfile_channel = grpc.insecure_channel(
   '{}:50051'.format(EditProfile_host)
)

EditProfile_client = EditProfileStub(EditProfile_channel)




@mod.route("/personal-data-tab/<username>", methods = ['PUT'])
def editProfile(username):
    
    data = request.get_json()


    required = [
        'fname',
        'lname',
        'nationalCode',
        'phone',
        'address', 
        'city', 
        'neighborhood',
        'gender',
		'maritalStatus',
		'score'
    ]


    if data == None:

         return jsonify({
             'message' : 'please provide required fields'
            })
    
    
    else:
        # check if all the fields are provided
        for item in required:
            if not item in data.keys():

                return jsonify({
                    f'{item}': 'this field should be provided'
                })
  

    request_message = InputMessage(
            username = username,
            fname = data['fname'],
            lname = data['lname'],
            nationalcode = data['nationalCode'],
            phone = data['phone'],
            address = data['address'],
            city = data['city'],
            neighborhood = data['neighborhood'],
            gender = data['gender'],
            maritalStatus = data['maritalStatus'],
            rate = data['score']
        )


    response = EditProfile_client.EditUserProfile(request_message)

    #avoids sending wrong format message
    message_dict = MessageToDict(response)

    return jsonify(message_dict)

