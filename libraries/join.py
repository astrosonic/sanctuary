import hashlib, time, sqlite3
from libraries.conf import baseloca

def makehash(password):
    password = str(password)
    passbyte = password.encode("utf-8")
    passhash = hashlib.sha512(passbyte)
    hexatext = passhash.hexdigest()
    return hexatext

def fetcqury(qurytext):
    location = baseloca["roomlist"]["loca"]
    database = sqlite3.connect(location)
    acticurs = database.cursor()
    fetcdata = acticurs.execute(qurytext)
    fetcdata = fetcdata.fetchone()
    database.close()
    return fetcdata

def roomexst(jnrmlink):
    qurytext = "select * from roomlist where iden = '" + str(jnrmlink) + "'"
    roomdata = fetcqury(qurytext)
    if roomdata is None:
        return False
    else:
        return True

def timevald(jnrmlink):
    if roomexst(jnrmlink) is True:
        qurytext = "select strt, stop from roomlist where iden = '" + str(jnrmlink) + "'"
        roomdata = fetcqury(qurytext)
        strttime = float(roomdata[0])
        stoptime = float(roomdata[1])
        curttime = time.time()
        if curttime > strttime and curttime < stoptime:
            return True
        else:
            return False
    else:
        return False

def passchek(jnrmlink, jnrmpass):
    if timevald(jnrmlink) is True:
        hexapass = makehash(jnrmpass)
        qurytext = "select keys from roomlist where iden = '" + str(jnrmlink) + "'"
        roomdata = fetcqury(qurytext)
        password = roomdata[0]
        if hexapass == password:
            return True
        else:
            return False
    else:
        return False

def bildrcrd(roomlink):
    qurytext = "select * from roomlist where iden = '" + str(roomlink) + "'"
    roomdata = fetcqury(qurytext)
    dictinfo = {
        "distinct": {
            "identity": str(roomdata[0]),
            "passhash": str(roomdata[1]),
        },
        "basedata": {
            "roomname": str(roomdata[2]),
            "ownrname": str(roomdata[3]),
        },
        "duration": {
            "totaperd": str(float(roomdata[5]) - float(roomdata[4])),
            "timezone": str(time.tzname[0]),
            "strttime": {
                "hour": time.localtime(float(roomdata[4])).tm_hour,
                "mins": time.localtime(float(roomdata[4])).tm_min,
                "secs": time.localtime(float(roomdata[4])).tm_sec,
            },
            "stoptime": {
                "hour": time.localtime(float(roomdata[5])).tm_hour,
                "mins": time.localtime(float(roomdata[5])).tm_min,
                "secs": time.localtime(float(roomdata[5])).tm_sec,
            },
        },
    }
    return dictinfo

def generate(jnrmlink):
    dictinfo = bildrcrd(jnrmlink)
    return dictinfo