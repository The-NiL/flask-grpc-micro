import pymssql
from flask import jsonify




def dbConnection():

    '''
        Creates a connection to DB
        :returns: connection and cursor
    '''

    try:

        
        conn = pymssql.connect(
            host = "185.128.82.62:11433",
            user = "saeidi",
            password = "aHnzv6RyCXLUFQFY",
            database = "Limoo_Trial")


    except:

        return jsonify("database connection failed!")

    cur = conn.cursor()
   
   
    return conn, cur



def makeStr(str):

    '''
    Adds quotations to the string for getting them ready to fit
    in SQL query
    :parameters: any string
    :returns: string with double quotations
    '''

    return '"' + str + '"'

