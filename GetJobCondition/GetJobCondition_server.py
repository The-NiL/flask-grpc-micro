from concurrent import futures
import grpc
from utils import makeStr, dbConnection
import os

from . import GetJobCondition_pb2 as pb2
from . import GetJobCondition_pb2_grpc as pb2_grpc



conn, cur = dbConnection()



class GetJobConditionService(pb2_grpc.GetJobConditionServicer):

    def GetUserJobCondition(self, request, context):

        username = makeStr(request.username)
        works = ""

        
        query = 'Exec dbo.GetServiceCatalog @serviceProvider = {0}, @opr_username = {1}'.format(username, username)
        cur.execute(query)
        services = cur.fetchall()

        
        query = 'Exec dbo.GetServiceProvider @username = {0}, @opr_username = {1}'.format(username, username)
        cur.execute(query)
        service_provider = cur.fetchall()
        

        # making works as strings separated by ,
        #this eases the process of sending output to client side(instead of list)
        for service in services:
            works = works + "," + service[6]


    
        return pb2.CondtionOutput(
            work = works,
            isPetFriendly = service_provider[0][15],
            startTime = service_provider[0][16],
            endTime = service_provider[0][17]
            )



def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    
    pb2_grpc.add_GetJobConditionServicer_to_server(
        GetJobConditionService(), server
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
