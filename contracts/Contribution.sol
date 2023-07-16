// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract Contribution {

    // roles
    address payable public immutable owner;
    address payable public immutable beneficiary;

    // countdown and threshold
    bool public materialReleaseConditionMet = false;
    uint256 public deadline;
    uint256 public countdownPeriod;
    uint256 public threshold;

    // commit and reveal
    bool public isKeySet = false;
    bytes32 public keyPlaintextHash;
    bytes public keyCiphertext;
    bytes public keyPlaintext;

    // testnet mode
    bool testnet;

    // bridge
    address public amb;
    address public destinationContract;
    uint256 public bridgeGasLimit = 100000;

    // contributions storage
    mapping(address => uint256) public amountContributedByAddress;
    address[] contributors;

    //events
    event Contribute(address indexed contributor, uint256 amount);
    event Decryptable(address indexed lastContributor);
    event Withdraw(address indexed beneficiary, uint256 amount);

    constructor(
        uint256 _countdownPeriod,
        uint256 _threshold,
        address payable _beneficiary,
        bool _testnet
    ) {
        countdownPeriod = _countdownPeriod;
        deadline = block.timestamp + _countdownPeriod;
        owner = payable(msg.sender);
        threshold = _threshold;
        beneficiary = _beneficiary;
        testnet = _testnet;
    }

    modifier onlyOwner() {
        require(msg.sender == owner, "Only the contract owner can call this function.");
        _;
    }

    modifier onlyBeneficiary() {
        require(
            msg.sender == beneficiary,
            "Only the beneficiary can call this function."
        );
        _;
    }

    //
    // Testnet functions
    //

    function resetClock() external onlyOwner {
        require(testnet, "This function is only available on testnet.");
        deadline = block.timestamp + countdownPeriod;
    }

    function setMaterialReleaseConditionMet(bool status) external onlyOwner {
        require(testnet, "This function is only available on testnet.");
        materialReleaseConditionMet = status;
    }

    function setThreshold(uint256 _threshold) external onlyOwner {
        require(testnet, "This function is only available on testnet.");
        threshold = _threshold;
    }

    function setAmb(address _amb) external onlyOwner {
        require(testnet, "This function is only available on testnet.");
        amb = _amb;
    }

    //
    // Production functions
    //

    function setBridgeGasLimit(uint256 _bridgeGasLimit) external onlyOwner {
        bridgeGasLimit = _bridgeGasLimit;
    }

    function setDestinationContract(address _destinationContract) external onlyOwner {
        destinationContract = _destinationContract;
    }

    function commitSecret(bytes32 _hash, bytes memory _ciphertext) external onlyOwner {
        if (!testnet) {
            require(!isKeySet, "Key already set.");
        }
        keyPlaintextHash = _hash;
        keyCiphertext = _ciphertext;
        isKeySet = true;
    }

    function bridgeContribution() internal {
        require(block.timestamp < deadline, "Cannot bridge after the deadline");
        bytes4 methodSelector = bytes4(keccak256(bytes('receiveContribution(address,uint256)')));
        uint amount = amountContributedByAddress[msg.sender];
        bytes memory data = abi.encodeWithSelector(methodSelector, msg.sender, amount);
        amb.call(abi.encodeWithSignature('requireToPassMessage(address,bytes,uint256)', destinationContract, data, bridgeGasLimit));
    }

    function revealSecret(bytes memory secret) external {
        require(materialReleaseConditionMet, "Material has not been set for a release.");
        require(keccak256(secret) == keyPlaintextHash, "Invalid secret provided, hash does not match.");
        keyPlaintext = secret;
    }

    function contribute() external payable {
        require(block.timestamp < deadline, "Cannot contribute after the deadline");
        require(isKeySet, "Key has not been set.");

        if (amountContributedByAddress[msg.sender] == 0) { // If this is the first contribution from this address
            contributors.push(msg.sender); // Add the address to the contributors array
        }
        amountContributedByAddress[msg.sender] += msg.value; // Add contribution to the mapping

        if (address(this).balance >= threshold) {
            materialReleaseConditionMet = true;
            emit Decryptable(msg.sender);
        }

        deadline = block.timestamp + countdownPeriod;
        bridgeContribution();
        emit Contribute(msg.sender, msg.value);
    }

    receive() external payable {
        emit Contribute(msg.sender, msg.value);
    }

    function withdraw() external onlyBeneficiary {
        require(deadline < block.timestamp, "Cannot withdraw funds before deadline");
        beneficiary.transfer(address(this).balance);
        emit Withdraw(beneficiary, address(this).balance);
    }

}
