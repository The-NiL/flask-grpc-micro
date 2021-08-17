from flask import Blueprint, jsonify, request
from google.protobuf.json_format import MessageToDict

import grpc
import os

from .EditJobCondition_pb2 import EditCondtionInput
from .EditJobCondition_pb2_grpc import EditJobConditionStub



mod = Blueprint('EditJobCondition', __name__)



# connecting to my own service
EditJobCondition_host = os.getenv('EDITJOBCONDITION_HOST', "localhost")
EditJobCondition_channel = grpc.insecure_channel(
   '{}:50051'.format(EditJobCondition_host)
)

EditJobCondition_client = EditJobConditionStub(EditJobCondition_channel)



@mod.route("/work-condition-tab/<username>", methods = ['PUT'])
def EditJobCondition(username):
    
    data = request.get_json()


    required = [
        'works',
        'isPetFriendly',
        'startTime',
        'endTime',
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


    request_message = EditCondtionInput(
        username = username,
        work = data['works'],
        isPetFriendly = data['isPetFriendly'],
        startTime = data['startTime'],
        endTime = data['endTime'],
        )

    response = EditJobCondition_client.EditUserJobCondition(request_message)
    
    message_dict = MessageToDict(response)

    return jsonify(message_dict)
