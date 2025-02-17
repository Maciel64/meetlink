/** Helpers */

var call = null;
var isAccessibilityShown = false;

const callId = document.querySelector("[data-js=call-id]")?.value;
const userRole = document.querySelector("[data-js=user-role]")?.value;
const callTimeoutTime = 60000;

/** DOM manipulation */
const { protocol, port, hostname } = window.location;
const wssProtocol = protocol === "https:" ? "wss://" : "ws://";
const wssPort = wssProtocol === "ws://" ? 8001 : port;
const chatSocket = new WebSocket(
  `${wssProtocol}${hostname}:${wssPort}/ws/calls`
);
const accessibilityButtonsContainerDOM = document.querySelector(
  "[data-js=accessibility-buttons-container]"
);
const buttonsContainerDOM = document.querySelector(
  "[data-js=buttons-container]"
);

const attendantEnterCallButton = document.querySelector(
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
const accessibilityButtonDOM = document.querySelector(
  "[data-js=accessibility-button]"
);
const adminEndCallButtonDOM = document.querySelector(
  "[data-js=admin-end-call-button]"
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

attendantEnterCallButton?.addEventListener(
  "click",
  handleAttendantEnterCallButtonClick
);
requestCallButtonDOM?.addEventListener("click", handleRequestCallButtonClick);
finishCallButtonDOM?.addEventListener("click", handleFinishCallButtonClick);
requestCallWithInterpreterButtonDOM?.addEventListener(
  "click",
  handleRequestCallWithInterpreterButtonClick
);
accessibilityButtonDOM?.addEventListener(
  "click",
  handleAccessibiltyButtonClick
);
adminEndCallButtonDOM?.addEventListener(
  "click",
  handleAdminFinishedCallButtonClick
);

/** Custom Functions */

function userIs(userRole, roles) {
  return roles.includes(userRole);
}

const eventHandlers = {
  MANAGER_NEEDED: async function (data) {
    if (
      attendantEnterCallButton &&
      userIs(userRole, ["SUPERADMIN", "MANAGER"])
    ) {
      attendantEnterCallButton.innerHTML =
        "Atendimento em Português solicitado";
      audioPhoneRing.play();
      enableAttendantButton();

      call = data.call;

      setTimeout(function () {
        disableAttendantButton();
        attendantEnterCallButton.innerHTML = "Chamada perdida...";
      }, callTimeoutTime);
    }
  },

  MANAGER_AND_INTERPRETER_NEEDED: function (data) {
    if (
      attendantEnterCallButton &&
      userIs(userRole, ["SUPERADMIN", "MANAGER", "INTERPRETER"])
    ) {
      enableAttendantButton();
      audioPhoneRing.play();

      if (userIs(userRole, ["SUPERADMIN", "MANAGER"])) {
        attendantEnterCallButton.innerHTML = "Atendimento em libras solicitado";
      }

      if (userRole === "INTERPRETER") {
        attendantEnterCallButton.innerHTML = "Intérprete sendo solicitado";
      }

      setTimeout(function () {
        disableAttendantButton();
        attendantEnterCallButton.innerHTML = "Chamada perdida...";
      }, callTimeoutTime);

      call = data.call;
    }
  },

  MANAGER_ENTERING: function (data) {
    if (userIs(userRole, ["MANAGER", "SUPERADMIN", "TOTEM"])) {
      return window.location.replace(
        window.location.origin + `/calls/${call.id}/in_progress`
      );
    }
  },

  INTERPRETER_ENTERING: function (data) {
    if (userIs(userRole, ["INTERPRETER"])) {
      return window.location.replace(
        window.location.origin + `/calls/${call.id}/in_progress`
      );
    }
  },

  SOMEONE_FINISHED_CALL: function (data) {
    console.log("Chegou no outro cliente");

    if (userIs(userRole, ["SUPERADMIN", "MANAGER"])) {
      window.location.replace(
        window.location.origin + `/calls/${data.call.id}`
      );
    } else if (userIs(userRole, ["TOTEM"])) {
      window.location.replace(window.location.origin + `/totem`);
    } else if (userIs(userRole, ["INTERPRETER"])) {
      window.location.replace(window.location.origin + `/dashboard`);
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
  console.error("Conexão WebSocket fechada inesperadamente", e);
}

function handleWebsocketConectionError(e) {
  console.log("Erro na conexão ", e);
}

async function handleAttendantEnterCallButtonClick() {
  attendantEnterCallButton.innerHTML = "Entrando na chamada!";
  attendantEnterCallButton.classList.remove("ring");
  const userId = document.querySelector("[data-js=user-id]").value;

  if (userIs(userRole, ["MANAGER", "SUPERADMIN"])) {
    chatSocket.send(JSON.stringify({ event: "MANAGER_ENTERING" }));
    await api.put(`/calls/${call.id}/insert_manager/`, {
      manager_id: userId,
    });
  }

  if (userIs(userRole, ["INTERPRETER"])) {
    chatSocket.send(JSON.stringify({ event: "INTERPRETER_ENTERING" }));
    await api.put(`/calls/${call.id}/insert_interpreter/`, {
      interpreter_id: userId,
    });
  }
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
  }, callTimeoutTime);
}

async function handleRequestCallWithInterpreterButtonClick() {
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
  }, callTimeoutTime);
}

async function handleFinishCallButtonClick() {
  updatedCall = await api.put(`/calls/${callId}/finish/`);
  call = updatedCall;

  chatSocket.send(JSON.stringify({ event: "SOMEONE_FINISHED_CALL", call }));

  if (userIs(userRole, ["MANAGER", "SUPERADMIN"])) {
    window.location.href = window.location.origin + `/calls/${callId}`;
  } else if (userIs(userRole, ["TOTEM"])) {
    window.location.href = window.location.origin + `/totem`;
  } else if (userIs(userRole, ["INTERPRETER"])) {
    window.location.href = window.location.origin + `/dashboard`;
  }
}

async function handleAccessibiltyButtonClick() {
  isAccessibilityShown = !isAccessibilityShown;

  if (isAccessibilityShown) {
    accessibilityButtonsContainerDOM.classList.remove("d-hidden");
    buttonsContainerDOM.classList.add("d-hidden");
  } else {
    accessibilityButtonsContainerDOM.classList.add("d-hidden");
    buttonsContainerDOM.classList.remove("d-hidden");
  }
}

async function handleAdminFinishedCallButtonClick() {
  console.log("Apertoun no botão");

  if (userIs(userRole, ["SUPERADMIN"])) {
    updatedCall = await api.put(`/calls/${callId}/finish/`);
    call = updatedCall;

    chatSocket.send(
      JSON.stringify({ event: "SOMEONE_FINISHED_CALL", call: call })
    );
  }
}

async function enableAttendantButton() {
  attendantEnterCallButton.disabled = false;
  attendantEnterCallButton.classList.add("ring");
  attendantEnterCallButton.classList.add("btn-warning");
  attendantEnterCallButton.classList.add("text-white");
  attendantEnterCallButton.classList.remove("btn-primary");
}

async function disableAttendantButton() {
  attendantEnterCallButton.disabled = true;
  attendantEnterCallButton.classList.add("btn-primary");
  attendantEnterCallButton.classList.remove("ring");
  attendantEnterCallButton.classList.remove("text-white");
  attendantEnterCallButton.classList.remove("btn-warning");
  attendantEnterCallButton.classList.remove("ring");
}
