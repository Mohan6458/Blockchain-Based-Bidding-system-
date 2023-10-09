
from flask import Flask, request, render_template, redirect, url_for
import os
import pyodbc
import uuid
import time
from datetime import datetime
from Constants import connString

from AuthorizedByModel import AuthorizedByModel
from DataOwnerModel import DataOwnerModel
from RoleModel import RoleModel
from TransactionDetailsModel import TransactionDetailsModel
from UsersModel import UsersModel
from VerifiedByModel import VerifiedByModel




app = Flask(__name__)
app.secret_key = "MySecret"
ctx = app.app_context()
ctx.push()

with ctx:
    pass
user_id = ""
emailid = ""
role_object = None
message = ""
msgType = ""
uploaded_file_name = ""

def initialize():
    global message, msgType
    message = ""
    msgType = ""

def process_role(option_id):

    
    if option_id == 0:
        if role_object.canAuthorizedBy == False:
            return False
        
    if option_id == 1:
        if role_object.canDataOwner == False:
            return False
        
    if option_id == 2:
        if role_object.canRole == False:
            return False
        
    if option_id == 3:
        if role_object.canTransactionDetails == False:
            return False
        
    if option_id == 4:
        if role_object.canUsers == False:
            return False
        
    if option_id == 5:
        if role_object.canVerifiedBy == False:
            return False
        

    return True



@app.route("/")
def index():
    global user_id, emailid
    return render_template("Login.html")

@app.route("/processLogin", methods=["POST"])
def processLogin():
    global user_id, emailid, role_object
    emailid = request.form["emailid"]
    password = request.form["password"]
    conn1 = pyodbc.connect(connString, autocommit=True)
    cur1 = conn1.cursor()
    sqlcmd1 = "SELECT * FROM Users WHERE emailid = '" + emailid + "' AND password = '" + password + "' AND isActive = 1";
    cur1.execute(sqlcmd1)
    row = cur1.fetchone()

    cur1.commit()
    if not row:
        return render_template("Login.html", processResult="Invalid Credentials")
    user_id = row[0]

    cur2 = conn1.cursor()
    sqlcmd2 = "SELECT * FROM Role WHERE RoleID = '" + str(row[6]) + "'"
    cur2.execute(sqlcmd2)
    row2 = cur2.fetchone()

    if not row2:
        return render_template("Login.html", processResult="Invalid Role")

    role_object = RoleModel(row2[0], row2[1], row2[2], row2[3], row2[4], row2[5], row2[6], row2[7])

    return render_template("Dashboard.html")


@app.route("/ChangePassword")
def changePassword():
    global user_id, emailid
    return render_template("ChangePassword.html")


@app.route("/ProcessChangePassword", methods=["POST"])
def processChangePassword():
    global user_id, emailid
    oldPassword = request.form["oldPassword"]
    newPassword = request.form["newPassword"]
    confirmPassword = request.form["confirmPassword"]
    conn1 = pyodbc.connect(connString, autocommit=True)
    cur1 = conn1.cursor()
    sqlcmd1 = "SELECT * FROM Users WHERE emailid = '" + emailid + "' AND password = '" + oldPassword + "'";
    cur1.execute(sqlcmd1)
    row = cur1.fetchone()
    cur1.commit()
    if not row:
        return render_template("ChangePassword.html", msg="Invalid Old Password")

    if newPassword.strip() != confirmPassword.strip():
        return render_template("ChangePassword.html", msg="New Password and Confirm Password are NOT same")

    conn2 = pyodbc.connect(connString, autocommit=True)
    cur2 = conn2.cursor()
    sqlcmd2 = "UPDATE Users SET password = '" + newPassword + "' WHERE emailid = '" + emailid + "'";
    cur1.execute(sqlcmd2)
    cur2.commit()
    return render_template("ChangePassword.html", msg="Password Changed Successfully")


@app.route("/Dashboard")
def Dashboard():
    global user_id, emailid
    return render_template("Dashboard.html")


@app.route("/Information")
def Information():
    global message, msgType
    return render_template("Information.html", msgType=msgType, message=message)


