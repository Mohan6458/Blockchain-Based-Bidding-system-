pragma solidity >=0.4.22 <0.9.0;
    contract AuthorizedByContract {
    string public authorizedByID;
	
    
    function perform_transactions(string memory _authorizedByID) public{
       authorizedByID = _authorizedByID;
		
    }
        
}
