const countdownTimer = document.getElementById('countdowntimer');
let timeleft = 10;

const downloadTimer = setInterval(() => {
    timeleft--;
    countdownTimer.textContent = timeleft;
    if (timeleft <= 0) {
        clearInterval(downloadTimer);
        setTimeout(() =>{
            alert("Time's up :( ");
        }, 1000);
    }
}, 1000);