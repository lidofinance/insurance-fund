import sys
import math
import brownie
import eth_utils

from utils.env import check_env_var
import utils.log as log
import utils.config as config

def main():
    if ("fork" not in brownie.network.show_active()):
        log.error("Active network is not a fork!")
        sys.exit()

    INSURANCE_FUND = check_env_var("INSURANCE_FUND")
    INSURANCE_WSTETH = check_env_var("INSURANCE_WSTETH")
    
    log.info("Initializing `InsuranceFund` at", INSURANCE_FUND)
    insurance_fund = brownie.interface.InsuranceFund(INSURANCE_FUND)

    owner_address = insurance_fund.owner()
    log.info("Owner", owner_address)
    log.proceed()

    log.info("Taking over owner account...")
    owner = brownie.accounts.at(owner_address, True)

    log.info("Initializing stETH...")
    steth_address = config.STETH[brownie.network.chain.id][0]
    steth = brownie.interface.stETH(steth_address)

    log.info("Initializing wstETH...")
    wsteth_address = config.WSTETH[brownie.network.chain.id][0]
    wsteth = brownie.interface.wstETH(wsteth_address)

    wsteth_amount = eth_utils.to_wei(INSURANCE_WSTETH, 'ether')
    equivalent_steth_amount = wsteth.getStETHByWstETH(wsteth_amount)
    log.info(f"{wsteth_amount} wstETH equals {equivalent_steth_amount} stETH.")
    log.proceed()

    log.info(f"Approving {equivalent_steth_amount} stETH to wstETH contract...")
    steth.approve(wsteth.address, equivalent_steth_amount, {"from": owner})

    prev_owner_balance = wsteth.balanceOf(owner.address)

    log.info("stETH balance", steth.balanceOf(owner.address))
    log.info(f"Wrapping {equivalent_steth_amount} sTETH...")
    wsteth.wrap(equivalent_steth_amount, {"from": owner})

    assert math.isclose(wsteth.balanceOf(owner.address), prev_owner_balance + wsteth_amount, abs_tol=config.STETH_ERROR_MARGIN)

    prev_fund_balance = wsteth.balanceOf(insurance_fund.address)
    corrected_wsteth_amount = wsteth.getWstETHByStETH(equivalent_steth_amount)

    log.info(f"Sending {wsteth_amount} wsTETH to the fund...")
    wsteth.transfer(insurance_fund.address, corrected_wsteth_amount, {"from": owner})

    assert math.isclose(wsteth.balanceOf(insurance_fund.address), prev_fund_balance + corrected_wsteth_amount, abs_tol=config.STETH_ERROR_MARGIN)
