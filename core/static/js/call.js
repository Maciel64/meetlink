const endCallButtonDOM = document.querySelector(
  "[data-js=video-end-call-button]"
);
const startCallButtonDOM = document.querySelector(
  "[data-js=video-start-call-button]"
);
const localVideo = document.querySelector("[data-js=video-local]");
const remoteVideo = document.querySelector("[data-js=video-remote]");
const videoContainerDOM = document.querySelector("[data-js=video-container]");

let localMediaStream = null;
let remoteMediaStream = null;

const websocket = new WebSocket("ws://localhost:8001/ws/meetings");

const serversConfig = {
  iceServers: [
    {
      urls: ["stun:stun1.l.google.com:19302", "stun:stun2.l.google.com:19302"],
    },
  ],
  iceCandidatePoolSize: 10,
};

let peer = new RTCPeerConnection(serversConfig);

startCallButtonDOM.addEventListener("click", async function () {
  localMediaStream = await navigator.mediaDevices.getUserMedia({
    audio: true,
    video: true,
  });
  remoteMediaStream = new MediaStream();
  const offerCandidates = [];

  localMediaStream.getTracks().forEach((track) => {
    peer.addTrack(track, localMediaStream);
  });

  peer.ontrack = (event) => {
    event.streams[0].getTracks().forEach((track) => {
      remoteMediaStream.addTrack(track);
    });
  };

  peer.onicecandidate((event) => {
    event.candidate && offerCandidates.push(event.candidate.toJSON());
  });

  localVideo.srcObject = localMediaStream;
  remoteVideo.srcObject = remoteMediaStream;

  const offerDescription = await peer.createOffer();
  await peer.setLocalDescription(offerDescription);

  const offer = {
    sdp: offerDescription.sdp,
    type: offerDescription.type,
  };

  websocket.send(JSON.stringify(offer));

  websocket.onmessage((event) => {
    const data = JSON.parse(event).data;

    if (peer.currentRemoteDescription && data?.answer) {
      const answerDescription = new RTCSessionDescription(data.answer);
      peer.setRemoteDescription(answerDescription);
    }
  });
});
