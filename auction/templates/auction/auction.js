// INITIALISATION
const host = window.location.host;
const protocol = host.startsWith("localhost")? "ws" : "wss";
const socket = new WebSocket(protocol + "://" + host + "/ws" + "{{request.path}}");

var phase, callTimeout, bidTimeout;


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
    console.log("RECEIVE:");
    console.log(payload);
    switch (payload.event) {
        case "join":
            phase = payload.phase;
            if (phase !== "awaiting participants") { // TEMP
                setParticipants(payload.participants);
                if (payload.participants.length === payload.total) {
                    $("#start-stop").prop("disabled", false);
                } else {$("#start-stop").prop("disabled", true);}
            }
            else {showAuctionDashboard();}
            break;
        case "start_auction":
            showAuctionDashboard();
            // not breaking here since we also wanna execute first round when starting
        case "continue":
            phase = "awaiting choice";
            stopBids();
            if ("{{user.club}}" === payload.buyer) {addPlayer(payload);}
            setPlayerChoice(payload.club, payload.role);
            if ("{{user.club}}" === payload.club) {startCountDown("call");}
            break;
        case "start_bid":
            phase = "bids";
            showPlayerInfo(payload);
            startBids(payload);
            // not breaking here since we also wanna execute first round when starting
        case "new_bid":
            clearInterval(bidTimeout);
            updateBid(payload);
            startCountDown("bid");
            break;
        // case "stop_auction":
        //     stopAuction();
        //     break;
        default:
            console.log(payload.event);
            console.error("Unknown message event");
    }
};

/**
 * Show participants in waiting room
 * @param {String} participants connected users
 */
function setParticipants(participants) {
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
        console.log("Get player done");
        for (let player of data) {
            console.log(player);
            var row = $(`#${player.role}`).children(".empty").first();
            console.log(row);
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
    $(".bid-button").prop("disabled", false);
    $("#bid-countdown-container").show();
    $("#assign").prop("disabled", false);
    $("current-bid-cover").remove();
    $("bid-player-info").html(`
        <div>${data.name}</div>
        <div style="margin: 0 3rem">${getRoleIcon(data.role)}</div>
        <div>${data.team}</div>
    `);
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
// function stopAuction() {
//     waitingForCall = true;
//     clearTimeout(callTimeout);
//     clearTimeout(bidTimeout);
//     $("#auction-info").hide();
//     $("#auction-chat").hide();
//     // Make AJAX call to fetch updated teams before showing this
//     $("#teams-info").show();
// }


// UTILITY FUNCTIONS

/**
 * Send message through the web-socket. Ensure data is not missing the "event" key.
 * @param {Object} data the raw data to be sent 
 */
function send(data) {
    if (!Object.keys(data).includes("event")) {throw new Error("Data is missing the event type");}
    console.log("SEND:");
    console.log(data);
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
        var timeLeft = 20;
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
        <td>${data.player.price}</td>
    `);
    $(row).removeClass("empty");
    $("#current-money").text(data.money);
}

// Socket close
socket.onclose = function(e) {console.error("Web socket closed unexpectedly");}




// CONTROLLI
//   uno non può più rilanciare né chiamare se è pieno per quel ruolo
