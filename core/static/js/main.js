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

/** Custom Functions */

const eventHandlers = {
  MANAGER_NEEDED: async function (data) {
    if (managerEnterCallButton) {
      managerEnterCallButton.disabled = false;
      managerEnterCallButton.innerHTML = "Gerente sendo solicitado!";
      managerEnterCallButton.classList.add("ring");
      audioPhoneRing.play();

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
  await api.put(`/calls/${call.id}/insert_manager/`, { manager_id: userId });
}

async function handleRequestCallButtonClick() {
  call = await api.post("/calls/");
  chatSocket.send(JSON.stringify({ event: "MANAGER_NEEDED", call: call }));
}

async function handleFinishCallButtonClick() {
  updatedCall = await api.put(`/calls/${callId}/finish/`);
  call = updatedCall;
  chatSocket.send(JSON.stringify({ event: "MANAGER_FINISHED_CALL" }));
  window.location.href = window.location.origin + `/calls/${callId}`;
}
