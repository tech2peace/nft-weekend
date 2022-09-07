### ETH Track, Session 1
# Basic ERC721 Contract

## Prerequisites

- A web browser

## Roadmap

- [x] Write a basic ERC721 contract
- [ ] Get verifiable randomness from VRF
- [ ] Implement delayed reveal of art
- [ ] Deploy contract
- [ ] Automate interaction with contract

## Provided Files

The directory contains the file `WordPieceFactory.sol` which is an example of what you should have by the end of this session. We recommend, however, to try and follow the instructions to write your own contract from scratch (lots of fun and feelings of accomplishment and reward are guaranteed :smirk:).

## Instructions

### Getting Started

We start by fetching a general tempalte for an ERC721 token contract and testing it locally on Remix.

1. Open **[Remix IDE](https://remix.ethereum.org/)** on your browser.
2. Create a new workspace with the **OpenZeppelin ERC721** template. This creates blank contract that is inheriting from [OpenZepplin's ERC721 token contract](https://github.com/OpenZeppelin/openzeppelin-contracts/blob/master/contracts/token/ERC721/ERC721.sol) ([docs](https://docs.openzeppelin.com/contracts/2.x/erc721)) which is the community's standard for NFT contracts, and provides an implementatoin of basic non-fungible token functionalities, e.g. token ownership, minting and transfer.
3. Set a fixed name and symbol for your token in `constructor`.
4. Add a `baseUri` field and initalize it in `constructor` with a string passed on as argument. Read more about [state variables](https://docs.soliditylang.org/en/v0.8.9/structure-of-a-contract.html#state-variables), data [types](https://docs.soliditylang.org/en/v0.8.9/types.html) and [locations](https://docs.soliditylang.org/en/v0.8.13/types.html#data-location-and-assignment-behaviour) in the solidity documentation pages.
5. Test what you've got so far, locally on a Remix's virtual machine:
    1. Go to the **Deploy & run transactions** tab on the sidebar on the left.
    2. Choose one of the **Remix VM** options for environment and your contract in the contract field.
    3. Fill in a `baseUri` input of your choice next to the orange **Deploy** button, then click it to deploy the contract.
    4. You can now see the locally deployed instance under **Deployed Contracts** and test it by interacting with the interface.

### Withdrawing from Contract

As a general rule of thumb, always implement a function that will let you withdraw all funds from any contract. You do not want funds to be locked in a contract for eternity :skull:.

6. Define a new `withdraw` function to allow withdrawing funds that are stored in the contract. Read more about [functions](https://docs.soliditylang.org/en/v0.6.5/contracts.html#functions) in solidity in the documentation.
7. Implement `withdraw`.
    1. Use `address(this).balance` to get the balance of the contract in Wei (see [docs](https://docs.soliditylang.org/en/develop/units-and-global-variables.html#address-related)).
    2. Use `msg.sender` to get the address of the caller of the function (see [docs](https://docs.soliditylang.org/en/develop/units-and-global-variables.html#block-and-transaction-properties)).
    3. Transfer funds to `msg.sender` using one of the transfer functions `call`, `transfer` or `send` (see [here](https://solidity-by-example.org/sending-ether/), [here](https://blockchain-academy.hs-mittweida.de/courses/solidity-coding-beginners-to-intermediate/lessons/solidity-2-sending-ether-receiving-ether-emitting-events/topic/sending-ether-send-vs-transfer-vs-call/) or [here](https://fravoll.github.io/solidity-patterns/secure_ether_transfer.html)). Make sure to cast `msg.sender` to a `payable` address type in order to allow the transfer of funds (read about [address type conversions](https://docs.soliditylang.org/en/v0.8.9/types.html#address) in the docs).

### The `OnlyOwner` Modifier

The current `withdraw` function allows anyone on the Ethereum network to steal all our contract's funds. We obviously want to restrict it to be called only using our account (i.e. public key), that is, only by whoever deployed this instance of the contract, namely its **owner**.

8. As a first step, let us store the address of the contract's owner upon deployment. Define an `owner` state field and initialize it in the `constructor` using `msg.sender`. Consider defining `owner` to be an `immutable` field (see the [docs](https://docs.soliditylang.org/en/v0.8.13/contracts.html#constant-and-immutable-state-variables)).
9. Now, we could simply compare the caller's address in `withdraw` to the address in `owner` and allow withdrawal only if they match. However, a better more modular approach would be to implement a **function modifier** that allows execution of any function only when the caller of the function is the owner of the contract. In general, modifiers in solidity can be thought of as "filters" that can be applied over any function in the contract to modify it as defined in the modifier. Read the [docs](https://docs.soliditylang.org/en/v0.8.13/contracts.html?highlight=modifier#function-modifiers) to read more about modifiers and their syntax, and to find an example for the `onlyOwner` modifier. As seen in the example, use `require` to handle the case when the caller's address does not match the owner's (read more about error handling in solidity [here](https://solidity-by-example.org/error/) and [here](https://ethereum.stackexchange.com/a/24185)).

### The Mint Function

While the [`ERC721` base class]((https://github.com/OpenZeppelin/openzeppelin-contracts/blob/master/contracts/token/ERC721/ERC721.sol))([docs](https://docs.openzeppelin.com/contracts/2.x/erc721)) implements a `_safeMint` function for minting tokens, this function is `internal` (see [here](https://docs.soliditylang.org/en/v0.8.13/contracts.html#function-visibility)) and, in fact, does not do much other than registering ownership of a given integer id (i.e. the minted token's id) to a certain address (i.e. the token's owner). In this section, we want to write a `public` function for minting tokens and attach a **token uri** to the newly token that would contain a link to any relevant data (as we will see later, this will contain in particular the image file for the NFT and its description).

10. Declare a `public` function. The function takes as input the uri of the new token (a `string`) and outputs an `uint256` that is the id of the new token (see [docs](https://docs.soliditylang.org/en/v0.8.13/contracts.html#return-variables) for return value declaration). We will refer to the function  by `createToken` but feel free to choose your own descriptive name.
11. Use `_safeMint` (see [documentation](https://docs.openzeppelin.com/contracts/2.x/api/token/erc721#ERC721-_safeMint-address-uint256-bytes-)) to register the id of the new token to the caller of the function (who is the new token's owner). Typically, tokens are given increasing ids, starting at 0 for the first minted token. To be able to keep track of the next available token id, declare `tokenCounter` variable and initialize it in `constructor` and implement the necessary logic in `createToken`.
12. To ensure **rarity** of the art pieces, NFT projects typically limit the total number of tokens that can be minted. Declare a `constant` state variable `supply` that contains the maximum amount of tokens and use `require` to enforce that no tokens beyond the specified amount are minted.
13. In order to attach the given uri to the new token, use the `mapping` data structure provided by solidity (see [documentation](https://docs.soliditylang.org/en/v0.8.9/types.html#mapping-types)) and use it to map between ids and uris. The examples given [here](https://solidity-by-example.org/mapping/) might be useful to understand the syntax. Make sure to declare the mapping as public to allow easy lookup of the token uris.
14. Lastly, notice that minting tokens should not be for free and/or available for anyone. There are two approaches to limit minting tokens:
    - The first specifies a price for minting a new token. This can be done by declaring the minting function as `payable` (see [docs](https://docs.soliditylang.org/en/v0.8.14/types.html#function-types)) and requiring a minimum amount of Wei to be sent with the function call. In this case, the funds will go to the contract and can be withdrawn using `withdraw`.
    - A second option, which we will follow since it is simpler, more controllable and is more friendly to the common user (yet is more "centralized" in a sense), is to let minting be free but allow it only for the owner using the `onlyOwner` modifier that we have already implemented. In this case, the ownership is tranferred to costumers in a latter stage, using the built-in `_transfer` function of the `ERC721` base class. 
15. Test your contract on Remix's VM (see step 5 above).
16. Dance :dancer:.
