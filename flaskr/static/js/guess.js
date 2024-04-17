const countdownTimer = document.getElementById('countdowntimer');
const countdownText = document.getElementById('countdownMessage');
const timeRemainingText = document.getElementById('countdowntext');
let timeLeft = 10;
let timerRunning = true;

// Start the timer
const downloadTimer = setInterval(() => {
    if (timeLeft <= 0) {
        clearInterval(downloadTimer);
        timerRunning = false;
        document.getElementById('submitguessBtn').setAttribute('disabled', true); // Disable button
        countdownText.classList.remove('hidden'); 
        timeRemainingText.classList.add('hidden'); 
    } else {
        countdownTimer.textContent = timeLeft;
    }
    timeLeft--; // Decrease timeLeft after updating countdownTimer.textContent
}, 1000);
