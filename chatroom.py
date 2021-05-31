#!/usr/bin/env python

import asyncio, json, websockets, sys, time


USERS = set()


def mesej_event(username, roomiden, textmesg):
    return json.dumps({"username": username, "roomiden": roomiden, "textmesg": textmesg})


async def notify_mesej(username, roomiden, textmesg):
    if USERS:
        message = mesej_event(username, roomiden, textmesg)
        await asyncio.wait([user.send(message) for user in USERS])


async def register(websocket):
    USERS.add(websocket)
    print(" > [" + str(time.ctime()) + "] [USERJOIN] User just joined the Sanctuary")


async def unregister(websocket):
    USERS.remove(websocket)
    dir(websocket)
    print(" > [" + str(time.ctime()) + "] [USERLEFT] User just left the Sanctuary")


async def chatroom(websocket, path):
    await register(websocket)
    try:
        async for message in websocket:
            data = json.loads(message)
            print(" > [" + str(time.ctime()) + "] [" + str(data["roomiden"]) + "] User '" + str(data["username"]) + "' sends message '" + str(data["textmesg"]) + "'")
            await notify_mesej(data["username"], data["roomiden"], data["textmesg"])
    finally:
        await unregister(websocket)


def servenow(netpdata="127.0.0.1", chatport="9696"):
    try:
        print(" > [" + str(time.ctime()) + "] [HOLAUSER] Sanctuary was started up on 'ws://" + str(netpdata) + ":" + str(chatport) + "/'")
        start_server = websockets.serve(chatroom, netpdata, int(chatport))
        asyncio.get_event_loop().run_until_complete(start_server)
        asyncio.get_event_loop().run_forever()
    except KeyboardInterrupt:
        print("\n" + " > [" + str(time.ctime()) + "] [SEEUSOON] Sanctuary was shut down")
        sys.exit()


def mainfunc(chatport, netprotc, ip_address):
    print(" > [" + str(time.ctime()) + "] [HOLAUSER] Starting Sanctuary...")
    netpdata = ""
    if netprotc == "ipprotv6":
        print(" > [" + str(time.ctime()) + "] [HOLAUSER] IP version : 6")
        netpdata = "::"
        if ip_address is not None:
            netpdata = ip_address
    elif netprotc == "ipprotv4":
        print(" > [" + str(time.ctime()) + "] [HOLAUSER] IP version : 4")
        netpdata = "0.0.0.0"
        if ip_address is not None:
            netpdata = ip_address
    servenow(netpdata, chatport)
