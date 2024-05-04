const stopwatchDisplay = document.getElementById('stopwatchDisplay');
const startGuessBtn = document.getElementById('startGuessBtn');
const submitGuessBtn = document.getElementById('submitguessBtn');
const guessInput = document.getElementById('userguess'); // Get the guess input field
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
        // Check if time's up
        if (elapsedTime >= 30) {
            clearInterval(stopwatchInterval);
            submitGuessBtn.disabled = true; // Disable submit button after time's up
            guessInput.disabled = true; // Disable guess input field after time's up
        }
    }, 1000);
    submitGuessBtn.removeAttribute('disabled'); // Enable the submit button
    guessInput.disabled = false; // Enable the guess input field
    drawnCanvas.style.filter = "none"; // Remove blur from the canvas
}

// Function to update the stopwatch display
function updateStopwatchDisplay() {
    const hours = Math.floor(elapsedTime / 3600);
    const minutes = Math.floor((elapsedTime % 3600) / 60);
    const seconds = elapsedTime % 60;
    stopwatchDisplay.textContent = `Time Elapsed: ${hours.toString().padStart(2, '0')}:${minutes.toString().padStart(2, '0')}:${seconds.toString().padStart(2, '0')}`;
}

// Function to update guess attempts display
function updateAttemptsDisplay() {
    attemptsDisplay.textContent = `Guess Attempts: ${guessAttempts}`;
}

// Handle guess submission, incrementing guess attempts and sending data to backend
function handleGuessSubmission(event) {
    event.preventDefault(); // Prevent form default submission
    guessAttempts++; // Increment guess attempts
    updateAttemptsDisplay(); // Update attempts display

    // Send data to backend (routes.py) using Fetch API or XMLHttpRequest
    const formData = new FormData();
    formData.append('userguess', guessInput.value);
    formData.append('guessAttempts', guessAttempts);

    fetch('/submit_guess', {
        method: 'POST',
        body: formData
    })
    .then(response => {
        // Handle response from the server if needed
        console.log('Guess submission response:', response);
        // Check if guess is correct
        if (response.feedback_message === "Correct! Good job!") {
            submitGuessBtn.disabled = true; // Disable submit button after correct guess
            guessInput.disabled = true; // Disable guess input field after correct guess
        }
    })
    .catch(error => {
        // Handle any errors that occur during the fetch request
        console.error('Error submitting guess:', error);
    });
}

startGuessBtn.addEventListener('click', startGame);
submitGuessBtn.addEventListener('click', handleGuessSubmission);
