// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract Contribution {
    address payable public immutable owner;
    address payable public immutable beneficiary;
    bool public isReleased;
    uint256 public deadline;
    uint256 public countdownPeriod;
    uint256 public threshold;

    event Contribute(address indexed contributor, uint256 amount);
    event Decryptable(address indexed lastContributor);
    event Withdraw(address indexed beneficiary, uint256 amount);

    constructor(
        uint256 _countdownPeriod,
        uint256 _threshold,
        address payable _beneficiary
    ) {
        countdownPeriod = _countdownPeriod;
        deadline = block.timestamp + _countdownPeriod;
        owner = payable(msg.sender);
        threshold = _threshold;
        beneficiary = _beneficiary;
    }

    function contribute() external payable {
        // This is "contribution-revealer logic"
        require(
            block.timestamp < deadline,
            "Cannot contribute after the deadline"
        );

        if (address(this).balance >= threshold) {
            // Mark the material as released
            isReleased = true;
            emit Decryptable(msg.sender);
        }

        // Reset the countdown period
        deadline = block.timestamp + countdownPeriod;

        emit Contribute(msg.sender, msg.value);
    }

    receive() external payable {
        emit Contribute(msg.sender, msg.value);
    }

    function withdraw() external {
        require(
            msg.sender == beneficiary,
            "Only the beneficiary can withdraw funds"
        );
        require(deadline < block.timestamp, "Cannot withdraw funds before deadline");

        beneficiary.transfer(address(this).balance);
        emit Withdraw(beneficiary, address(this).balance);
    }
}
