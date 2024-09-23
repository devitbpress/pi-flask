const url = new URL(window.location.href);
const urlParams = new URLSearchParams(window.location.search);
const btnChevron = document.getElementById("btn-chevron");
const childTools = document.getElementById("child-tools");

let miniNavIndikacator = { status: false, nav: "13rem", tools: "13rem" };
let idNotif = 1;
let idProgress = 1;
let gridApi;
let dataProduct = {};
let columnDefs = {};

const fetchProducts = async (agU, agD) => {
    try {
        const response = await fetch(agU, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify(agD),
        });

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        const products = await response.json();

        return ["success", products];
    } catch (error) {
        return ["error", error];
    }
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

    const gridOptions = {
        columnDefs: agCol,
        rowData: rowData,
        defaultColDef: defaultColDef,
        getRowClass: (params) => {
            if (params.data.action) {
                return "no-border";
            }
            return "";
        },
    };

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
        header.textContent = "List Produk";
        headerAction.innerHTML = ``;

        childContent.innerHTML = `<div class="w-full h-full bg-white rounded-xl shadow p-3 flex flex-col gap-3">
            <h1 class="font-medium text-lg text-blue-900">Produk PI</h1>
            <div id="aggrid-website" class="ag-theme-quartz w-full h-full"></div>
        </div>`;

        columnDefs["list"] = [
            { headerName: "Material Code", field: "p_code", minWidth: 150 },
            { headerName: "Material Description", field: "p_description", minWidth: 100 },
            { headerName: "Unit Price", field: "p_price", minWidth: 100 },
            { headerName: "Estimasi Lead Time (mon)", field: "p_lead_m", minWidth: 150 },
            { headerName: "Estimasi Lead Time (day)", field: "p_lead_d", minWidth: 150 },
        ];

        let page = 1;
        const paramsPage = urlParams.get("p");
        if (paramsPage) {
            page = parseInt(paramsPage);
        } else {
            url.searchParams.set("p", "1");
            window.history.replaceState({}, "", url.toString());
        }

        setupAggrid(dataProduct[page], columnDefs.list, false);
    }

    url.searchParams.set("t", agT);
    window.history.replaceState({}, "", url.toString());
};

const setHeight = () => document.getElementById("container").style.setProperty("--vh", `${window.innerHeight * 0.01}px`);
const setLoading = (value) => gridApi.setGridOption("loading", value);

childTools.querySelectorAll(".tools").forEach((element) => element.addEventListener("click", () => tools(element.getAttribute("data-tools"))));
btnChevron.addEventListener("click", () => miniNav());
window.addEventListener("resize", setHeight);

document.addEventListener("DOMContentLoaded", async () => {
    setHeight();

    const data = { page: 1 };

    const [status, product] = await fetchProducts("/get-product", data);

    if (status === "success") {
        dataProduct[data.page] = product;
    } else {
        notification("show", "Gagal ambil produk");
        return;
    }

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
