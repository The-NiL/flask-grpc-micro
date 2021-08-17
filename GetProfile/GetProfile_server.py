from concurrent import futures
import grpc
import os, sys

from . import GetProfile_pb2 as pb2
from . import GetProfile_pb2_grpc as pb2_grpc

# making it possible to call utils module from the parent directory
currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)


from utils import makeStr, dbConnection


conn, cur = dbConnection()


class GetProfileService(pb2_grpc.GetUserProfileServicer):

    def GetUserProfile(self, request, context):

        username = makeStr(request.username)

        query = 'Exec dbo.GetServiceProvider @username = {0}, @opr_username = {1}'.format(username, username)
        cur.execute(query)

        service_provider = cur.fetchall()

        
        full_name = service_provider[0][1].split(" ")


            
        return pb2.MessageResponse(
            fname = full_name[0],
            lname = full_name[1],
            nationalcode = service_provider[0][12],
            phone = service_provider[0][2],
            address = service_provider[0][5],
            city = service_provider[0][3],
            neighborhood = service_provider[0][4],
            gender = service_provider[0][13],
            maritalStatus = service_provider[0][14],
            rate = service_provider[0][11]
                )
    


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    pb2_grpc.add_GetUserProfileServicer_to_server(
        GetProfileService(), server
    )
    server.add_insecure_port("localhost:50051")
    server.start()
    server.wait_for_termination()


if __name__ == "__main__":

    if os.environ.get('https_proxy'):
        del os.environ['https_proxy']

    if os.environ.get('http_proxy'):
        del os.environ['http_proxy']
    
    serve()
