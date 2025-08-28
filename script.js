const socket = io();
let mediaRecorder;
let audioChunks = [];
// this is about the backend of the speech to text recognition
const startBtn = document.getElementById('startBtn');
const stopBtn = document.getElementById('stopBtn');
const chatMessages = document.getElementById('chatMessages');
const status = document.getElementById('status');

startBtn.addEventListener('click', async () => {
    const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
    mediaRecorder = new MediaRecorder(stream);
    audioChunks = [];
    mediaRecorder.ondataavailable = (e) => audioChunks.push(e.data);
    mediaRecorder.onstop = () => {
        const audioBlob = new Blob(audioChunks, { type: 'audio/webm' });
        socket.emit('audio', audioBlob);
    };
    mediaRecorder.start();
    startBtn.disabled = true;
    stopBtn.disabled = false;
    status.textContent = 'Listening...';
});
// handling the events such as mouse listener
stopBtn.addEventListener('click', () => {
    mediaRecorder.stop();
    startBtn.disabled = false;
    stopBtn.disabled = true;
    status.textContent = '';
});

socket.on('status', (data) => {
    status.textContent = data.message;
});

socket.on('chat_message', (data) => {
    const userDiv = document.createElement('div');
    userDiv.className = 'message user';
    userDiv.textContent = You: ${data.transcription};
    chatMessages.appendChild(userDiv);

    const botDiv = document.createElement('div');
    botDiv.className = 'message bot';
    botDiv.textContent = Bot: ${data.response};
    chatMessages.appendChild(botDiv);

    chatMessages.scrollTop = chatMessages.scrollHeight;
    status.textContent = '';
});

socket.on('error', (data) => {
    const errorDiv = document.createElement('div');
    errorDiv.className = 'message bot';
    errorDiv.textContent = data.message;
    chatMessages.appendChild(errorDiv);
    status.textContent = '';
});