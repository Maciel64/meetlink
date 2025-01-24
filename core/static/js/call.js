const userId =
  generateUUID(); /* document.querySelector("[data-js=user-id]")?.value; */

const videoStartCallButton = document.querySelector(
  "[data-js=video-start-call-button]"
);
const videoContainerDOM = document.querySelector("[data-js=video-container]");
const localVideoDOM = document.querySelector("[data-js=video-local]");
const showPeersButton = document.querySelector("[data-js=show-peers]");

const serversConfig = {
  iceServers: [
    {
      urls: ["stun:stun1.l.google.com:19302", "stun:stun2.l.google.com:19302"],
    },
  ],
};

var peers = {};
let localStream = new MediaStream();
let websocket;

let userMedia = navigator.mediaDevices
  .getUserMedia({ audio: true, video: true })
  .then((stream) => {
    localStream = stream;
    localVideoDOM.srcObject = localStream;
  })
  .catch((error) => window.alert(error));

function generateUUID() {
  return "xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx".replace(/[xy]/g, function (c) {
    const r = (Math.random() * 16) | 0;
    const v = c === "x" ? r : (r & 0x3) | 0x8;
    return v.toString(16);
  });
}

function sendSignal(type, body) {
  websocket.send(JSON.stringify({ type, senderId: userId, ...body }));
}

function addLocalTracks(peer) {
  localStream.getTracks().forEach((track) => peer.addTrack(track, localStream));
}

function createVideo(senderId) {
  if (
    !document.querySelector(`[data-remote-video-user=${CSS.escape(senderId)}]`)
  ) {
    const remoteVideo = document.createElement("video");

    remoteVideo.muted = false;
    remoteVideo.autoplay = true;
    remoteVideo.playsInline = true;
    remoteVideo.setAttribute("data-remote-video-user", senderId);

    if (senderId != userId) {
      videoContainerDOM.appendChild(remoteVideo);
    }

    return remoteVideo;
  }
}

function setOnTrack(peer, remoteVideo) {
  const remoteMediaStream = new MediaStream();

  remoteVideo.srcObject = remoteMediaStream;

  peer.addEventListener("track", async function (event) {
    remoteMediaStream.addTrack(event.track, remoteMediaStream);
  });
}

async function createOffer(senderId, channel) {
  const peer = new RTCPeerConnection(serversConfig);

  addLocalTracks(peer);

  const remoteVideo = createVideo(senderId);

  setOnTrack(peer, remoteVideo);

  peers[senderId] = [peer];

  peer.addEventListener("iceconnectionstatechange", function (event) {
    const iceState = peer.iceConnectionState;

    if (["failed", "disconnected", "closed"].includes(iceState)) {
      delete peers[senderId];

      if (iceState != "closed") {
        peer.close();
      }

      remoteVideo.remove();
    }
  });

  peer.addEventListener("icecandidate", function (event) {
    if (event.candidate) return;

    sendSignal("offer", {
      sdp: peer.localDescription,
      channel: channel,
    });
  });

  const offer = await peer.createOffer();

  peer.setLocalDescription(offer);
}

async function createAnswer(offer, senderId, channel) {
  const peer = new RTCPeerConnection(serversConfig);

  addLocalTracks(peer);

  const remoteVideo = createVideo(senderId);

  setOnTrack(peer, remoteVideo);

  peers[senderId] = [peer];

  peer.addEventListener("iceconnectionstatechange", function (event) {
    const iceState = peer.iceConnectionState;

    if (["failed", "disconnected", "closed"].includes(iceState)) {
      delete peers[senderId];

      if (iceState != "closed") {
        peer.close();
      }

      remoteVideo.remove();
    }
  });

  peer.addEventListener("icecandidate", function (event) {
    if (event.candidate) return;

    sendSignal("answer", {
      sdp: peer.localDescription,
      channel: channel,
    });
  });

  peer.setRemoteDescription(offer);

  const answer = await peer.createAnswer();

  peer.setLocalDescription(answer);
}

videoStartCallButton.addEventListener("click", function () {
  const { protocol, port, hostname } = window.location;
  const wssProtocol = protocol === "https:" ? "wss://" : "ws://";
  const wssPort = wssProtocol === "ws://" ? 8001 : port;
  websocket = new WebSocket(`${wssProtocol}${hostname}:${wssPort}/ws/meetings`);

  websocket.addEventListener("open", function () {
    sendSignal("join", {});
  });

  websocket.addEventListener("message", function (event) {
    const { type, senderId, sdp, channel } = JSON.parse(event.data);

    if (type === "join") {
      createOffer(senderId, channel);
    } else if (type === "offer") {
      createAnswer(sdp, senderId, channel);
    } else if (type === "answer") {
      const peer = peers[senderId][0];

      peer.setRemoteDescription(sdp);
    }
  });
});
