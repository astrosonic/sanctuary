from flask import Flask, render_template
import click
import os, sys

#the first configuration allows us to build executables
if getattr(sys, 'frozen', False):
    base_dir = os.path.join(sys._MEIPASS)
    servchat = Flask(__name__,
        static_folder=os.path.join(base_dir, 'static'),
        template_folder=os.path.join(base_dir, 'templates'))
else:
    servchat = Flask(__name__)




@servchat.route("/")
def chatroom():
    return render_template("chatroom.html", chatport=chatp0rt)


def chrumnow(netpdata, servport):
    servchat.run(host=netpdata, port=servport)


@click.command()
@click.option("-s", "--servport", "servport", help="Set the port value for Chatroom [0-65536]", required=True)
@click.option("-c", "--chatport", "chatport", help="Set the port value for WebSockets [0-65536]", required=True)
@click.option("-6", "--ipprotv6", "netprotc", flag_value="ipprotv6", help="Start the server on an IPv6 address", required=True)
@click.option("-4", "--ipprotv4", "netprotc", flag_value="ipprotv4", help="Start the server on an IPv4 address", required=True)
@click.version_option(version="22072020", prog_name="Sanctuary Chatroom by AstroSonic")
def mainfunc(servport, chatport, netprotc):
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
        elif netprotc == "ipprotv4":
            print(" * IP version  : 4")
            netpdata = "0.0.0.0"
        chrumnow(netpdata, servport)


if __name__ == "__main__":
    mainfunc()
