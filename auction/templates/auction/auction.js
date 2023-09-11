// INITIALISATION
const host = window.location.host;
const protocol = host.startsWith("localhost")? "ws" : "wss";
const socket = new WebSocket(protocol + "://" + host + "/ws" + "{{request.path}}");
var phase;
var callTimeout = 0;
var bidTimeout = 0;


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
// function selectPlayer() {
//     clearTimeout(callTimeout);  // stop timer on player selection
//     const playerID = $("#player-selector").val();
//     const playerInfo = $( "#player-selector option:selected" ).text();
//     send({"event": "start_bid", "player": playerID});
// }

/**
 * Make new bid
 * @param {Number} value the bid value 
 */
// function raiseBid(value) {
//     const currentBid = parseInt($("#best-bid").text());
//     if (!waitingForCall && !isNaN(value) && value > currentBid) {
//         send({"event": "new_bid", "club": "{{request.user.club}}", "value": value});
//     }
// }


// REACTIONS (RECEIVE MESSAGES)

// Get messages and dispatch them to correct action
socket.onmessage = function(event) {
    const payload = JSON.parse(event.data);
    switch (payload.event) {
        case "join":
            phase = payload.phase;
            if (phase === "awaiting participants") {
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
            setPlayerChoice(payload.club, payload.role);
            // callTimeout = setTimeout(function() {send({"event": "continue"})}, 1000*15);
            break;
        // case "start_bid":
        //     showBidInfo(payload);
        //     startBids();
        //     bidTimeout = setTimeout(function() {buyPlayer(payload.club, 1);}, 1000*3);
        //     break;
        // case "new_bid":
        //     clearTimeout(bidTimeout);
        //     updateBid(payload.club, payload.value);
        //     bidTimeout = setTimeout(function() {buyPlayer(payload.club, payload.value);}, 1000*3);
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
}

/**
 * Let user choose player for next round choice for new round
 * @param {String} club name of the club of the attending user 
 * @param {String} role letter indicating the role of players for the current round
 */
function setPlayerChoice(club, role) {
    if ("{{request.user.club}}" === club) {
        const fullRole = getRole(role);
        $("#player-selector").html(`<option value="">Scegli un ${fullRole}</option>`);
        setPlayerSelector(club, role);
        $("selector-container").show();
    }
    else {$("selector-container").hide();}
}

/**
 * Stop bids during player choice
 */
// function stopBids() {
//     waitingForCall = true;
//     $(".bid-button").css("background-color", "lightgrey");
// }

/**
 * Prepare players list for selection
 * @param {String} club name of the club of the attending user 
 * @param {String} roleIndex letter indicating the role of players for the current round
 */
function setPlayerSelector(club, roleIndex) {
    $.get("{% url 'players' role='-' %}".replace("-", roleIndex)).done(function(data) {
        console.log(data);
        for (let player of data) {
            console.log(player.id);
            console.log(player.name);
            console.log(player.team);
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
// function showBidInfo(data) {
//     $("#auction-info").append(`<p>Gioatore chiamato: ${data.player_name} (${data.player_team} - ${data.player_role})</p>`);
//     $("#auction-info").append(`
//         <p>
//             Offerta corrente: <span id="best-bid">1</span> <span class="currency">M</span>
//             (<span id="best-bidder">${data.club}</span>)
//         </p>
//     `);
// }

/**
 * Activate bidding
 */
// function startBids() {
//     waitingForCall = false;
//     $(".bid-button").css("background-color", "DarkMagenta");
// }

/**
 * Update bid info with new bid
 * @param {String} club name of the club making the bid 
 * @param {Number} value amount of the bid
 */
// function updateBid(club, value) {
//     $("#best-bid").text(value);
//     $("#best-bidder").text(club);
// }

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

// Socket close
socket.onclose = function(e) {console.error("Web socket closed unexpectedly");}





// INFO PERSONALI
//   quanti soldi hai

// CONTROLLI
//   uno non può più rilanciare né chiamare se è pieno per quel ruolo
//   uno non può più rilanciare più di soldi rimasti - 1 * giocatori mancanti