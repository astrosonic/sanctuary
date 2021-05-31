from flask import Flask, render_template


servchat = Flask(__name__)


@servchat.route("/")
def chatroom():
    return render_template("chatroom.html", chatport=chatp0rt)


def chrumnow(netpdata, servport):
    servchat.run(host=netpdata, port=servport)


def mainfunc(servport, chatport, netprotc, ip_address):
    global chatp0rt
    chatp0rt = chatport
    print(" * Starting Sanctuary...")
    if servport == chatport:
        print(" * [FAILMESG] The port values for Chatroom server and WebSocket server cannot be the same!")
    else:
        print(" * Chatroom server started on port " + str(servport) + ".")
        print(" * WebSocket server started on port " + str(chatport) + ".")
        netpdata = ""
        if netprotc == "ipprotv6":
            print(" * IP version  : 6")
            netpdata = "::"
            if ip_address is not None:
                netpdata = ip_address
        elif netprotc == "ipprotv4":
            print(" * IP version  : 4")
            netpdata = "0.0.0.0"
            if ip_address is not None:
                netpdata = ip_address
        chrumnow(netpdata, servport)
