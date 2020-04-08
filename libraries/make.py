import hashlib, time, sqlite3
from libraries.conf import baseloca

def execqury(qurytext):
    location = baseloca["roomlist"]["loca"]
    print(location)
    database = sqlite3.connect(location)
    acticurs = database.cursor()
    acticurs.execute(qurytext)
    database.commit()
    database.close()

def makehash(password):
    password = str(password)
    passbyte = password.encode("utf-8")
    passhash = hashlib.sha512(passbyte)
    hexatext = passhash.hexdigest()
    return hexatext

def bildrcrd(roomname, ownrname, password):
    strttime = time.time()
    stoptime = time.time() + 3600
    recgtion = str(ownrname) + "@" + str(roomname) + "-" + str(strttime)
    passhash = makehash(password)
    identity = makehash(recgtion)
    qurytext = "insert into roomlist values ('" + str(identity) + "', '" + str(passhash) + "', " + \
                                            "'" + str(roomname) + "', '" + str(ownrname) + "', " + \
                                            "'" + str(strttime) + "', '" + str(stoptime) + "') "
    execqury(qurytext)
    dictinfo = {
        "distinct": {
            "identity": str(identity),
            "passhash": str(passhash),
        },
        "basedata": {
            "roomname": str(roomname),
            "ownrname": str(ownrname),
        },
        "duration": {
            "totaperd": str(stoptime - strttime),
            "timezone": str(time.tzname[0]),
            "strttime": {
                "hour": time.localtime(strttime).tm_hour,
                "mins": time.localtime(strttime).tm_min,
                "secs": time.localtime(strttime).tm_sec,
            },
            "stoptime": {
                "hour": time.localtime(stoptime).tm_hour,
                "mins": time.localtime(stoptime).tm_min,
                "secs": time.localtime(stoptime).tm_sec,
            },
        },
    }
    return dictinfo

def generate(makedict):
    mkrmname = makedict["mkrmname"]
    mkrmownr = makedict["mkrmownr"]
    mkrmpass = makedict["mkrmpass"]
    dictinfo = bildrcrd(mkrmname, mkrmownr, mkrmpass)
    return dictinfo