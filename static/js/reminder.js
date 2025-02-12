function checkReminders() {
    fetch('/get_tasks')
        .then(response => response.json())
        .then(tasks => {
            const now = new Date();

            tasks.forEach(task => {
                const taskTime = new Date(task.reminder_time); // Convert reminder_time to Date object

                if (Math.abs(taskTime - now) <= 60000) { // 1-minute tolerance
                    alert("Reminder: " + task.name);
                    playSound();
                }
            });
        })
        .catch(error => console.error("Error fetching tasks:", error));
}

// Play reminder sound
function playSound() {
    const audio = new Audio('/static/icicles.mp3');
    audio.play().catch(error => {
        console.log("Audio autoplay blocked. Trying with user interaction.");
        document.body.addEventListener("click", function() {
            audio.play();
        }, { once: true });
    });
}

// Check reminders every minute
setInterval(checkReminders, 60000);
