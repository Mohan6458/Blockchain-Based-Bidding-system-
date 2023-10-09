from Constants import connString
import pyodbc
import datetime
import uuid
import time    

class VerifiedByModel:
    def __init__(self, verifiedByID = '',verifiedByName = ''):
        self.verifiedByID = verifiedByID
        self.verifiedByName = verifiedByName
       
        

    @staticmethod
    def get_all():
        conn = pyodbc.connect(connString, autocommit=True)
        cursor = conn.cursor()
        sqlcmd1 = "SELECT * FROM VerifiedBy ORDER BY verifiedByName"
        cursor.execute(sqlcmd1)
        records = []
        for dbrow in cursor.fetchall():
            row = VerifiedByModel(dbrow[0],dbrow[1])
            records.append(row)
        cursor.close()
        conn.close()
        return records

    @staticmethod
    def get_name_id():
        conn = pyodbc.connect(connString, autocommit=True)
        cursor = conn.cursor()
        sqlcmd1 = "SELECT verifiedByID, verifiedByName FROM VerifiedBy ORDER BY verifiedByName"
        cursor.execute(sqlcmd1)
        records = []
        for dbrow in cursor.fetchall():
            row = VerifiedByModel(dbrow[0],dbrow[1])
            records.append(row)
        cursor.close()
        conn.close()
        return records
        
    @staticmethod
    def get_by_id(unique_id):
        conn = pyodbc.connect(connString, autocommit=True)
        cursor = conn.cursor()
        sqlcmd1 = "SELECT * FROM VerifiedBy WHERE verifiedByID = ?"
        cursor.execute(sqlcmd1, unique_id)
        record = None
        for dbrow in cursor.fetchall():
            record = VerifiedByModel(dbrow[0],dbrow[1])
        cursor.close()
        conn.close()
        return record
    
    @staticmethod
    def insert(obj):
        obj.verifiedByID = str(uuid.uuid4())
        conn = pyodbc.connect(connString, autocommit=True)
        cursor = conn.cursor()
        sqlcmd1 = "INSERT INTO VerifiedBy (verifiedByID,verifiedByName) VALUES(?,?)"
        cursor.execute(sqlcmd1, (obj.verifiedByID,obj.verifiedByName))
        cursor.close()
        conn.close()
        
    
    @staticmethod
    def update(obj):
        conn = pyodbc.connect(connString, autocommit=True)
        cursor = conn.cursor()
        sqlcmd1 = "UPDATE VerifiedBy SET verifiedByName = ? WHERE verifiedByID = ?"
        cursor.execute(sqlcmd1,  (obj.verifiedByName,obj.verifiedByID))
        cursor.close()
        conn.close()
    
    @staticmethod
    def delete(unique_id):
        conn = pyodbc.connect(connString, autocommit=True)
        cursor = conn.cursor()
        sqlcmd1 = "DELETE FROM VerifiedBy WHERE verifiedByID = ?"
        cursor.execute(sqlcmd1, (unique_id))
        cursor.close()
        conn.close()

