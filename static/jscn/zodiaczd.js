class SocketConnection {
    constructor (sockaddr, username) {
        this.sockaddr = sockaddr;
        this.username = username;
        this.sockobjc = new WebSocket(sockaddr);
    }

    identify_username_in_dispatch_service () {
        sessionStorage.setItem("dspchuri", this.sockaddr);
        sessionStorage.setItem("username", this.username);
        let userinfo = {
            "username": this.username,
            "conntime": Date(),
            "fullname": "",
            "descdata": "",
        }
        let comdtext = {
            "operands": "IDENTIFY",
            "userinfo": userinfo
        }
        console.log(this.sockobjc);
        this.sockobjc.send(JSON.stringify(comdtext));
    }

    async keep_listening_to_the_server () {
        this.sockobjc.onmessage = function (event) {
            let dataobjc = JSON.parse(event.data);
            console.log(dataobjc);
            if (dataobjc["operands"] === "CHEKFAIL") {
                $("#dupluser").modal("setting", "closable", false).modal("show");
            } else if (dataobjc["operands"] === "CHEKFAIL") {
                $("#userttle").text(dataobjc["userinfo"]["username"]);
            }
        }
    }
}

//let connobjc = new SocketConnection("ws://localhost:8080/", "username");

let connobjc = 0;

function chektime (chekqant) {
    if (chekqant < 10)
        return "0" + chekqant;
    else
        return chekqant;
}

function timeqant () {
    let curtdate = new Date();
    let hour = curtdate.getHours(); let mint = curtdate.getMinutes(); let secs = curtdate.getSeconds();
    hour = chektime(hour); mint = chektime(mint); secs = chektime(secs);
    $("#timehead").text(hour + ":" + mint + ":" + secs);
    let time = setTimeout(timeqant, 500);
}

function SwitchTabActiveState (head) {
    let sectlist = {
        "wlcm-ttle": "wlcm-body",
        "chrm-ttle": "chrm-body",
        "user-ttle": "user-body",
        "make-ttle": "make-body",
    };
    for (indx in sectlist) {
        if (indx !== head) {
            $("#" + indx).removeClass("active");
            $("#" + sectlist[indx]).removeClass("active");
        }
    }
    $("#" + head).addClass("active");
    $("#" + sectlist[head]).addClass("active");
}

function OnLoadExecutables () {
    timeqant();
    sessionStorage.clear();
    $("#restwarn").modal("setting", "closable", false).modal("show");
}

async function RegisterPersonOnDispatch () {
    let dspchuri = $("#dspchuri").val()
    let username = $("#usertext").val();
    connobjc = new SocketConnection(dspchuri, username);
    await new Promise(r => setTimeout(r, 100));
    connobjc.identify_username_in_dispatch_service();
    $("#restwarn").modal("hide");
    await connobjc.keep_listening_to_the_server();
}