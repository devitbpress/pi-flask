const sessionId = localStorage.getItem("spiganeca10");
let sId = ``;
!sessionId ? (window.location = "/masuk") : (sId = sessionId);