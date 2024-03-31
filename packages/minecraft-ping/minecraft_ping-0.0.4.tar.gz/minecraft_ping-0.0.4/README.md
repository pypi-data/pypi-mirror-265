# Minecraft Ping

- Pings asynchronously Minecraft servers
- Only gets their Online/Offline boolean
- Useful to ping a huge list of ips to test for running MC servers.

# Sample code / Quickstart

```python
import asyncio

from minecraft_ping import MinecraftPing


async def callback(addr: str, port: int, is_online: bool) -> None:
    # Here handle the server, put it in a json file or anything else.
    print(addr, port, is_online)


async def main() -> None:
    mc_ping: MinecraftPing = MinecraftPing(
        timeout=5,
        callback=callback
    )

    is_online: bool = await mc_ping.get_state('mc.hypixel.net', 25565)
    print(f'The server is {"online" if is_online else "offline"}.')

    servers: set[tuple[str, int]] = {
        ('mc.hypixel.net', 25565),
        ('hub.opblocks.com', 25565),
        ('valheim_is_a_great_game', 123)
    }

    # Here for every server, the callback function will be called.
    await mc_ping.get_state_bulk(servers)

    # If no callback function is provided, default is to write a file with all the online servers.

    # You can modify the default callback output filepath with the `callback_filepath_out`
    # when instantiating MinecraftPing.


if __name__ == '__main__':
    asyncio.run(main())
```