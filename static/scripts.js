document.getElementById('stage_msg').addEventListener('submit', function(event) {
    event.preventDefault();

    const userInput = document.getElementById('user-stage-msg').value;
    const buttonId = event.submitter.id;

    if(buttonId == "send"){
        fetch('/stage/send_msg', {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ user_input: userInput })
        })

        .then(response => response.json())
        .then(data => {
            const resultContainer = document.getElementById('result-container');
            resultContainer.innerHTML = data.result ? "" : "Erreur, message non enovyé";
        })
        .catch(error => {
            console.error('Erreur:', error);
        });
    }
    else if(buttonId == "delete"){
        fetch('/stage/delete_msg', {
            method: 'DELETE',
            headers: {
                'Content-Type': 'application/json',
            }
        })
        .then(response => response.json())
        .then(data => {
            const resultContainer = document.getElementById('result-container');
            var pl = document.getElementById('user-stage-msg');
            if(data.result){
                resultContainer.innerHTML =  '';
                pl.placeholder = 'Envoyer msg prompteur';
            }
            else{
                resultContainer.innerHTML =  "Erreur, message non supprimé";
            }
        })
        .catch(error => {
            console.error('Erreur:', error);
        });
    }
});

document.getElementById('submit-button').addEventListener('click', () => {
    const name = document.getElementById('clock_name').value;
    const hours = document.getElementById('hours').value;
    const minutes = document.getElementById('minutes').value;
    const seconds = document.getElementById('seconds').value;

    const timeData = {
        clock_name: name,
        hours: hours,
        minutes: minutes,
        seconds: seconds
    };

    fetch('/timer', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(timeData)
    })
    .then(response => response.json())
    .then(data => {
        console.log('Résultat pour ajout clock: ', data);
    })
    .catch((error) => {
        console.error('Error:', error);
    });
});

function fetchStreamData() {
    const eventSource = new EventSource('/current_status_stream');
    const timeContainer = document.getElementById('time-container');
    const messageContainer = document.getElementById('stage-message-container');
    const clockContainer = document.getElementById('clock-container');
    const videoContainer = document.getElementById('video-container');

    eventSource.onmessage = function(event) {
        try {
            const data = JSON.parse(event.data);
            if(data.url == "timer/system_time"){
                var date = new Date(data.data * 1000);
                var hours = date.getHours();
                var minutes = date.getMinutes();
                var seconds = date.getSeconds();
                const formattedTime = `${hours.toString().padStart(2, '0')}:${minutes.toString().padStart(2, '0')}:${seconds.toString().padStart(2, '0')}`;
                timeContainer.innerHTML = "Heure: " + formattedTime;
            }
            else if(data.url == "stage/message"){
                messageContainer.innerHTML = "Message prompteur: " + data.data;
            }
            else if(data.url == "timers/current"){
                clockContainer.innerHTML= "";
                for(const timer of data.data){
                    const h3Element = document.createElement('h3');
                    const clockName = document.createTextNode(`${timer.id.name}: `);
                    const time = document.createElement('span');
                    time.textContent = `${timer.time}`;
                    
                    switch (timer.state) {
                        case 'running':
                            time.classList.add('status-running');
                            break;
                        case 'overrunning':
                            time.classList.add('status-overrun');
                            break;
                        case 'overran':
                            time.classList.add('status-overrun');
                            break;
                        case 'stopped':
                            time.classList.add('status-stopped');
                            break;
                        default:
                            break;
                    }

                    const delete_timer = document.createElement('button');
                    const delete_icon = document.createElement('i');
                    delete_icon.classList.add('fa-solid', 'fa-trash');
                    delete_timer.appendChild(delete_icon);
                    delete_timer.classList.add('button-container');
                    delete_timer.addEventListener('click', () => deleteTimer(timer.id.uuid));

                    const pause_timer = document.createElement('button');
                    pause_timer.classList.add('button-container');
                    if(timer.state != "stopped"){
                        const pause_icon = document.createElement('i');
                        pause_icon.classList.add('fa-solid', 'fa-stop');
                        pause_timer.appendChild(pause_icon);
                        pause_timer.addEventListener('click', () => pauseTimer(timer.id.uuid));
                    }
                    else{
                        const play_icon = document.createElement('i');
                        play_icon.classList.add('fa-solid', 'fa-play');
                        pause_timer.appendChild(play_icon);
                        pause_timer.addEventListener('click', () => playTimer(timer.id.uuid));
                    }

                    const reset_timer = document.createElement('button');
                    reset_timer.classList.add('button-container');
                    const reset_icon = document.createElement('i');
                    reset_icon.classList.add('fa-solid', 'fa-rotate');
                    reset_timer.appendChild(reset_icon);
                    reset_timer.addEventListener('click', () => resetTimer(timer.id.uuid));

                    const buttonsContainer = document.createElement('div');
                    buttonsContainer.classList.add('buttons-container');
                    buttonsContainer.appendChild(pause_timer);
                    buttonsContainer.appendChild(reset_timer);
                    buttonsContainer.appendChild(delete_timer);
            
                    h3Element.appendChild(clockName);
                    h3Element.appendChild(time);
                    clockContainer.appendChild(h3Element);
                    clockContainer.appendChild(buttonsContainer);
                }
            }
            else if(data.url == "timer/video_countdown"){
                videoContainer.innerHTML = "";
                vTimer = data.data
                if(vTimer != "0:00:00"){
                    const time = document.createElement('span');
                    time.textContent = `${vTimer}`;
                    const clockName = document.createTextNode(`Temps restant vidéo: `);                    
                    if(parseInt(vTimer.slice(-2)) < 11){
                        time.classList.add('blinking');
                    }
                    else{
                        time.classList.remove('blinking');
                    }
                    videoContainer.appendChild(clockName);
                    videoContainer.appendChild(time);
                }
            }
        } catch (error) {
            console.error('Failed to parse JSON:', error);
        }
    };

    eventSource.onerror = function(event) {
        console.error('EventSource failed:', event);
        timeContainer.innerHTML ="PROPRESENTER NON CONNECTE";
        timeContainer.classList.add('ALERT');
        eventSource.close();
    };

    eventSource.onopen = function(event) {
        console.log('EventSource opened');
    };
}

function pauseTimer(uuid) {
    fetch(`/timer/pause/${uuid}`, {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json',
        }
    })

    .then(response => response.json())
    .then(data => {
        console.log(`pause_timer: ${data.result}`);
    })
    .catch(error => {
        console.error('Erreur:', error);
    });
}

function playTimer(uuid) {
    fetch(`/timer/play/${uuid}`, {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json',
        }
    })

    .then(response => response.json())
    .then(data => {
        console.log(`play_timer: ${data.result}`);
    })
    .catch(error => {
        console.error('Erreur:', error);
    });
}

function resetTimer(uuid) {
    fetch(`/timer/reset/${uuid}`, {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json',
        }
    })

    .then(response => response.json())
    .then(data => {
        console.log(`reset_timer: ${data.result}`);
    })
    .catch(error => {
        console.error('Erreur:', error);
    });
}

function deleteTimer(uuid) {
    fetch(`/timer/${uuid}`, {
        method: 'DELETE',
        headers: {
            'Content-Type': 'application/json',
        }
    })

    .then(response => response.json())
    .then(data => {
        console.log(`delete_timer: ${data.result}`);
    })
    .catch(error => {
        console.error('Erreur:', error);
    });
}

// Appeler la fonction fetchStreamData une fois au chargement de la page
fetchStreamData();
