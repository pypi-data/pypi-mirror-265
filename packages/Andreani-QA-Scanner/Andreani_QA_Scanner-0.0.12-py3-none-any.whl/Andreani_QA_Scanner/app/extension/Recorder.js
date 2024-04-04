let eventCache = null;
let accionsCache = null;
localStorage.setItem('elementContext', JSON.stringify({}));

const searchAllElements = () => {
  /**
   * Activa la busqueda de elementos y le agrega los listener para la captura de los eventos ocurridos sobre ellos.
   * @param {null}.
   * @returns {null}
   **/

  allElements = document.querySelectorAll('*:not(iframe)');
  allElements.forEach(element => {
    element.addEventListener("mousemove", handleMove, true);
    element.addEventListener("click", handleClick, true);
  });
}
handleMove = (event) => {
  /**
  * @param {event} event - evento DOM.
  * @returns {null}
  **/
  if (event.target !== eventCache) {
    let elementContext = buildXpaths(event.target.tagName.toLowerCase(), event.target);
    localStorage.setItem('elementContext', JSON.stringify(elementContext));
    eventCache = event.target;
  }
}

handleClick = () => {
  if (checkIsTextInputElement(eventCache)) {
    inputEventBackendCall(eventCache);
  }
  if (accionsCache !== "Se realizo click en... " + JSON.parse(localStorage.getItem('elementContext'))['XPATH']) {
    accionsCache = "Se realizo click en... " + JSON.parse(localStorage.getItem('elementContext'))['XPATH'];
    let payload = buildResponseBody("click", JSON.parse(localStorage.getItem('elementContext')));
    call_listener_log_events(payload);
    console.log(accionsCache);
  }
}

checkIsTextInputElement = (element) => {
  // retorna true o false si un elemento es un input element o textarea
  return (
    (element.tagName.toLowerCase() === "input" && ['text', 'password', 'number', 'email', 'tel', 'url', 'search'].includes(element.type)) ||
    (element.tagName.toLowerCase() === "input" && element.getAttribute("role") === undefined) ||
    element.tagName.toLowerCase() === "textarea" ||
    element.isContentEditable
  );
};

inputEventBackendCall = (inputElement) => {
  /**
  * Llamo al backend para avisar que se esta escribiendo en un input 
  * Llamo al backend cuando el foco deje de ser un elemento input, se envia el value del input
  * @param {object} inputElement - elemento web
  * @returns {null}
  **/
  inputElement.addEventListener("blur", function () {
    if (inputElement.value) {
      if (accionsCache !== "Escribio " + inputElement.value + " en " + buildXpaths(inputElement.tagName.toLowerCase(), inputElement)["XPATH"]) {
        accionsCache = "Escribio " + inputElement.value + " en " + buildXpaths(inputElement.tagName.toLowerCase(), inputElement)["XPATH"];
        let payload = buildResponseBody("input", buildXpaths(inputElement.tagName.toLowerCase(), inputElement), inputElement.value);
        call_listener_log_events(payload);
        console.log(accionsCache);
      }
    }
  }, true);
}

const observerConfigRecord = {
  childList: true,
  subtree: true
};

const observerRecorder = new MutationObserver(searchAllElements);

// Iniciar la observación del DOM con las opciones configuradas
observerRecorder.observe(document, observerConfigRecord);
