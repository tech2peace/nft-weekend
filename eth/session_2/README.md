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

The directory contains the file `WordPieceFactory.sol` which is an example of what you should have by the end of this session. Again, we recommend you to follow the instructions and try it out by yourselves and use the given file for final comparison.

## Instructions

So far, we have written a contract where we can mint a limited number of ERC721 tokens, and attach a uri to each of them. While this is typically the most basic form of NFTs, our project consists of randomly generated art. Complying with the spirit of crypto, we would like this randomness to be verifiable, unpredictable and unmanipulable by any of the involved parties. To accomplish this, we will rely on [Chainlink's VRF](https://docs.chain.link/docs/vrf/v2/introduction/) as a source of trusted randomness and use the obtained randomness to generate the art pieces in a deterministic manner.

### Extending the Data Structure

First, let us extend the data structure in which we store the information attached to the tokens. So far, this information contains only the uri (i.e. a string). We would like now to attach to every token a random value that will be used to generate the art, at the last (we will latter see that we need to have additional fields). Solidity gives us the possibility to define structs (similar to structs in C) that pack a collection of variables into a newly defined data type.

1. Define a new `struct` that captures all data attached to a token (see (docs)[https://docs.soliditylang.org/en/v0.8.16/types.html#structs] for syntax and further details). Hereby, we refer to the new data type by `TokenData`, but allow yourself to call it by a different descriptive name (possibly derived by your token's name). At this point `TokenData` should contain the token's uri (a `string`) and the token's id (`uint256`).
2. Modify the existing mapping to map any token id to a `TokenData` value, rather than a `string`.
3. Apply the necessary changes in `createToken`. Take a look at the examples [here](https://solidity-by-example.org/structs/).


### Filling in the Randomness

### Implement Delayed Reveal
