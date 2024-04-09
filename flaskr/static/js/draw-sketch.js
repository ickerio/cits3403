document.addEventListener('DOMContentLoaded', function() {
    let canvas = document.getElementById('drawingCanvas');
    let ctx = canvas.getContext('2d');
    let painting = false;
    let submittedDiv = document.createElement('div'); // Div to hold submitted drawings
    document.body.appendChild(submittedDiv); // Append it to the body or to a specific container where you want the drawings to show

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
    
        let bounds = canvas.getBoundingClientRect();
        // Calculate the scale factor for X and Y
        let scaleX = canvas.width / bounds.width;
        let scaleY = canvas.height / bounds.height;
    
        // Adjust mouse coordinates using the scale factor
        let mouseX = (e.clientX - bounds.left) * scaleX;
        let mouseY = (e.clientY - bounds.top) * scaleY;
    
        ctx.lineWidth = 5;
        ctx.lineCap = 'round';
    
        ctx.lineTo(mouseX, mouseY);
        ctx.stroke();
        ctx.beginPath();
        ctx.moveTo(mouseX, mouseY);
    }    

    // EventListeners for drawing
    canvas.addEventListener('mousedown', startPosition);
    canvas.addEventListener('mouseup', finishedPosition);
    canvas.addEventListener('mousemove', draw);
    canvas.addEventListener('mouseout', finishedPosition); // Stop drawing when the mouse leaves the canvas

    // Submit and clear the canvas, then show the drawing below
    document.getElementById('submitCanvas').addEventListener('click', function() {
        let dataURL = canvas.toDataURL();
        let img = new Image();
        img.src = dataURL;

        // Clear the canvas after submitting
        ctx.clearRect(0, 0, canvas.width, canvas.height);

        // Wait for the image to load before appending it, to ensure it's displayed
        img.onload = function() {
            submittedDiv.appendChild(img); // Append the image to the submittedDiv
        };
    });
});
