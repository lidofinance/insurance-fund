from brownie import network
from utils.config import STETH


def is_steth(chain_id, address):
    return address == STETH[chain_id][0]


def is_development() -> bool:
    dev_networks = [
        "development",
        "hardhat",
        "hardhat-fork",
        "mainnet-fork",
        "goerli-fork",
    ]
    return network.show_active() in dev_networks
