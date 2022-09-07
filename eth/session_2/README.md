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
- `VRFv2Consumer.sol` -- an example for a contract that calls Chainlink's VRF. This file will be useful to understand how the interaction with the VRF oracle works.

## Instructions

So far, we have written a contract where we can mint a limited number of ERC721 tokens, and attach a uri to each of them. While this is typically the most basic form of NFTs, our project consists of randomly generated art. Complying with the spirit of crypto, we would like this randomness to be verifiable, unpredictable and unmanipulable by any of the involved parties. To accomplish this, we will rely on [Chainlink's VRF](https://docs.chain.link/docs/vrf/v2/introduction/) as a source of trusted randomness and use the obtained randomness to generate the art pieces in a deterministic manner.

### Extending the Data Structure

First, let us extend the data structure in which we store the information attached to the tokens. So far, this information contains only the uri (i.e. a `string`). We would like now to additionally attach to every token a random value that will be used to generate the art, and possibly some other relevant information. For that, we will use Solidity's structs that pack a collection of variables into a newly defined data type (similar to structs in C).

1. Define a new `struct` that captures all data attached to a token (see [docs](https://docs.soliditylang.org/en/v0.8.16/types.html#structs) for syntax and further details). Hereby, we refer to the new data type by `TokenData`, but allow yourself to call it by a different descriptive name (possibly derived by your token's name). At this point, `TokenData` should contain the token's uri (a `string`) and the token's id (`uint256`).
2. Modify the existing mapping to map any token id to a `TokenData` value, rather than a `string`.
3. Apply the necessary changes in `createToken`. Take a look at the examples [here](https://solidity-by-example.org/structs/).


### Filling in the Randomness

Let us take a look at `VRFv2Consumer.sol`. This is an example of a basic contract that uses Chainlink's VRF oracle to obtain verifiable randomness. Pay attention to few things:
- The contract inherits `VRFConsumerBaseV2` (which is imported via an `import` command). This is a `virtual` base class (i.e. an interface) that specifies a certain template that should be followed in any contract that uses the VRF (see the code [here](https://github.com/smartcontractkit/chainlink/blob/develop/contracts/src/v0.8/VRFConsumerBaseV2.sol)). In particular, any such contract should implement a `fulfillRandomWords` function. This function is called whenever the contract receives new verifiable randomness from the VRF and should define how the contract handles the new randomness (looking ahead, in our case, `fulfillRandomWords` will attach the received randomness to a corresponding token).
- The interaction with the VRF oracle is done via a "VRF Coordinator" contract that implements the `VRFCoordinatorV2Interface` (which is also imported via an `import` and can be found [here](https://github.com/smartcontractkit/chainlink/blob/develop/contracts/src/v0.8/interfaces/VRFCoordinatorV2Interface.sol)). Take a look at the [code](https://github.com/smartcontractkit/chainlink/blob/develop/contracts/src/v0.8/interfaces/VRFCoordinatorV2Interface.sol) and focus on the `requestRandomWords` function which we will be using to request randomness from the VRF. This function takes as input a number of parameters that specify the way in which we interact with the VRF and returns a `requestId`, which is a unique identifier number for the request that has been made by the call.

To summarize:
- The contract `VRFv2Consumer` stores a pointer `COORDINATOR` to the a VRF coordinator which is specified by an address `vrfCoordinator` (that is different for different networks).
- The contract request randomness by calling `COORDINATOR.requestRandomWords` with some specified parameters (in paritcular, the number of requested random words, `numWords`) and gets back a `requestId` (of type `uint256`).
- To handle the VRF responces, the contract implements the `fulfillRandomWords` function that takes as input a `requestId` specifying the corresponding request the VRF is reponsindg to to and an `uint256` array of size `numWords` that contains the randomness returned by the VRF.

4. Add an `uint256` randomness field to the `TokenData` struct. This will contain the randomness attached to the corresponding token.
5. Following the template in `VRFv2Consumer.sol` and the explanation above, implement the logic for requesting a random word for every new token minted in `createToken`, and a `fulfillRandomWords` function that fills in the received randomness. Make sure to keep track of which randomness belongs to which token (hint: recall that you can use the `mapping` data structure to map between VRF request ids and token ids).

### Implement Delayed Reveal
