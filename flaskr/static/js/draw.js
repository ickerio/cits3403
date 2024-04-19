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

    // Function to fetch word to draw (not implemented) and place in DOM
    function fetchWordAndStartGame() {
        let word = "Banana"; // Placeholder, need to fetch and handle errors appropriately
        $('#wordPlaceholder').text(word);
        startGame();
    }    

    // Function to handle the drawing submission
    function submitDrawing() {
        clearInterval(timerInterval); // Ensure to clear the interval on submission
        let dataURL = canvas.toDataURL();
        let img = $('<img>').attr('src', dataURL).on('load', function() {
            $('body').append(img); // Append the submitted drawing somewhere on the page (placeholder functionality, need to send somewhere)
        });

        ctx.clearRect(0, 0, canvas.width, canvas.height); // Clear the canvas

        toggleDrawing(false); // Disable drawing after submission
        $('#beginButton').show(); // Show the begin button again for a new game
        $('#timerPlaceholder').text("30"); // Reset the timer display
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

        ctx.lineWidth = 5;
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

    // EventLister to update the currentColor when a new color is picked
    $('.color-button').click(function() {
        currentColor = $(this).css('background-color');
        ctx.strokeStyle = currentColor;
    });

    // Both mouse and touch event listeners for drawing
    $('#drawingCanvas').on('mousedown touchstart', startPosition)
                    .on('mouseup touchend', finishedPosition)
                    .on('mousemove touchmove', draw)
                    .on('mouseout touchcancel', finishedPosition);
});
