#!/usr/bin/env python

import asyncio, json, websockets, sys, time


USERS = set()

WAITAREA = []

USERLIST = {}

ROOMLIST = {}

'''
USERLIST = {
    <websockets.server.WebSocketServerProtocol object at 0x7fd58a985580> : {
        'username': 'Hello',
        'conntime': 'Wed Dec 23 2020 13:05:56 GMT+0530 (India Standard Time)',
        'fullname': '',
        'descdata': ''
    }
}
'''

'''
ROOMLIST = {
    "DEADCAFE": {
        "roomname": "Dead Men Strategist Committee",
        "protstat": False,
        "ownrname": "t0xic0der",
        "passcode": "DEADCAFE",
        "maketime": "Wed Dec 23 2020 13:05:56 GMT+0530 (India Standard Time)",
        "partlist": [
            <websockets.server.WebSocketServerProtocol object at 0x7fd58a985580>,
            <websockets.server.WebSocketServerProtocol object at 0x7fd58a985580>
        ]
    }
'''


def mesej_event(username, roomiden, textmesg):
    return json.dumps({"username": username, "roomiden": roomiden, "textmesg": textmesg})

'''
async def notify_mesej(username, roomiden, textmesg):
    if USERS:
        message = mesej_event(username, roomiden, textmesg)
        await asyncio.wait([user.send(message) for user in USERS])
'''


async def notify_mesej(sockobjc, mesgtext):
    if USERS:
        await sockobjc.send(mesgtext)


async def register(websocket):
    USERS.add(websocket)
    print(" > [" + str(time.ctime()) + "] [USERJOIN] User just joined the Sanctuary")


async def unregister(websocket):
    USERS.remove(websocket)
    dir(websocket)
    print(" > [" + str(time.ctime()) + "] [USERLEFT] User just left the Sanctuary")


def check_websocket_object_presence(sockobjc):
    if sockobjc in USERLIST.keys():
        return True
    else:
        return False


async def old_username_userlist_and_roomlist_removal(sockobjc):
    if sockobjc in USERLIST.keys():
        leftname = USERLIST[sockobjc]["username"]
        USERLIST.pop(sockobjc)
        print(leftname + " left the Dispatch instance")
        for roomname in ROOMLIST.keys():
            if sockobjc in ROOMLIST[roomname]["partlist"]:
                print(leftname + " left the room " + roomname)
                ROOMLIST[roomname]["partlist"].remove(sockobjc)
                for partsock in ROOMLIST[roomname]["partlist"]:
                    roomltmg = {
                        "operands": "LEFTROOM",
                        "leftname": leftname,
                        "chatroom": roomname,
                    }
                    await partsock.send(json.dumps(roomltmg))
        for sockette in USERLIST:
            servltmg = {
                "operands": "LEFTSERV",
                "leftname": leftname,
            }
            await sockette.send(json.dumps(servltmg))
    elif sockobjc in WAITAREA:
        print("An unidentified user left.")
        WAITAREA.remove(sockobjc)


async def new_username_presence_check_and_identification(sockobjc, mesgdict):
    flagavbl = False
    for indx in USERLIST.keys():
        if USERLIST[indx]["username"] == mesgdict["username"]:
            print(mesgdict["username"] + " could not connect due to uniqueness failure.")
            psntmesg = {
                "operands": "CHEKFAIL",
                "userinfo": mesgdict["username"]
            }
            await sockobjc.send(json.dumps(psntmesg))
            await sockobjc.close()
            WAITAREA.remove(sockobjc)
            flagavbl = True
    if not flagavbl:
        print(mesgdict["username"] + " was successfully connected.")
        USERLIST[sockobjc] = {
            "username": mesgdict["username"],
            "jointime": mesgdict["jointime"],
            "chatroom": "--------",
        }
        psntmesg = {
            "operands": "CHEKPASS",
            "userinfo": mesgdict["username"]
        }
        await sockobjc.send(json.dumps(psntmesg))
        nwusrnot = {
            "operands": "WLCMUSER",
            "username": mesgdict["username"]
        }
        for indxobjc in USERLIST.keys():
            if indxobjc != sockobjc:
                await indxobjc.send(json.dumps(nwusrnot))


async def chatroom(sockobjc, path):
    try:
        if sockobjc not in USERLIST.keys():
            WAITAREA.append(sockobjc)
        if sockobjc in WAITAREA:
            async for mesgjson in sockobjc:
                mesgdict = json.loads(mesgjson)
                if mesgdict["operands"] == "IDENTIFY":
                    print(mesgdict)
                    await new_username_presence_check_and_identification(sockobjc, mesgdict)
    finally:
        await old_username_userlist_and_roomlist_removal(sockobjc)


def servenow(netpdata="127.0.0.1", chatport="9696"):
    try:
        print(" > [" + str(time.ctime()) + "] [HOLAUSER] Sanctuary was started up on 'ws://" + str(netpdata) + ":" + str(chatport) + "/'")
        start_server = websockets.serve(chatroom, netpdata, int(chatport))
        asyncio.get_event_loop().run_until_complete(start_server)
        asyncio.get_event_loop().run_forever()
    except KeyboardInterrupt:
        print("\n" + " > [" + str(time.ctime()) + "] [SEEUSOON] Sanctuary was shut down")
        sys.exit()


def mainfunc(chatport, netprotc):
    print(" > [" + str(time.ctime()) + "] [HOLAUSER] Starting Sanctuary...")
    netpdata = ""
    if netprotc == "ipprotv6":
        print(" > [" + str(time.ctime()) + "] [HOLAUSER] IP version : 6")
        netpdata = "::"
    elif netprotc == "ipprotv4":
        print(" > [" + str(time.ctime()) + "] [HOLAUSER] IP version : 4")
        netpdata = "0.0.0.0"
    servenow(netpdata, chatport)