@app.route("/AuthorizedByListing")
def AuthorizedBy_listing():
    global user_id, emailid

    global message, msgType, role_object
    if role_object == None:
        message = "Application Error Occurred. Logout"
        msgType = "Error"
        return redirect(url_for("Information"))
    canAuthorizedBy = process_role(0)

    if canAuthorizedBy == False:
        message = "You Don't Have Permission to Access AuthorizedBy"
        msgType = "Error"
        return redirect(url_for("Information"))

    records = AuthorizedByModel.get_all()

    return render_template("AuthorizedByListing.html", records=records)

@app.route("/AuthorizedByOperation")
def AuthorizedBy_operation():
    global user_id, user_name, message, msgType, role_object
    if role_object is None:
        message = "Application Error Occurred. Logout"
        msgType = "Error"
        return redirect(url_for("Information"))
    canAuthorizedBy = process_role(0)

    if not canAuthorizedBy:
        message = "You Don't Have Permission to Access AuthorizedBy"
        msgType = "Error"
        return redirect(url_for("Information"))
    unique_id = ""
    operation = request.args.get("operation")
    row = AuthorizedByModel("", "")

    AuthorizedBy = AuthorizedByModel.get_all()
    
    if operation != "Create":
        unique_id = request.args.get("unique_id").strip()
        row = AuthorizedByModel.get_by_id(unique_id)

    return render_template("AuthorizedByOperation.html", row=row, operation=operation, AuthorizedBy=AuthorizedBy, )

@app.route("/ProcessAuthorizedByOperation", methods=["POST"])
def process_AuthorizedBy_operation():
    global user_id, user_name, message, msgType, role_object

    if role_object is None:
        message = "Application Error Occurred. Logout"
        msgType = "Error"
        return redirect(url_for("/"))

    canAuthorizedBy = process_role(0)
    if not canAuthorizedBy:
        message = "You Don't Have Permission to Access AuthorizedBy"
        msgType = "Error"
        return redirect(url_for("Information"))

    operation = request.form["operation"]
    obj = AuthorizedByModel("", "")

    if operation != "Delete":
       obj.authorizedByID = request.form['authorizedByID']
       obj.authorizedByName = request.form['authorizedByName']
       

    if operation == "Create":
        obj.insert(obj)

    if operation == "Edit":
        obj.authorizedByID = request.form["authorizedByID"]
        obj.update(obj)

    if operation == "Delete":
        authorizedByID = request.form["authorizedByID"]
        obj.delete(authorizedByID)


    return redirect(url_for("AuthorizedBy_listing"))
                    
@app.route("/DataOwnerListing")
def DataOwner_listing():
    global user_id, emailid

    global message, msgType, role_object
    if role_object == None:
        message = "Application Error Occurred. Logout"
        msgType = "Error"
        return redirect(url_for("Information"))
    canDataOwner = process_role(1)

    if canDataOwner == False:
        message = "You Don't Have Permission to Access DataOwner"
        msgType = "Error"
        return redirect(url_for("Information"))

    records = DataOwnerModel.get_all()

    return render_template("DataOwnerListing.html", records=records)

@app.route("/DataOwnerOperation")
def DataOwner_operation():
    global user_id, user_name, message, msgType, role_object
    if role_object is None:
        message = "Application Error Occurred. Logout"
        msgType = "Error"
        return redirect(url_for("Information"))
    canDataOwner = process_role(1)

    if not canDataOwner:
        message = "You Don't Have Permission to Access DataOwner"
        msgType = "Error"
        return redirect(url_for("Information"))
    unique_id = ""
    operation = request.args.get("operation")
    row = DataOwnerModel("", "")

    DataOwner = DataOwnerModel.get_all()
    
    if operation != "Create":
        unique_id = request.args.get("unique_id").strip()
        row = DataOwnerModel.get_by_id(unique_id)

    return render_template("DataOwnerOperation.html", row=row, operation=operation, DataOwner=DataOwner, )

