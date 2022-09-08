from utils.config import STETH


def is_steth(chain_id, address):
    return address == STETH[chain_id][0]
