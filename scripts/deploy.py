import sys
import json
import brownie
from utils.env import check_env_var
import utils.log as log
from utils.helpers import is_development


def main():
    DEPLOYER = check_env_var("DEPLOYER")

    try:
        deployer = brownie.accounts.load(DEPLOYER)
    except FileNotFoundError:
        log.error(f"Local account with id `{DEPLOYER}` not found!")
        sys.exit()

    ETHERSCAN_TOKEN = check_env_var("ETHERSCAN_TOKEN", display=False)

    publish_source = not is_development() and bool(ETHERSCAN_TOKEN)

    OWNER = check_env_var("OWNER")

    log.info("NETWORK", brownie.network.show_active())
    log.proceed()

    log.info("Deploying `InsuranceFund`...")
    log.proceed()

    insurance_fund = brownie.InsuranceFund.deploy(
        OWNER,
        {"from": deployer},
        publish_source=publish_source,
    )

    log.okay(
        "`InsuranceFund` has been deployed successfully at", insurance_fund.address
    )

    log.info("Creating JSON...")
    deployed_filename = f"deployed.{brownie.network.show_active()}.json"
    with open(deployed_filename, "w") as outfile:
        json.dump(
            {
                "insurance_fund": insurance_fund.address,
                "initial_owner": OWNER,
            },
            outfile,
        )

    log.okay("JSON created at", deployed_filename)
