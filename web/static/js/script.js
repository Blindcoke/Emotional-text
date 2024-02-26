function toggleMode() {
    const textMode = document.getElementById('text-mode');
    const voiceMode = document.getElementById('voice-mode');
    const switchCheckbox = document.getElementById('mode-switch');
    const modeLabel = document.getElementById('mode-text');
    if (switchCheckbox.checked) {
        textMode.style.display = 'none';
        voiceMode.style.display = 'block';
        modeLabel.innerHTML = 'Voice mode';
    } else {
        textMode.style.display = 'block';
        voiceMode.style.display = 'none';
        modeLabel.innerHTML = 'Text mode';
    }
}

const emotionMap = {
    "admiration": "😍",
    "amusement": "😄",
    "anger": "😡",
    "annoyance": "😒",
    "approval": "👍",
    "caring": "❤️",
    "confusion": "😕",
    "curiosity": "🤔",
    "desire": "😏",
    "disappointment": "😞",
    "disapproval": "👎",
    "disgust": "🤢",
    "embarrassment": "😳",
    "excitement": "😃",
    "fear": "😱",
    "gratitude": "🙏",
    "grief": "😢",
    "joy": "😂",
    "love": "❤️",
    "nervousness": "😬",
    "optimism": "😊",
    "pride": "🏆",
    "realization": "😲",
    "relief": "😅",
    "remorse": "😔",
    "sadness": "😢",
    "surprise": "😮",
};
function submitForm(){
    sentence = document.getElementById("fname").value;
    fetch('http://127.0.0.1/submit', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        }, 
        body: JSON.stringify({text: sentence})
    }).then(response => response.json())
        .then(data => {
            console.log(data.sentences);
            console.log(data.symbol_emojies);
            genereateAnswer(data);
            })
    .catch((error) => {
        console.error('Error:', error);
    });
}


buttonEnabled = true;
buttonClickTime = null;
ending = false;
audio = null


function speak() {
    if (audio != null && !audio.paused) {
        audio.pause();
    }
    audio = new Audio("/speak");
    audio.play();
}

mediaRecorder = null;
isRecording = false;

function startRecording() {
    isRecording = true;
    record();
}

function stopRecording() {
    document.getElementById("recButton").classList.add("bg-gr");
    isRecording = false;
    if(mediaRecorder !== null)
        mediaRecorder.stop();
}

function record() {
    navigator.mediaDevices.getUserMedia({ audio: true })
    .then(stream => {
        mediaRecorder = new MediaRecorder(stream);
        if (document.getElementById("realTimeCheckbox").checked) {
            mediaRecorder.start(timeslice = 1500);
            const audioChunks = [];
            mediaRecorder.addEventListener("dataavailable", event => {
                audioChunks.push(event.data);
                const partialAudioBlob = new Blob(audioChunks, { type: "audio/webm" });
                submitAudio(partialAudioBlob);

            });
        } else {
            mediaRecorder.start();
            const audioChunks = [];
            mediaRecorder.addEventListener("dataavailable", event => {
                audioChunks.push(event.data);
            });
            mediaRecorder.addEventListener('stop', () => {
                stream.getTracks().forEach(track => track.stop());
                const audioBlob = new Blob(audioChunks, {"type": "audio/webm"});
                submitAudio(audioBlob);
            });
        }
        
    });
}



function submitAudio(audioBlob) {
    if (!document.getElementById("realTimeCheckbox").checked) {
        document.getElementById("imgRec").classList.add("d-none");
        document.getElementById("spinner").classList.remove("d-none");
    }
    const formData = new FormData();
    formData.append("audioFile", audioBlob);
    const transcribeOptions = {
        method: "POST",
        body: formData,
        headers: { }
    };
    fetch('http://127.0.0.1/submit_voice', transcribeOptions)
    .then(response => response.json())
    .then(data => {
        buttonEnabled = true;
        var button = document.getElementById("recButton");
        button.removeAttribute("disabled");
        if (data.ending == true) {
            console.log(data);
            console.log("Transcribed Text:", data.partial_transcriptions);
            ending = true;
            if (!document.getElementById("realTimeCheckbox").checked) {
                document.getElementById("imgRec").classList.add("d-none");
                document.getElementById("spinner").classList.remove("d-none");
            }
            button.innerHTML = "休憩";
            button.classList.toggle("btn-light");
            button.classList.toggle("btn-info");
        }
        else {
            genereateAnswer(data);
            document.getElementById("imgRec").classList.remove("d-none");
            document.getElementById("spinner").classList.add("d-none");
            data.sentences = "";
        }

    })
    .catch(error => {
        console.error(error);
    });
}

