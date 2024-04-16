
//create timer
const countdownTimer = document.getElementById('countdowntimer');
let timeleft = 10;

const downloadTimer = setInterval(() => {
    timeleft--;
    countdownTimer.textContent = timeleft;
    if (timeleft <= 0) {
        clearInterval(downloadTimer);
        setTimeout(() =>{
            alert("Time's up :( ");
        }, 1000);
    }
}, 1000);

//stop timer
document.getElementById("submitguessBtn").addEventListener("click", function() {
    clearInterval(downloadTimer);

//check if the guess is correct
function checkGuess() {
    var userGuess = document.getElementById('userguess').value;
    var wordPlaceholder = document.getElementById('wordPlaceholder').textContent;
    userGuess = userGuess.toLowerCase();
    wordPlaceholder = wordPlaceholder.toLowerCase();
    if (userGuess === wordPlaceholder) {
        // action when correct NEED TO CHANGE*******
        alert("correct");
    } else {
        // action when incorrect NEED TO CHANGE******
        alert("incorrect");
    }
    //clear userguess
    document.getElementById('userguess').value = "";
}
                                                           
