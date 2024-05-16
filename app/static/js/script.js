$(document).ready(function() {
    // Background music and mute functionality
    let backgroundMusic = new Audio("{{ url_for('static', filename='audio/background.mp3') }}");
    let isMuted = false;

    // Function to toggle background music
    function toggleBackgroundMusic() {
        if (isMuted) {
            backgroundMusic.play();
            $('#muteIcon').attr('src', '{{ url_for('static', filename='images/unmute.png') }}');
        } else {
            backgroundMusic.pause();
            $('#muteIcon').attr('src', '{{ url_for('static', filename='images/mute.png') }}');
        }
    }

    // Event listener for mute button
    $('#muteButton').click(function() {
        isMuted = !isMuted;
        toggleBackgroundMusic();
    });

    // Play background music on page load
    toggleBackgroundMusic();
});

// Guessing functionality
// Include correct and alarm sounds
let correctSound = new Audio("{{ url_for('static', filename='audio/correct.mp3') }}");
let alarmSound = new Audio("{{ url_for('static', filename='audio/alarm.mp3') }}");

// Guessing logic

// Drawing functionality
// Drawing logic

// Common functions for sound effects
// Play correct sound effect
function playCorrectSound() {
    correctSound.play();
}

// Play alarm sound and restart background music
function playAlarm() {
    alarmSound.play();
    setTimeout(function() {
        backgroundMusic.play(); // Restart background music after alarm finishes
    }, alarmSound.duration * 1000);
}
