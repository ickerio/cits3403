const stopwatchDisplay = document.getElementById('stopwatchDisplay');
const startGuessBtn = document.getElementById('startGuessBtn');
const submitGuessBtn = document.getElementById('submitguessBtn');
const guessInput = document.getElementById('userguess'); // Get the guess input field
const successMessage = document.getElementById('successMessage');
const feedbackMessage = document.getElementById('feedbackMessage'); // Get the feedback message element
const drawnCanvas = document.getElementById('drawnCanvas');
const attemptsDisplay = document.getElementById('attemptsDisplay'); // Element to display attempts
let stopwatchInterval;
let elapsedTime = 0; // Time in seconds
let guessAttempts = 0; // Initialize guess attempts counter

// Function to start the game and stopwatch
function startGame() {
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
    guessInput.disabled = false; // Enable the guess input field
    drawnCanvas.style.filter = "none"; // Remove blur from the canvas
    feedbackMessage.classList.add('hidden'); // Hide feedback message at game start
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

// Handle guess submission, incrementing guess attempts
function handleGuessSubmission(event) {
    event.preventDefault(); // Prevent form default submission
    guessAttempts++; // Increment guess attempts
    updateAttemptsDisplay(); // Update attempts display

    // Placeholder for checking the correctness of the guess
    const isCorrect = false; // This should be replaced with actual correctness checking logic

    if (isCorrect) {
        clearInterval(stopwatchInterval); // Stop the stopwatch
        submitGuessBtn.setAttribute('disabled', true); // Disable the submit button
        guessInput.disabled = true; // Disable further guesses
        successMessage.classList.remove('hidden'); // Show success message
        feedbackMessage.classList.add('hidden'); // Ensure feedback message is hidden
    } else {
        feedbackMessage.textContent = 'Try again!'; // Update and show feedback message
        feedbackMessage.classList.remove('hidden');
    }

    // Clear the input after each guess
    guessInput.value = '';
}

startGuessBtn.addEventListener('click', startGame);
submitGuessBtn.addEventListener('click', handleGuessSubmission);
