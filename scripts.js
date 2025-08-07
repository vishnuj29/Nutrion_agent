function startListening() {
    const recognition = new (window.SpeechRecognition || window.webkitSpeechRecognition)();
    recognition.lang = 'en-US';
    recognition.interimResults = false;

    recognition.onresult = function (event) {
        const transcript = event.results[0][0].transcript;
        document.getElementById("dish").value = transcript;
    };

    recognition.onerror = function (event) {
        alert("Voice recognition error: " + event.error);
    };

    recognition.start();
}
