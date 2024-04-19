const stopwatchDisplay = document.getElementById('stopwatchDisplay');
const startGuessBtn = document.getElementById('startGuessBtn');
const submitGuessBtn = document.getElementById('submitguessBtn');
const successMessage = document.getElementById('successMessage');
const drawnCanvas = document.getElementById('drawnCanvas');
let stopwatchInterval;
let elapsedTime = 0; // Time in seconds

// Function to start the stopwatch
function startStopwatch() {
    clearInterval(stopwatchInterval); // Clear any existing intervals
    elapsedTime = 0; // Reset stopwatch
    updateStopwatchDisplay(); // Immediately update the display
    stopwatchInterval = setInterval(() => {
        elapsedTime++; // Increase every second
        updateStopwatchDisplay(); // Update the displayed time
    }, 1000);
    submitGuessBtn.removeAttribute('disabled'); // Enable the submit button
    drawnCanvas.style.filter = "none"; // Remove blur from the canvas
}

// Function to update the stopwatch display
function updateStopwatchDisplay() {
    const hours = Math.floor(elapsedTime / 3600);
    const minutes = Math.floor((elapsedTime % 3600) / 60);
    const seconds = elapsedTime % 60;
    stopwatchDisplay.textContent = `Tik! Tok! time is ticking! ${hours.toString().padStart(2, '0')}:${minutes.toString().padStart(2, '0')}:${seconds.toString().padStart(2, '0')}`;
}

// Simulate stopping the stopwatch and displaying success on correct guess
function handleGuessSubmission() {
    clearInterval(stopwatchInterval); // Stop the stopwatch
    submitGuessBtn.setAttribute('disabled', true); // Disable the submit button
    successMessage.classList.remove('hidden'); // Show success message
    // Here you can add logic to check if the guess is correct
}

startGuessBtn.addEventListener('click', function() {
    startGuessBtn.classList.add('hidden'); // Hide the start button
    startStopwatch();
});

submitGuessBtn.addEventListener('click', handleGuessSubmission);