@app.route("/ProcessDataOwnerOperation", methods=["POST"])
def process_DataOwner_operation():
    global user_id, user_name, message, msgType, role_object

    if role_object is None:
        message = "Application Error Occurred. Logout"
        msgType = "Error"
        return redirect(url_for("/"))

    canDataOwner = process_role(1)
    if not canDataOwner:
        message = "You Don't Have Permission to Access DataOwner"
        msgType = "Error"
        return redirect(url_for("Information"))

    operation = request.form["operation"]
    obj = DataOwnerModel("", "")

    if operation != "Delete":
       obj.dataOwnerID = request.form['dataOwnerID']
       obj.dataOwnerName = request.form['dataOwnerName']
       obj.address = request.form['address']
       obj.city = request.form['city']
       obj.state = request.form['state']
       obj.pincode = request.form['pincode']
       obj.country = request.form['country']
       obj.emailID = request.form['emailID']
       obj.mobileNbr = request.form['mobileNbr']
       if len(request.files) != 0 :
        
                file = request.files['addressProofFile']
                if file.filename != '':
                    addressProofFile = file.filename
                    obj.addressProofFile = addressProofFile
                    f = os.path.join('static/UPLOADED_FILES', addressProofFile)
                    file.save(f)
                else:
                    obj.addressProofFile = request.form['haddressProofFile']
                
                file = request.files['identityProofFile']
                if file.filename != '':
                    identityProofFile = file.filename
                    obj.identityProofFile = identityProofFile
                    f = os.path.join('static/UPLOADED_FILES', identityProofFile)
                    file.save(f)
                else:
                    obj.identityProofFile = request.form['hidentityProofFile']
                

    if operation == "Create":
        obj.insert(obj)

    if operation == "Edit":
        obj.dataOwnerID = request.form["dataOwnerID"]
        obj.update(obj)

    if operation == "Delete":
        dataOwnerID = request.form["dataOwnerID"]
        obj.delete(dataOwnerID)


    return redirect(url_for("DataOwner_listing"))
                    
@app.route("/RoleListing")
def Role_listing():
    global user_id, emailid

    global message, msgType, role_object
    if role_object == None:
        message = "Application Error Occurred. Logout"
        msgType = "Error"
        return redirect(url_for("Information"))
    canRole = process_role(2)

    if canRole == False:
        message = "You Don't Have Permission to Access Role"
        msgType = "Error"
        return redirect(url_for("Information"))

    records = RoleModel.get_all()

    return render_template("RoleListing.html", records=records)

@app.route("/RoleOperation")
def Role_operation():
    global user_id, user_name, message, msgType, role_object
    if role_object is None:
        message = "Application Error Occurred. Logout"
        msgType = "Error"
        return redirect(url_for("Information"))
    canRole = process_role(2)

    if not canRole:
        message = "You Don't Have Permission to Access Role"
        msgType = "Error"
        return redirect(url_for("Information"))
    unique_id = ""
    operation = request.args.get("operation")
    row = RoleModel("", "")

    Role = RoleModel.get_all()
    
    if operation != "Create":
        unique_id = request.args.get("unique_id").strip()
        row = RoleModel.get_by_id(unique_id)

    return render_template("RoleOperation.html", row=row, operation=operation, Role=Role, )

@app.route("/ProcessRoleOperation", methods=["POST"])
def process_Role_operation():
    global user_id, user_name, message, msgType, role_object

    if role_object is None:
        message = "Application Error Occurred. Logout"
        msgType = "Error"
        return redirect(url_for("/"))

    canRole = process_role(2)
    if not canRole:
        message = "You Don't Have Permission to Access Role"
        msgType = "Error"
        return redirect(url_for("Information"))

    operation = request.form["operation"]
    obj = RoleModel("", "")

    if operation != "Delete":
       obj.roleID = request.form['roleID']
       obj.roleName = request.form['roleName']
       obj.canRole = 0 
       if request.form.get("canRole") != None : 
              obj.canRole = 1       
       obj.canUsers = 0 
       if request.form.get("canUsers") != None : 
              obj.canUsers = 1       
       obj.canAuthorizedBy = 0 
       if request.form.get("canAuthorizedBy") != None : 
              obj.canAuthorizedBy = 1       
       obj.canDataOwner = 0 
       if request.form.get("canDataOwner") != None : 
              obj.canDataOwner = 1       
       obj.canTransactionDetails = 0 
       if request.form.get("canTransactionDetails") != None : 
              obj.canTransactionDetails = 1       
       obj.canVerifiedBy = 0 
       if request.form.get("canVerifiedBy") != None : 
              obj.canVerifiedBy = 1       
       

    if operation == "Create":
        obj.insert(obj)

    if operation == "Edit":
        obj.roleID = request.form["roleID"]
        obj.update(obj)

    if operation == "Delete":
        roleID = request.form["roleID"]
        obj.delete(roleID)


    return redirect(url_for("Role_listing"))
                    
