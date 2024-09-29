// set up parameters
const url = new URL(window.location.href);
const urlParams = new URLSearchParams(window.location.search);
const btnChevron = document.getElementById("btn-chevron");
const childTools = document.getElementById("child-tools");

let miniNavIndikacator = { status: false, nav: "13rem", tools: "13rem" };
let idProgress = 1;
let sInterval = {};
let gridApi;
let idNotif = 1;
let columnDefs = {};

// post file
const postFiles = async (agUrl, agFile, agId, agModel) => {
    const formData = new FormData();
    formData.append("file", agFile);
    formData.append("file_id", agId);
    formData.append("session", sId);
    formData.append("model", agModel);

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

// progress
const progress = (agH, agS) => {
    const elementProgress = document.getElementById("progress");
    const idProgressNow = idProgress;

    elementProgress.innerHTML += `<div id="box-${idProgressNow}" class="w-full flex flex-col bg-white shadow border px-2 py-1 rounded gap-1 origin-right duration-300">
            <h1 class="py-1 text-sm font-medium">${agH}</h1>
            <span id="span-subtitle-${idProgressNow}">${agS}</span>
            <div class="w-[15rem] flex gap-2 items-center">
                <div class="w-full h-3 relative">
                    <div class="w-full h-full rounded bg-blue-700"></div>
                    <div id="width-${idProgressNow}" class="w-1 h-full rounded bg-green-600 absolute top-0 left-0"></div>
                </div>
                <div id="bar-${idProgressNow}" class="whitespace-nowrap">0%</div>
            </div>
        </div>`;

    idProgress += 1;

    return { width: `width-${idProgressNow}`, bar: `bar-${idProgressNow}`, box: `box-${idProgressNow}`, span: `span-subtitle-${idProgressNow}` };
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

// fungsi pertama progres bar
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

// notifikasi
const notification = (agS, agE, agSt) => {
    const notif = document.getElementById("notification");
    const notifNow = idNotif;
    const status = { success: "done-green.png", failed: "error-red.png" };

    if (agS === "show") {
        notif.innerHTML += `
            <div id="notif-${notifNow}" class="px-2 py-1 flex items-center gap-2 bg-white border rounded scale-0 origin-right duration-300">
                <img src="./static/assets/${status[agSt]}" alt="${agSt}" class="h-5 w-fit cursor-pointer" />
                ${agE}
            </div>
        `;

        idNotif += 1;
        setTimeout(() => {
            document.getElementById(`notif-${notifNow}`).classList.remove("scale-0");
        }, 150);
    } else {
        const elementDelete = document.getElementById(`${agE}`);
        elementDelete.classList.add("scale-0");
        setTimeout(() => elementDelete.remove(), 150);
    }

    setTimeout(() => {
        try {
            notification("hide", `notif-${notifNow}`);
        } catch (error) {
            void 0;
        }
    }, 5000);
};

// aggrid
const setupAggrid = async (agData, agCol, agView) => {
    const eGrid = document.getElementById("aggrid-website");
    const cGrid = document.querySelectorAll(".ag-header-cell-label");

    let rowData = [];

    try {
        rowData = agData.map((item) => {
            return Object.entries(item).reduce((acc, entry) => {
                if (entry[0].toLowerCase().includes("date")) {
                    const dateObj = new Date(entry[1]);
                    const year = dateObj.getFullYear();
                    const month = String(dateObj.getMonth() + 1).padStart(2, "0");
                    const day = String(dateObj.getDate()).padStart(2, "0");
                    acc[entry[0]] = `${year}-${month}-${day}`;
                } else {
                    acc[entry[0]] = entry[1];
                }
                return acc;
            }, {});
        });
    } catch (error) {
        rowData = agData;
    }

    defaultColDef = { flex: 1 };

    const gridOptions = {
        pagination: true,
        paginationPageSize: 50,
        paginationPageSizeSelector: [50, 100, 500, 1000, 5000],
        columnDefs: agCol,
        rowData: rowData,
        defaultColDef: defaultColDef,
    };

    eGrid.innerHTML = "";
    gridApi = agGrid.createGrid(eGrid, gridOptions);

    document.querySelector(".ag-paging-panel").classList.add("text-xs");
    document.querySelector(".ag-paging-panel").style.height = "35px";
    setLoading(agView);
    cGrid.forEach((element) => (element.textContent.trim() === "Total" ? element.classList.add("justify-end", "pr-5") : ""));
};

// addon aggrid
const setLoading = (value) => gridApi.setGridOption("loading", value);
const downloadCsv = () => gridApi.exportDataAsCsv();
const searchData = (agV) => gridApi.setGridOption("quickFilterText", agV);

// mini nav
const miniNav = () => {
    const boxNav = document.getElementById("box-nav");
    const boxContent = document.getElementById("box-content");
    const imgTitle = document.getElementById("img-title");
    const childNav = document.getElementById("child-nav");
    const boxAccount = document.getElementById("box-account");

    if (miniNavIndikacator.status) {
        boxNav.style.width = "11rem";
        miniNavIndikacator.nav = "11rem";
        miniNavIndikacator.status = false;
        btnChevron.querySelector("img").classList.remove("rotate-180");
        imgTitle.style.width = "80%";
        imgTitle.classList.add("ml-3");
        childNav.querySelectorAll("span").forEach((element) => (element.style.display = "block"));
        boxAccount.querySelectorAll("span").forEach((element) => (element.style.display = "block"));
        imgTitle.src = "./static/assets/pupuk-indonesia-white.png";
    } else {
        boxNav.style.width = "4rem";
        miniNavIndikacator.nav = "4rem";
        miniNavIndikacator.status = true;
        btnChevron.querySelector("img").classList.add("rotate-180");
        childNav.querySelectorAll("span").forEach((element) => (element.style.display = "none"));
        boxAccount.querySelectorAll("span").forEach((element) => (element.style.display = "none"));
        imgTitle.src = "./static/assets/pupuk-indonesia-logo.png";
        imgTitle.style.width = "100%";
        imgTitle.classList.remove("ml-3");
    }

    boxContent.style.width = `calc(100vw - ${miniNavIndikacator.nav} - ${miniNavIndikacator.tools})`;
};

// ubah indikator
const indikatorNavigation = (agN, agI) => {
    const element = document.querySelector(`.int-${agN}`);
    color = { P: "#3b82f6", D: "#22c55e", U: "#eab308" };

    element.textContent = agI;
    element.style.color = color[agI];
    element.style.textShadow = `
        -1px -1px 0 white,  
        1px -1px 0 white,
        -1px 1px 0 white,
        1px 1px 0 white
    `;
};

// set height
const setHeight = () => document.getElementById("container").style.setProperty("--vh", `${window.innerHeight * 0.01}px`);

// set up element
childTools.querySelectorAll(".tools").forEach((element) => element.addEventListener("click", () => tools(element.getAttribute("data-tools"))));
btnChevron.addEventListener("click", () => miniNav());
window.addEventListener("resize", setHeight);