function genereateAnswer(data) {
    const emotionsArray = [];
    document.getElementById("result").innerHTML = "";
    data.predictions.forEach((p, index) => {
        console.log(p[0].label);
        const emotionsString = p[0].label;
        emotionsArray.push(emotionsString);
        const emoji = emotionMap[emotionsString] || ".";
        var emojiOut = emoji;

        if (data.symbol_emojies && data.symbol_emojies[index]) {
            data.symbol_emojies[index] = data.symbol_emojies[index].trim();
            console.log(data.symbol_emojies[index]);
                if (data.symbol_emojies[index]== "!") {
                    if (emojiOut == ".") {
                        emojiOut = "❗️";
                    } else {
                        emojiOut += "❗️";
                    }
                } else if (data.symbol_emojies[index] == "?") {
                    if (emojiOut == ".") {
                        emojiOut = "❓";
                    } else {
                        emojiOut += "❓";
                    }
                } else if (data.symbol_emojies[index] == "...") {
                        emojiOut += "😐";

                }

        } 

        document.getElementById("result").innerHTML += data.sentences[index] + emojiOut + " "; 
        // mediaRecorder.pause();
        // mediaRecorder.resume();
    });
}


function buttonClick() {
    if (ending) {
        window.location.replace("/feedback")
    }
    else if (buttonEnabled && (!isRecording || Date.now() - buttonClickTime > 1500)) {
        var button = document.getElementById("recButton");
        button.classList.remove("bg-gr");
        // button.classList.toggle("btn-light");
        button.classList.toggle("btn-danger");
        if (isRecording) {
            stopRecording();
            buttonEnabled = false;
            button.setAttribute("disabled", "");
        }
        else {
            buttonClickTime = Date.now();
            startRecording();
        }
    }
}
// function submitAudio(audioBlob) {
//     document.getElementById("imgRec").classList.add("d-none");
//     document.getElementById("spinner").classList.remove("d-none");
//     buttonEnabled = false
//     document.getElementById("recButton").setAttribute("disabled", "");
//     const formData = new FormData();
//     formData.append("audioFile", audioBlob);
//     const transcribeOptions = {
//         method: "POST",
//         body: formData,
//         headers: { }
//     };
//     fetch('http://127.0.0.1:80/submit_voice', transcribeOptions)
//     .then(response => response.json())
//     .then(data => {
//         buttonEnabled = true;
//         var button = document.getElementById("recButton");
//         button.removeAttribute("disabled");
//         if (data.ending == true) {
//             console.log(data);
//             console.log("Transcribed Text:", data.partial_transcriptions);
//             ending = true;
//             document.getElementById("imgRec").classList.add("d-none");
//             document.getElementById("spinner").classList.remove("d-none");
//             button.innerHTML = "休憩";
//             button.classList.toggle("btn-light");
//             button.classList.toggle("btn-info");
//         }
//         else {
//             console.log(data);
//             console.log("Transcribed Text:", data.partial_transcriptions);
//             console.log("Emotions:", data.symbol_emojies);
//             const emotionsArray = [];
//             document.getElementById("result").innerHTML = "";
//             for (var i = 0; i < data.predictions.length; i++) {
//                 console.log(data.predictions[i][0].label);
//                 const emotionsString = data.predictions[i][0].label;
//                 emotionsArray.push(emotionsString);
//                 const emoji = emotionMap[emotionsString] || ".";
//                 var emojiOut = emoji;
//                 var dotCount = 0;
                
//                 if (data.symbol_emojies && data.symbol_emojies[i]) {
//                     for (var j = 0; j < data.symbol_emojies[i].length; j++) {
//                         if (data.symbol_emojies[i][j] == "!") {
//                             if (emojiOut == ".") {
//                                 emojiOut = "❗️";
//                             } else {
//                                 emojiOut += "❗️";
//                             }

//                         } else if (data.symbol_emojies[i][j] == "?") {
//                             if (emojiOut == ".") {
//                                 emojiOut = "❓";
//                             } else {
//                                 emojiOut += "❓";
//                             }
//                         } else if (data.symbol_emojies[i][j] == ".") {
//                             dotCount++;
//                             if (dotCount >= 3) {
//                                 emojiOut += "😐";
//                             } else {
//                                 emojiOut = emojiOut;
//                             }
//                         }
//                     }
//                 }else {
//                             emojiOut = emojiOut;
//                         }

//                 document.getElementById("result").innerHTML += data.sentences[i] + emojiOut + " ";
//             }
//             document.getElementById("imgRec").classList.remove("d-none");
//             document.getElementById("spinner").classList.add("d-none");
//         }

//     })
//     .catch(error => {
//         console.error(error);
//     });
// }