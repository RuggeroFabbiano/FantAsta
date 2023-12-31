// INITIALISATION
const host = window.location.host;
const protocol = host.startsWith("localhost")? "ws" : "wss";
const socket = new WebSocket(protocol + "://" + host + "/ws" + "{{request.path}}");

var participantList, phase, caller, role, player, callTimeout, bidTimeout;
var slots = {"P": 3, "D": 8, "C": 8, "A": 6}


// ACTIONS (SEND MESSAGES)

/**
 * Toggle auction activation/pause
 * @param {Object} element the start/stop button 
 */
function startStop(element) {
    if ($(element).text() == "Avvia") {
        send({"event": "start_auction"});
        $(element).text("Arresta");
    } else {
        send({"event": "stop_auction"});
        $(element).text("Avvia");
    }
}

/**
 * Call next player and start bids
 */
function selectPlayer() {
    const playerID = $("#player-selector").val();
    if (playerID) {
        clearInterval(callTimeout);
        send({"event": "start_bid", "player": playerID});
    }
}

/**
 * Raise bid by fixed value
 * @param {Number} value the bid raise value
 */
function raiseBid(value) {
    const currentBid = parseInt($("#best-bid").text());
    makeBid(currentBid + value);
}

/**
 * Double current bid
 */
function doubleBid() {
    const currentBid = parseInt($("#best-bid").text());
    makeBid(currentBid*2);
}

/**
 * Make new bid of custom value
 * @param {Number} value the bid value
 */
function customBid(value) {
    const currentBid = parseInt($("#best-bid").text());
    const money = parseInt($("#current-money").text());
    const missing = $(".empty").length;
    if (!isNaN(value) && value > currentBid && money-value >= missing-1) {makeBid(value);}
}

/**
 * Assign player to club manually
 */
function assign() {send({"event": "assign"});}


// REACTIONS (RECEIVE MESSAGES)

// Get messages and dispatch them to correct action
socket.onmessage = function(event) {
    const payload = JSON.parse(event.data);
    switch (payload.event) {
        case "join":
            // New participants: initialise
            if (!phase) {phase = "awaiting participants";}
            setParticipants(payload.participants);
            // Detected late joiner after auction started: share global values for synchronisation
            if ("{{user.club}}" === caller) {
                const bidder = $("#bidder").text();
                const label = $("#current-bid").attr("class");
                const amount = parseInt($("#best-bid").text());
                send({
                    "event": "late_join",
                    "club": payload.enter,
                    "phase": phase,
                    "participants": participantList,
                    "caller": caller,
                    "role": role,
                    "player": player,
                    "bidder": bidder,
                    "label": label,
                    "amount": amount
                });
            }
            break;
        case "synchronise":
            if ("{{user.club}}" === payload.club) {
                phase = payload.phase;
                participantList = payload.participants;
                showAuctionDashboard();
                if (phase === "awaiting choice") {
                    caller = payload.caller;
                    role = payload.role;
                    setPlayerChoice(payload.caller, payload.role);
                    stopBids();
                    $("#current-bid-cover").show();
                } else {
                    player = payload.player;
                    showPlayerInfo(payload);
                    startBids(payload);
                    // `updateBid` expects the bidder club being named `club`, but since this
                    // payload contains data for both init. and bid "catch-up", it has been
                    // named `bidder` to not override `club` holding current turn
                    payload.club = payload.bidder;
                    updateBid(payload);
                }
            }
            break;
        case "start_auction":
            if (phase !== "stopped") {showAuctionDashboard();}
            // not breaking here since we also wanna execute first round when starting
        case "continue":
            phase = "awaiting choice";
            stopBids();
            if ("{{user.club}}" === payload.buyer) {addPlayer(payload);}
            caller = payload.club;
            role = payload.role;
            setPlayerChoice(payload.club, payload.role);
            if ("{{user.club}}" === payload.club) {startCountDown("call");}
            break;
        case "start_bid":
            phase = "bids";
            player = payload.id;
            showPlayerInfo(payload);
            startBids(payload);
            // not breaking here since we also wanna execute first round when starting
        case "new_bid":
            clearInterval(bidTimeout);
            updateBid(payload);
            startCountDown("bid");
            break;
        case "stop_auction":
            phase = "stopped";
            stopAuction();
            break;
        case "leave":
            setParticipants(payload.participants);
            break;
        default:
            console.log(payload);
    }
};

/**
 * Show participants in waiting room
 * @param {String} participants connected users
 */
function setParticipants(participants) {
    participantList = participants;
    $("#participants > p").each(function() {
        if (participants.includes($(this).attr("class"))) {$(this).show();}
        else {$(this).hide();}
    });
}

/**
 * Show auctions dashboard on auction start
 */
function showAuctionDashboard() {
    $("#page-container").css("background-color", "white");
    $("#participants").hide();
    $("#auction-dashboard").show();
    $.get("{% url 'players-club' %}").done(function(data) {
        for (let player of data) {
            slots[player.role]--;
            var row = $(`#${player.role}`).children(".empty").first();
            row.html(`
                <td>${player.name}</td>
                <td>${player.team}</td>
                <td>${player.price}</td>
            `);
            row.removeClass("empty");
        }
    });
}

/**
 * Stop bids during player choice
 */
function stopBids() {
    clearInterval(bidTimeout);
    $(".bid-button").prop("disabled", true);
    $("#bid-countdown-container").hide();
    $("#assign").prop("disabled", true);
}

/**
 * Let user choose player for next round choice for new round
 * @param {String} club name of the club of the attending user 
 * @param {String} role letter indicating the role of players for the current round
 */
