AGENT = {
    1: "0x3e40D73EB977Dc6a537aF587D48316feE66E9C8c",
    5: "0x4333218072D5d7008546737786663c38B4D561A4",
}

STETH = {
    1: (
        "0xae7ab96520DE3A18E5e111B5EaAb095312D7fE84",  # token
        "0x1982b2F5814301d4e9a8b0201555376e62F82428",  # holder
    ),
    5: (
        "0x1643E812aE58766192Cf7D2Cf9567dF2C37e9B7F",  # token
        "0x1c5AbE736C6CCb743Bc933241AB462e6b38c6EA4",  # holder
    ),
}

WSTETH = {
    1: (
        "0x7f39C581F595B53c5cb19bD0b3f8dA6c935E2Ca0",  # token
        "0x248ccbf4864221fc0e840f29bb042ad5bfc89b5c",  # holder
    ),
    5: (
        "0x6320cD32aA674d2898A68ec82e869385Fc5f7E2f",  # token
        "0xf890982f9310df57d00f659cf4fd87e65aded8d7",  # holder
    ),
}

LDO = {
    1: (
        "0x5A98FcBEA516Cf06857215779Fd812CA3beF1B32",  # token
        "0x09f82ccd6bae2aebe46ba7dd2cf08d87355ac430",  # holder
    ),
    5: (
        "0x56340274fB5a72af1A3C6609061c451De7961Bd4",  # token
        "0xa5f1d7d49f581136cf6e58b32cbe9a2039c48ba1",  # holder
    ),
}

TETHER = {
    1: (
        "0xdAC17F958D2ee523a2206206994597C13D831ec7",  # token
        "0x5041ed759Dd4aFc3a72b8192C143F72f4724081A",  # holder
    ),
    5: (
        "0x509Ee0d083DdF8AC028f2a56731412edD63223B9",  # token
        "0x2F62CEACb04eAbF8Fc53C195C5916DDDfa4BED02",  # holder
    ),
}

DAI = {
    1: (
        "0x6B175474E89094C44Da98b954EedeAC495271d0F",  # token
        "0x5777d92f208679DB4b9778590Fa3CAB3aC9e2168",  # holder
    ),
    5: (
        "0x11fE4B6AE13d2a6055C8D9cF65c55bac32B5d844",  # token
        "0x5dcdbd3ccf9b09eaad03bc5f50fa2b3d3aca0121",  # holder
    ),
}

ERC20_TOKENS = [STETH, WSTETH, LDO, TETHER, DAI]

STETH_ERROR_MARGIN = 2