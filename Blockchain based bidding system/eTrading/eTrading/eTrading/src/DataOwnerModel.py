from Constants import connString
import pyodbc
import datetime
import uuid
import time    

class DataOwnerModel:
    def __init__(self, dataOwnerID = '',dataOwnerName = '',address = '',city = '',state = '',pincode = '',country = '',emailID = '',mobileNbr = '',addressProofFile = '',identityProofFile = '',emailModel = None):
        self.dataOwnerID = dataOwnerID
        self.dataOwnerName = dataOwnerName
        self.address = address
        self.city = city
        self.state = state
        self.pincode = pincode
        self.country = country
        self.emailID = emailID
        self.mobileNbr = mobileNbr
        self.addressProofFile = addressProofFile
        self.identityProofFile = identityProofFile
        self.emailModel = emailModel
       
        

    @staticmethod
    def get_all():
        conn = pyodbc.connect(connString, autocommit=True)
        cursor = conn.cursor()
        sqlcmd1 = "SELECT * FROM DataOwner ORDER BY dataOwnerName"
        cursor.execute(sqlcmd1)
        records = []
        for dbrow in cursor.fetchall():
            row = DataOwnerModel(dbrow[0],dbrow[1],dbrow[2],dbrow[3],dbrow[4],dbrow[5],dbrow[6],dbrow[7],dbrow[8],dbrow[9],dbrow[10])
            records.append(row)
        cursor.close()
        conn.close()
        return records

    @staticmethod
    def get_name_id():
        conn = pyodbc.connect(connString, autocommit=True)
        cursor = conn.cursor()
        sqlcmd1 = "SELECT dataOwnerID, dataOwnerName FROM DataOwner ORDER BY dataOwnerName"
        cursor.execute(sqlcmd1)
        records = []
        for dbrow in cursor.fetchall():
            row = DataOwnerModel(dbrow[0],dbrow[1])
            records.append(row)
        cursor.close()
        conn.close()
        return records
        
    @staticmethod
    def get_by_id(unique_id):
        conn = pyodbc.connect(connString, autocommit=True)
        cursor = conn.cursor()
        sqlcmd1 = "SELECT * FROM DataOwner WHERE dataOwnerID = ?"
        cursor.execute(sqlcmd1, unique_id)
        record = None
        for dbrow in cursor.fetchall():
            record = DataOwnerModel(dbrow[0],dbrow[1],dbrow[2],dbrow[3],dbrow[4],dbrow[5],dbrow[6],dbrow[7],dbrow[8],dbrow[9],dbrow[10])
        cursor.close()
        conn.close()
        return record
    
    @staticmethod
    def insert(obj):
        obj.dataOwnerID = str(uuid.uuid4())
        conn = pyodbc.connect(connString, autocommit=True)
        cursor = conn.cursor()
        sqlcmd1 = "INSERT INTO DataOwner (dataOwnerID,dataOwnerName,address,city,state,pincode,country,emailID,mobileNbr,addressProofFile,identityProofFile) VALUES(?,?,?,?,?,?,?,?,?,?,?)"
        cursor.execute(sqlcmd1, (obj.dataOwnerID,obj.dataOwnerName,obj.address,obj.city,obj.state,obj.pincode,obj.country,obj.emailID,obj.mobileNbr,obj.addressProofFile,obj.identityProofFile))
        cursor.close()
        conn.close()
        
    
    @staticmethod
    def update(obj):
        conn = pyodbc.connect(connString, autocommit=True)
        cursor = conn.cursor()
        sqlcmd1 = "UPDATE DataOwner SET dataOwnerName = ?,address = ?,city = ?,state = ?,pincode = ?,country = ?,emailID = ?,mobileNbr = ?,addressProofFile = ?,identityProofFile = ? WHERE dataOwnerID = ?"
        cursor.execute(sqlcmd1,  (obj.dataOwnerName,obj.address,obj.city,obj.state,obj.pincode,obj.country,obj.emailID,obj.mobileNbr,obj.addressProofFile,obj.identityProofFile,obj.dataOwnerID))
        cursor.close()
        conn.close()
    
    @staticmethod
    def delete(unique_id):
        conn = pyodbc.connect(connString, autocommit=True)
        cursor = conn.cursor()
        sqlcmd1 = "DELETE FROM DataOwner WHERE dataOwnerID = ?"
        cursor.execute(sqlcmd1, (unique_id))
        cursor.close()
        conn.close()

