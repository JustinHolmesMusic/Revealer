from revealer_bot.decryption_action import decrypt_attached_tmk

command_maping = [
    ("vegetables", "I like vegetables"),
    ("nft", "Once 10 ETH have been contributed the album will be relased and anyone can listen to the album."),
    ("threshold", "Threshold is an..."),
    ("contributed", "25 (variable) people have contributed"),
    ("website", "http://www.justinholmes.com/music.html"),
    ("art", "http://www.justinholmes.com/music.html"),
    ("justin", "http://www.justinholmes.com/talks.html"),
    ("decentralized",
     "The album.release is decentralized -- once the contract is enacted no one has control over when and how the album is released."),
    ("not enough", "Until 10 ETH have been contributed, the album will remain locked."),
    ("verify", "All transactions are stamped on the blockchain. Click this 'link' to view your transaction."),
    ("multiple", "Yes, everyone is welcome to contribute as many times as they like."),
    ("number", "NFT numbers will be allocated in order of the largest contribution to the smalled."),
    ("minimum",
     "There are two ways to think about contributions. Any contribution is welcome -- but ... have to be more than .1 ETH"),
    ("usd", "USD is welcomed as a contribution."),
    ("after",
     "Yes. Contributions to the artist are welomed after the album has been released. These contributions will not yeald an NFT and they will not be recorded on the album.release block chain."),
    ("3 ETH", "Once 3 ETH have been contribued, 3 songs will be release."),
    ("released", "The album is relased and open to all once 10 ETH have been contributed."),
]



async def parse_message(message):
    if "decrypt" in message.content.lower():
        message_to_look_for_attachments = message.reference.resolved
        if message_to_look_for_attachments.attachments:
            await decrypt_attached_tmk(message_to_look_for_attachments)
        # await message.reply(reply)
############################


    for question, reply in command_maping:

        if question in message.content.lower():
            await message.reply(reply)
