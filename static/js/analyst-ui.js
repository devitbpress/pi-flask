const url = new URL(window.location.href);
const urlParams = new URLSearchParams(window.location.search);
const btnChevron = document.getElementById("btn-chevron");
const boxAccount = document.getElementById("box-account");
const childTools = document.getElementById("child-tools");
const childContent = document.getElementById("child-content");
const inpFile = document.getElementById("inp-file");

let miniNavIndikacator = { status: false, nav: "13rem", tools: "13rem" };
let accountOptionIndikator = false;
let gridApi;
let idNotif = 1;
let idProgress = 1;
let dataList = [];
let dataMentah = {};
let columnDefs = {
    list: [
        { headerName: "NAMA", field: "name" },
        { headerName: "UKURAN", field: "size", minWidth: 150, maxWidth: 200 },
        {
            headerName: "AKSI",
            field: "action",
            cellRenderer: (params) => {
                const span = document.createElement("span");
                span.innerHTML = params.value;
                span.addEventListener("click", () => {
                    const rowIndex = params.node.rowIndex;
                    const index = dataList.findIndex((item) => item.name === params.data.name);
                    if (index !== -1) {
                        dataList.splice(index, 1);
                    }
                    delete dataMentah[params.data.name];
                    gridApi.applyTransaction({ remove: [params.data] });
                });
                return span;
            },
            minWidth: 150,
            maxWidth: 200,
        },
        {
            headerName: "STATUS",
            field: "status",
            futoHeight: true,
            cellRenderer: (params) => {
                return params.value;
            },
            minWidth: 150,
            maxWidth: 200,
        },
    ],
    mentah: [],
};

const uploadFiles = async (agUrl, agData) => {
    const formData = new FormData();
    formData.append("file", agData);

    try {
        const response = await fetch(agUrl, {
            method: "POST",
            body: formData,
        });

        const data = await response.json();

        if (response.ok) {
            return ["success", data];
        } else {
            return ["error", data];
        }
    } catch (error) {
        return ["error", error];
    }
};

