const VerifiedBy = artifacts.require("VerifiedByContract.sol");
        module.exports = function (deployer) {
          deployer.deploy(VerifiedBy);
        };
        