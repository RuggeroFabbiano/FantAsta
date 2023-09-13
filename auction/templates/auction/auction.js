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
    clearInterval(callTimeout);
    const playerID = $("#player-selector").val();
    console.log(playerID);
    send({"event": "start_bid", "player": playerID});
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


// REACTIONS (RECEIVE MESSAGES)

// Get messages and dispatch them to correct action
socket.onmessage = function(event) {
    const payload = JSON.parse(event.data);
    switch (payload.event) {
        case "join":
            phase = payload.phase;
            if (phase === "awaiting participants") { // TEMP
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
            setPlayerChoice(payload.club, payload.role);
            if ("{{request.user.club}}" === payload.club) {startCountDown("call");}
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
        for (let player of data) {
            var row = $(`#${player.role}`).children(".empty").first();
            $(row).html(`
                <td>${player.name}</td>
                <td>${player.team}</td>
                <td>${player.price}</td>
            `);
            $(row).removeClass("empty");
        }
    });
}

/**
 * Let user choose player for next round choice for new round
 * @param {String} club name of the club of the attending user 
 * @param {String} role letter indicating the role of players for the current round
 */
function setPlayerChoice(club, role) {
    $("#selection-result").hide();
    const fullRole = getRole(role);
    if ("{{request.user.club}}" === club) {
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
    $("#player-role").text(data.role);
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
    $("#bid-info").css("visibility", "visible");
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
 * Buy current player and continue
 * @param {String} club name of the club buying the player
 * @param {Number} value purchase price
 */
// function buyPlayer(club, value) {
//     waitingForCall = true;
//     const bid = $("#best-bid").text(value);
//     const bidder = $("#best-bidder").text(club);
//     $("#auction-info").html(`
//         <h1>${data.player_name} comprato da ${bidder} per ${bid} <span class="currency">M</span>!</h1>
//         <p>In attesa della prossima chiamata...</p>
//     `);
//     send({"event": "buy", "club": club, "value": value});
// }

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
 * Stop bids during player choice
 */
function stopBids() {$(".bid-button").prop("disabled", true);}

/**
 * Start count-down for player choice; skip turn at expiry.
 * @param {String} action the action to be performed in the given time
 */
function startCountDown(action) {
    if (action === "call") {
        var timeLeft = 15;
        $("#choice-countdown").text(timeLeft);
        callTimeout = setInterval(function() {
            $("#choice-countdown").text(timeLeft--);
            if (timeLeft == 0) {
                clearInterval(callTimeout);
                send({"event": "continue"});
            }
        }, 1000);
    } else {
        var timeLeft = 5;
        $("#bid-countdown").text(timeLeft);
        bidTimeout = setInterval(function() {
            $("#bid-countdown").text(timeLeft--);
            if (timeLeft == 0) {
                clearInterval(bidTimeout);
                send({"event": "buy"});
            }
        }, 1000);
    }
}

/**
 * Send bid message
 * @param {amount} the bid amount
 */
function makeBid(amount) {
    send({
        "event": "new_bid",
        "club": "{{user.club}}",
        "label": "{{user.club.label}}",
        "amount": amount
    });

}

// Socket close
socket.onclose = function(e) {console.error("Web socket closed unexpectedly");}





// INFO PERSONALI
//   quanti soldi hai

// CONTROLLI
//   uno non può più rilanciare né chiamare se è pieno per quel ruolo
//   uno non può più rilanciare più di soldi rimasti - 1 * giocatori mancanti