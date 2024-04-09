$(document).ready(function() {
    //Probably should be using let?
    var canvas = $('#drawingCanvas')[0];
    var ctx = canvas.getContext('2d');
    let timeLeft = 10;
    var timerInterval;
    var currentColor = '#000000'; // Default color
    var painting = false;
    // These 2 lines are placeholders -> used for pasting the submitted drawing below the canvas
    var submittedDiv = $('<div></div>'); // Create a div to hold submitted drawings
    $('body').append(submittedDiv); // Append it to the body

    // Function to disable/enable drawing and UI elements
    function toggleDrawing(enable) {
        $('#drawingCanvas').css('pointer-events', enable ? 'auto' : 'none');
        $('#colorPicker').css('pointer-events', enable ? 'auto' : 'none');
        $('#submitCanvas').css('pointer-events', enable ? 'auto' : 'none');
        $('#wordPlaceholder').css('display', enable ? 'inline' : 'none');
    }

    // Function to start the drawing game
    function startGame() {
        timeLeft = 10; // Reset the timer each time the game starts
        clearInterval(timerInterval); // Clear any existing timer interval
        toggleDrawing(true);
        $('#beginButton').hide(); // Hide the begin button
        timerInterval = setInterval(function() {
            $('#timerPlaceholder').text(timeLeft + 's');
            timeLeft -= 1;
            if (timeLeft < 0) {
                clearInterval(timerInterval);
                submitDrawing(); // Automatically submit the drawing when the time is up
            }
        }, 1000);
    }

    // Function to handle the drawing submission
    function submitDrawing() {
        clearInterval(timerInterval); // Ensure to clear the interval on submission
        var dataURL = canvas.toDataURL();
        var img = $('<img>').attr('src', dataURL).on('load', function() {
            $('body').append(img); // Append the submitted drawing somewhere on the page
        });

        ctx.clearRect(0, 0, canvas.width, canvas.height); // Clear the canvas

        toggleDrawing(false); // Disable drawing after submission
        $('#beginButton').show(); // Show the begin button again for a new game
        $('#timerPlaceholder').text("00:00"); // Reset the timer display
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
        var clientX = e.clientX || e.touches[0].clientX;
        var clientY = e.clientY || e.touches[0].clientY;

        var bounds = canvas.getBoundingClientRect();
        var scaleX = canvas.width / bounds.width;
        var scaleY = canvas.height / bounds.height;

        var mouseX = (clientX - bounds.left) * scaleX;
        var mouseY = (clientY - bounds.top) * scaleY;

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
    $('#beginButton').on('click', startGame);
    $('#submitCanvas').on('click', submitDrawing);

    // EventLister to update the currentColor when a new color is picked
    $('#colorPicker').on('change', function() {
        currentColor = $(this).val();
        ctx.strokeStyle = currentColor; // Set the new color as the stroke style
    });

    // Both mouse and touch event listeners for drawing
    $('#drawingCanvas').on('mousedown touchstart', startPosition)
                    .on('mouseup touchend', finishedPosition)
                    .on('mousemove touchmove', draw)
                    .on('mouseout touchcancel', finishedPosition);
});
