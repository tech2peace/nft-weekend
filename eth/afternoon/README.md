### ETH Track, Session 2
# Basic ERC721 Contract

## Prerequisites

- A web browser
- A metamask wallet

## Roadmap

- [x] Write a basic ERC721 contract
- [x] Get verifiable randomness from VRF
- [x] Implement delayed reveal of art
- [ ] Deploy contract
- [ ] Automate interaction with contract

## Provided Files

- `WordPieceFactory.sol` -- An example of what you should have by the end of this session. Again, we recommend you to follow the instructions and try it out by yourselves and use the given file for final comparison.
- `VRFv2Consumer.sol` -- An example for a contract that calls Chainlink's VRF. This file will be useful to understand how the interaction with the VRF oracle works.

## Instructions

> So far, we have written a contract where we can mint a limited number of ERC721 tokens, and attach a uri to each of them. While this is typically the most basic form of NFTs, our project consists of randomly generated art. Complying with the spirit of crypto, we would like this randomness to be verifiable, unpredictable and unmanipulable by any of the involved parties. To accomplish this, we will rely on [Chainlink's VRF](https://docs.chain.link/docs/vrf/v2/introduction/) as a source of trusted randomness and use the obtained randomness to generate the art pieces in a deterministic manner.
>

### Extending the Data Structure

> First, let us extend the data structure in which we store the information attached to the tokens. So far, this information contains only the uri (i.e. a `string`). We would like now to additionally attach to every token a random value that will be used to generate the art, and possibly some other relevant information. For that, we will use Solidity's structs that pack a collection of variables into a newly defined data type (similar to structs in C).
>

1. Define a new `struct` that captures all data attached to a token (see [docs](https://docs.soliditylang.org/en/v0.8.16/types.html#structs) for syntax and further details). Hereby, we refer to the new data type by `TokenData`, but allow yourself to call it by a different descriptive name (possibly derived by your token's name). At this point, `TokenData` should contain the token's uri (a `string`) and the token's id (`uint256`).
2. Modify the existing mapping to map any token id to a `TokenData` value, rather than a `string`.
3. Apply the necessary changes in `createToken`. Take a look at the examples [here](https://solidity-by-example.org/structs/).


### Filling in the Randomness

> Let us take a look at `VRFv2Consumer.sol`. This is an example of a basic contract that uses Chainlink's VRF oracle to obtain verifiable randomness. Pay attention to few things:
> - The contract inherits `VRFConsumerBaseV2` (which is imported via an `import` command). This is a `virtual` base class (i.e. an interface) that specifies a certain template that should be followed in any contract that uses the VRF (see the code [here](https://github.com/smartcontractkit/chainlink/blob/develop/contracts/src/v0.8/VRFConsumerBaseV2.sol)). In particular, any such contract should implement a `fulfillRandomWords` function. This function is called whenever the contract receives new verifiable randomness from the VRF and should define how the contract handles the new randomness (looking ahead, in our case, `fulfillRandomWords` will attach the received randomness to a corresponding token).
> - The interaction with the VRF oracle is done via a "VRF Coordinator" contract that implements the `VRFCoordinatorV2Interface` (which is also imported via an `import` and can be found [here](https://github.com/smartcontractkit/chainlink/blob/develop/contracts/src/v0.8/interfaces/VRFCoordinatorV2Interface.sol)). Take a look at the [code](https://github.com/smartcontractkit/chainlink/blob/develop/contracts/src/v0.8/interfaces/VRFCoordinatorV2Interface.sol) and focus on the `requestRandomWords` function which we will be using to request randomness from the VRF. This function takes as input a number of parameters that specify the way in which we interact with the VRF and returns a `requestId`, which is a unique identifier number for the request that has been made by the call.
>
> To summarize:
> - The contract `VRFv2Consumer` stores a pointer `COORDINATOR` to the a VRF coordinator which is specified by an address `vrfCoordinator` (that is different for different networks).
> - The contract request randomness by calling `COORDINATOR.requestRandomWords` with some specified parameters (in paritcular, the number of requested random words, `numWords`) and gets back a `requestId` (of type `uint256`).
> - To handle the VRF responces, the contract implements the `fulfillRandomWords` function that takes as input a `requestId` specifying the corresponding request the VRF is reponsindg to to and an `uint256` array of size `numWords` that contains the randomness returned by the VRF.
>

4. Add an `uint256` randomness field to the `TokenData` struct. This will contain the randomness attached to the corresponding token.
5. Copy the following code to your contract. The code contains declarations of state variables that will be passed on as arguments to the VRF-related functions.

```solidity

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

```
6. Following the template in `VRFv2Consumer.sol` and the explanation above, implement the logic to request a random word for every new token minted in `createToken`, and a `fulfillRandomWords` function that fills in the received randomness. Make sure to keep track of which randomness belongs to which token (hint: recall that you can use a `mapping` to map between VRF request ids and token ids).

> To test the new changes on Remix's local VM, we need to simulate the behavior of the VRF coordinator as if we were interacting with the oracles on Ethereum's mainnet (or testnets). We do that using a mock contract that mimics a legit VRF Coordinator (the only difference being that it outoputs "fake randomness" (which is predictable). Luckily, such a contract is publicly available [here](https://github.com/smartcontractkit/chainlink/blob/develop/contracts/src/v0.8/mocks/VRFCoordinatorV2Mock.sol).
>

7. In order to compile the mock contract to Remix, add the following line at the import section of the file:
```solidity
import "@chainlink/contracts/src/v0.8/mocks/VRFCoordinatorV2Mock.sol";
```
8. Compile the contract through the **Solidity Compiler** sidebar tab.
9. Go to the **Deploy & Run Transactions** tab and deploy the `VRFCoordinatorV2Mock` contract, which can now found in the dropdown list. Set the input arguments for the deployment to `0,0`.
10. At this point you should be seeing an instance of the mock contract under the **Deployed Contracts** section at the bottom of the sidebar. Click on the clipboard icon next to the contract to copy its address on the local network. This is the address of the VRF Coordinator that we will be using when we test our contract on the local network. Paste address to assign it to the `vrfCoordinator` state variable.
11. Now that we have a mock deployed and its address copied to our contract, we need to create a subscription through which the VRF calls will be "funded" (more about Chainlink's VRF subscriptions in the [documentation](https://docs.chain.link/docs/vrf/v2/introduction/#subscriptions)). Click on the **createSubscription** button under the sidebar instant to call the mock contract and create a subscription. You should see a confirmation for the transaction in the terminal. Congratualations! you have subscribed to the mock VRF Coordinator. Since this is your first subscription, its id will be 1. You can verify that using a call to the `getSubscription` function (just click the button). Now you can fill in your subscription id (1) to the `vrfSubscriptionId` state variable.
12. Having filled in all necessary configurations, we are ready to deploy the ERC721 contract. Go ahead and deploy it. Test your new functions. In order to "trigger" the mock VRF and make it respond to requests, call the `fulfillRandomWords` function in the mock oracle with the arguments specifying the id of the request you wish to get a respose to and the address of the contract that made this request (that is, the ERC721 contract).
13. Take a break :tropical_drink:.

### Implement Delayed Reveal

> Now that we have the funcionality to mint tokens and attach them to a verifiably random value, the only piece that is missing in our contract is a function that will allow to "reveal" the art obtained by the generative algorithm when given the randomness.
>

14. Define and implement a reveal function that takes as input a token id and a uri (a `string`) and sets the uri of the corresponding token to the given uri.
15. Apply the `onlyOwner` modifer to the reveal function.
16. Implement the logic to enforce that the reveal function can be called only once (hint: one possibility is to an `enum` (see [docs](https://docs.soliditylang.org/en/v0.8.16/structure-of-a-contract.html?highlight=struct#enum-types)) to describe the status of a token).
17. Declare a `tokenUri` function as follows
```solidity
    function tokenURI(uint256 tokenId) public override view returns (string memory) {
```
and implement it so it returns the uri of the token corresponding to the given id. This function is required to nicely display your NFT art on OpenSea (see the [documentation of the OpenSea format](https://docs.opensea.io/docs/metadata-standards)).

### Freestyle

18. This is the time to wake up your creative self and add fancy features and game rules in your contract to make you NFT project unique and interesting :alien::monkey::sparkles:.