$(document).ready(function() {
    let canvas = $('#drawingCanvas')[0];
    let ctx = canvas.getContext('2d');
    let timeLeft = 30;
    let timerInterval;
    let currentColor = '#000000'; // Default drawing color
    let painting = false;

    // Function to disable/enable drawing and UI elements
    function toggleDrawing(enable) {
        $('#drawingCanvas').css('pointer-events', enable ? 'auto' : 'none');
        $('.color-button').css('pointer-events', enable ? 'auto' : 'none');
        $('#submitCanvas').css('pointer-events', enable ? 'auto' : 'none');
        $('#wordPlaceholder').css('display', enable ? 'inline' : 'none');
    }

    // Function to start the drawing game
    function startGame() {
        timeLeft = 30; // Reset the timer each time the game starts
        clearInterval(timerInterval); // Clear any existing timer interval
        ctx.strokeStyle = '#000000'; // Reset the color to black
        ctx.lineWidth = 15;
        ctx.globalCompositeOperation = 'source-over';
        toggleDrawing(true);
        $('#beginButton').hide(); // Hide the begin button
        timerInterval = setInterval(function() {
            $('#timerPlaceholder').text(timeLeft);
            timeLeft -= 1;
            if (timeLeft < 0) {
                clearInterval(timerInterval);
                submitDrawing(); // Automatically submit the drawing when the time is up
            }
        }, 1000);
    }

    // Function to fetch word to draw and place in DOM
    function fetchWordAndStartGame() {
        $.ajax({
            url: '/begin-draw',
            type: 'GET',
            success: function(response) {
                let word = response.word;  // Get the word from the response
                $('#wordPlaceholder').text(word);
                startGame();
            },
            error: function() {
                $('#wordPlaceholder').text("Error fetching word");
                console.error("Failed to fetch word");
            }
        });
    }       

    function submitDrawing() {
        clearInterval(timerInterval); // Ensure to clear the interval on submission
        let dataURL = canvas.toDataURL();
    
        // Clear the canvas
        ctx.clearRect(0, 0, canvas.width, canvas.height);
        
        // Disable drawing after submission
        toggleDrawing(false);
        
        // Show the begin button again for a new game
        $('#beginButton').show();
        
        // Reset the timer display
        $('#timerPlaceholder').text("30");
    
        // Send the drawing data to the server
        $.ajax({
            url: '/submit-draw',
            method: 'POST',
            contentType: 'application/json',
            data: JSON.stringify({ image: dataURL }),
            headers: {
                'X-CSRFToken': $('#csrf_token').val()  // Include the CSRF token in the header
            },
            success: function(response) {
                console.log('Submission successful:', response);
                // Optionally display a message to the user or handle the response further
            },
            error: function(xhr, status, error) {
                console.error('Submission failed:', xhr.responseText);
                // Optionally handle the error, like displaying a message to the user
            }
        });
    }    

    // Function to handle the start of a touch/draw
    function startPosition(e) {
        painting = true;
        // Prevent scrolling when touching the canvas
        if (e.type !== 'mousedown') {
            e.preventDefault();
        }
        draw(e);
    }

    // Function to handle the end of a touch/draw
    function finishedPosition() {
        painting = false;
        ctx.beginPath();
    }

    // Draw function, handles mouse and touch
    function draw(e) {
        if (!painting) return;

        // Determine whether this is a mouse event or a touch event
        let clientX = e.clientX || e.touches[0].clientX;
        let clientY = e.clientY || e.touches[0].clientY;

        let bounds = canvas.getBoundingClientRect();
        let scaleX = canvas.width / bounds.width;
        let scaleY = canvas.height / bounds.height;

        let mouseX = (clientX - bounds.left) * scaleX;
        let mouseY = (clientY - bounds.top) * scaleY;

        ctx.lineCap = 'round';

        ctx.lineTo(mouseX, mouseY);
        ctx.stroke();
        ctx.beginPath();
        ctx.moveTo(mouseX, mouseY);
    }

    // Adding both mouse and touch event listeners for drawing
    $('#drawingCanvas').on('mousedown touchstart', startPosition)
                    .on('mouseup touchend', finishedPosition)
                    .on('mousemove touchmove', draw)
                    .on('mouseout touchcancel', finishedPosition);


    // EventListeners for starting and ending the game
    $('#beginButton').on('click', fetchWordAndStartGame);
    $('#submitCanvas').on('click', submitDrawing);

    // EventListener to update the currentColor when a new color is picked
    $('.color-button').click(function() {
        currentColor = $(this).css('background-color');
        ctx.lineWidth = 15;
        ctx.globalCompositeOperation = 'source-over'; // Set to normal drawing mode
        ctx.strokeStyle = currentColor;
    });

    // EventListener to pick the eraser
    $('.eraser').click(function() {
        ctx.lineWidth = 75;
        ctx.globalCompositeOperation = 'destination-out'; // Set to erase mode
    });

    // Both mouse and touch event listeners for drawing
    $('#drawingCanvas').on('mousedown touchstart', startPosition)
                    .on('mouseup touchend', finishedPosition)
                    .on('mousemove touchmove', draw)
                    .on('mouseout touchcancel', finishedPosition);
});
