from concurrent import futures
import grpc
import os, sys

from . import EditProfile_pb2 as pb2
from . import EditProfile_pb2_grpc as pb2_grpc

# making it possible to call utils module from the parent directory
currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)

from utils import makeStr, dbConnection



conn, cur = dbConnection()



class EditProfileService(pb2_grpc.EditProfileServicer):

    def EditUserProfile(self, request, context):

        username = makeStr(request.username)
        

        #service provider informations  
        query = 'Exec dbo.GetServiceProvider @username = {0}, @opr_username = {1}'.format(username, username)
            
        cur.execute(query)
        service_provider = cur.fetchall()


        # concatinating name and last name as db field is fullname
        full_name = request.fname + ' ' + request.lname


        query_part1 = 'Exec dbo.UpdateServiceProvider @username = {0}, @fullname = {1}, @tel = {2}, @city = {3}, @address = {4}, ' 
        query_part2 = '@lastActivity = {5}, @customerCount = {6}, @reputation = {7}, @rate = {8}, @nationalId = {9}, @gender = {10}, '
        query_part3 = '@maritalStatus = {11}, @animalProblemStatus = {12}, @startTime = {13}, @endTime = {14}, @neighborhood = {15}, @opr_username = {16}'
        query_string = query_part1 + query_part2 + query_part3

        
        query = query_string.format(

            username,
            makeStr(full_name),
            makeStr(request.phone), 
            makeStr(request.city), 
            makeStr(request.address),
            service_provider[0][8], 
            service_provider[0][9],
            service_provider[0][10],
            makeStr(request.rate),
            makeStr(request.nationalcode),
            makeStr(request.gender),
            request.maritalStatus,
            service_provider[0][15],
            service_provider[0][16],
            service_provider[0][17],
            makeStr(request.neighborhood),

            username
        )

        # None is not understandable by MS sql server
        query = query.replace("None", "NULL")


        try:
            cur.execute(query)
            conn.commit()


            return pb2.Response(
                message = 'successfully updated',
                status = 1
                )   
        
        
        except:

            return pb2.Response(
                message = 'couldn\'t update',
                status = 0
                )                


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    pb2_grpc.add_EditProfileServicer_to_server(
        EditProfileService(), server
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
