const countdownTimer = document.getElementById('countdowntimer');
let timeLeft = 10;
let timerRunning = true;
let attempts = 0;
let correct = false;
let incorrectAlertShown = false;
let oneMoreTryAlertShown = false;

// Start the timer
const downloadTimer = setInterval(() => {
    countdownTimer.textContent = timeLeft;
    timeLeft--;

    if (timeLeft < 0) {
        clearInterval(downloadTimer);
        timerRunning = false;
        if (!correct && !incorrectAlertShown) {
            incorrectAlertShown = true;
            setTimeout(() => {
                alert("Time's up :( ");
                document.getElementById('userguess').setAttribute('disabled', true); // disable input
                document.getElementById('submitguessBtn').setAttribute('disabled', true); // disable button
            }, 1000);
        }
    }
}, 1000);

document.getElementById("submitguessBtn").addEventListener("click", function() {
    if (!timerRunning) return; // If time is up, do not evaluate

    // add the number of attempts
    attempts++;

    // check
    checkGuess();
});

//check the guess
function checkGuess() {
    var userGuess = document.getElementById('userguess').value;
    var wordPlaceholder = document.getElementById('wordPlaceholder').textContent // word/prompt that sketcher used to draw
    userGuess = userGuess.toLowerCase();
    wordPlaceholder = wordPlaceholder.toLowerCase();
    if (userGuess === wordPlaceholder) {
        // when correct
        if (!correct) {
            correct = true;
            alert("Correct");
            document.getElementById('userguess').setAttribute('disabled', true); // disable input
            document.getElementById('submitguessBtn').setAttribute('disabled', true); // disable button
            clearInterval(downloadTimer); // Stop the timer
        }
    } else {
        //  when incorrect
        if (attempts === 1 && !oneMoreTryAlertShown) {
            oneMoreTryAlertShown = true;
            alert("Incorrect. You have one more try.");
        } else if (attempts >= 2 && !incorrectAlertShown) {
            incorrectAlertShown = true;
            alert("Incorrect");
            document.getElementById('userguess').setAttribute('disabled', true); // disable input
            document.getElementById('submitguessBtn').setAttribute('disabled', true); // disable button
            clearInterval(downloadTimer); // stop timer
        }
    }
}
