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


def check_websocket_object_presence(sockobjc):
    if sockobjc in USERLIST.keys():
        return True
    else:
        return False


async def old_username_userlist_and_roomlist_removal(sockobjc):
    if sockobjc in USERLIST:
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


async def new_username_presence_check_and_identification(sockobjc, mesgdict):
    for indx in USERLIST.keys():
        if USERLIST[indx]["username"] == mesgdict["userinfo"]["username"]:
            psntmesg = {
                "operands": "CHEKFAIL",
                "userinfo": mesgdict["userinfo"]
            }
            await sockobjc.send(json.dumps(psntmesg))
            await sockobjc.close()
            WAITAREA.remove(sockobjc)
        else:
            USERLIST[sockobjc] = mesgdict["userinfo"]
            psntmesg = {
                "operands": "CHEKPASS",
                "userinfo": mesgdict["userinfo"],
                "userlist": USERLIST,
                "roomlist": ROOMLIST,
            }
            await sockobjc.send(json.dumps(psntmesg))
            nwusrnot = {
                "operands": "WLCMUSER",
                "username": mesgdict["userinfo"]["username"],
                "userlist": USERLIST
            }
            for indxobjc in USERLIST.keys():
                if indxobjc != sockobjc:
                    await indxobjc.send(json.dumps(nwusrnot));


'''
async def chatroom(sockobjc, path):
    try:
        if sockobjc not in USERLIST.keys():
            WAITAREA.append(sockobjc)
        elif sockobjc in WAITAREA:
            async for mesgjson in sockobjc:
                mesgdict = json.loads(mesgjson)
                if mesgdict["operands"] == "IDENTIFY":
                    await new_username_presence_check_and_identification(sockobjc, mesgdict)
    finally:
        await old_username_userlist_and_roomlist_removal(sockobjc)
'''

async def chatroom(websocket, path):
    await register(websocket)
    try:
        async for message in websocket:
            data = json.loads(message)
            print(data)
            await websocket.send("Hello");
            #print(" > [" + str(time.ctime()) + "] [" + str(data["roomiden"]) + "] User '" + str(data["username"]) + "' sends message '" + str(data["textmesg"]) + "'")
            #await notify_mesej(data["username"], data["roomiden"], data["textmesg"])
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