@app.route("/TransactionDetailsListing")
def TransactionDetails_listing():
    global user_id, emailid

    global message, msgType, role_object
    if role_object == None:
        message = "Application Error Occurred. Logout"
        msgType = "Error"
        return redirect(url_for("Information"))
    canTransactionDetails = process_role(3)

    if canTransactionDetails == False:
        message = "You Don't Have Permission to Access TransactionDetails"
        msgType = "Error"
        return redirect(url_for("Information"))

    records = TransactionDetailsModel.get_all()

    return render_template("TransactionDetailsListing.html", records=records)

@app.route("/TransactionDetailsOperation")
def TransactionDetails_operation():
    global user_id, user_name, message, msgType, role_object
    if role_object is None:
        message = "Application Error Occurred. Logout"
        msgType = "Error"
        return redirect(url_for("Information"))
    canTransactionDetails = process_role(3)

    if not canTransactionDetails:
        message = "You Don't Have Permission to Access TransactionDetails"
        msgType = "Error"
        return redirect(url_for("Information"))
    unique_id = ""
    operation = request.args.get("operation")
    row = TransactionDetailsModel("", "")

    TransactionDetails = TransactionDetailsModel.get_all()
    authorizedBy_list = AuthorizedByModel.get_name_id()
    verifiedBy_list = VerifiedByModel.get_name_id()
    dataOwner_list = DataOwnerModel.get_name_id()
    if operation != "Create":
        unique_id = request.args.get("unique_id").strip()
        row = TransactionDetailsModel.get_by_id(unique_id)

    return render_template("TransactionDetailsOperation.html", row=row, operation=operation, TransactionDetails=TransactionDetails, authorizedBy_list = authorizedBy_list,verifiedBy_list = verifiedBy_list,dataOwner_list = dataOwner_list)

@app.route("/ProcessTransactionDetailsOperation", methods=["POST"])
def process_TransactionDetails_operation():
    global user_id, user_name, message, msgType, role_object

    if role_object is None:
        message = "Application Error Occurred. Logout"
        msgType = "Error"
        return redirect(url_for("/"))

    canTransactionDetails = process_role(3)
    if not canTransactionDetails:
        message = "You Don't Have Permission to Access TransactionDetails"
        msgType = "Error"
        return redirect(url_for("Information"))

    operation = request.form["operation"]
    obj = TransactionDetailsModel("", "")

    if operation != "Delete":
       obj.transactionDetailsID = request.form['transactionDetailsID']
       obj.transactionDetailsName = request.form['transactionDetailsName']
       obj.createdDate = request.form['createdDate']
       obj.ipAddress = request.form['ipAddress']
       obj.authorizedByID = request.form['authorizedByID']
       obj.verifiedByID = request.form['verifiedByID']
       obj.dataOwnerID = request.form['dataOwnerID']
       if len(request.files) != 0 :
        
                file = request.files['imageFile']
                if file.filename != '':
                    imageFile = file.filename
                    obj.imageFile = imageFile
                    f = os.path.join('static/UPLOADED_FILES', imageFile)
                    file.save(f)
                else:
                    obj.imageFile = request.form['himageFile']
                

    if operation == "Create":
        obj.insert(obj)

    if operation == "Edit":
        obj.transactionDetailsID = request.form["transactionDetailsID"]
        obj.update(obj)

    if operation == "Delete":
        transactionDetailsID = request.form["transactionDetailsID"]
        obj.delete(transactionDetailsID)


    return redirect(url_for("TransactionDetails_listing"))
                    
@app.route("/UsersListing")
def Users_listing():
    global user_id, emailid

    global message, msgType, role_object
    if role_object == None:
        message = "Application Error Occurred. Logout"
        msgType = "Error"
        return redirect(url_for("Information"))
    canUsers = process_role(4)

    if canUsers == False:
        message = "You Don't Have Permission to Access Users"
        msgType = "Error"
        return redirect(url_for("Information"))

    records = UsersModel.get_all()

    return render_template("UsersListing.html", records=records)

@app.route("/UsersOperation")
def Users_operation():
    global user_id, user_name, message, msgType, role_object
    if role_object is None:
        message = "Application Error Occurred. Logout"
        msgType = "Error"
        return redirect(url_for("Information"))
    canUsers = process_role(4)

    if not canUsers:
        message = "You Don't Have Permission to Access Users"
        msgType = "Error"
        return redirect(url_for("Information"))
    unique_id = ""
    operation = request.args.get("operation")
    row = UsersModel("", "")

    Users = UsersModel.get_all()
    role_list = RoleModel.get_name_id()
    if operation != "Create":
        unique_id = request.args.get("unique_id").strip()
        row = UsersModel.get_by_id(unique_id)

    return render_template("UsersOperation.html", row=row, operation=operation, Users=Users, role_list = role_list)

