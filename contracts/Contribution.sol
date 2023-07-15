// SPDX-License-Identifier: GPL-3.0-only
pragma solidity ^0.8.0;

contract Contribution {
    
    // roles
    address public immutable owner;
    address payable public immutable beneficiary;

    // countdown and threshold
    bool public materialReleaseConditionMet = false;
    uint256 public deadline;
    uint256 public countdownPeriod;
    uint256 public threshold;
    uint256 public minContribution;

    // commit and reveal
    bool public isKeySet = false;
    bytes32 public keyPlaintextHash;
    bytes public keyCiphertext;
    bytes public keyPlaintext;

    // testnet mode
    bool public testnet;
    
    // contributions storage
    mapping(address => uint256[]) public contributionsByAddress;
    address[] public contributors;
    address public artifactContract;

    //events
    event Contribute(address indexed contributor, uint256 amount);
    event Decryptable(address indexed lastContributor);
    event Withdraw(address indexed beneficiary, uint256 amount);
    event ClockReset(uint256 deadline);

    constructor(
        uint256 _countdownPeriod,
        uint256 _threshold,
        uint256 _minContribution,
        address payable _beneficiary,
        bool _testnet
    ) {
        countdownPeriod = _countdownPeriod;
        deadline = 0;
        owner = msg.sender;
        beneficiary = payable(_beneficiary);
        threshold = _threshold;
        minContribution = _minContribution;
        testnet = _testnet;
    }

    modifier onlyOwner() {
        require(msg.sender == owner,
            "Only the contract owner can call this function.");
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

    //
    // Production functions
    //

    function setArtifactContract(address _artifactContract) public onlyOwner {
        artifactContract = _artifactContract;
    }

    function commitSecret(bytes32 _hash, bytes memory _ciphertext) external onlyOwner {
        if (!testnet) {
            require(!isKeySet, "Key already set.");
        }
        keyPlaintextHash = _hash;
        keyCiphertext = _ciphertext;
        isKeySet = true;
    }

    function revealSecret(bytes memory secret) external {
        require(materialReleaseConditionMet, "Material has not been set for a release.");
        require(keccak256(secret) == keyPlaintextHash, "Invalid secret provided, hash does not match.");
        keyPlaintext = secret;
    }

    function _contribute(bool combine) internal {
        require(isKeySet, "Key has not been set.");
        require(!materialReleaseConditionMet || block.timestamp < deadline,
            "Cannot contribute after the deadline");
        require(msg.value >= minContribution,
            "Contribution must be equal to or greater than the minimum.");

        if (contributionsByAddress[msg.sender].length == 0) { // If this is the first contribution from this address
            contributors.push(msg.sender); // Add the address to the contributors array
        }

        if (combine) {
            contributionsByAddress[msg.sender][0] += msg.value;
        } else {
            contributionsByAddress[msg.sender].push(msg.value); // Add contribution to the mapping
        }

        if (address(this).balance >= threshold && !materialReleaseConditionMet) {
            materialReleaseConditionMet = true;
            emit Decryptable(msg.sender);
        }

        if (materialReleaseConditionMet) {
            deadline = block.timestamp + countdownPeriod;
            emit ClockReset(deadline);
        }

        emit Contribute(msg.sender, msg.value);
    }

    function contribute() external payable {
        _contribute(false);
    }

    function contributeAndCombine() external payable {
        _contribute(true);
    }

    function totalContributedByAddress(address contributor) external view returns (uint256) {
        uint256 total = 0;
        for (uint256 i = 0; i < contributionsByAddress[contributor].length; i++) {
            total += contributionsByAddress[contributor][i];
        }
        return total;
    }

    function getContributors() external view returns (address[] memory) {
        return contributors;
    }

    function getContributionsByAddress(address contributor) external view returns (uint256[] memory) {
        return contributionsByAddress[contributor];
    }

    receive() external payable {
        emit Contribute(msg.sender, msg.value);
    }

    function withdraw() external onlyBeneficiary {
        require(materialReleaseConditionMet, "Material has not been set for a release.");
        require(deadline < block.timestamp, "Cannot withdraw funds before deadline");
        uint256 balance = address(this).balance;
        beneficiary.transfer(balance);
        emit Withdraw(beneficiary, balance);
    }

}
