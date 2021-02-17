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

async function RegisterPersonOnDispatch () {
    let dspchuri = $("#dspchuri").val()
    let username = $("#usertext").val();
    connobjc = new SocketConnection(dspchuri, username);
    await new Promise(r => setTimeout(r, 100));
    connobjc.identify_username_in_dispatch_service();
    $("#restwarn").modal("hide");
    await connobjc.keep_listening_to_the_server();
}

async function attempt_identification_to_dispatch_service () {
    let username = document.getElementById("username").value;
    let cleantxt = DOMPurify.sanitize(username, {USE_PROFILES: {html: false}}).trim();
    if (cleantxt.match(/^[A-Z0-9]{1,15}$/i)) {
        sessionStorage.setItem("username", cleantxt);
        sessionStorage.setItem("chatroom", "--------");
        let timestmp = new Date;
        let idencode = JSON.stringify({
            "username": cleantxt,
            "jointime": timestmp.toString(),
            "operands": "IDENTIFY"
        });
        await sockobjc.send(idencode);
        document.getElementById("headuser").innerText = cleantxt;
        dataload.hide();
    } else {
        console.log("Invalid username entered");
        invluser.show();
    }
}

function randgene() {
    let randstrg = "";
    let lent = 8; let list = "0123456789ABCDEF";
    for (let indx = lent; indx > 0; indx--) {
        randstrg += list[Math.floor(Math.random() * list.length)];
    }
    return randstrg;
}

function loadexec () {
    timeqant();
    dataload.show();
    sessionStorage.clear();
    sessionStorage.setItem("greplyto", "--------");
    document.getElementById("mesgtext").value = "";
}

function print_help_message() {
    let srceuser = "SANCTUARY";
    $("#mesglist").append(
        `
        <a class="list-group-item list-group-item-action" id="${mesgiden}" onclick="greplyto('${mesgiden}')">
            <div style="margin-bottom: 1%;">
                <span class="float-none">
                    <strong class="jtbn-bold">${srceuser}</strong>
                </span>
                <span class="float-end">
                    <code class="jtbn-rlar">${localstr}</code>&nbsp;
                    <div class="badge jtbn-rlar pill-bord">${mesgiden}</div>
                </span>
            </div>
            <p class="jtbn-rlar small" style="margin: 0%;">
                <dl class="row small">
                    <dt class="col-sm-5 jtbn-bold">/join [chatroom] [password]</dt>
                    <dd class="col-sm-7 jtbn-rlar">Join an existing chatroom with their name and password</dd>
                    <dt class="col-sm-5 jtbn-bold">/make [chatroom] [password]</dt>
                    <dd class="col-sm-7 jtbn-rlar">Create a new chatroom and set its password</dd>
                    <dt class="col-sm-5 jtbn-bold">/exit</dt>
                    <dd class="col-sm-7 jtbn-rlar">Leave the chatroom you are in now</dd>
                    <dt class="col-sm-5 jtbn-bold">/lsus</dt>
                    <dd class="col-sm-7 jtbn-rlar">Show the list of users in your current chatroom</dd>
                    <dt class="col-sm-5 jtbn-bold">/lsal</dt>
                    <dd class="col-sm-7 jtbn-rlar">Show the list of users connected to the Dispatch instance</dd>
                    <dt class="col-sm-5 jtbn-bold">/lsrm</dt>
                    <dd class="col-sm-7 jtbn-rlar">Show the list of chatrooms active in the Dispatch instance</dd>
                    <dt class="col-sm-5 jtbn-bold">/save</dt>
                    <dd class="col-sm-7 jtbn-rlar">Save your current connection profile to a file</dd>
                    <dt class="col-sm-5 jtbn-bold">/wipe</dt>
                    <dd class="col-sm-7 jtbn-rlar">Clear the screen buffer of all the messages</dd>
                    <dt class="col-sm-5 jtbn-bold">/ownr</dt>
                    <dd class="col-sm-7 jtbn-rlar">Fetch the owner name of your current chatroom</dd>
                    <dt class="col-sm-5 jtbn-bold">/stop</dt>
                    <dd class="col-sm-7 jtbn-rlar">Shut down the chatroom and remove all users</dd>
                    <dt class="col-sm-5 jtbn-bold">/purr [username] [mesgtext]</dt>
                    <dd class="col-sm-7 jtbn-rlar">Whisper messages to a specific user in the chatroom</dd>
                    <dt class="col-sm-5 jtbn-bold">/anon [username] [mesgtext]</dt>
                    <dd class="col-sm-7 jtbn-rlar">Anonymously dispatch messages to a specific user</dd>
                    <dt class="col-sm-5 jtbn-bold">/cont</dt>
                    <dd class="col-sm-7 jtbn-rlar">Know more about the folks we are thankful to</dd>
                    <dt class="col-sm-5 jtbn-bold">/help</dt>
                    <dd class="col-sm-7 jtbn-rlar">Show help and support topics</dd>
                </dl>
            </p>
        </a>
        `
    );
    document.getElementById("mesgtext").value = "";
}

