const startGuessBtn = document.getElementById('startGuessBtn');
const submitGuessBtn = document.getElementById('submitguessBtn');
const guessInput = document.getElementById('userguess');
const drawnCanvas = document.getElementById('drawnCanvas');
const attemptsDisplay = document.getElementById('attemptsDisplay');
const feedbackMessage = document.getElementById('feedbackMessage'); // Define feedbackMessage variable

function startGame() {
    submitGuessBtn.removeAttribute('disabled'); 
    guessInput.disabled = false; 
    drawnCanvas.style.filter = "none"; 
}

// Function to generate a random success message
function getRandomSuccessMessage() {
    const successMessages = [
        "Congratulations! You got it right!",
        "Amazing job! That's correct!",
        "You nailed it! Well done!",
        "Fantastic! Your guess is correct!",
        "Bravo! You guessed it right!",
        "Hooray! That's the correct guess!",
        "Excellent! You got it spot on!",
        "Impressive! You guessed correctly!"
    ];
    const randomIndex = Math.floor(Math.random() * successMessages.length);
    return successMessages[randomIndex];
}

function handleGuessSubmission(event) {
    event.preventDefault(); 

    const formData = new FormData();
    formData.append('userguess', guessInput.value);

    fetch(`/guess/${sketchId}`, {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        submitGuessBtn.disabled = data.submit_disabled; 
        guessInput.disabled = data.submit_disabled;
        if (data.feedback_message === "Correct! Good job!") {
            // Display random success message
            const successMessage = getRandomSuccessMessage();
            // Display success message
            feedbackMessage.textContent = `${successMessage} You earned ${data.points} points!`;
        } 
        else if (data.feedback_message === "Time's up! Please try again.") {
            feedbackMessage.textContent = "Time's up! Sorry";
        }
        else {
            // Display incorrect guess message
            feedbackMessage.textContent= "Incorrect guess";
        }
        feedbackMessage.classList.remove('hidden'); // Show the feedback message
    })
    .catch(error => {
        console.error('Error submitting guess:', error);
    });
}

startGuessBtn.addEventListener('click', startGame);
submitGuessBtn.addEventListener('click', handleGuessSubmission);
