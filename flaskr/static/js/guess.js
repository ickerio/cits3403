const stopwatchDisplay = document.getElementById('stopwatchDisplay');
const startGuessBtn = document.getElementById('startGuessBtn');
const submitGuessBtn = document.getElementById('submitguessBtn');
const successMessage = document.getElementById('successMessage');
const drawnCanvas = document.getElementById('drawnCanvas');
const attemptsDisplay = document.getElementById('attemptsDisplay'); // Element to display attempts
let stopwatchInterval;
let elapsedTime = 0; // Time in seconds
let guessAttempts = 0; // Initialize guess attempts counter

// Function to start the stopwatch
function startStopwatch() {
    clearInterval(stopwatchInterval); // Clear any existing intervals
    elapsedTime = 0; // Reset stopwatch
    guessAttempts = 0; // Reset guess attempts
    updateStopwatchDisplay(); // Immediately update the display
    updateAttemptsDisplay(); // Update attempts display
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
    stopwatchDisplay.textContent = `Tik! Tok! Time is Ticking! ${hours.toString().padStart(2, '0')}:${minutes.toString().padStart(2, '0')}:${seconds.toString().padStart(2, '0')}`;
}

// Function to update guess attempts display
function updateAttemptsDisplay() {
    attemptsDisplay.textContent = `Guess Attempts: ${guessAttempts}`;
}

// Simulate stopping the stopwatch, incrementing guess attempts, and displaying success on correct guess
function handleGuessSubmission() {
    guessAttempts++; // Increment guess attempts
    updateAttemptsDisplay(); // Update attempts display

    // Placeholder for checking the correctness of the guess
    // If the guess is correct:
    clearInterval(stopwatchInterval); // Stop the stopwatch
    submitGuessBtn.setAttribute('disabled', true); // Disable the submit button
    successMessage.classList.remove('hidden'); // Show success message
}

startGuessBtn.addEventListener('click', function() {
    startGuessBtn.classList.add('hidden'); // Hide the start button
    startStopwatch();
});

submitGuessBtn.addEventListener('click', handleGuessSubmission);
