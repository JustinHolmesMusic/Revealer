// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "@openzeppelin/contracts/token/ERC721/extensions/ERC721URIStorage.sol";
import "@openzeppelin/contracts/access/Ownable.sol";

contract VowelSoundsNFT is ERC721URIStorage, Ownable {
    uint256 private _tokenIdCounter;
    mapping(address => bool) public members;
    mapping(address => bool) private _hasMinted;

    constructor() ERC721("VowelSoundsNFT", "AEIOU") {}

    function addMember(address member) public onlyOwner {
        members[member] = true;
    }

    function mintNFT() public {
        require(members[msg.sender], "Only members can mint NFTs");
        require(!_hasMinted[msg.sender], "Address has already minted an NFT");
        _safeMint(msg.sender, _tokenIdCounter);
        _setTokenURI(_tokenIdCounter, "https://vowelsoundsnft.com/metadata/" + string(abi.encodePacked(_tokenIdCounter)));
        _tokenIdCounter++;
        _hasMinted[msg.sender] = true;
    }

    function updateTokenURI(uint256 tokenId, string memory newURI) public onlyOwner {
        _setTokenURI(tokenId, newURI);
    }
}
