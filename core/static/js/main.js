/** Helpers */

var call = null;

const callId = document.querySelector("[data-js=call-id]")?.value;
const userRole = document.querySelector("[data-js=user-role]")?.value;

/** DOM manipulation */

const protocol = window.location.protocol === "https:" ? "wss://" : "ws://";
const chatSocket = new WebSocket(
  protocol + window.location.hostname + ":8001" + "/ws/calls"
);
const managerEnterCallButton = document.querySelector(
  "[data-js=manager-enter-call-button]"
);
const requestCallButtonDOM = document.querySelector(
  "[data-js=request-call-button]"
);
const requestCallWithInterpreterButtonDOM = document.querySelector(
  "[data-js=request-interpreter-call-button]"
);
const finishCallButtonDOM = document.querySelector(
  "[data-js=video-finish-call-button]"
);

const audioPhoneRing = document.querySelector("[data-js=audio-phone-ring]");

/** Requests service */

function getCookie(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== "") {
    const cookies = document.cookie.split(";");
    for (let i = 0; i < cookies.length; i++) {
      const cookie = cookies[i].trim();
      if (cookie.substring(0, name.length + 1) === name + "=") {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}

const api = {
  baseUrl: window.location.origin + "/api",

  get: async function (url) {
    const response = await fetch(this.baseUrl + url);
    return response.json();
  },

  post: async function (url, data) {
    const csrftoken = getCookie("csrftoken");
    const response = await fetch(this.baseUrl + url, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "X-CSRFToken": csrftoken,
      },
      body: JSON.stringify(data),
    });
    return response.json();
  },

  put: async function (url, data) {
    const csrftoken = getCookie("csrftoken");
    const response = await fetch(this.baseUrl + url, {
      method: "PUT",
      headers: {
        "Content-Type": "application/json",
        "X-CSRFToken": csrftoken,
      },
      body: JSON.stringify(data),
    });
    return response.json();
  },
};

/** Server sent events */

const initialTime = new Date();

chatSocket.onmessage = handleEventIncoming;
chatSocket.onclose = handleWebsocketConectionClosed;
chatSocket.onerror = handleWebsocketConectionError;
chatSocket.onopen = () =>
  console.log(
    "Conectado no servidor websockets => Levou " +
      (new Date() - initialTime + " ms")
  );

/** Client side events */

managerEnterCallButton?.addEventListener("click", handleManagerEnterCallButton);
requestCallButtonDOM?.addEventListener("click", handleRequestCallButtonClick);
finishCallButtonDOM?.addEventListener("click", handleFinishCallButtonClick);
requestCallWithInterpreterButtonDOM?.addEventListener(
  "click",
  handleRequestCallWithInterpreter
);

/** Custom Functions */

const eventHandlers = {
  MANAGER_NEEDED: async function (data) {
    if (
      managerEnterCallButton &&
      ["SUPERADMIN", "MANAGER"].includes(userRole)
    ) {
      managerEnterCallButton.disabled = false;
      managerEnterCallButton.innerHTML = "Gerente sendo solicitado!";
      managerEnterCallButton.classList.add("ring");
      audioPhoneRing.play();

      call = data.call;
    }
  },

  MANAGER_AND_INTERPRETER_NEEDED: function (data) {
    if (
      managerEnterCallButton &&
      ["SUPERADMIN", "MANAGER", "INTERPRETER"].includes(userRole)
    ) {
      console.log(data);
      managerEnterCallButton.disabled = false;
      managerEnterCallButton.classList.add("ring");
      audioPhoneRing.play();

      if (userRole === "MANAGER") {
        managerEnterCallButton.innerHTML = "Gerente sendo solicitado";
      }

      if (userRole === "INTERPRETER") {
        managerEnterCallButton.innerHTML = "Intérprete sendo solicitado";
      }

      console.log(call);

      call = data.call;
    }
  },

  MANAGER_ENTERING: function (data) {
    window.location.replace(
      window.location.origin + `/calls/${call.id}/in_progress`
    );
  },

  MANAGER_FINISHED_CALL: function (data) {
    if (userRole.includes("SUPERADMIN", "MANAGER")) {
      window.location.replace(window.location.origin + `/calls/${call.id}`);
    } else if (userRole.includes("TOTEM")) {
      window.location.replace(window.location.origin + `/totem`);
    }
  },
};

function handleEventIncoming(e) {
  const data = JSON.parse(e.data);
  const eventIsNotInHandlers = !(data.event in eventHandlers);

  if (eventIsNotInHandlers) {
    return console.error("Evento não registrado: ", event);
  }

  eventHandlers[data.event](data);
}

function handleWebsocketConectionClosed(e) {
  console.error("Conexão WebSocket fechada inesperadamente");
}

function handleWebsocketConectionError(e) {
  console.log("Erro na conexão ", e);
}

async function handleManagerEnterCallButton() {
  managerEnterCallButton.innerHTML = "Entrando na chamada!";
  managerEnterCallButton.classList.remove("ring");

  chatSocket.send(JSON.stringify({ event: "MANAGER_ENTERING" }));

  const userId = document.querySelector("[data-js=user-id]").value;
  await api.put(`/calls/${call.id}/insert_interpreter/`, {
    interpreter_id: userId,
  });
}

async function handleRequestCallButtonClick() {
  requestCallButtonDOM.disabled = true;
  requestCallWithInterpreterButtonDOM.disabled = true;
  requestCallButtonDOM.innerHTML = "Chamando atendente";

  call = await api.post("/calls/");
  chatSocket.send(JSON.stringify({ event: "MANAGER_NEEDED", call: call }));

  setTimeout(function () {
    requestCallButtonDOM.disabled = false;
    requestCallWithInterpreterButtonDOM.disabled = false;
    requestCallButtonDOM.innerHTML = "Solicitar atendente";
  }, 10000);
}

async function handleRequestCallWithInterpreter() {
  requestCallButtonDOM.disabled = true;
  requestCallWithInterpreterButtonDOM.disabled = true;
  requestCallWithInterpreterButtonDOM.innerHTML =
    "Chamando atendimento em libras";

  call = await api.post("/calls/");
  chatSocket.send(
    JSON.stringify({ event: "MANAGER_AND_INTERPRETER_NEEDED", call: call })
  );

  setTimeout(function () {
    requestCallButtonDOM.disabled = false;
    requestCallWithInterpreterButtonDOM.disabled = false;
    requestCallWithInterpreterButtonDOM.innerHTML = "Atendimento em libras";
  }, 10000);
}

async function handleFinishCallButtonClick() {
  updatedCall = await api.put(`/calls/${callId}/finish/`);
  call = updatedCall;
  chatSocket.send(JSON.stringify({ event: "MANAGER_FINISHED_CALL" }));
  window.location.href = window.location.origin + `/calls/${callId}`;
}
