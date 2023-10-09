const DataOwner = artifacts.require("DataOwnerContract.sol");
        module.exports = function (deployer) {
          deployer.deploy(DataOwner);
        };
        