@app.route("/ProcessUsersOperation", methods=["POST"])
def process_Users_operation():
    global user_id, user_name, message, msgType, role_object

    if role_object is None:
        message = "Application Error Occurred. Logout"
        msgType = "Error"
        return redirect(url_for("/"))

    canUsers = process_role(4)
    if not canUsers:
        message = "You Don't Have Permission to Access Users"
        msgType = "Error"
        return redirect(url_for("Information"))

    operation = request.form["operation"]
    obj = UsersModel("", "")

    if operation != "Delete":
       obj.userID = request.form['userID']
       obj.userName = request.form['userName']
       obj.emailid = request.form['emailid']
       obj.password = request.form['password']
       obj.contactNo = request.form['contactNo']
       obj.isActive = 0 
       if request.form.get("isActive") != None : 
              obj.isActive = 1       
       obj.roleID = request.form['roleID']
       

    if operation == "Create":
        obj.insert(obj)

    if operation == "Edit":
        obj.userID = request.form["userID"]
        obj.update(obj)

    if operation == "Delete":
        userID = request.form["userID"]
        obj.delete(userID)


    return redirect(url_for("Users_listing"))
                    
@app.route("/VerifiedByListing")
def VerifiedBy_listing():
    global user_id, emailid

    global message, msgType, role_object
    if role_object == None:
        message = "Application Error Occurred. Logout"
        msgType = "Error"
        return redirect(url_for("Information"))
    canVerifiedBy = process_role(5)

    if canVerifiedBy == False:
        message = "You Don't Have Permission to Access VerifiedBy"
        msgType = "Error"
        return redirect(url_for("Information"))

    records = VerifiedByModel.get_all()

    return render_template("VerifiedByListing.html", records=records)

@app.route("/VerifiedByOperation")
def VerifiedBy_operation():
    global user_id, user_name, message, msgType, role_object
    if role_object is None:
        message = "Application Error Occurred. Logout"
        msgType = "Error"
        return redirect(url_for("Information"))
    canVerifiedBy = process_role(5)

    if not canVerifiedBy:
        message = "You Don't Have Permission to Access VerifiedBy"
        msgType = "Error"
        return redirect(url_for("Information"))
    unique_id = ""
    operation = request.args.get("operation")
    row = VerifiedByModel("", "")

    VerifiedBy = VerifiedByModel.get_all()
    
    if operation != "Create":
        unique_id = request.args.get("unique_id").strip()
        row = VerifiedByModel.get_by_id(unique_id)

    return render_template("VerifiedByOperation.html", row=row, operation=operation, VerifiedBy=VerifiedBy, )

@app.route("/ProcessVerifiedByOperation", methods=["POST"])
def process_VerifiedBy_operation():
    global user_id, user_name, message, msgType, role_object

    if role_object is None:
        message = "Application Error Occurred. Logout"
        msgType = "Error"
        return redirect(url_for("/"))

    canVerifiedBy = process_role(5)
    if not canVerifiedBy:
        message = "You Don't Have Permission to Access VerifiedBy"
        msgType = "Error"
        return redirect(url_for("Information"))

    operation = request.form["operation"]
    obj = VerifiedByModel("", "")

    if operation != "Delete":
       obj.verifiedByID = request.form['verifiedByID']
       obj.verifiedByName = request.form['verifiedByName']
       

    if operation == "Create":
        obj.insert(obj)

    if operation == "Edit":
        obj.verifiedByID = request.form["verifiedByID"]
        obj.update(obj)

    if operation == "Delete":
        verifiedByID = request.form["verifiedByID"]
        obj.delete(verifiedByID)


    return redirect(url_for("VerifiedBy_listing"))
                    


import hashlib
import json


