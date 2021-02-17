function openside () {
    $(".ui.sidebar").sidebar("toggle");
}

function print_help_message () {
    document.getElementById("primtext").value = "";
    let mesgobjc = `
        <strong class="forelite">Sanctuary</strong><br/>
        <em class="forelite">This message is visible only to you.</em>
        <dl class="row small">
            <dt class="monofont forelite">/iden [username]</dt>
            <dd class="forelite">Connect to the Dispatch instance using an alias of your choice</dd>
            <dt class="monofont forelite">/join [chatroom] [password]</dt>
            <dd class="forelite">Join an existing chatroom with their name and password</dd>
            <dt class="monofont forelite">/make [chatroom] [password]</dt>
            <dd class="forelite">Create a new chatroom and set its password</dd>
            <dt class="monofont forelite">/exit</dt>
            <dd class="forelite">Leave the chatroom you are in now</dd>
            <dt class="monofont forelite">/lsus</dt>
            <dd class="forelite">Show the list of users in your current chatroom</dd>
            <dt class="monofont forelite">/lsal</dt>
            <dd class="forelite">Show the list of users connected to the Dispatch instance</dd>
            <dt class="monofont forelite">/lsrm</dt>
            <dd class="forelite">Show the list of chatrooms active in the Dispatch instance</dd>
            <dt class="monofont forelite">/save</dt>
            <dd class="forelite">Save your current connection profile to a file</dd>
            <dt class="monofont forelite">/wipe</dt>
            <dd class="forelite">Clear the screen buffer of all the messages</dd>
            <dt class="monofont forelite">/ownr</dt>
            <dd class="forelite">Fetch the owner name of your current chatroom</dd>
            <dt class="monofont forelite">/stop</dt>
            <dd class="forelite">Shut down the chatroom and remove all users</dd>
            <dt class="monofont forelite">/purr [username] [mesgtext]</dt>
            <dd class="forelite">Whisper messages to a specific user in the chatroom</dd>
            <dt class="monofont forelite">/anon [username] [mesgtext]</dt>
            <dd class="forelite">Anonymously dispatch messages to a specific user</dd>
            <dt class="monofont forelite">/cont</dt>
            <dd class="forelite">Know more about the folks we are thankful to</dd>
            <dt class="monofont forelite">/help</dt>
            <dd class="forelite">Show help and support topics</dd>
        </dl>
        <hr/>
    `;
    document.getElementById("mesglist").innerHTML += mesgobjc;
}

function transmit_normal_messages () {
    document.getElementById("primtext").value = "";
    let mesgobjc = "<div class='item forelite'><div class='header forelite'>You</div>" + DOMPurify.sanitize(primvalu, {USE_PROFILES: {html: false}}) + "</div><hr/>";
    document.getElementById("mesglist").innerHTML += mesgobjc;
}

function sendmesg () {
    let primvalu = DOMPurify.sanitize(document.getElementById("primtext").value, {USE_PROFILES: {html: false}}).trim();
    if (primvalu !== "") {
        if (primvalu.split()[0] === "/iden") {
            print_help_message();
        } else if (primvalu.split()[0] === "/join") {
            print_help_message();
        } else if (primvalu.split()[0] === "/make") {
            print_help_message();
        } else if (primvalu === "/exit") {
            print_help_message();
        } else if (primvalu === "/lsus") {
            print_help_message();
        } else if (primvalu === "/lsal") {
            print_help_message();
        } else if (primvalu === "/lsrm") {
            print_help_message();
        } else if (primvalu === "/save") {
            print_help_message();
        } else if (primvalu === "/wipe") {
            print_help_message();
        } else if (primvalu === "/ownr") {
            print_help_message();
        } else if (primvalu === "/stop") {
            print_help_message();
        } else if (primvalu.split()[0] === "/purr") {
            print_help_message();
        } else if (primvalu.split()[0] === "/anon") {
            print_help_message();
        } else if (primvalu === "/cont") {
            print_help_message();
        } else if (primvalu === "/help") {
            print_help_message();
        } else {
            transmit_normal_messages()
        }
    }
}

let primtext = document.getElementById("primtext");
primtext.onkeyup = function (evnt) {
    if (evnt.keyCode === 13) {
        sendmesg();
    }
}