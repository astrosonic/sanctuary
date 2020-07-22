from flask import Flask, render_template

servchat = Flask(__name__)

@servchat.route("/")
def chatroom():
    return render_template("chatroom.html")

if __name__ == "__main__":
    servchat.run(host="0.0.0.0", port=6969)
