from flask import Flask, render_template, request, session
from flask_socketio import SocketIO
from libraries.conf import erorlist
import libraries.make as make
import libraries.join as join

main = Flask(__name__)
main.config["SECRET_KEY"] = "vnkdjnfjknfl1232#"
socketio = SocketIO(main)

def makeroom(makedict):
    dictinfo = make.generate(makedict)
    distinct = dictinfo["distinct"]
    basedata = dictinfo["basedata"]
    duration = dictinfo["duration"]
    strttime = duration["strttime"]
    stoptime = duration["stoptime"]
    return render_template("makeredy.html", distinct=distinct, basedata=basedata,
                           duration=duration, strttime=strttime, stoptime=stoptime)

def joinroom(joindict):
    ftchinfo = join.generate(joindict["jnrmlink"])
    session["username"] = joindict["jnrmuser"]
    session["actiroom"] = joindict["jnrmlink"]
    distinct = ftchinfo["distinct"]
    basedata = ftchinfo["basedata"]
    duration = ftchinfo["duration"]
    strttime = duration["strttime"]
    stoptime = duration["stoptime"]
    return render_template("joinredy.html", distinct=distinct, basedata=basedata,
                           duration=duration, strttime=strttime, stoptime=stoptime,
                           curtuser=joindict["jnrmuser"])

@main.route("/",methods=["GET","POST"])
def mainmenu(erormesg=""):
    if request.method == "POST":
        if "makebutn" in request.form:
            mkrmname = request.form["mkrmname"]
            mkrmownr = request.form["mkrmownr"]
            mkrmpass = request.form["mkrmpass"]
            if mkrmname == "":
                erormesg = erorlist["mknameab"]
            elif " " in mkrmname:
                erormesg = erorlist["nospname"]
            elif mkrmownr == "":
                erormesg = erorlist["mkownrab"]
            elif " " in mkrmownr:
                erormesg = erorlist["nospownr"]
            elif mkrmpass == "":
                erormesg = erorlist["mkpassab"]
            else:
                makedict = {
                    "mkrmname": mkrmname,
                    "mkrmownr": mkrmownr,
                    "mkrmpass": mkrmpass,
                }
                return makeroom(makedict)
            return render_template("homepage.html", erormesg=erormesg)
        elif "joinbutn" in request.form:
            jnrmlink = request.form["jnrmlink"]
            jnrmuser = request.form["jnrmuser"]
            jnrmpass = request.form["jnrmpass"]
            if jnrmlink == "":
                erormesg = erorlist["jnlinkab"]
            elif jnrmuser == "":
                erormesg = erorlist["jnuserab"]
            elif " " in jnrmuser:
                erormesg = erorlist["nospuser"]
            elif jnrmpass == "":
                erormesg = erorlist["jnpassab"]
            else:
                if join.roomexst(jnrmlink) is False:
                    erormesg = erorlist["noscroom"]
                else:
                    if join.timevald(jnrmlink) is False:
                        erormesg = erorlist["expiroom"]
                    else:
                        if join.passchek(jnrmlink, jnrmpass) is False:
                            erormesg = erorlist["wrngpass"]
                        else:
                            joindict = {
                                "jnrmlink": jnrmlink,
                                "jnrmuser": jnrmuser,
                                "jnrmpass": jnrmpass,
                            }
                            print(joindict)
                            return joinroom(joindict)
                        return render_template("homepage.html", erormesg=erormesg)
                    return render_template("homepage.html", erormesg=erormesg)
                return render_template("homepage.html", erormesg=erormesg)
            return render_template("homepage.html", erormesg=erormesg)
        #return render_template("homepage.html", erormesg=erormesg)
    return render_template("homepage.html", erormesg=erormesg)

def messageReceived(methods=["GET", "POST"]):
    print("message was received!!!")

@socketio.on("my event")
def handle_my_custom_event(json, methods=["GET", "POST"]):
    print("received my event: " + str(json))
    socketio.emit("my response", json, callback=messageReceived)

if __name__ == "__main__":
    socketio.run(main, host="0.0.0.0", port=6969, debug=True)