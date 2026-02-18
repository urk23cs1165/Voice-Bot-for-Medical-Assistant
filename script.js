const recordBtn = document.getElementById('recordBtn');
const statusText = document.getElementById('status');
const transcriptText = document.getElementById('transcript');
const symptomsList = document.getElementById('symptomsList');

recordBtn.addEventListener('click', async () => {
    // UI Feedback
    statusText.innerText = "Status: Listening for 5 seconds...";
    recordBtn.classList.add('recording');
    recordBtn.disabled = true;

    try {
        // We trigger the Python backend to start recording
        const response = await fetch('/ask', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ symptom: "trigger_mic" }) 
        });

        const data = await response.json();

        // Update UI with results
        statusText.innerText = "Status: Done!";
        transcriptText.innerText = `"${data.reply.user_said}"`;
        
        symptomsList.innerHTML = ""; // Clear old list
        data.reply.symptoms.forEach(s => {
            let li = document.createElement('li');
            li.innerText = s;
            symptomsList.appendChild(li);
        });

    } catch (error) {
        console.error("Error:", error);
        statusText.innerText = "Status: Error connecting to server";
    } finally {
        recordBtn.classList.remove('recording');
        recordBtn.disabled = false;
    }
});