function setPlayerChoice(club, role) {
    $("#selection-result").hide();
    const fullRole = getRole(role);
    if ("{{user.club}}" === club) {
        $("#player-selector").html(`<option value="">Scegli un ${fullRole}</option>`);
        setPlayerSelector(club, role);
        $("#selection-choice").show();
        $("#selection-wait").hide();
    }
    else {
        $("#selection-wait").html(`
            <p style="margin: auto">${club} sta scegliendo un ${fullRole}...</p>
        `);
        $("#selection-choice").hide();
        $("#selection-wait").show();
    }
}

/**
 * Prepare players list for selection
 * @param {String} club name of the club of the attending user 
 * @param {String} roleIndex letter indicating the role of players for the current round
 */
function setPlayerSelector(club, roleIndex) {
    $.get("{% url 'players' role='-' %}".replace("-", roleIndex)).done(function(data) {
        for (let player of data) {
            $("#player-selector").append(`
                <option value="${player.id}">${player.name} (${player.team})</option>
            `);
        }
    });
}

/**
 * Initialise bid information after player choice
 * @param {Object} data information on selected player and club holding the current round
 */
function showPlayerInfo(data) {
    $("#selection-choice").hide();
    $("#selection-wait").hide();
    $("#player-name").text(data.name);
    $("#player-role").text(getRoleIcon(data.role));
    $("#player-team").text(data.team);
    $("#player-price").text(data.price);
    $("#selection-result").show();
}

/**
 * Start bids
 * @param {Object} data info on the calling bidder
 */
function startBids(data) {
    $("#bid-player-info").html(`
        <div>${data.name}</div>
        <div>${getRoleIcon(data.role)}</div>
        <div>${data.team}</div>
    `);
    $("#current-bid-cover").hide();
    $("#assign").prop("disabled", false);
    if (slots[data.role] > 0) {$(".bid-button").prop("disabled", false);}
    $("#bid-countdown-container").show();
}

/**
 * Update bid info with new bid
 * @param {Object} data new bid
 */
function updateBid(data) {
    const amount = data.amount || 1;
    $("#bidder").text(data.club);
    $("#best-bid").text(amount);
    $("#current-bid").removeClass();
    $("#current-bid").addClass(data.label);
    const money = parseInt($("#current-money").text());
    const needed = $(".empty").length - 1;
    if (money - (amount+10) < needed) {$("bid-10").prop("disabled", true);}
    else {$("bid-10").prop("disabled", false);}
    if (money - (amount+5) < needed) {$("bid-5").prop("disabled", true);}
    else {$("bid-5").prop("disabled", false);}
    if (money - (amount+1) < needed) {$("bid-1").prop("disabled", true);}
    else {$("bid-1").prop("disabled", false);}
    if (money - (amount*2) < needed) {$("bid-2").prop("disabled", true);}
    else {$("bid-2").prop("disabled", false);}
}

/**
 * Stop auction
 */
function stopAuction() {
    clearTimeout(callTimeout);
    clearTimeout(bidTimeout);
    $(".bid-button").prop("disabled", true);
    $("#assign").prop("disabled", true);
    $("#current-bid-cover").show();
}


// UTILITY FUNCTIONS

/**
 * Send message through the web-socket. Ensure data is not missing the `event` key.
 * @param {Object} data the raw data to be sent 
 */
function send(data) {
    if (!Object.keys(data).includes("event")) {throw new Error("Data is missing the event type");}
    const serialisedData = JSON.stringify(data);
    socket.send(serialisedData);
}

/**
 * Map role letter to role full-word
 * @param {Object} roleIndex the role letter
 */
function getRole(roleIndex) {
    switch (roleIndex) {
        case "P":
            return "portiere";
        case "D":
            return "difensore";
        case "C":
            return "centrocampista";
        case "A":
            return "attaccante";
        default:
            return null;
    }
}

/**
 * Start count-down for player choice; skip turn at expiry.
 * @param {String} action the action to be performed in the given time
 */
function startCountDown(action) {
    if (action === "call") {
        var timeLeft = 30;
        $("#choice-countdown").text(timeLeft);
        callTimeout = setInterval(function() {
            $("#choice-countdown").text(timeLeft--);
            if (timeLeft == 0) {
                clearInterval(callTimeout);
                send({"event": "continue"});
            }
        }, 1000);
    } else {
        var timeLeft = 10;
        $("#bid-countdown").text(timeLeft);
        bidTimeout = setInterval(function() {
            $("#bid-countdown").text(timeLeft--);
            if (timeLeft == 0) {
                clearInterval(bidTimeout);
                if ("{{user.is_superuser}}" === "True") {assign();}
            }
        }, 1000);
    }
}

/**
 * Return rounded letter corresponding to player role
 * @param {Object} roleIndex the role letter
 */
function getRoleIcon(roleIndex) {
    switch (roleIndex) {
        case "P":
            return "Ⓟ";
        case "D":
            return "Ⓓ";
        case "C":
            return "Ⓒ";
        case "A":
            return "Ⓐ";
        default:
            return null;
    }
}

/**
 * Send bid message
 * @param {Number} amount the bid amount
 */
function makeBid(amount) {
    send({
        "event": "new_bid",
        "club": "{{user.club}}",
        "label": "{{user.club.label}}",
        "amount": amount
    });

}

/**
 * Add player to buyer's roster
 * @param {Object} data the club and player data
 */
function addPlayer(data) {
    var row = $(`#${data.player.role}`).children(".empty").first();
    $(row).html(`
        <td>${data.player.name}</td>
        <td>${data.player.team}</td>
        <td align="right">${data.player.price}</td>
    `);
    $(row).removeClass("empty");
    $("#current-money").text(data.money);
    slots[data.player.role]--;
}

// Socket close
socket.onclose = function(e) {console.error("Web socket closed unexpectedly");}