from Constants import connString
import pyodbc
import datetime
import uuid
import time    

class AuthorizedByModel:
    def __init__(self, authorizedByID = '',authorizedByName = ''):
        self.authorizedByID = authorizedByID
        self.authorizedByName = authorizedByName
       
        

    @staticmethod
    def get_all():
        conn = pyodbc.connect(connString, autocommit=True)
        cursor = conn.cursor()
        sqlcmd1 = "SELECT * FROM AuthorizedBy ORDER BY authorizedByName"
        cursor.execute(sqlcmd1)
        records = []
        for dbrow in cursor.fetchall():
            row = AuthorizedByModel(dbrow[0],dbrow[1])
            records.append(row)
        cursor.close()
        conn.close()
        return records

    @staticmethod
    def get_name_id():
        conn = pyodbc.connect(connString, autocommit=True)
        cursor = conn.cursor()
        sqlcmd1 = "SELECT authorizedByID, authorizedByName FROM AuthorizedBy ORDER BY authorizedByName"
        cursor.execute(sqlcmd1)
        records = []
        for dbrow in cursor.fetchall():
            row = AuthorizedByModel(dbrow[0],dbrow[1])
            records.append(row)
        cursor.close()
        conn.close()
        return records
        
    @staticmethod
    def get_by_id(unique_id):
        conn = pyodbc.connect(connString, autocommit=True)
        cursor = conn.cursor()
        sqlcmd1 = "SELECT * FROM AuthorizedBy WHERE authorizedByID = ?"
        cursor.execute(sqlcmd1, unique_id)
        record = None
        for dbrow in cursor.fetchall():
            record = AuthorizedByModel(dbrow[0],dbrow[1])
        cursor.close()
        conn.close()
        return record
    
    @staticmethod
    def insert(obj):
        obj.authorizedByID = str(uuid.uuid4())
        conn = pyodbc.connect(connString, autocommit=True)
        cursor = conn.cursor()
        sqlcmd1 = "INSERT INTO AuthorizedBy (authorizedByID,authorizedByName) VALUES(?,?)"
        cursor.execute(sqlcmd1, (obj.authorizedByID,obj.authorizedByName))
        cursor.close()
        conn.close()
        
    
    @staticmethod
    def update(obj):
        conn = pyodbc.connect(connString, autocommit=True)
        cursor = conn.cursor()
        sqlcmd1 = "UPDATE AuthorizedBy SET authorizedByName = ? WHERE authorizedByID = ?"
        cursor.execute(sqlcmd1,  (obj.authorizedByName,obj.authorizedByID))
        cursor.close()
        conn.close()
    
    @staticmethod
    def delete(unique_id):
        conn = pyodbc.connect(connString, autocommit=True)
        cursor = conn.cursor()
        sqlcmd1 = "DELETE FROM AuthorizedBy WHERE authorizedByID = ?"
        cursor.execute(sqlcmd1, (unique_id))
        cursor.close()
        conn.close()

