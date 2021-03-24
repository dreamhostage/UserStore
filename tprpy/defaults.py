CONF_MAINNET = {
    "fullnode": "https://api.trongrid.io",
    "event": "https://api.trongrid.io",
}

# The long running, maintained by the tpr-us community
CONF_SHASTA = {
    "fullnode": "https://api.shasta.trongrid.io",
    "event": "https://api.shasta.trongrid.io",
    "faucet": "https://www.trongrid.io/faucet",
}

# Maintained by the official team
CONF_NILE = {
    "fullnode": "https://api.nileex.io",
    "event": "https://event.nileex.io",
    "faucet": "http://nileex.io/join/getJoinPage",
}

# Maintained by the official team
CONF_TPREX = {
    "fullnode": "https://testhttpapi.tronex.io",
    "event": "https://testapi.tronex.io",
    "faucet": "http://testnet.tronex.io/join/getJoinPage",
}

ALL = {
    "mainnet": CONF_MAINNET,
    "nile": CONF_NILE,
    "shasta": CONF_SHASTA,
    "tronex": CONF_TPREX,
}


def conf_for_name(name: str) -> dict:
    return ALL.get(name, None)
