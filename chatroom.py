#!/usr/bin/env python

import asyncio, json, websockets, sys


USERS = set()


def mesej_event(username, roomiden, textmesg):
    return json.dumps({"username": username, "roomiden": roomiden, "textmesg": textmesg})


async def notify_mesej(username, roomiden, textmesg):
    if USERS:
        message = mesej_event(username, roomiden, textmesg)
        await asyncio.wait([user.send(message) for user in USERS])


async def register(websocket):
    USERS.add(websocket)
    print("* [USERJOIN] A user just joined the Sanctuary!")


async def unregister(websocket):
    USERS.remove(websocket)
    dir(websocket)
    print("* [USERLEFT] A user just left the Sanctuary!")


async def counter(websocket, path):
    await register(websocket)
    try:
        async for message in websocket:
            data = json.loads(message)
            print("* " + "[" + str(data["roomiden"]) + "] '" + str(data["username"]) + "' sends '" + str(data["textmesg"]) + "'")
            await notify_mesej(data["username"], data["roomiden"], data["textmesg"])
    finally:
        await unregister(websocket)


if __name__ == "__main__":
    try:
        print("* [HOLAUSER] Sanctuary was started up on 'ws://localhost:6789/'")
        start_server = websockets.serve(counter, "localhost", 6789)
        asyncio.get_event_loop().run_until_complete(start_server)
        asyncio.get_event_loop().run_forever()
    except KeyboardInterrupt:
        print("\n" + "* [SEEUSOON] Sanctuary was shut down")
        sys.exit()
