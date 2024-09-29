const sessionId = localStorage.getItem("spiganeca10");
let sId = ``;
!sessionId ? (window.location = "/masuk") : (sId = sessionId);

const now = new Date();

const year = now.getFullYear();
const month = `${now.getMonth() + 1}`.padStart(2, "0");
const day = `${now.getDate()}`.padStart(2, "0");
const hours = `${now.getHours()}`.padStart(2, "0");
const minutes = `${now.getMinutes()}`.padStart(2, "0");
const seconds = `${now.getSeconds()}`.padStart(2, "0");

sId += `${year}${month}${day}${hours}${minutes}${seconds}`;

window.addEventListener("beforeunload", function (event) {
    postFetch("delete-session", { session: sId });
    event.preventDefault();
    event.returnValue = "";
});
