from nucypher.blockchain.eth.registry import InMemoryContractRegistry
from nucypher.characters.lawful import Bob

staking_provider_uri = "https://goerli.infura.io/v3/a11313ddcf61443898b6a47e952d255c"
network = "lynx"
coordinator_provider_uri = "https://polygon-mumbai.infura.io/v3/a11313ddcf61443898b6a47e952d255c"
coordinator_network = "mumbai"

bob = Bob(
    eth_provider_uri=staking_provider_uri,
    domain=network,
    coordinator_provider_uri=coordinator_provider_uri,
    coordinator_network=coordinator_network,
    registry=InMemoryContractRegistry.from_latest_publication(network=network),
)
