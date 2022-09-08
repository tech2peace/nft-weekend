// SPDX-License-Identifier: GPL-3.0

pragma solidity >=0.7.0 <0.9.0;

import "@openzeppelin/contracts/token/ERC721/ERC721.sol";
import "@chainlink/contracts/src/v0.8/interfaces/LinkTokenInterface.sol";
import "@chainlink/contracts/src/v0.8/interfaces/VRFCoordinatorV2Interface.sol";
import "@chainlink/contracts/src/v0.8/VRFConsumerBaseV2.sol";
import "@chainlink/contracts/src/v0.8/mocks/VRFCoordinatorV2Mock.sol";

/**
 * @title WordPieceFactory
 * @dev ERC721 token contract for WordPiece NFT
 */
contract WordPieceFactory is ERC721, VRFConsumerBaseV2 {

    address private immutable _owner;

    string public baseURI;

    uint256 public constant supply = 11;
    uint256 public tokenCounter;

    enum Status{ PENDING_RANDOMNESS, PENDING_REVEAL, REVEALED }

    struct WordPiece {
        uint256 id;
        uint256 vrfRequestId;
        uint256 randomness;
        string uri;
        Status status;
    }

    mapping(uint256 => WordPiece) public pieceById;
    mapping(uint256 => uint256) public idByRequest;

    // VRF coordinator interface.
    VRFCoordinatorV2Interface COORDINATOR;

    // Your subscription ID.
    // For Rinkeby use 21372.
    uint64 public constant vrfSubscriptionId = 21372;

    // VRF coordinator address.
    // For Rinkeby use 0x6168499c0cFfCaCD319c818142124B7A15E857ab.
    address public constant vrfCoordinator = 0x6168499c0cFfCaCD319c818142124B7A15E857ab;

    // The gas lane to use for Rinkeby, which specifies the maximum gas price to bump to.
    bytes32 public constant vrfKeyHash = 0xd89b2bf150e3b9e13446986e571fb9cab24b13cea0a43ea20a6049a85cc807cc;

    // Depends on the number of requested values that you want sent to the
    // fulfillRandomWords() function. Storing each word costs about 20,000 gas,
    // so 100,000 is a safe default for this example contract. Test and adjust
    // this limit based on the network that you select, the size of the request,
    // and the processing of the callback request in the fulfillRandomWords()
    // function.
    uint32 public constant vrfCallbackGasLimit = 100000;

    // The default is 3, but you can set this higher.
    uint16 public constant vrfRequestConfirmations = 3;

    // For this example, retrieve 2 random values in one request.
    // Cannot exceed VRFCoordinatorV2.MAX_NUM_WORDS.
    uint32 public constant vrfNumWords =  1;

    constructor(string memory base) ERC721("WordPiece", "WRD") VRFConsumerBaseV2(vrfCoordinator) {
        COORDINATOR = VRFCoordinatorV2Interface(vrfCoordinator);
        _owner = msg.sender;
        baseURI = base;
        tokenCounter = 0;
    }

    function tokenRandomness(uint256 pieceId) public view returns (uint256) {
        return pieceById[pieceId].randomness;
    }

    // for OpenSea
    function tokenURI(uint256 pieceId) public override view returns (string memory) {
        return pieceById[pieceId].uri;
    }

    function createPiece() public onlyOwner() returns (uint256) {
        require(tokenCounter < supply, "supply limit reached");
        uint256 newId = tokenCounter;
        tokenCounter++;

        uint256 vrfRequestId = COORDINATOR.requestRandomWords(
            vrfKeyHash,
            vrfSubscriptionId,
            vrfRequestConfirmations,
            vrfCallbackGasLimit,
            vrfNumWords
        );

        _safeMint(msg.sender, newId);

        WordPiece storage newPiece = pieceById[newId];
        newPiece.id = newId;
        newPiece.vrfRequestId = vrfRequestId;
        newPiece.status = Status.PENDING_RANDOMNESS;
        idByRequest[vrfRequestId] = newId;

        return newId;
    }

    function revealPiece(uint256 pieceId, string memory pieceUri) public onlyOwner() {
        WordPiece storage piece = pieceById[pieceId];
        require(piece.status == Status.PENDING_REVEAL, "piece with given id cannot be revealed");

        piece.uri = pieceUri;
        piece.status = Status.REVEALED;
    }

    function fulfillRandomWords(uint256 requestId, uint256[] memory randomWords)
    internal override {
        WordPiece storage piece = pieceById[idByRequest[requestId]];
        require(piece.vrfRequestId == requestId, "VRF request with given id does not exist");

        require(randomWords.length > 0, "VRF response is empty");

        piece.randomness = randomWords[0];
        piece.status = Status.PENDING_REVEAL;
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