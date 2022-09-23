import sys
import math
import brownie
import eth_utils

from utils.env import check_env_var
import utils.log as log
import utils.config as config


def main():
    if "fork" not in brownie.network.show_active():
        log.error("Active network is not a fork!")
        sys.exit()

    INSURANCE_FUND = check_env_var("INSURANCE_FUND")
    INSURANCE_WSTETH = check_env_var("INSURANCE_WSTETH")

    log.info("Initializing Insurance Fund...")
    insurance_fund = brownie.interface.InsuranceFund(INSURANCE_FUND)
    log.okay("Insurance Fund", insurance_fund.address)
    log.proceed()

    log.info("Taking over owner account...")
    owner = brownie.accounts.at(insurance_fund.owner(), True)
    log.okay("Owner", owner.address)
    log.proceed()

    log.info("Initializing stETH contract...")
    steth = brownie.interface.stETH(config.STETH[brownie.network.chain.id][0])
    log.okay("stETH", steth.address)
    log.proceed()

    log.info(
        f"Transferring {INSURANCE_WSTETH} wstETH to the fund using `transferShares`..."
    )
    shares_to_transfer = float(INSURANCE_WSTETH) * 10 ** steth.decimals()
    sender_shares = steth.sharesOf(owner.address)
    recipient_shares = steth.sharesOf(insurance_fund.address)
    log.info("Sender", owner.address)
    log.info("Sender shares", sender_shares)
    log.info("Recipient", insurance_fund.address)
    log.info("Recipient shares", recipient_shares)
    log.info("Shares to transfer", shares_to_transfer)
    log.proceed()

    steth.transferShares(insurance_fund.address, shares_to_transfer, {"from": owner})
    assert steth.sharesOf(owner.address) == sender_shares - shares_to_transfer
    assert (
        steth.sharesOf(insurance_fund.address) == recipient_shares + shares_to_transfer
    )
    log.okay("Transfer succesful!")
    log.info("Sender shares", steth.sharesOf(owner.address))
    log.info("Recipient shares", steth.sharesOf(insurance_fund.address))
    log.proceed()

    log.info(f"Recovering all stETH back from the fund...")
    steth_amount = steth.balanceOf(insurance_fund.address)
    recipient_balance = steth.balanceOf(owner.address)
    log.info("Method", "transferERC20")
    log.info("Recipient", owner.address)
    log.info("StETH to recover", steth_amount)
    log.proceed()

    insurance_fund.transferERC20(
        steth.address, owner.address, steth_amount, {"from": owner}
    )
    assert math.isclose(
        steth.balanceOf(owner.address),
        recipient_balance + steth_amount,
        abs_tol=config.STETH_ERROR_MARGIN,
    )

    log.okay("Recover successful!")
    log.info("Insurance Fund shares", steth.sharesOf(insurance_fund.address))
    log.info("Recipient shares", steth.sharesOf(owner.address))

    log.okay("Check successful!")
