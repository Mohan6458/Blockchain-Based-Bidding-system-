pragma solidity >=0.4.22 <0.9.0;
    contract DataOwnerContract {
    string public dataOwnerID;
	
    
    function perform_transactions(string memory _dataOwnerID) public{
       dataOwnerID = _dataOwnerID;
		
    }
        
}
