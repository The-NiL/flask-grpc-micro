from flask.json import dumps
from flask import Blueprint, jsonify, request
import os, sys
import grpc
from google.protobuf.json_format import MessageToDict, MessageToJson


from .GetJobCondition_pb2 import CondtionInput
from .GetJobCondition_pb2_grpc import GetJobConditionStub


# making it possible to call utils module from the parent directory
currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)

from utils import makeStr



mod = Blueprint('GetJobCondition', __name__)



GetJobCondition_host = os.getenv('GETJOBCONDITION_HOST', "localhost")
GetJobCondition_channel = grpc.insecure_channel(
    '{}:50051'.format(GetJobCondition_host)
)
GetJobCondition_client = GetJobConditionStub(GetJobCondition_channel)



@mod.route("/work-condition-tab/<username>", methods = ['GET'])
def jobCondition(username):


    request_message = CondtionInput(
        username = username
    )

    response = GetJobCondition_client.GetUserJobCondition(request_message)

    # avoids sending wrong format message
    message_dict = MessageToDict(response)

    return jsonify(message_dict)
