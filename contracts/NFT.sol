// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "@openzeppelin/contracts/utils/Strings.sol";
import "@openzeppelin/contracts/token/ERC721/extensions/ERC721URIStorage.sol";
import "@openzeppelin/contracts/access/Ownable.sol";

contract VowelSoundsNFT is ERC721URIStorage, Ownable {
    uint256 private _tokenIdCounter;
    address payable public admin;
    bool isEnrollmentOpen = true;
    mapping(address => uint) public members;
    mapping(address => bool) private _hasMinted;

    constructor(
        address payable _amb
    ) ERC721("VowelSoundsNFT", "AEIOU") {
        amb = address(_amb);
    }

    function addMember(address member, uint value) external {
        require(msg.sender == admin, "Only amb can add members");
        members[member] = value;
    }

    function endEnrollment() external {
        require(msg.sender == admin, "Only amb can end enrollment");
        isEnrollmentOpen = false;
    }

    // sort members by value in descending order
    function sortMembers() external {
        require(!isEnrollmentOpen, "Enrollment must be closed before sorting");
        uint n = 0;
        address[] memory keys = new address[](members.length);
        for (uint i = 0; i < members.length; i++) {
            keys[i] = members[i];
        }
        for (uint i = 0; i < members.length; i++) {
            for (uint j = i + 1; j < members.length; j++) {
                if (members[keys[i]] < members[keys[j]]) {
                    address temp = keys[i];
                    keys[i] = keys[j];
                    keys[j] = temp;
                }
            }
        }
        for (uint i = 0; i < members.length; i++) {
            members[keys[i]] = i;
        }
    }

    function setAdmin(address payable _admin) external onlyOwner {
        admin = _admin;
    }

    function mintNFT() public {
        require(members[msg.sender], "Only members can mint NFTs");
        require(!_hasMinted[msg.sender], "Address has already minted an NFT");
        _safeMint(msg.sender, _tokenIdCounter);
        _setTokenURI(_tokenIdCounter, string(abi.encodePacked("https://vowelsoundsnft.com/metadata/", Strings.toString(_tokenIdCounter))));
        _tokenIdCounter++;
        _hasMinted[msg.sender] = true;
    }

    function updateTokenURI(uint256 tokenId, string memory newURI) public onlyOwner {
        _setTokenURI(tokenId, newURI);
    }
}
