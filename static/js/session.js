const sessionId = localStorage.getItem("spiganeca10");
let sId = ``;
!sessionId ? (window.location = "/masuk") : (sId = sessionId);

window.addEventListener("beforeunload", function (event) {
    postFetch("delete-session", { session: sId });
    event.preventDefault();
    event.returnValue = "";
});