@app.route("/BlockChainGeneration")
def BlockChainGeneration():

    conn = pyodbc.connect(connString, autocommit=True)
    cursor = conn.cursor()
    sqlcmd = "SELECT COUNT(*) FROM TransactionDetails WHERE isBlockChainGenerated = 1"
    cursor.execute(sqlcmd)
    while True:
        dbrow = cursor.fetchone()
        if not dbrow:
            break
        blocksCreated = dbrow[0]

    sqlcmd = "SELECT COUNT(*) FROM TransactionDetails WHERE isBlockChainGenerated = 0 or isBlockChainGenerated is null"
    cursor.execute(sqlcmd)
    while True:
        dbrow = cursor.fetchone()
        if not dbrow:
            break
        blocksNotCreated = dbrow[0]
    return render_template('BlockChainGeneration.html', blocksCreated=blocksCreated, blocksNotCreated=blocksNotCreated)


@app.route("/ProcessBlockchainGeneration", methods=['POST'])
def ProcessBlockchainGeneration():

    conn = pyodbc.connect(connString, autocommit=True)
    cursor = conn.cursor()
    sqlcmd = "SELECT COUNT(*) FROM TransactionDetails WHERE isBlockChainGenerated = 1"
    cursor.execute(sqlcmd)
    blocksCreated = 0
    while True:
        dbrow = cursor.fetchone()
        if not dbrow:
            break
        blocksCreated = dbrow[0]

    prevHash = ""
    if blocksCreated != 0:
        connx = pyodbc.connect(connString, autocommit=True)
        cursorx = connx.cursor()
        sqlcmdx = "SELECT * FROM TransactionDetails WHERE isBlockChainGenerated = 0 or isBlockChainGenerated is null ORDER BY sequenceNumber"
        cursorx.execute(sqlcmdx)
        dbrowx = cursorx.fetchone()
        if dbrowx:
            uniqueID = dbrowx[11]
            conny = pyodbc.connect(connString, autocommit=True)
            cursory = conny.cursor()
            sqlcmdy = "SELECT hash FROM TransactionDetails WHERE sequenceNumber < '" + str(uniqueID) + "' ORDER BY sequenceNumber DESC"
            cursory.execute(sqlcmdy)
            dbrowy = cursory.fetchone()
            if dbrowy:
                prevHash = dbrowy[0]
            cursory.close()
            conny.close()
        cursorx.close()
        connx.close()
    conn = pyodbc.connect(connString, autocommit=True)
    cursor = conn.cursor()
    sqlcmd = "SELECT * FROM TransactionDetails WHERE isBlockChainGenerated = 0 or isBlockChainGenerated is null ORDER BY sequenceNumber"
    cursor.execute(sqlcmd)

    while True:
        sqlcmd1 = ""
        dbrow = cursor.fetchone()
        if not dbrow:
            break
        unqid = str(dbrow[11])

        bdata = str(dbrow[1]) + str(dbrow[2]) + str(dbrow[3]) + str(dbrow[4])
        block_serialized = json.dumps(bdata, sort_keys=True).encode('utf-8')
        block_hash = hashlib.sha256(block_serialized).hexdigest()

        conn1 = pyodbc.connect(connString, autocommit=True)
        cursor1 = conn1.cursor()
        sqlcmd1 = "UPDATE TransactionDetails SET isBlockChainGenerated = 1, hash = '" + block_hash + "', prevHash = '" + prevHash + "' WHERE sequenceNumber = '" + unqid + "'"
        cursor1.execute(sqlcmd1)
        cursor1.close()
        conn1.close()
        prevHash = block_hash
    return render_template('BlockchainGenerationResult.html')


@app.route("/BlockChainReport")
def BlockChainReport():

    conn = pyodbc.connect(connString, autocommit=True)
    cursor = conn.cursor()

    sqlcmd1 = "SELECT * FROM TransactionDetails WHERE isBlockChainGenerated = 1"
    cursor.execute(sqlcmd1)
    conn2 = pyodbc.connect(connString, autocommit=True)
    cursor = conn2.cursor()
    sqlcmd1 = "SELECT * FROM TransactionDetails ORDER BY sequenceNumber DESC"
    cursor.execute(sqlcmd1)
    records = []

    while True:
        dbrow = cursor.fetchone()
        if not dbrow:
            break
        row = TransactionDetailsModel(dbrow[0],dbrow[1],dbrow[2],dbrow[3],dbrow[4],dbrow[5],dbrow[6],dbrow[7],dbrow[8],dbrow[9],dbrow[10],dbrow[11])
        records.append(row)
    return render_template('BlockChainReport.html', records=records)         

            

 
if __name__ == "__main__":
    app.run()

                    