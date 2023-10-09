pragma solidity >=0.4.22 <0.9.0;
    contract TransactionDetailsContract {
    string public transactionDetailsID;
	string public transactionDetailsName;
	string public imageFile;
	string public ipAddress;
	string public authorizedByID;
	string public dataOwnerID;
	
    
    function perform_transactions(string memory _transactionDetailsID, string memory _transactionDetailsName, string memory _imageFile, string memory _ipAddress, string memory _authorizedByID, string memory _dataOwnerID) public{
       transactionDetailsID = _transactionDetailsID;
		transactionDetailsName = _transactionDetailsName;
		imageFile = _imageFile;
		ipAddress = _ipAddress;
		authorizedByID = _authorizedByID;
		dataOwnerID = _dataOwnerID;
		
    }
        
}
