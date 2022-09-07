// SPDX-License-Identifier: GPL-3.0

pragma solidity >=0.7.0 <0.9.0;

import "@openzeppelin/contracts/token/ERC721/ERC721.sol";

/**
 * @title WordPieceFactory
 * @dev ERC721 token contract for WordPiece NFT
 */
contract WordPieceFactory is ERC721, VRFConsumerBaseV2 {

    address private immutable _owner;

    string public baseURI;

    uint256 public constant supply = 11;
    uint256 public tokenCounter;

    struct WordPiece {
        uint256 id;
        string uri;
    }

    mapping(uint256 => WordPiece) public pieceById;

    constructor(string memory base) ERC721("WordPiece", "WRD") VRFConsumerBaseV2(vrfCoordinator) {
        _owner = msg.sender;
        baseURI = base;
        tokenCounter = 0;
    }

    function createPiece(string memory pieceUri) public onlyOwner() returns (uint256) {
        require(tokenCounter < supply, "supply limit reached");
        uint256 newId = tokenCounter;
        tokenCounter++;

        _safeMint(msg.sender, newId);

        WordPiece storage newPiece = pieceById[newId];
        newPiece.id = newId;
        newPiece.uri = pieceUri;
        return newId;
    }

    function withdraw() public onlyOwner() {
        uint balance = address(this).balance;
        payable(msg.sender).transfer(balance);
    }

    modifier onlyOwner() {
        require(msg.sender == _owner, "only owner can withdraw");
        _;
    }
}