function sendmesg() {
    if (sockobjc.readyState === 3) {
        sockfail.show();
    } else {
        let mesgtext = document.getElementById("mesgtext").value;
        let cleantxt = DOMPurify.sanitize(mesgtext, {USE_PROFILES: {html: false}}).trim();
        let mesgiden = randgene();
        let curtdate = new Date;
        let localstr = curtdate.toLocaleTimeString();
        if (cleantxt !== "") {
            if (cleantxt === "/help") {
                print_help_message();
            } else if (cleantxt.split(" ")[0] === "/make") {
                if (cleantxt.split(" ").length === 3) {
                    let roomname = cleantxt.split(" ")[1];
                    let password = cleantxt.split(" ")[2];
                    let makeroom = JSON.stringify({
                        "username": sessionStorage.getItem("username"),
                        "roomname": roomname,
                        "password": password,
                        "operands": "MAKEROOM"
                    });
                    sockobjc.send(makeroom);
                } else {
                    $("#mesglist").append(
                        `
                        <a class="list-group-item list-group-item-action" id="${mesgiden}" onclick="greplyto('${mesgiden}')">
                            <div style="margin-bottom: 1%;">
                                <span class="float-none">
                                    <strong class="jtbn-bold">${srceuser}</strong>
                                </span>
                                <span class="float-end">
                                    <code class="jtbn-rlar">${localstr}</code>&nbsp;
                                    <div class="badge jtbn-rlar pill-bord">${mesgiden}</div>
                                </span>
                            </div>
                            <p class="jtbn-rlar small" style="margin: 0%;">
                                Please correct the syntax for creating a chatroom and try again.
                            </p>
                        </a>
                        `
                    );
                    convfail.show();
                    document.getElementById("mesgtext").value = "";
                }
            } else {
                if (sessionStorage.getItem("chatroom") === "--------") {
                    let srceuser = "SANCTUARY";
                    $("#mesglist").append(
                        `
                        <a class="list-group-item list-group-item-action" id="${mesgiden}" onclick="greplyto('${mesgiden}')">
                            <div style="margin-bottom: 1%;">
                                <span class="float-none">
                                    <strong class="jtbn-bold">${srceuser}</strong>
                                </span>
                                <span class="float-end">
                                    <code class="jtbn-rlar">${localstr}</code>&nbsp;
                                    <div class="badge jtbn-rlar pill-bord">${mesgiden}</div>
                                </span>
                            </div>
                            <p class="jtbn-rlar small" style="margin: 0%;">
                                You have not yet joined in any chatroom.
                            </p>
                        </a>
                        `
                    );
                    convfail.show();
                    document.getElementById("mesgtext").value = "";
                } else {
                    let srceuser = sessionStorage.getItem("username");
                    let sencode = JSON.stringify({
                        "operands": "CONVEYMG",
                        "mesgtext": cleantxt,
                        "localstr": curtdate.toString(),
                        "chatroom": sessionStorage.getItem("chatroom"),
                        "srceuser": srceuser
                    });
                    sockobjc.send(cleantxt);
                    $("#mesglist").append(
                        `
                        <a class="list-group-item list-group-item-action" id="${mesgiden}" onclick="greplyto('${mesgiden}')">
                            <div style="margin-bottom: 1%;">
                                <span class="float-none">
                                    <strong class="jtbn-bold">${srceuser}</strong>
                                </span>
                                <span class="float-end">
                                    <code class="jtbn-rlar">${localstr}</code>&nbsp;
                                    <div class="badge jtbn-rlar pill-bord">${mesgiden}</div>
                                </span>
                            </div>
                            <p class="jtbn-rlar small" style="margin: 0%;">${cleantxt}</p>
                        </a>
                        `
                    );
                    document.getElementById("mesgtext").value = "";
                }
            }
        } else {
            console.log("Empty messages are not allowed");
            document.getElementById("mesgtext").value = "";
        }
    }
}

function greplyto (mesgiden) {
    if (sessionStorage.getItem("greplyto") !== mesgiden) {
        document.getElementById("mesgtext").setAttribute("placeholder", "Replying to " + mesgiden);
        sessionStorage.setItem("greplyto", mesgiden);
    } else {
        document.getElementById("mesgtext").setAttribute("placeholder", "Enter your message here");
        sessionStorage.setItem("greplyto", "--------");
    }
}
