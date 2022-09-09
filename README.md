<h1 align="center">Lido Insurance Fund</h1>

![solidity 0.8.§3](https://img.shields.io/badge/solidity-0.8.16-lightgray)
![python ~3.8.9](https://img.shields.io/badge/python-~3.9-blue)
![eth_brownie ^1.19.0](https://img.shields.io/badge/eth__brownie-^1.19.1-brown)
![license GPL](https://img.shields.io/badge/license-GPL-green)

The Lido Insurance Fund is a vault contract that serves as a simple transparent store for funds allocated for self-insurance purposes.

## 💰 About Insurance Fund

The Lido Insurance Fund is a vault contract intended for storing Lido insurance funds in a secure and transparent manner with the DAO Agent preserving full control over the assets.

For further details [read ADR](https://hackmd.io/qGnEmiSBTLiPJLa0VZOBGQ?view).

## 🏁 Getting started

This project uses Brownie development framework. Learn more about [Brownie](https://eth-brownie.readthedocs.io/en/stable/index.html).

### Prerequisites

- Python 3.9+
- Poetry 1.1.13

#### Step 1. Install Python dependencies.
Install project dependendencies from the lockfile,

```bash
$ poetry install
```

#### Step 2. Activate venv.
Activate Poetry virtual environment,

```bash
$ poetry shell
```

Learn more about [Poetry](https://python-poetry.org/docs/).


#### Step 3. Specify your Infura project id.

Replace `%YOUR-INFURA-PROJECT-ID%` below with your actual project id. Learn more about [Infura](https://infura.io/).

```bash
$ export WEB3_INFURA_PROJECT_ID=%YOUR-INFURA-PROJECT-ID%
```

#### Step 4 (recommended). Specify your Etherscan API key.

Replace `%YOUR-ETHERSCAN-TOKEN%` below with your actual API key. Learn more about [Etherscan API](https://etherscan.io/apis).

```bash
$ export ETHERSCAN_TOKEN=%YOUR-ETHERSCAN-TOKEN%
```

#### Step 5 (optional). Add a Goerli development fork.

The project uses the `mainnet-fork` network by default. To run the test suite on Goerli, you can add `goerli-fork` by running the following command,

```bash
$ brownie networks add "Development" goerli-fork host=http://127.0.0.1 cmd=ganache-cli port=8545 gas_limit=12000000 fork=https://goerli.infura.io/v3/${WEB3_INFURA_PROJECT_ID} chain_id=5 mnemonic=brownie accounts=10 fork=goerli
```

## 🧪 Testing the Insurance Fund

Before you proceed, please follow [Getting Started](#-getting-started) instructions.

To run the entire test suite, execute the following command,

```bash
$ brownie test
```
Alternatively, you can run a specific test module by specifying the path,

Note! This project uses `mainnet-fork` by default.

Learn more about Brownie [tests](https://eth-brownie.readthedocs.io/en/stable/tests-pytest-intro.html).
