const eventSource = new EventSource('/subtitles/update');

        // Écouter les mises à jour des sous-titres
        eventSource.onmessage = function(event) {
            const data = JSON.parse(event.data);
            const subtitleElement = document.getElementById("subtitle");
            subtitleElement.innerHTML = ""
            if(data.type == "louanges"){
                subtitleElement.textContent = data.subtitle;
            }
            else if(data.type == "versets"){
                const refContainer = document.createElement('h3');
                const versetsContainer = document.createElement('p');
                refContainer.textContent = data.ref;
                versetsContainer.textContent = data.versets
                subtitleElement.appendChild(refContainer);
                subtitleElement.appendChild(versetsContainer);
            }
            else{
                console.error(data);
            }
        };

        eventSource.onerror = function(event) {
            console.error('EventSource failed:', event);
        };