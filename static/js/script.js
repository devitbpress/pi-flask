// set up parameters
let idProgress = 1;
let sInterval = {};

// post file
const postFiles = async (agUrl, agFile, agId) => {
    const formData = new FormData();
    formData.append("file", agFile);
    formData.append("file_id", agId);
    formData.append("session", sId);

    try {
        const response = await fetch(agUrl, { method: "POST", body: formData });

        const data = await response.json();
        const { ok, statusText } = response;

        if (ok) {
            return ["success", data];
        } else {
            return ["error", statusText || data];
        }
    } catch (error) {
        return ["error", error.message || error];
    }
};

// post data
const postFetch = async (agU, agD) => {
    try {
        const response = await fetch(agU, { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify(agD) });

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        const data = await response.json();

        return data;
    } catch (error) {
        return ["error", error];
    }
};

// progres bar
const progresBarStatus = (agId) => {
    try {
        document.getElementById(`width-${agId}`).style.width = `100%`;
        document.getElementById(`bar-${agId}`).textContent = `100%`;
    } catch (error) {
        console.error("Error setting progress bar width or text:", error);
    }

    setTimeout(() => {
        try {
            document.getElementById(`box-${agId}`).classList.add("scale-0");
            setTimeout(() => document.getElementById(`box-${agId}`).remove(), 150);
        } catch (error) {
            console.error("Error removing progress bar element:", error);
        }
    }, 250);
};

const progresBar = (agTM, agBM, agT) => {
    const elementProgress = document.getElementById("progress");
    const idProgressNow = idProgress;

    const content = `<div id="box-${idProgressNow}" class="w-full flex flex-col bg-white shadow border px-2 py-1 rounded gap-1 origin-right duration-300"><h1 class="py-1 text-sm font-medium">${agTM}</h1><span id="span-subtitle-${idProgressNow}">${agBM}</span><div class="w-[15rem] flex gap-2 items-center"><div class="w-full h-3 relative"><div class="w-full h-full rounded bg-blue-700"></div><div id="width-${idProgressNow}" class="w-1 h-full rounded bg-green-600 absolute top-0 left-0"></div></div><div id="bar-${idProgressNow}" class="whitespace-nowrap">0%</div></div></div>`;
    elementProgress.innerHTML += content;

    let number = 0;
    sInterval[idProgressNow] = "run";
    idProgress += 1;

    const interval = setInterval(() => {
        try {
            document.getElementById(`width-${idProgressNow}`).style.width = `${number}%`;
            document.getElementById(`bar-${idProgressNow}`).textContent = `${number}%`;
        } catch (error) {
            clearInterval(interval);
        }

        number += 1;

        sInterval[idProgressNow] === "done" ? (clearInterval(interval), progresBarStatus(idProgressNow)) : void 0;

        if (number > 95) {
            clearInterval(interval);
            sInterval[idProgressNow] = "done";
        }
    }, agT / 100);

    return idProgressNow;
};
