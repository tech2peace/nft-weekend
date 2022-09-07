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

## Instructions

1. Open **[Remix IDE](https://remix.ethereum.org/)** on your browser.
2. Create a new workspace with the **OpenZeppelin ERC721** template.
3. Set a fixed name and symbol for your token in `constructor`.
4. Add a `baseUri` field and initalize it in `constructor` with a string passed on as argument. Read more about [state variables](https://docs.soliditylang.org/en/v0.8.9/structure-of-a-contract.html#state-variables), data [types](https://docs.soliditylang.org/en/v0.8.9/types.html) and [locations](https://docs.soliditylang.org/en/v0.8.13/types.html#data-location-and-assignment-behaviour) in the solidity documentation pages.
5. Test what you've got so far locally on a Remix's virtual machine:
    1. Go to the **Deploy & run transactions** tab on the sidebar on the left.
    2. Choose one of the **Remix VM** options for environment and your contract in the contract field.
    3. Fill in the a base Uri of your choice next to the orange **Deploy** button, then click it to deploy the contract.