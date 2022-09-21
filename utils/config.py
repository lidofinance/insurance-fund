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

# Disclaimer to ERC721, ERC1155 tokens
# Goerli counterparts may be completely different projects
# as some Mainnet projects do not have/maintain Goerli deployments

ENS_REGISTRAR = {
    1: (
        "0x57f1887a8BF19b14fC0dF6Fd9B2acc9Af147eA85",  # token
        "0x3e40D73EB977Dc6a537aF587D48316feE66E9C8c",  # holder
        63621153800417233641014210776106383967309728151643198591333607114886514684126,  # token id
    ),
    5: (
        "0xff02b7d59975E76F67B63b20b813a9Ec0f6AbD60",  # token
        "0x3e50931b32e49fb9c4938198fd5ef4293e15b90f",  # holder
        0,  # token id
    ),
}

RARIBLE = {
    1: (
        "0x60F80121C31A0d46B5279700f9DF786054aa5eE5",  # token
        "0xedba5d56d0147aee8a227d284bcaac03b4a87ed4",  # holder
        502173,  # token id
    ),
    5: (
        "0x50b9E17D1BA03f569C534002cd7B4bAdFf88c4fC",  # token
        "0x9e3310d1610e4ecad0e6acf021c63aca130f8d5d",  # holder
        2,  # token id
    ),
}

BAYC = {
    1: (
        "0xBC4CA0EdA7647A8aB7C2061c2E118A18a936f13D",  # token
        "0x1b523dc90a79cf5ee5d095825e586e33780f7188",  # holder
        9547,  # token id
    ),
    5: (
        "0xbd4541858bdd5ccF7CfE0228C3767185ac1A4352",  # token
        "0x54e1b9ca7d5a58c3227319c1142708ec8c695e0c",  # holder
        1,  # token id
    ),
}

ERC721_TOKENS = [ENS_REGISTRAR, RARIBLE, BAYC]

MECHA = {
    1: (
        "0xf4baCB2375654Ef2459f427C8c6cF34573f75154", # token
        "0xd387a6e4e84a6c86bd90c158c6028a58cc8ac459", # holder,
        26, # token id
    )
}

ERC1155_TOKENS= [MECHA]

STETH_ERROR_MARGIN = 2
