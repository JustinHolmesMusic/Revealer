// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract Contribution {
    address payable public immutable owner;
    address payable public immutable beneficiary;
    bool public materialReleaseConditionMet = false;
    uint256 public deadline;
    uint256 public countdownPeriod;
    uint256 public threshold;
    bool public isKeySet = false;

    bytes32 public keyPlaintextHash;
    bytes public keyCiphertext;
    bytes public keyPlaintext;

    bool testnet;

    mapping(address => uint256) public amountContributedByAddress;

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

    function commitSecret(bytes32 _hash, bytes memory _ciphertext) external onlyOwner {
        require(!isKeySet, "Key already set.");

        keyPlaintextHash = _hash;
        keyCiphertext = _ciphertext;
        isKeySet = true;
    }

    function revealSecret(bytes memory secret) external {
        require(materialReleaseConditionMet, "Material has not been set for a release.");
        require(keccak256(secret) == keyPlaintextHash, "Invalid secret provided, hash does not match.");
        keyPlaintext = secret;
    }

    function contribute() external payable {
        require(block.timestamp < deadline, "Cannot contribute after the deadline");
        require(isKeySet, "Key has not been set.");

        amountContributedByAddress[msg.sender] += msg.value; // Add contribution to the mapping

        if (address(this).balance >= threshold) {
            materialReleaseConditionMet = true;
            emit Decryptable(msg.sender);
        }

        deadline = block.timestamp + countdownPeriod;
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

    function bridgeContributor(address member) internal onlyOwner {
        bytes4 methodSelector = bytes4(keccak256(bytes('addMember(address, value)')));
        bytes memory data = abi.encodeWithSelector(methodSelector, member);
        amb.call(abi.encodeWithSignature('requireToPassMessage(address,bytes,uint256)', destContract, data, 141000));
    }
}
