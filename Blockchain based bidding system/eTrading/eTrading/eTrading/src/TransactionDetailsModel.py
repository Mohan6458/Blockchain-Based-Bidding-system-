from Constants import connString
import pyodbc
import datetime
import uuid
import time    
from Constants import contract_address
from web3 import Web3, HTTPProvider
import json
import pprint
        
class TransactionDetailsModel:
    def __init__(self, transactionDetailsID = '',transactionDetailsName = '',imageFile = '',createdDate = None,ipAddress = '',authorizedByID = '',verifiedByID = '',dataOwnerID = '',isBlockChainGenerated = False,hash = '',prevHash = '',sequenceNumber = 0,authorizedByModel = None,verifiedByModel = None,dataOwnerModel = None):
        self.transactionDetailsID = transactionDetailsID
        self.transactionDetailsName = transactionDetailsName
        self.imageFile = imageFile
        self.createdDate = createdDate
        self.ipAddress = ipAddress
        self.authorizedByID = authorizedByID
        self.verifiedByID = verifiedByID
        self.dataOwnerID = dataOwnerID
        self.isBlockChainGenerated = isBlockChainGenerated
        self.hash = hash
        self.prevHash = prevHash
        self.sequenceNumber = sequenceNumber
        self.authorizedByModel = authorizedByModel
        self.verifiedByModel = verifiedByModel
        self.dataOwnerModel = dataOwnerModel
       
        

    @staticmethod
    def get_all():
        conn = pyodbc.connect(connString, autocommit=True)
        cursor = conn.cursor()
        sqlcmd1 = "SELECT * FROM TransactionDetails ORDER BY transactionDetailsName"
        cursor.execute(sqlcmd1)
        records = []
        for dbrow in cursor.fetchall():
            row = TransactionDetailsModel(dbrow[0],dbrow[1],dbrow[2],dbrow[3],dbrow[4],dbrow[5],dbrow[6],dbrow[7],dbrow[8],dbrow[9],dbrow[10],dbrow[11])
            records.append(row)
        cursor.close()
        conn.close()
        return records

    @staticmethod
    def get_name_id():
        conn = pyodbc.connect(connString, autocommit=True)
        cursor = conn.cursor()
        sqlcmd1 = "SELECT transactionDetailsID, transactionDetailsName FROM TransactionDetails ORDER BY transactionDetailsName"
        cursor.execute(sqlcmd1)
        records = []
        for dbrow in cursor.fetchall():
            row = TransactionDetailsModel(dbrow[0],dbrow[1])
            records.append(row)
        cursor.close()
        conn.close()
        return records
        
    @staticmethod
    def get_by_id(unique_id):
        conn = pyodbc.connect(connString, autocommit=True)
        cursor = conn.cursor()
        sqlcmd1 = "SELECT * FROM TransactionDetails WHERE transactionDetailsID = ?"
        cursor.execute(sqlcmd1, unique_id)
        record = None
        for dbrow in cursor.fetchall():
            record = TransactionDetailsModel(dbrow[0],dbrow[1],dbrow[2],dbrow[3],dbrow[4],dbrow[5],dbrow[6],dbrow[7],dbrow[8],dbrow[9],dbrow[10],dbrow[11])
        cursor.close()
        conn.close()
        return record
    
    @staticmethod
    def insert(obj):
        obj.transactionDetailsID = str(uuid.uuid4())
        conn = pyodbc.connect(connString, autocommit=True)
        cursor = conn.cursor()
        sqlcmd1 = "INSERT INTO TransactionDetails (transactionDetailsID,transactionDetailsName,imageFile,createdDate,ipAddress,authorizedByID,verifiedByID,dataOwnerID,isBlockChainGenerated,hash,prevHash) VALUES(?,?,?,?,?,?,?,?,?,?,?)"
        cursor.execute(sqlcmd1, (obj.transactionDetailsID,obj.transactionDetailsName,obj.imageFile,datetime.datetime.strptime(obj.createdDate.replace('T', ' '), '%Y-%m-%d %H:%M'),obj.ipAddress,obj.authorizedByID,obj.verifiedByID,obj.dataOwnerID,obj.isBlockChainGenerated,obj.hash,obj.prevHash))
        cursor.close()
        conn.close()
        

        w3 = Web3(HTTPProvider('http://localhost:7545'))
        
        
        compiled_contract_path = '../../../eTrading-Truffle/build/contracts/TransactionDetailsContract.json'
        deployed_contract_address = contract_address
        
        with open(compiled_contract_path) as file:
            contract_json = json.load(file)
            contract_abi = contract_json["abi"]
        
        contract = w3.eth.contract(address=deployed_contract_address, abi=contract_abi)
        
        accounts = w3.eth.accounts
    
        
        tx_hash = contract.functions.perform_transactions(obj.transactionDetailsID, obj.transactionDetailsName, obj.imageFile, obj.ipAddress, obj.authorizedByID, obj.dataOwnerID).transact({'from': accounts[0]})
        receipt = w3.eth.wait_for_transaction_receipt(tx_hash)        
        
    
    @staticmethod
    def update(obj):
        conn = pyodbc.connect(connString, autocommit=True)
        cursor = conn.cursor()
        sqlcmd1 = "UPDATE TransactionDetails SET transactionDetailsName = ?,imageFile = ?,createdDate = ?,ipAddress = ?,authorizedByID = ?,verifiedByID = ?,dataOwnerID = ?,isBlockChainGenerated = ?,hash = ?,prevHash = ? WHERE transactionDetailsID = ?"
        cursor.execute(sqlcmd1,  (obj.transactionDetailsName,obj.imageFile,datetime.datetime.strptime(obj.createdDate.replace('T', ' '), '%Y-%m-%d %H:%M'),obj.ipAddress,obj.authorizedByID,obj.verifiedByID,obj.dataOwnerID,obj.isBlockChainGenerated,obj.hash,obj.prevHash,obj.transactionDetailsID))
        cursor.close()
        conn.close()
    
    @staticmethod
    def delete(unique_id):
        conn = pyodbc.connect(connString, autocommit=True)
        cursor = conn.cursor()
        sqlcmd1 = "DELETE FROM TransactionDetails WHERE transactionDetailsID = ?"
        cursor.execute(sqlcmd1, (unique_id))
        cursor.close()
        conn.close()

