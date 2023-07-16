// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "@openzeppelin/contracts/utils/Strings.sol";
import "@openzeppelin/contracts/token/ERC721/extensions/ERC721URIStorage.sol";
import "@openzeppelin/contracts/access/Ownable.sol";

contract VowelSoundsNFT is ERC721URIStorage, Ownable {
    uint256 private _tokenIdCounter;
    mapping(address => uint256) public contributors;
    mapping(address => bool) private _hasMinted;
    address public amb;

    constructor(address _amb) ERC721("VowelSoundsNFT", "AEIOU") {
        amb = _amb;
    }


    function setAmb(address _amb) external onlyOwner {
        amb = _amb;
    }

    function receiveContribution(address contributor, uint256 amount) public {
        require(msg.sender == amb, "Only the AMB can call this function");
        require(amount > 0, "Amount must be greater than 0");
        require(contributors[contributor] > 0, "Address has already been synced");
        contributors[contributor] = amount;
    }

    function mintNFT() public {
        require(contributors[msg.sender] > 0, "Only members can mint NFTs");
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
