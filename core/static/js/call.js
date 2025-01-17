const userId = document.querySelector("[data-js=user-id]")?.value;
const videoStartCallButton = document.querySelector(
  "[data-js=video-start-call-button]"
);

const videoContainerDOM = document.querySelector("[data-js=video-container]");
const localVideoDOM = document.querySelector("[data-js=video-local]");

const websocket = new WebSocket(`ws://localhost:8001/ws/meetings`);

const serversConfig = {
  iceServers: [
    {
      urls: ["stun:stun1.l.google.com:19302", "stun:stun2.l.google.com:19302"],
    },
  ],
};

const peer = new RTCPeerConnection(serversConfig);
const remoteStream = new MediaStream();

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

peer.ontrack = (event) => {
  const [remoteStream] = event.streams;

  if (!document.querySelector("#remote-video-" + remoteStream.id)) {
    const remoteVideo = document.createElement("video");

    remoteVideo.muted = false;
    remoteVideo.autoplay = true;
    remoteVideo.playsInline = true;
    remoteVideo.id = "remote-video-" + remoteStream.id;
    remoteVideo.srcObject = remoteStream;

    videoContainerDOM.appendChild(remoteVideo);
  }
};

videoStartCallButton.addEventListener("click", async function () {
  const localMediaStream = await navigator.mediaDevices.getUserMedia({
    video: true,
    audio: true,
  });

  localMediaStream.getTracks().forEach((track) => {
    peer.addTrack(track, localMediaStream);
  });

  const offer = await peer.createOffer();
  await peer.setLocalDescription(offer);

  localVideoDOM.srcObject = localMediaStream;

  websocket.send(JSON.stringify(offer));
});

websocket.onmessage = async (event) => {
  const data = JSON.parse(event.data);

  if (data.type === "offer") {
    await peer.setRemoteDescription(new RTCSessionDescription(data));

    const answer = await peer.createAnswer();

    await peer.setLocalDescription(new RTCSessionDescription(answer));

    websocket.send(JSON.stringify(answer));
  } else if (data.type === "answer") {
    console.log(data);
    await peer.setRemoteDescription(new RTCSessionDescription(data));
  } else if (data.type === "candidate") {
    await peer.addIceCandidate(new RTCIceCandidate(data.candidate));
  }
};
