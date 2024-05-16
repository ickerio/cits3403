$(document).ready(function() {
    let interval;
    let secondsRemaining = 30; // Countdown time in seconds
    let guessCount = 0;

    function startTimer(duration) {
        secondsRemaining = duration;
        interval = setInterval(function() {
            $('#stopwatchDisplay').text(` ${secondsRemaining}s`);

            if (--secondsRemaining < 0) {
                clearInterval(interval);
                disableGuessing();
                $('#feedbackMessage').text('Time is up!').addClass('text-danger').removeClass('hidden');
            }
        }, 1000);
    }

    function disableGuessing() {
        $('#userguess').prop('disabled', true);
        $('#submitguessBtn').prop('disabled', true);
    }

    function enableGuessing() {
        $('#userguess').prop('disabled', false);
        $('#submitguessBtn').prop('disabled', false);
    }

    function drawImageOnCanvas(dataUrl) {
        const canvas = document.getElementById('drawnCanvas');
        const context = canvas.getContext('2d');
        const image = new Image();
        image.onload = function() {
            context.drawImage(image, 0, 0, canvas.width, canvas.height);
        };
        image.src = dataUrl;
    }

    $('#startGuessBtn').click(function() {
        $(this).hide();
        $.ajax({
            url: `/begin-guess`,
            type: 'GET',
            success: function(response) {
                if (response.image_data) {
                    drawImageOnCanvas(response.image_data);
                    startTimer(30);
                    enableGuessing();
                } else if (response.error) {
                    $('#feedbackMessage').text(response.error).addClass('text-danger').removeClass('hidden');
                }
            },
            error: function() {
                $('#feedbackMessage').text('Error loading the sketch. Please try again.').addClass('text-danger').removeClass('hidden');
            }
        });
    });

    $('form').submit(function(event) {
        event.preventDefault();
        let userGuess = $('#userguess').val();
        guessCount++;
        $('#attemptsDisplay').text(guessCount);

        $.ajax({
            url: '/submit-guess',
            type: 'POST',
            data: {
                userguess: userGuess,
                csrf_token: $('#csrf_token').val()
            },
            success: function(response) {
                if (response.correct) {
                    $('#feedbackMessage').text('You Got It!').addClass('text-success').removeClass('hidden');
                    $('#feedbackMessage').removeClass('text-danger'); // Ensure it's green
                    clearInterval(interval);
                    disableGuessing();
                } else {
                    $('#feedbackMessage').text('Incorrect, try again!').addClass('text-danger').removeClass('hidden');
                    $('#userguess').val(''); // Clear the input field after incorrect guess
                }
            },
            error: function() {
                $('#feedbackMessage').text('Error processing your guess. Please try again.').addClass('text-danger').removeClass('hidden');
                $('#userguess').val(''); // Clear the input field after error
            }
        });
    });
});
