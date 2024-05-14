$(document).ready(function() {
    const $stopwatchDisplay = $('#stopwatchDisplay');
    const $startGuessBtn = $('#startGuessBtn');
    const $submitGuessBtn = $('#submitguessBtn');
    const $guessInput = $('#userguess'); // Get the guess input field
    const $successMessage = $('#successMessage');
    const $feedbackMessage = $('#feedbackMessage'); // Get the feedback message element
    const $drawnCanvas = $('#drawnCanvas');
    const $attemptsDisplay = $('#attemptsDisplay'); // Element to display attempts
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
        stopwatchInterval = setInterval(function() {
            elapsedTime++; // Increase every second
            updateStopwatchDisplay(); // Update the displayed time
        }, 1000);
        $submitGuessBtn.prop('disabled', false); // Enable the submit button
        $guessInput.prop('disabled', false); // Enable the guess input field
        $drawnCanvas.css('filter', 'none'); // Remove blur from the canvas
        $feedbackMessage.addClass('hidden'); // Hide feedback message at game start
    }

    // Function to update the stopwatch display
    function updateStopwatchDisplay() {
        const hours = Math.floor(elapsedTime / 3600);
        const minutes = Math.floor((elapsedTime % 3600) / 60);
        const seconds = elapsedTime % 60;
        $stopwatchDisplay.text(`Tik! Tok! Time is Ticking! ${hours.toString().padStart(2, '0')}:${minutes.toString().padStart(2, '0')}:${seconds.toString().padStart(2, '0')}`);
    }

    // Function to update guess attempts display
    function updateAttemptsDisplay() {
        $attemptsDisplay.text(`Guess Attempts: ${guessAttempts}`);
    }

    // Handle guess submission, incrementing guess attempts
    function handleGuessSubmission(event) {
        event.preventDefault(); // Prevent form default submission
        guessAttempts++; // Increment guess attempts
        updateAttemptsDisplay(); // Update attempts display

        // Send guess to server for checking
        $.ajax({
            type: 'POST',
            url: '/check-guess',
            data: {
                guess: $guessInput.val()
            },
            success: function(response) {
                if (response.isCorrect) {
                    clearInterval(stopwatchInterval); // Stop the stopwatch
                    $submitGuessBtn.prop('disabled', true); // Disable the submit button
                    $guessInput.prop('disabled', true); // Disable further guesses
                    $successMessage.removeClass('hidden'); // Show success message
                    $feedbackMessage.addClass('hidden'); // Ensure feedback message is hidden
                } else {
                    $feedbackMessage.text('Try again!'); // Update and show feedback message
                    $feedbackMessage.removeClass('hidden');
                }
                // Clear the input after each guess
                $guessInput.val('');
            }
        });
    }

    $startGuessBtn.on('click', startGame);
    $submitGuessBtn.on('click', handleGuessSubmission);
});
