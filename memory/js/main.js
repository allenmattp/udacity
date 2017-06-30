document.addEventListener("DOMContentLoaded", function() {
	dealCards(makeDeck(arrayValues, cardNumber));
	var starCount = starAward(roundCount);
	document.getElementById("fire").innerHTML = starCount;
}, false);

/**
 * Set variables:
 * arrayValues are the "faces" of each of our cards. Should all be listed twice (pairs)
 * storeValues is an empty array that will be used to track cards while playing
 * cardValue is an empty array that will be used to evaluate card matches
 * flipCount will track how many pairs have been matched
 * cardNumber will determine size of deck and compared to flipCount to evaluate victory condition
 * roundCount tracks number of attempts
 * seconds tracks time elapsed
 */
var arrayValues = ["🤔", "🤔", "🤗", "🤗", "🙄", "🙄", "🤐", "🤐", "🙃", "🙃", "🤑", "🤑", "🤒", "🤒", "🤕", "🤕", "🤓", "🤓", "🤖", "🤖", "🦁", "🦁", "🦄", "🦄", "🦃", "🦃", "🦀", "🦀", "🦂", "🦂"];
var storeValues = [];
var cardValue = [];
var flipCount = 0;
var cardNumber = prompt("How many cards would you like dealt? (max 30) ", 12);
var roundCount = 0;
var seconds = 0;
function starAward(rounds) {
	if (roundCount <= (cardNumber*.8)) {
		return "🔥 🔥 🔥";
	} else if (roundCount <= (cardNumber*1.2)) {
		return "🔥 🔥";
	} else {
		return "🔥";
	}
};
/**
 * @description begins and start of game and runs until victory conditions are met
 * @returns Displays value for seconds elapsed
 */
var time = setInterval(function(){ 
	if (cardNumber != flipCount) {
		seconds += 1;
		document.getElementById("timer").innerHTML = seconds;
	} 
}, 1000);
// @returns Victory message when user completes games
function victory() {
	var starCount = starAward(roundCount);
	if (confirm("Congratulations! You won! And it only took you... " +roundCount+ " rounds and " +seconds+ " seconds. That's " +starCount+ " Play again?") == true) {
		location.reload();
	}
};
/**
 * From Mozilla Developer Network:
 * Returns a random integer between min (inclusive) and max (inclusive)
 * Using Math.round() will give you a non-uniform distribution!
 */
function getRandomInt(min, max) {
    return Math.floor(Math.random() * (max - min + 1)) + min;
};
/**
 * @description Builds the deck of cards
 * @param {array} array - Value of cards the game should use
 * @param {int} cardNumber - Number of cards in the deck
 * @returns Shuffled deck of specified size
 */
function makeDeck(array, cardNumber) {
	if (cardNumber > 30) {
		alert("Whoa there, that's a little ambitious. Let's pick a smaller number.");
		location.reload();
	} else if (cardNumber % 2) {
		alert("You can't win if there are an odd number of cards... Try an even number!");
		location.reload();
	} else {
	// Create an array based on size of user's input. "build the deck"
		deck = [];
		for (var i = 0; i < (cardNumber); i++) {
			deck.push(array[i]);
		}
	// Rearrange array elements in random order. "shuffle the deck"
		var shuffleDeck = [];
		for (var cards = 0; cards < cardNumber; cards++) {
			shuffleDeck[cards] = deck.splice((getRandomInt(0, deck.length-1)), 1);
		} return shuffleDeck;
	}
};

/**
 * @description Deal the cards
 * @param {array} playerDeck - The deck that will be dealt
 * @returns HTML code of Div objects for each card with unique ids that will run flipCard function onclick
 */
function dealCards(playerDeck) {
	flipCount = 0;
	var output = '';
	for(var i = 0; i < playerDeck.length; i++) {
		output += '<div id='+i+' onclick=flipCard(this,"'+playerDeck[i]+'")></div>';
	}
	document.getElementsByClassName("card-table")[0].innerHTML = output;
};

/**
 * Shout out to Adam Khoury's tutorial for help providing framework for game logic
 * @description "Flips" cards and evaluates if they match (and if successful match solves the puzzle)
 * @param {string} card - The card (div object) that a user clicks on
 * @param {string} value - The card's value
 * @returns Behaves differently depending whether match found and whether game won
 */
function flipCard(card, value) {
	// Check to make sure the selected card is unflipped and that we aren't flipping more than 2 in a round
	// Flipping a card changes its style and displays the cards "face" (value)
	if (card.innerHTML == "" && storeValues.length < 2) {
		card.style.background = "#4cb963";
		card.innerHTML = value;
		// If this is the first card flipped in a round, its value to the storage arrays
		if(storeValues.length == 0) {
			storeValues.push(value);
			cardValue.push(card.id);
		}
		// If this is the second card flipped we need to evaluate if it's a match
		else if (storeValues.length == 1) {
			storeValues.push(value);
			cardValue.push(card.id);
			// If they match, add to flipCount/roundCount, check to see if game is won or prepare for next round
			if (storeValues[0] == storeValues[1]) {
				var card_1 = document.getElementById(cardValue[0]);
				var card_2 = document.getElementById(cardValue[1]);
				card_1.style.background = "#5c6784";
				card_2.style.background = "#5c6784";
				flipCount += 2;
				roundCount += 1;
				var starCount = starAward(roundCount);
				document.getElementById("fire").innerHTML = starCount;
				document.getElementById("round").innerHTML = roundCount;
				storeValues = [];
				cardValue = [];
				// Did we win?
				if (flipCount == cardNumber) {
					victory();
				}
			} 
			// If they don't match, flip them over (revert to unflipped styles) and get ready for the next round
			else {
				function nextRound() {
					var card_1 = document.getElementById(cardValue[0]);
					var card_2 = document.getElementById(cardValue[1]);
					card_1.style.background = "#157f1f";
					card_1.innerHTML = "";
					card_2.style.background = "#156f1f";
					card_2.innerHTML = "";
					roundCount += 1;
					var starCount = starAward(roundCount);
					document.getElementById("fire").innerHTML = starCount;
					document.getElementById("round").innerHTML = roundCount;
					storeValues = [];
					cardValue = [];
				}
				// How much time we wait before flipping cards back over
				setTimeout(nextRound, 500);
			}
		}
	}
};
