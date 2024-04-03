$(document).ready(function() {
    const $canvas = $('#drawingCanvas');
    const ctx = $canvas[0].getContext('2d');
    let painting = false;

    function startPosition(e) {
        painting = true;
        draw(e);
    }

    function finishedPosition() {
        painting = false;
        ctx.beginPath();
    }

    function draw(e) {
        if (!painting) return;
        const mouseX = e.clientX - $canvas.offset().left;
        const mouseY = e.clientY - $canvas.offset().top;
        ctx.lineWidth = 5; 
        ctx.lineCap = 'round'; 

        ctx.lineTo(mouseX, mouseY); 
        ctx.stroke();
        ctx.beginPath(); 
        ctx.moveTo(mouseX, mouseY); 
    }

    $canvas.mousedown(startPosition);
    $canvas.mouseup(finishedPosition);
    $canvas.mousemove(draw);

    //This is a placeholder, currently just pastes the drawing below and clears the canvas
    $('#submitCanvas').click(function() {
        const image = new Image();
        image.src = $canvas[0].toDataURL();
        image.onload = function() {
            const displayCanvas = $('<canvas></canvas>').attr({
                width: $canvas[0].width / 2,
                height: $canvas[0].height / 2
            })[0];
            const displayCtx = displayCanvas.getContext('2d');
            displayCtx.drawImage(image, 0, 0, displayCanvas.width, displayCanvas.height);
            $('body').append(displayCanvas);
        };

        ctx.clearRect(0, 0, $canvas[0].width, $canvas[0].height);
    });
});
