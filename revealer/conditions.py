from nucypher.policy.conditions.lingo import Lingo

is_material_released_condition: Lingo = {
        "version": "1.0.0",
        "condition": {
            "conditionType": "contract",
            "contractAddress": "0x96ebdf35199219BDd16E3c3E1aD8C89C9185b734",  # contract with initialWindow
            "functionAbi": {
                "inputs": [],
                "name": "isKeySet",
                "outputs": [{"internalType": "bool", "name": "", "type": "bool"}],
                "stateMutability": "view",
                "type": "function",
            },  # type: ignore
            "method": "isKeySet",
            "chain": 5,
            "returnValueTest": {"comparator": "==", "value": True},
        },
    }