import sys
import brownie
from utils.env import check_env_var
import utils.log as log

def main():
    DEPLOYER = check_env_var("DEPLOYER")

    try:
        deployer = brownie.accounts.load(DEPLOYER)
    except FileNotFoundError:
        log.error(f"Local account with id `{DEPLOYER}` not found!")
        sys.exit()


    OWNER  = check_env_var("OWNER")

    log.info('NETWORK', brownie.network.show_active())
    log.proceed()

    log.info("Deploying `InsuranceFund`...")
    log.proceed()

    insurance_fund = brownie.InsuranceFund.deploy(
        OWNER,
        {"from": deployer}
    )

    log.okay("`InsuranceFund` has been deployed successfully at", insurance_fund.address)


