var roundCount = 0
// Based on the number of rounds it takes to win, user is awarded "stars"
var stars = starAward(roundCount)

function starAward(rounds) {
	if (roundCount < 10) {
		return "🤘 🤘 🤘"
	} else if (roundCount < 14) {
		return "🤘 🤘"
	} else {
		return "🤘"
	}
};

console.log(stars)