const chatSocket = new WebSocket(
  "ws://" + window.location.hostname + ":8001" + "/ws/calls"
);
const requestCallButtonDOM = document.querySelector(
  "[data-js=request-call-button]"
);

const testButton = document.querySelector("[data-js=testButton]");

testButton.addEventListener("click", () => {
  chatSocket.send(JSON.stringify({ message: "TEstabdi" }));
});

chatSocket.onmessage = function (e) {
  const data = JSON.parse(e.data);
  console.log("Mensagem recebida do outro cliente:", data.message);
};

chatSocket.onclose = function (e) {
  console.error("Conexão WebSocket fechada inesperadamente");
};

chatSocket.onerror = function (e) {
  console.log("Erro na conexão ", e);
};

requestCallButtonDOM.addEventListener("click", function () {
  const message = "Mensagem do botão!";
  chatSocket.send(JSON.stringify({ message: message }));
});
