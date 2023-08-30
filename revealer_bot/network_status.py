import asyncio

import aiohttp


async def get_lynx_network_status(interaction):
    await interaction.response.send_message("OK!  I'll check Threshold lynx network status.")
    initial_reply = await interaction.original_response()
    thread_name = f"Network Status requested by {interaction.user.display_name} at {interaction.created_at.isoformat()[0:16]}"
    thread = await initial_reply.create_thread(name=thread_name, auto_archive_duration=60)

    # Fire off a request to the network status endpoint, along with a message to the user that info is incoming.
    async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(ssl=False)) as session:
        async with session.get(
            "https://lynx-1.nucypher.network:9151/status/?json=true"
        ) as response:
            overall_status = await response.json()

    network_name = overall_status["domain"]

    fleet_state_name = overall_status["fleet_state"]["nickname"]["text"]
    fleet_state_checksum = overall_status["fleet_state"]["checksum"]

    known_nodes = overall_status["known_nodes"]

    up_nodes = []
    down_nodes = []

    async def hit_node_status_endpoint(node):
        print(f"Hitting node status endpoint: {node['rest_url']}")
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(
                    f"https://{node['rest_url']}/status", ssl=False
                ) as response:
                    if response.status == 200:
                        up_nodes.append(node)
        except aiohttp.ClientError:
            down_nodes.append(node)

    pings = set()

    for node in known_nodes:
        status_coro = hit_node_status_endpoint(node)
        pings.add(asyncio.create_task(status_coro))

    # TODO: Ensure that thread is adhered?
    while not thread:  # Horrible.
        await asyncio.sleep(0.01)
    reply_awaitable = thread.send(
        f"Fleet state for {network_name} is:\n **{fleet_state_name}** ({fleet_state_checksum})"
    )
    pings.add(asyncio.create_task(reply_awaitable))

    for ping in pings:
        await ping  # TODO: Do something with result?

    summary = f"Found {len(up_nodes)} up nodes and {len(down_nodes)} down nodes.\n"
    if down_nodes:
        summary += "## Down Nodes:\n"
        summary += "".join(
            f"* {node['nickname']['text']} ({node['rest_url']})\n" for node in down_nodes
        )
    if up_nodes:
        summary += "----\n"
        summary += "**Up Nodes**:\n"
        summary += "".join(
            f"* {node['nickname']['text']} ({node['rest_url']})\n" for node in up_nodes
        )
    await thread.send(summary)
