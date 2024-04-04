buildResponseBody = (callName, myElement, value = null) => {
    /**
    * Dependiendo del parametro recibido se genera el payload a enviar al backend
    * @param {string} callName 
    * @returns {Object|null} 
    **/
    return {
        // si se llama tanto del recorder con un evento click o input, o si se esta utilizando en modo inspector
        event: callName,
        target: myElement,
        value: value,
        frame: myElement["FRAME"]
    };
};

call_listener_log_events = (payload) => {
    /**
    * Realiza una peticion al backend enviando el payload del evento.
    * @param {string} payload  
    * @returns {null}
    **/ 
    const myHeaders = new Headers();
    myHeaders.append("Content-Type", "application/json");
    const requestOptions = {
        method: 'POST',
        headers: myHeaders,
        body: JSON.stringify(payload),
        redirect: 'follow'
    };
    let eventsUrl = "http://127.0.0.1:30505/api/events";
    fetch(eventsUrl, requestOptions)
        .then(response => response.text())
        .then(result => console.log(result))
        .catch(error => console.log('error', error));
}


// Escucha un evento para realizar el escaneo.
document.addEventListener("runScann", function () {
    scann();
  });

// Escucha un evento para realizar el escaneo.
document.addEventListener("runAxe", function () {
    runAxe();
  });

// Escucha un evento para realizar el escaneo.
document.addEventListener("runMonkeyTest", function () {
    monkeyTest();
  });
