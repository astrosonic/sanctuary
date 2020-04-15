from flask import Flask, render_template, request, session, redirect, url_for
from flask_socketio import SocketIO
from libraries.conf import erorlist
import libraries.make as make
import libraries.join as join
import libraries.shut as shut

main = Flask(__name__)
main.config["SECRET_KEY"] = "2190913f505d968cee4d2b6050f85b36e57ae2fdf765c9f1f9f47fbc59ab7c60a4fcf933d00760e9a6c0d1dc1b0450c1d52e4427976644ff22223445472a3add"
socketio = SocketIO(main)

@main.route("/makeroom/<roomname>/<roomlink>")
def makeroom(roomname, roomlink):
    dictinfo = make.fetcrcrd(roomlink)
    distinct = dictinfo["distinct"]
    basedata = dictinfo["basedata"]
    duration = dictinfo["duration"]
    strttime = duration["strttime"]
    stoptime = duration["stoptime"]
    return render_template("makeredy.html", distinct=distinct, basedata=basedata,
                           duration=duration, strttime=strttime, stoptime=stoptime)

@main.route("/joinroom/<username>/<roomlink>")
def joinroom(username, roomlink):
    ftchinfo = join.generate(roomlink)
    distinct = ftchinfo["distinct"]
    basedata = ftchinfo["basedata"]
    duration = ftchinfo["duration"]
    strttime = duration["strttime"]
    stoptime = duration["stoptime"]
    return render_template("joinredy.html", distinct=distinct, basedata=basedata,
                           duration=duration, strttime=strttime, stoptime=stoptime,
                           curtuser=username)

@main.route("/sesskill/")
def sesskill():
    if "username" in session:
        session.pop("username", None)
        return render_template("sesskill.html")
    else:
        return redirect(url_for("exprsess"))

@main.route("/actiroom/<roomname>/<roomlink>/", methods=["GET","POST"])
def actiroom(roomname, roomlink):
    if "username" in session:
        return render_template("actiroom.html", roomlink=roomlink,
                               roomname=roomname, curtuser=session["username"])
    else:
        return redirect(url_for("exprsess"))

@main.route("/exprsess/")
def exprsess():
    return render_template("exprsess.html")

@main.route("/shutroom/<username>/<roomlink>")
def shutroom(username, roomlink):
    dictinfo = {
        "username": username,
        "roomlink": roomlink,
    }
    shut.generate(dictinfo)
    return render_template("shutroom.html")

@main.route("/shutkick/")
def shutkick():
    if "username" in session:
        #session.pop("username", None)
        return render_template("shutkick.html")
    else:
        return redirect(url_for("exprsess"))

@main.route("/timekick/")
def timekick():
    if "username" in session:
        #session.pop("username", None)
        return render_template("timekick.html")
    else:
        return redirect(url_for("exprsess"))

@main.route("/", methods=["GET","POST"])
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
                roomlink = make.generate(makedict)
                return redirect(url_for("makeroom", roomname=mkrmname, roomlink=roomlink))
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
                        if join.shutvald(jnrmlink) is True:
                            erormesg = erorlist["roomshut"]
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
                                session["username"] = jnrmuser
                                session["actiroom"] = jnrmlink
                                return redirect(url_for("joinroom", username=jnrmuser, roomlink=jnrmlink))
                            return render_template("homepage.html", erormesg=erormesg)
                        return render_template("homepage.html", erormesg=erormesg)
                    return render_template("homepage.html", erormesg=erormesg)
                return render_template("homepage.html", erormesg=erormesg)
            return render_template("homepage.html", erormesg=erormesg)
        return render_template("homepage.html", erormesg=erormesg)
    return render_template("homepage.html", erormesg=erormesg)

def mailrecv():
    print("Message was received!!!")

@socketio.on("shutkick")
def shutkick_event():
    socketio.emit("shutkick")

@socketio.on("sendevnt")
def handle_my_custom_event(jsonobjc):
    if "username" in session:
        #print(session)
        roomlink = jsonobjc["roomlink"]
        if join.timevald(roomlink) is True:
            if join.shutvald(roomlink) is False:
                print("Received my event: " + str(jsonobjc))
                socketio.emit("response", jsonobjc, callback=mailrecv)
            else:
                return redirect(url_for("shutkick"))
        else:
            return redirect(url_for("timekick"))
    else:
        return redirect(url_for("exprsess"))

if __name__ == "__main__":
    socketio.run(main, host="0.0.0.0", port=6969, debug=True)