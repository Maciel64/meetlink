const videoStartCallButton = document.querySelector(
  "[data-js=video-start-call-button]"
);

const websocket = new WebSocket("ws://localhost:8001/ws/meetings");

const serversConfig = {
  iceServers: [
    {
      urls: ["stun:stun1.l.google.com:19302", "stun:stun2.l.google.com:19302"],
    },
  ],
};

let peer = new RTCPeerConnection(serversConfig);
let localMediaStream = null;
let remoteMediaStream = new MediaStream();

const localVideo = document.querySelector("[data-js=video-local]");
const remoteVideo = document.querySelector("[data-js=video-remote]");

peer.ontrack = (event) => {
  event.streams[0].getTracks().forEach((track) => {
    remoteMediaStream.addTrack(track);
  });
  remoteVideo.srcObject = remoteMediaStream;
};

peer.onicecandidate = (event) => {
  if (event.candidate) {
    websocket.send(
      JSON.stringify({
        type: "candidate",
        candidate: event.candidate,
      })
    );
  }
};

videoStartCallButton.addEventListener("click", async () => {
  localMediaStream = await navigator.mediaDevices.getUserMedia({
    video: true,
    audio: true,
  });

  localMediaStream.getTracks().forEach((track) => {
    peer.addTrack(track, localMediaStream);
  });

  localVideo.srcObject = localMediaStream;

  const offer = await peer.createOffer();
  await peer.setLocalDescription(offer);

  websocket.send(
    JSON.stringify({
      type: "offer",
      offer: peer.localDescription,
    })
  );
});

websocket.onmessage = async (event) => {
  const data = JSON.parse(event.data);

  if (data.type === "offer") {
    await peer.setRemoteDescription(new RTCSessionDescription(data.offer));

    const answer = await peer.createAnswer();
    await peer.setLocalDescription(answer);

    websocket.send(
      JSON.stringify({
        type: "answer",
        answer: peer.localDescription,
      })
    );
  } else if (data.type === "answer") {
    await peer.setRemoteDescription(new RTCSessionDescription(data.answer));
  } else if (data.type === "candidate") {
    await peer.addIceCandidate(new RTCIceCandidate(data.candidate));
  }
};