const miniNav = () => {
    const boxNav = document.getElementById("box-nav");
    const boxContent = document.getElementById("box-content");
    const imgTitle = document.getElementById("img-title");
    const childNav = document.getElementById("child-nav");

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

const showOption = () => {
    const accountOption = document.getElementById("account-option");
    if (accountOptionIndikator) {
        accountOption.style.display = "none";
        accountOptionIndikator = false;
    } else {
        accountOption.style.display = "flex";
        accountOptionIndikator = true;
    }
};

const setupAggrid = async (agData, agCol, agView) => {
    const eGrid = document.getElementById("aggrid-website");
    const cGrid = document.querySelectorAll(".ag-header-cell-label");

    defaultColDef = { flex: 1 };

    const gridOptions = {
        columnDefs: agCol,
        rowData: agData,
        defaultColDef: defaultColDef,
    };

    eGrid.innerHTML = "";
    gridApi = agGrid.createGrid(eGrid, gridOptions);

    setLoading(agView);
    cGrid.forEach((element) => (element.textContent.trim() === "Total" ? element.classList.add("justify-end", "pr-5") : ""));
};

const tools = (agT) => {
    const header = document.getElementById("header");

    childTools.querySelectorAll(`.tools`).forEach((element) => {
        element.classList.remove("bg-sky-500");
        element.classList.add("hover:bg-sky-500");
        element.classList.remove("text-white");
        element.classList.add("hover:text-white");
    });

    const toolsSelected = childTools.querySelector(`.${agT}`);
    toolsSelected.classList.remove("hover:bg-sky-500");
    toolsSelected.classList.add("bg-sky-500");
    toolsSelected.classList.remove("hover:text-white");
    toolsSelected.classList.add("text-white");

    childContent.innerHTML = "";

    if (agT === "list") {
        header.textContent = "List File";
        childContent.innerHTML = `<div class="w-full h-full bg-white rounded-xl shadow p-3 flex flex-col gap-3">
            <h1 class="font-medium text-lg text-blue-900">File Terunggah</h1>
            <div id="aggrid-website" class="ag-theme-quartz w-full h-full"></div>
        </div>`;

        setupAggrid(dataList, columnDefs.list, false);
    }

    if (agT === "mentah") {
        header.textContent = "Data Mentah";
        let option = Object.keys(dataMentah).map((key) => {
            return `<option value='${key}'>${key}</option>`;
        });

        childContent.innerHTML = `<div class="w-full h-full bg-white rounded-xl shadow p-3 flex flex-col gap-3">
            <div class="w-full flex justify-between text-sm">
                <div class="flex gap-2">
                    <span>Nama File: </span>
                    <select id="slc-mentah" class="cursor-pointer">${option}</select>
                </div>
            </div>
            <div id="aggrid-website" class="ag-theme-quartz w-full h-full"></div>
        </div>`;

        try {
            columnDefs.mentah = Object.keys(dataMentah[document.getElementById("slc-mentah").value][0]).map((key) => {
                return { headerName: key, field: key };
            });
        } catch (error) {
            columnDefs.mentah = [
                { headerName: "Material Code", field: "code" },
                { headerName: "Material Description", field: "desc" },
            ];
        }

        setupAggrid(dataMentah[document.getElementById("slc-mentah").value], columnDefs.mentah, false);
    }

    url.searchParams.set("t", agT);
    window.history.replaceState({}, "", url.toString());
};

const notification = (agS, agE) => {
    const notif = document.getElementById("notification");
    const notifNow = idNotif;

    if (agS === "show") {
        notif.innerHTML += `
            <div id="notif-${notifNow}" class="px-2 py-1 flex items-top gap-2 bg-white border rounded scale-0 origin-right duration-300">
                <img onclick="notification('hide', 'notif-${notifNow}')" src="./static/assets/delete.png" alt="delete" class="h-5 w-fit cursor-pointer" />
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
};

const progress = (agH, agS) => {
    const elementProgress = document.getElementById("progress");
    const idProgressNow = idProgress;

    elementProgress.innerHTML += `<div id="box-${idProgressNow}" class="w-full flex flex-col bg-white shadow border px-2 py-1 rounded gap-1 origin-right duration-300">
            <h1 class="py-1 text-sm font-medium">${agH}</h1>
            <span>${agS}</span>
            <div class="w-[15rem] flex gap-2 items-center">
                <div class="w-full h-3 relative">
                    <div class="w-full h-full rounded bg-blue-700"></div>
                    <div id="width-${idProgressNow}" class="w-1 h-full rounded bg-green-600 absolute top-0 left-0"></div>
                </div>
                <div id="bar-${idProgressNow}" class="whitespace-nowrap">1%</div>
            </div>
        </div>`;

    idProgress += 1;

    return { width: `width-${idProgressNow}`, bar: `bar-${idProgressNow}`, box: `box-${idProgressNow}` };
};

const uploadFile = async (agN) => {
    numUpload = agN;
    const file = inpFile.files[numUpload];

    const resProg = progress("Reading File", `${file.name}`);
    const times = file.size / 100;

    let number = 0;
    let sInverval = "start";

    const interval = setInterval(() => {
        document.getElementById(`${resProg.width}`).style.width = `${number}%`;
        document.getElementById(`${resProg.bar}`).textContent = `${number}%`;

        number += 1;

        if (sInverval === "done") {
            clearInterval(interval);
            document.getElementById(`${resProg.width}`).style.width = `100%`;
            document.getElementById(`${resProg.bar}`).textContent = `100%`;
            document.getElementById(`${resProg.box}`).classList.add("scale-0");
            setTimeout(() => {
                try {
                    document.getElementById(`${resProg.box}`).remove();
                } catch (error) {
                    ("");
                }
            }, 200);
        }

        if (number >= 95) {
            clearInterval(interval);
            sInverval = "done";
        }
    }, times / 100);

    const [status, response] = await uploadFiles("upload-file", file);

    let statusAggrid = status === "success" ? `<div class="flex gap-1 items-center cursor-pointer"><img src="./static/assets/done-green.png" alt="delete" class="w-4 h-4" /><span class="text-green-500">Terunggah</span></div>` : `<div class="flex gap-1 items-center cursor-pointer"><img src="./static/assets/error-yellow.png" alt="delete" class="w-4 h-4" /><span class="text-yellow-500">Gagal</span></div>`;

    if (response) {
        dataList.push({
            name: file.name,
            size: file.size,
            action: `<div class="flex gap-1 items-center cursor-pointer"><img src="./static/assets/delete-red.png" alt="delete" class="w-4 h-4" /><span class="text-red-500">Hapus</span></div>`,
            status: statusAggrid,
        });

        tools("list");

        dataMentah[file.name] = response;

        if ((sInverval = "done")) {
            document.getElementById(`${resProg.width}`).style.width = `100%`;
            document.getElementById(`${resProg.bar}`).textContent = `100%`;
            document.getElementById(`${resProg.box}`).classList.add("scale-0");
            setTimeout(() => {
                try {
                    document.getElementById(`${resProg.box}`).remove();
                } catch (error) {
                    ("");
                }
            }, 200);
        } else {
            sInverval = "done";
        }

        if (numUpload < [...inpFile.files].length - 1) {
            uploadFile(numUpload + 1);
        }
    }
};

const setHeight = () => document.getElementById("container").style.setProperty("--vh", `${window.innerHeight * 0.01}px`);
const setLoading = (value) => gridApi.setGridOption("loading", value);

childTools.querySelectorAll(".tools").forEach((element) => element.addEventListener("click", () => tools(element.getAttribute("data-tools"))));
inpFile.addEventListener("change", () => uploadFile(0));
boxAccount.addEventListener("click", () => showOption());
btnChevron.addEventListener("click", () => miniNav());
window.addEventListener("resize", setHeight);

document.addEventListener("DOMContentLoaded", () => {
    setHeight();

    const ParamTools = urlParams.get("t");
    if (ParamTools) {
        tools(ParamTools);
    } else {
        url.searchParams.set("t", "list");
        window.history.replaceState({}, "", url.toString());
        tools("list");
    }
});
