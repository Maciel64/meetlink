const chatSocket = new WebSocket(
  "ws://" + window.location.hostname + ":8001" + "/ws/calls"
);
const managerEnterCallButton = document.querySelector(
  "[data-js=manager-enter-call-button]"
);
const requestCallButtonDOM = document.querySelector(
  "[data-js=request-call-button]"
);

const audioPhoneRing = document.querySelector("[data-js=audio-phone-ring]");

/** Server sent events */

chatSocket.onmessage = handleEventIncoming;
chatSocket.onclose = handleWebsocketConectionClosed;
chatSocket.onerror = handleWebsocketConectionError;

/** Client side events */

managerEnterCallButton?.addEventListener("click", handleManagerEnterCallButton);
requestCallButtonDOM?.addEventListener("click", handleRequestCallButtonClick);

/** Custom Functions */

const eventHandlers = {
  MANAGER_NEEDED: function () {
    if (managerEnterCallButton) {
      managerEnterCallButton.disabled = false;
      managerEnterCallButton.innerHTML = "Gerente sendo solicitado!";
      managerEnterCallButton.classList.add("ring");
      audioPhoneRing.play();
    }
  },

  MANAGER_ENTERING: function () {
    console.log("Manager Entering");
  },
};

function handleEventIncoming(e) {
  const event = JSON.parse(e.data).event;
  const eventIsNotInHandlers = !(event in eventHandlers);

  if (eventIsNotInHandlers) {
    return console.error("Evento não registrado: ", event);
  }

  eventHandlers[event]();
  console.log("Mensagem recebida do outro cliente:", event);
}

function handleWebsocketConectionClosed(e) {
  console.error("Conexão WebSocket fechada inesperadamente");
}

function handleWebsocketConectionError(e) {
  console.log("Erro na conexão ", e);
}

function handleManagerEnterCallButton() {
  managerEnterCallButton.innerHTML = "Entrando na chamada!";
  managerEnterCallButton.classList.remove("ring");
  chatSocket.send(JSON.stringify({ event: "MANAGER_ENTERING" }));
}

function handleRequestCallButtonClick() {
  chatSocket.send(JSON.stringify({ event: "MANAGER_NEEDED" }));
}
