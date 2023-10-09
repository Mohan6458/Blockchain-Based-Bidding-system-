const AuthorizedBy = artifacts.require("AuthorizedByContract.sol");
        module.exports = function (deployer) {
          deployer.deploy(AuthorizedBy);
        };
        