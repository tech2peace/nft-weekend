// Your subscription ID.
// For Rinkeby use 21372.
uint64 public constant vrfSubscriptionId = ;

// VRF coordinator address.
// For Rinkeby use 0x6168499c0cFfCaCD319c818142124B7A15E857ab.
address public constant vrfCoordinator = ;

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

// For our purpose, retrieve 1 random value in one request.
// Cannot exceed VRFCoordinatorV2.MAX_NUM_WORDS.
uint32 public constant vrfNumWords =  1;