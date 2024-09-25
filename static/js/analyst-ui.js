const url = new URL(window.location.href);
const urlParams = new URLSearchParams(window.location.search);
const btnChevron = document.getElementById("btn-chevron");
const childTools = document.getElementById("child-tools");
const inpFile = document.getElementById("inp-file");

let fileId = 0;
let miniNavIndikacator = { status: false, nav: "13rem", tools: "13rem" };
let accountOptionIndikator = false;
let gridApi;
let idNotif = 1;
let dataList = [];
let dataMentah = {};
let dataSubset = [];
let dataFiltered = [];
let idProduct = 1;
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
                span.addEventListener("click", async () => {
                    const rowIndex = params.node.rowIndex;
                    const index = dataList.findIndex((item) => item.name === params.data.name);
                    if (index !== -1) {
                        dataList.splice(index, 1);
                    }

                    const responseDelete = await postFetch("delete-file", { file_id: params.data.id, session: sId });

                    if (responseDelete === "success") {
                        notification("show", "File berhasil terhapus");
                        delete dataMentah[params.data.name];
                        gridApi.applyTransaction({ remove: [params.data] });
                    } else {
                        notification("show", "Gagal menghapus file");
                    }
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

const uploadFiles = async (agUrl, agData, agId) => {
    const formData = new FormData();
    formData.append("file", agData);
    formData.append("numid", agId);
    formData.append("session", sessionStorage.getItem("id"));

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

const processingFiles = async (agUrl, agId) => {
    const formData = new FormData();
    formData.append("numid", agId);
    formData.append("session", sessionStorage.getItem("id"));

    try {
        const response = await fetch(agUrl, { method: "POST", body: formData });

        const { ok, statusText } = response;

        if (!ok) {
            const errorData = await response.json();
            return ["failed", errorData.error || statusText];
        }

        const result = await response.json();
        return ["success", result];
    } catch (error) {
        return ["failed", error.message || error];
    }
};

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

    const gridOptions = { columnDefs: agCol, rowData: rowData, defaultColDef: defaultColDef };

    eGrid.innerHTML = "";
    gridApi = agGrid.createGrid(eGrid, gridOptions);

    setLoading(agView);
    cGrid.forEach((element) => (element.textContent.trim() === "Total" ? element.classList.add("justify-end", "pr-5") : ""));
};

const tools = (agT) => {
    const header = document.getElementById("header");
    const headerAction = document.getElementById("header-action");
    const childContent = document.getElementById("child-content");

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
        headerAction.innerHTML = "";

        childContent.innerHTML = `<div class="w-full h-full bg-white rounded-xl shadow p-3 flex flex-col gap-3">
            <h1 class="font-medium text-lg text-blue-900">File Terunggah</h1>
            <div id="aggrid-website" class="ag-theme-quartz w-full h-full"></div>
        </div>`;

        setupAggrid(dataList, columnDefs.list, false);
    }

    if (agT === "mentah") {
        header.textContent = "Data Mentah";
        headerAction.innerHTML = "";

        let option = Object.keys(dataMentah).map((key) => {
            return `<option value='${key}'>${key}</option>`;
        });

        childContent.innerHTML = `<div class="w-full h-full bg-white rounded-xl shadow p-3 flex flex-col gap-3">
            <div class="w-full flex justify-between text-sm">
                <div class="flex gap-2">
                    <span>Nama File: </span>
                    <select id="slc-mentah" class="cursor-pointer bg-transparent">${option}</select>
                </div>
            </div>
            <div id="aggrid-website" class="ag-theme-quartz w-full h-full"></div>
        </div>`;

        try {
            headerAction.innerHTML = `<button id="btn-process-mentah" class="bg-transparent hover:bg-blue-500 text-blue-700 font-semibold hover:text-white py-2 px-4 border border-blue-500 hover:border-transparent rounded text-xs">Proses Dataframe</button>`;

            columnDefs.mentah = Object.keys(dataMentah[document.getElementById("slc-mentah").value][0]).map((key) => {
                const lenght = key.length >= 20 ? key.length * 8 : key.length >= 15 ? key.length * 9 : key.length >= 10 ? key.length * 10 : key.length * 12;
                return {
                    headerName: key,
                    field: key,
                    minWidth: lenght,
                    cellRenderer: (params) => {
                        return params.value;
                    },
                };
            });

            document.getElementById("slc-mentah").addEventListener("change", () => {
                columnDefs.mentah = Object.keys(dataMentah[document.getElementById("slc-mentah").value][0]).map((key) => {
                    const lenght = key.length >= 20 ? key.length * 8 : key.length >= 15 ? key.length * 9 : key.length >= 10 ? key.length * 10 : key.length * 12;
                    return {
                        headerName: key,
                        field: key,
                        minWidth: lenght,
                        cellRenderer: (params) => {
                            return params.value;
                        },
                    };
                });

                setupAggrid(dataMentah[document.getElementById("slc-mentah").value], columnDefs.mentah, false);
            });

            document.getElementById("btn-process-mentah").addEventListener("click", () => subset());
        } catch (error) {
            columnDefs.mentah = [
                { headerName: "Base Unit of Measure", field: "code" },
                { headerName: "Material", field: "code" },
                { headerName: "Material.1", field: "code" },
                { headerName: "Movement Type", field: "code" },
                { headerName: "Posting Date", field: "code" },
                { headerName: "Purchase Order", field: "code" },
            ];
        }

        setupAggrid(dataMentah[document.getElementById("slc-mentah").value], columnDefs.mentah, false);
    }

    if (agT === "subset") {
        header.textContent = "Subset Data";
        headerAction.innerHTML = "";

        childContent.innerHTML = `<div class="w-full h-full bg-white rounded-xl shadow p-3 flex flex-col gap-3">
            <div class="w-full flex justify-between text-sm">
                <div>Testing</div>
            </div>
            <div id="aggrid-website" class="ag-theme-quartz w-full h-full"></div>
        </div>`;

        try {
            columnDefs.subset = Object.keys(dataSubset[0]).map((key) => {
                const lenght = key.length >= 20 ? key.length * 8 : key.length >= 15 ? key.length * 9 : key.length >= 10 ? key.length * 10 : key.length * 12;
                return {
                    headerName: key,
                    field: key,
                    minWidth: lenght,
                    cellRenderer: (params) => {
                        return params.value;
                    },
                };
            });

            setupAggrid(dataSubset, columnDefs.subset, false);
        } catch (error) {
            columnDefs.subset = [
                { headerName: "Material_Code", field: "Material_Code" },
                { headerName: "Material Description", field: "Material Description" },
                { headerName: "Movement Type", field: "Movement Type" },
                { headerName: "Posting Date", field: "Posting Date" },
                { headerName: "Quantity(EA)", field: "Quantity(EA)" },
            ];

            setupAggrid("", columnDefs.subset, false);
        }
    }

    if (agT === "filtered") {
        header.textContent = "Data Klasifikasi";
        headerAction.innerHTML = "";

        childContent.innerHTML = `<div class="w-full h-full bg-white rounded-xl shadow p-3 flex flex-col gap-3">
            <div class="w-full flex justify-between text-sm">
                <div>Testing</div>
            </div>
            <div id="aggrid-website" class="ag-theme-quartz w-full h-full"></div>
        </div>`;

        try {
            columnDefs.filtered = Object.keys(dataFiltered[0]).map((key) => {
                const lenght = key.length >= 20 ? key.length * 8 : key.length >= 15 ? key.length * 9 : key.length >= 10 ? key.length * 10 : key.length * 12;
                return {
                    headerName: key,
                    field: key,
                    minWidth: lenght,
                    cellRenderer: (params) => {
                        return params.value;
                    },
                };
            });

            setupAggrid(dataFiltered, columnDefs.filtered, false);
        } catch (error) {
            columnDefs.filtered = [
                { headerName: "Material_Code", field: "Material_Code" },
                { headerName: "Material Description", field: "Material Description" },
                { headerName: "Movement Type", field: "Movement Type" },
                { headerName: "Posting Date", field: "Posting Date" },
                { headerName: "Quantity(EA)", field: "Quantity(EA)" },
            ];

            setupAggrid("", columnDefs.filtered, false);
        }
    }

    url.searchParams.set("t", agT);
    window.history.replaceState({}, "", url.toString());
};

const notification = (agS, agE) => {
    const notif = document.getElementById("notification");
    const notifNow = idNotif;

    if (agS === "show") {
        notif.innerHTML += `
            <div id="notif-${notifNow}" class="px-2 py-1 flex items-center gap-2 bg-white border rounded scale-0 origin-right duration-300">
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

    setTimeout(() => {
        try {
            notification("hide", `notif-${notifNow}`);
        } catch (error) {
            void 0;
        }
    }, 5000);
};

const uploadFile = async (agN) => {
    try {
        const fileIdNow = agN;
        const file = inpFile.files[fileIdNow];

        const idProgress = progresBar("Baca data histori Good Issue (GI)", `${file.name}`, file.size / 250);

        const responseFile = await postFiles("upload-file", file, idProduct);

        let statusAggrid = ``;
        if (responseFile[0] === "success") {
            statusAggrid = `<div class="flex gap-1 items-center cursor-pointer"><img src="./static/assets/done-green.png" alt="delete" class="w-4 h-4" /><span class="text-green-500">Terunggah</span></div>`;
            dataMentah[file.name] = responseFile[1];
        } else {
            notification("show", "File gagal diunggah");
            statusAggrid = `<div class="flex gap-1 items-center cursor-pointer"><img src="./static/assets/error-yellow.png" alt="delete" class="w-4 h-4" /><span class="text-yellow-500">Gagal</span></div>`;
        }

        dataList.push({
            name: file.name,
            size: file.size,
            action: `<div class="flex gap-1 items-center cursor-pointer"><img src="./static/assets/delete-red.png" alt="delete" class="w-4 h-4" /><span class="text-red-500">Hapus</span></div>`,
            status: statusAggrid,
            id: idProduct,
        });

        sInterval[idProgress] === "done" ? progresBarStatus(idProgress) : (sInterval[idProgress] = "done");

        tools("list");

        idProduct += 1;

        fileIdNow < [...inpFile.files].length - 1 ? uploadFile(fileIdNow + 1) : void 0;
    } catch (error) {
        void 0;
    }
};

const subset = async () => {
    let lengData = 0;

    Object.values(dataMentah).map((item) => (lengData += item.length));

    const responseSubset = await postFetch("subset", { session: sId });
    console.log(responseSubset);
};

const semetarta = async () => {
    if (lengData > 90000) {
        notification("show", "Data melebihi batas makasimal 90.000 Data");
    } else {
        const resProg = progress("Filterisasi Data", `Normalisasi data Input Histori Good Issue (GI)`);

        let times = Object.values(dataMentah).reduce((sum, data) => sum + data.length, 0);

        let number = 0;
        let sInverval = "start";

        const interval = setInterval(() => {
            try {
                document.getElementById(`${resProg.width}`).style.width = `${number}%`;
                document.getElementById(`${resProg.bar}`).textContent = `${number}%`;
            } catch (error) {
                clearInterval(interval);
            }

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
                        void 0;
                    }
                }, 200);
            }

            if (number >= 95) {
                clearInterval(interval);
                sInverval = "done";
            }
        }, times / 100);

        const [status, result] = await processingFiles("subset");

        if (status === "success") {
            dataSubset = result;
            tools("subset");
            filtered();
        } else {
            notification("show", "Gagal mengolah data");
        }

        if ((sInverval = "done")) {
            document.getElementById(`${resProg.width}`).style.width = `100%`;
            document.getElementById(`${resProg.bar}`).textContent = `100%`;
            document.getElementById(`${resProg.box}`).classList.add("scale-0");
            setTimeout(() => {
                try {
                    document.getElementById(`${resProg.box}`).remove();
                } catch (error) {
                    void 0;
                }
            }, 200);
        } else {
            sInverval = "done";
        }
    }
};

const filtered = async () => {
    const resProg = progress("Filterisasi Data", `Filtering data Histori Good Issue (GI)`);

    let times = dataSubset.length;

    let number = 0;
    let sInverval = "start";

    const interval = setInterval(() => {
        try {
            document.getElementById(`${resProg.width}`).style.width = `${number}%`;
            document.getElementById(`${resProg.bar}`).textContent = `${number}%`;
        } catch (error) {
            clearInterval(interval);
        }

        number += 1;

        if (number === 50) {
            document.getElementById(resProg.span).textContent = "Agregasi Data";
        }

        if (sInverval === "done") {
            clearInterval(interval);
            document.getElementById(`${resProg.width}`).style.width = `100%`;
            document.getElementById(`${resProg.bar}`).textContent = `100%`;
            document.getElementById(`${resProg.box}`).classList.add("scale-0");
            setTimeout(() => {
                try {
                    document.getElementById(`${resProg.box}`).remove();
                } catch (error) {
                    void 0;
                }
            }, 200);
        }

        if (number >= 95) {
            clearInterval(interval);
            sInverval = "done";
        }
    }, times / 100);

    const [status, result] = await processingFiles("classification");

    if (status === "success") {
        dataFiltered = result;

        tools("filtered");
    } else {
        notification("show", "Gagal mengolah data");
    }

    if ((sInverval = "done")) {
        document.getElementById(`${resProg.width}`).style.width = `100%`;
        document.getElementById(`${resProg.bar}`).textContent = `100%`;
        document.getElementById(`${resProg.box}`).classList.add("scale-0");
        setTimeout(() => {
            try {
                document.getElementById(`${resProg.box}`).remove();
            } catch (error) {
                void 0;
            }
        }, 200);
    } else {
        sInverval = "done";
    }
};

const setHeight = () => document.getElementById("container").style.setProperty("--vh", `${window.innerHeight * 0.01}px`);
const setLoading = (value) => gridApi.setGridOption("loading", value);

childTools.querySelectorAll(".tools").forEach((element) => element.addEventListener("click", () => tools(element.getAttribute("data-tools"))));
inpFile.addEventListener("change", () => uploadFile(fileId));
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

    setTimeout(() => miniNav(), 300);
});
