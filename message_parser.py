import requests
import io
import discord
from nucypher.characters.chaotic import NiceGuyEddie as _Enrico
from nucypher.characters.chaotic import ThisBobAlwaysDecrypts as Bob
from nucypher.policy.conditions.lingo import ConditionLingo
from nucypher_core import ThresholdDecryptionRequest

command_maping = [
    ("vegetables", "I like vegetables"),
    ("nft", "Once 10 ETH have been contributed the album will be relased and anyone can listen to the album."),
    ("threshold", "Threshold is an..."),
    ("contributed", "25 (variable) people have contributed"),
    ("website", "http://www.justinholmes.com/music.html"),
    ("art", "http://www.justinholmes.com/music.html"),
    ("justin", "http://www.justinholmes.com/talks.html"),
    ("decentralized", "The album.release is decentralized -- once the contract is enacted no one has control over when and how the album is released."),
    ("not enough", "Until 10 ETH have been contributed, the album will remain locked."),
    ("verify", "All transactions are stamped on the blockchain. Click this 'link' to view your transaction."),
    ("multiple", "Yes, everyone is welcome to contribute as many times as they like." ),
    ("number", "NFT numbers will be allocated in order of the largest contribution to the smalled."),
    ("minimum", "There are two ways to think about contributions. Any contribution is welcome -- but ... have to be more than .1 ETH"),
    ("usd","USD is welcomed as a contribution."),
    ("after", "Yes. Contributions to the artist are welomed after the album has been released. These contributions will not yeald an NFT and they will not be recorded on the album.release block chain."),
    ("3 ETH", "Once 3 ETH have been contribued, 3 songs will be release."),
    ("released", "The album is relased and open to all once 10 ETH have been contributed."),  
]


bob = Bob(domain="lynx", eth_provider_uri="Nowhere")

async def parse_message(message):
    if message.attachments:
        url = message.attachments[0].url
        filename = message.attachments[0].filename
        print(url)
        attachment_response = requests.get(url)
        attachment_filelike = io.BytesIO(attachment_response.content)
        attachment_df = discord.File(attachment_filelike, filename=filename)
        await message.reply("right back at you", file=attachment_df)
  
        try:
            tdr = ThresholdDecryptionRequest.from_bytes(bytes(attachment_response.content))
        except:
            await message.reply("wrong file type")
            return      
        print("--------- Threshold Decryption ---------")

        bob = Bob(
            eth_provider_uri=staking_provider_uri,
            domain=network,
            coordinator_provider_uri=coordinator_provider_uri,
            coordinator_network=coordinator_network,
            registry=InMemoryContractRegistry.from_latest_publication(network=network),
        )

        bob.start_learning_loop(now=True)

        #### Nonsense
        ritual = self.get_ritual_from_id(15)
        cohort = self.resolve_cohort(ritual=ritual, timeout=20)




        cleartext_from_ciphertext = bob.decrypt_using_existing_decryption_request(
            tdr,
            participant_public_keys=ritual.participant_public_keys,
            cohort=cohort,
            threshold=1,
        )

        print(bytes(cleartext).decode())


     
    for question, reply in command_maping:

     if question in message.content.lower():
        await message.reply(reply)
