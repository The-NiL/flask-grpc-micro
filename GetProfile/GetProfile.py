from flask import Blueprint, jsonify, request

import os, sys
import grpc
from google.protobuf.json_format import MessageToDict

from .GetProfile_pb2 import Message
from .GetProfile_pb2_grpc import GetUserProfileStub

# assuming these files exist from other microservice for auth
#from .Authentication_pb2 import InputToken
#from .Authentication_pb2_grpc import VerifyUserTokenStub



mod = Blueprint('GetProfile', __name__)



# connecting to auth service (since there's no server yet, assumming localhost)
#Authentication_host = os.getenv('VERIFYUSERTOKEN_HOST', "localhost")
#Authentication_channel = grpc.insecure_channel(
#   '{}:50051'.format(Authentication_host)
#)
#Authentication_client = VerifyUserTokenStub(Authentication_channel)



# connecting to my own service
GetProfile_host = os.getenv('GETUSERPROFILE_HOST', "localhost")
GetProfile_channel = grpc.insecure_channel(
    '{}:50051'.format(GetProfile_host)
)
GetProfile_client = GetUserProfileStub(GetProfile_channel)




@mod.route("/personal-data-tab/<username>", methods = ['GET'])
def userProfile(username):
    
    #token = request.headers['Authorization']

    # assuming the input of the authentication proto is InputToken
    # input message will be the token to be validated
    #request_message = InputToken(
    #    token = token
    #)

    #try:

        # assuming the service function for the authentication is VerifyUserToken
        # calling auth service
    #    outputMessage = VerifyUserToken(request_message)
    #    outputMessage_dict = MessageToDict(outputMessage)
    
    #except: 

    #    return jsonify({
    #        'message':'Encountered error while trying to connect to authentication service'
    #    })


    # if the token is verified we'll take username from output of auth sevice
    #if outputMessage_dict['status'] == True:

    request_message = Message(
        username = username
        )

    response = GetProfile_client.GetUserProfile(request_message)
    #avoids sending wrong format message
    message_dict = MessageToDict(response)
    

    return jsonify(message_dict)


    #else:
        
        #return jsonify({
            #'message': 'token is not valid',
            #'status': False
        #})
