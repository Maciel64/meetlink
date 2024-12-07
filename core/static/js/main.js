const chatSocket = new WebSocket(
  "ws://" + window.location.hostname + ":8001" + "/ws/calls"
);
const requestCallButtonDOM = document.querySelector(
  "[data-js=request-call-button]"
);
const enterCallButton = document.querySelector("[data-js=enter-call-button]");

const audioPhoneRing = document.querySelector("[data-js=audio-phone-ring]");
const managerMeetingFrame = document.querySelector(
  "[data-js=manager-call-frame]"
);

const managerEnterCallButton = document.querySelector(
  "[data-js=manager-enter-call-button]"
);

/** Server sent events */

chatSocket.onmessage = function (e) {
  const data = JSON.parse(e.data);

  if (data.event == "MANAGER_NEEDED") {
    if (enterCallButton) {
      enterCallButton.disabled = false;
      enterCallButton.innerHTML = "Gerente sendo solicitado!";
      enterCallButton.classList.add("ring");
      audioPhoneRing.play();
    }
  }

  console.log("Mensagem recebida do outro cliente:", data.event);
};

chatSocket.onclose = function (e) {
  console.error("Conexão WebSocket fechada inesperadamente");
};

chatSocket.onerror = function (e) {
  console.log("Erro na conexão ", e);
};

/** Client side events */

requestCallButtonDOM?.addEventListener("click", function () {
  chatSocket.send(JSON.stringify({ event: "MANAGER_NEEDED" }));
});

enterCallButton?.addEventListener("click", function () {
  enterCallButton.innerHTML = "Entrando na chamada!";
  enterCallButton.classList.remove("ring");
  chatSocket.send(JSON.stringify({ event: "MANAGER_ENTERING" }));
});

managerEnterCallButton?.addEventListener("click", function () {
  managerMeetingFrame.src =
    managerEnterCallButton.getAttribute("data-meet-url");
});
