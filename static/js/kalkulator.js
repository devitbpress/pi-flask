const url = new URL(window.location);
const urlParams = new URLSearchParams(window.location.search);
const paramsContent = urlParams.get("c");
const inpAmbil = document.getElementById("inpAmbil");
const slcModel = document.getElementById("slcModel");
const notifStatus = document.getElementById("notifStatus");
const notifMessage = document.getElementById("notifMessage");
const btnTemplate = document.getElementById("btnTemplate");
const textAmbil = document.getElementById("textAmbil");
const btnProses = document.getElementById("btnProses");
const headerTabsInput = document.getElementById("headerTabsInput");
const headerTabsManual = document.getElementById("headerTabsManual");
const slcQ = document.getElementById("slcQ");
const slcPoisson = document.getElementById("slcPoisson");
const slcWilson = document.getElementById("slcWilson");
const slcTchebycheff = document.getElementById("slcTchebycheff");
const slcRegret = document.getElementById("slcRegret");
const slcLinear = document.getElementById("slcLinear");
const slcNonLinear = document.getElementById("slcNonLinear");
const slcBCR = document.getElementById("slcBCR");
const headerParameter = document.getElementById("headerParameter");
const btnHitung = document.getElementById("btnHitung");
const scrollableDiv = document.getElementById("scrollableDiv");
const boxLoadingUpload = document.getElementById("boxLoadingUpload");
const statusUp = document.getElementById("statusUp");
const barPersen = document.getElementById("barPersen");
const textPersen = document.getElementById("textPersen");
const statusDown = document.getElementById("statusDown");

let gridApi;
let boxNotif = document.getElementById("boxNotif");
const formatString = (str) => str.replace(/_/g, " ").replace(/\b\w/g, (char) => char.toUpperCase());
let idNotif = 1;
let paramsPast = "";

const postFile = async (argUrl, argFile, argModel) => {
    const formData = new FormData();
    formData.append("file", argFile);
    formData.append("model", argModel);

    try {
        const response = await fetch(argUrl, {
            method: "POST",
            body: formData,
        });

        if (!response.ok) {
            const errorData = await response.json();
            return ["failed", errorData.error];
        }

        const result = await response.json();
        return ["success", result];
    } catch (error) {
        return ["failed", error];
    }
};

const postManual = async (argUrl, argModel, argForm) => {
    const formData = new FormData();
    formData.append("model", argModel);

    Object.entries(argForm).map((item) => {
        formData.append(item[0], item[1]);
    });

    try {
        const response = await fetch(argUrl, {
            method: "POST",
            body: formData,
        });

        if (!response.ok) {
            const errorData = await response.json();
            return ["failed", errorData.error];
        }

        const result = await response.json();
        return ["success", result];
    } catch (error) {
        return ["failed", error];
    }
};

const removeNotif = (argId) => {
    try {
        document.getElementById(`${argId}`).remove();
    } catch (error) {
        ("");
    }
};

const notifShow = (argStatus, argMessage) => {
    const idNotifNow = idNotif;
    boxNotif.innerHTML += `                
        <div id="notif${idNotifNow}" class="relative py-2 origin-top-left px-4 bg-white shadow-xl border rounded-lg flex gap-4 items-center w-fit max-w-[50vw] duration-300">
            <img src="static/assets/error.png" alt="error" class="h-6 w-6" />
            <div class="flex flex-col">
                <h1 id="notifStatus" class="text-sm font-semibold">${argStatus}</h1>
                <p id="notifMessage" class="text-xs">${argMessage}</p>
            </div>
            <h1 onclick="removeNotif('notif${idNotifNow}')" class="cursor-pointer text-red-500 font-semibold pl-4">X</h1>
        </div>`;

    setTimeout(() => {
        try {
            document.getElementById(`notif${idNotifNow}`).classList.add("scale-0");

            setTimeout(() => {
                removeNotif(`notif${idNotifNow}`);
            }, 300);
        } catch (error) {
            ("");
        }
    }, 5000);

    idNotif += 1;
};

const setupAgGrid = (data_grid) => {
    const dom_grid = document.getElementById("aggrid");
    dom_grid.classList.remove("hidden");
    dom_grid.innerHTML = ``;
    let data = [];
    let columnDefs = [];

    if (data_grid) {
        const dataframe = data_grid;
        data = dataframe.map((row) => {
            let newRow = {};
            for (let key in row) {
                newRow[key] = key === "Posting Date" ? row[key] : String(row[key]);
            }
            return newRow;
        });

        Object.keys(data[0]).map((entry) => {
            columnDefs.push({
                headerName: entry,
                field: entry,
                filter: false,
                minWidth: entry.length * 10 < 90 ? 90 : entry.length * 10,
                maxWidth: 700,
            });
        });
    }

    const gridOptions = {
        defaultColDef: {
            flex: 1,
        },
        columnDefs: columnDefs,
        rowData: data,
        pagination: true,
        paginationPageSize: 100,
    };

    gridApi = agGrid.createGrid(dom_grid, gridOptions);
};

const aggridNonMoving = (argData) => {
    const dom_grid = document.getElementById("aggrid");
    dom_grid.innerHTML = ``;

    let columnDefs = [];
    Object.entries(argData[0]).map((header) => {
        if (header[0] !== "model") {
            columnDefs.push({
                headerName: header[0],
                field: header[0],
                filter: false,
                minWidth: header[0].length * 10 < 90 ? 90 : header[0].length * 9,
                maxWidth: 700,
            });
        } else {
            Object.entries(header[1]).map((childHed) => {
                let childHeader = [];

                Object.keys(childHed[1]).map((itemHeade) => {
                    childHeader.push({
                        headerName: itemHeade,
                        field: `${childHed[0]} ${itemHeade}`,
                        filter: false,
                        minWidth: itemHeade.length * 10 < 90 ? 90 : itemHeade.length * 9,
                        maxWidth: 700,
                    });
                });

                columnDefs.push({
                    headerName: formatString(childHed[0]),
                    children: childHeader,
                });
            });
        }
    });

    const rowData = [];
    argData.map((item) => {
        let dataFirst = {};
        Object.entries(item).map((subItem) => {
            if (subItem[0] !== "model") {
                dataFirst[subItem[0]] = subItem[1];
            } else {
                Object.entries(subItem[1]).map((childItem) => {
                    Object.entries(childItem[1]).map((childSubItem) => {
                        dataFirst[`${childItem[0]} ${childSubItem[0]}`] = childSubItem[1];
                    });
                });
            }
        });
        rowData.push(dataFirst);
    });

    const gridOptions = {
        columnDefs: columnDefs,
        rowData: rowData,
        defaultColDef: {
            flex: 1,
        },
        pagination: true,
        paginationPageSize: 100,
    };

    // Setup the grid
    const eGridDiv = document.querySelector("#aggrid");
    new agGrid.Grid(eGridDiv, gridOptions);
};

const downloadTemplate = () => {
    const dataTemplate = {
        wilson: ["Material Code", "Material Description", "ABC Indicator", "Permintaan Barang (D) Unit/Tahun", "Harga Barang (p) /Unit", "Ongkos Pesan (A) /Pesan", "Lead Time (L) Tahun", "Ongkos Simpan (h) /Unit/Tahun"],
        tchebycheff: ["Material Code", "Material Description", "ABC Indicator", "Harga Barang (p) /Unit", "Kerugian Ketidakadaan Barang (Cu) /Unit", "Standar Deviasi Permintaan Barang (s)", "Rata_Rata/Bulan"],
        q: ["Material Code", "Material Description", "ABC Indicator", "Rata - Rata Permintaan Barang (D) Unit/Tahun", "Lead Time (L) Tahun", "Standar Deviasi Permintaan Barang (s) Unit/Tahun", "Ongkos Pesan (A) /Pesan	Harga Barang (p) /Unit", "Ongkos Simpan (h) /Unit/Tahun", "Ongkos Kekurangan Inventori (Cu) /Unit/Tahun"],
        poisson: ["Material Code", "Material Description", "ABC Indicator", "Rata - Rata Permintaan Barang (D) Unit/Tahun", "Standar Deviasi Permintaan Barang (s) Unit/Tahun", "Lead Time (L) Tahun", "Ongkos Pesan (A) /Pesan", "Harga Barang (p) /Unit	Ongkos Simpan (h) /Unit/Tahun", "Ongkos Kekurangan Inventori (Cu) /Unit/Tahun"],
        nonmoving: ["Material Code", "Material Description", "ABC Indicator", "Ongkos Pemakaian Komponen (H)", "Ongkos Kerugian Akibat Kerusakan (L)", "Jumlah Komponen Terpasang (m)"],
        bcr: ["Material Code", "Material Description", "ABC Indicator", "Harga Komponen (Ho)", "Kerugian Komponen (Co)", "Suku Bunga (I)", "Waktu Sisa Operasi (tahun)"],
    };

    const data = dataTemplate[slcModel.value];
    const worksheet = XLSX.utils.aoa_to_sheet([data]);
    const workbook = XLSX.utils.book_new();
    XLSX.utils.book_append_sheet(workbook, worksheet, "Sheet1");
    XLSX.writeFile(workbook, `template ${slcModel.value}.xlsx`);
};

const manualCalc = (argElement, argIdManual) => {
    const color = argElement.getAttribute("data-color");
    let styleIden = ["bg-[#1A8FCB]", "bg-[#47AD41]", "bg-[#F9CD2B]", "bg-[#F68B33]", "bg-[#7961F2]", "bg-[#F33D3D]", "bg-[#E667E6]", "bg-[#FF5975]"];

    url.searchParams.set("m", argIdManual.replace("calc", ""));
    window.history.pushState({}, "", url);
    paramsPast = argIdManual.replace("calc", "");

    document.querySelectorAll(".slc-manual").forEach((element) => {
        const elementColor = element.getAttribute("data-color");
        element.classList.remove(`bg-[#${elementColor}]`);
        element.classList.add("bg-white");
        element.classList.remove("text-white");
    });

    document.querySelectorAll(".calc-model").forEach((element) => {
        element.classList.remove("flex");
        element.classList.add("hidden");
    });

    headerParameter.textContent = `Parameter Input ${argElement.querySelector("span").textContent}`;

    document.getElementById(`${argIdManual}`).classList.remove("hidden");
    document.getElementById(`${argIdManual}`).classList.add("flex");

    argElement.classList.remove("bg-white");
    argElement.classList.add(`bg-[#${color}]`);
    argElement.classList.add("text-white");

    document.querySelectorAll(`#boxResult .result-model`).forEach((element) => {
        element.classList.add("hidden");
        element.classList.remove("flex");
    });

    document.getElementById(`result${argIdManual.replace("calc", "")}`).classList.remove("hidden");
    document.getElementById(`result${argIdManual.replace("calc", "")}`).classList.add("flex");
};

const tabsContent = (argElement) => {
    const dataTabs = argElement.getAttribute("data-tabs");

    url.search = "";
    url.searchParams.set("c", dataTabs);
    window.history.pushState({}, "", url);

    document.querySelectorAll(".header-tabs").forEach((element) => {
        element.classList.remove("border-b", "border-[#1A8FCB]", "text-[#1A8FCB]");
    });

    document.querySelectorAll(".tab-contents").forEach((element) => {
        element.classList.remove("flex");
        element.classList.add("hidden");
    });

    document.querySelectorAll(`.tab-${dataTabs}`).forEach((element) => {
        element.classList.remove("hidden");
        element.classList.add("flex");
    });

    argElement.classList.add("border-b", "border-[#1A8FCB]", "text-[#1A8FCB]");
    if (dataTabs === "manual") {
        if (paramsPast !== "") {
            manualCalc(document.getElementById(`slc${paramsPast}`), `calc${paramsPast}`);
        } else {
            manualCalc(slcQ, "calcQ");
        }
    }
};

const prosesFile = async () => {
    const response = await postFile(`/calc`, inpAmbil.files[0], slcModel.value);
    if (response[0] === "success") {
        const result = response[1];
        if (result.error) {
            notifShow("Gagal Proses", result.error);
            return;
        }

        if (slcModel.value !== "nonmoving") {
            setupAgGrid(result);
        } else {
            let dataResponse = [];
            Object.entries(result).map((oneModel) => {
                let groupResult = {
                    "Material Code": 0,
                    "Material Description": 0,
                    "ABC Indicator": 0,
                    "Ongkos Pemakaian Komponen (H)": 0,
                    "Ongkos Kerugian Akibat Kerusakan (L)": 0,
                    "Jumlah Komponen Terpasang (m)": 0,
                    model: {
                        regret: {},
                        linear: {},
                        non_linear: {},
                    },
                };

                Object.entries(oneModel[1]).map((item) => {
                    const model = item[0];

                    groupResult["Material Code"] = item[1]["Material Code"];
                    groupResult["Material Description"] = item[1]["Material Description"];
                    groupResult["ABC Indicator"] = item[1]["ABC Indicator"];
                    groupResult["Ongkos Pemakaian Komponen (H)"] = item[1]["Ongkos Pemakaian Komponen (H)"];
                    groupResult["Ongkos Kerugian Akibat Kerusakan (L)"] = item[1]["Ongkos Kerugian Akibat Kerusakan (L)"];
                    groupResult["Jumlah Komponen Terpasang (m)"] = item[1]["Jumlah Komponen Terpasang (m)"];

                    groupResult.model[model]["Harga Resale Komponen (O)"] = item[1]["Harga Resale Komponen (O)"];
                    model === "regret" ? (groupResult.model[model]["Minimum Regret (Rp )"] = item[1]["Minimum Regret (Rp )"]) : (groupResult.model[model]["Ongkos Model Probabilistik Kerusakan"] = item[1]["Ongkos Model Probabilistik Kerusakan"]);
                    groupResult.model[model]["Strategi Penyediaan Optimal (Unit)"] = item[1]["Strategi Penyediaan Optimal (Unit)"];
                });

                dataResponse.push(groupResult);
            });

            aggridNonMoving(dataResponse);
        }
    } else {
        console.error("failed");
    }
};

const numericInput = (event) => {
    event.target.value = event.target.value.replace(/[^0-9.]/g, "");
};

const calcManual = async (argModel) => {
    let dataForm = {};
    let status = "success";
    let number = 0;

    document.querySelectorAll(`#calc${argModel} input`).forEach((element) => {
        if (element.value === "") {
            if (element.name !== "material_code" && element.name !== "material_description" && element.name !== "abc_indikator") {
                element.classList.add("placeholder-red-500");
                notifShow("Gagal Perhitungan Model", `Silakan lengkapi form ${element.name}`);
                status = "failed";
            }
        }

        dataForm[element.name] = element.value ? element.value : "";
    });

    if (status === "success") {
        barPersen.style.width = "0%";
        boxLoadingUpload.classList.remove("hidden");
        boxLoadingUpload.classList.add("flex");

        statusUp.textContent = `Perhitungan Model ${argModel}`;
        barPersen.style.transitionDuration = "2500ms";
        statusDown.textContent = "Proses kalkulasi";

        setTimeout(() => {
            barPersen.style.width = "90%";
        }, 100);

        const interval = setInterval(() => {
            textPersen.textContent = `${number + 1}% Done`;
            number += 1;

            if (number >= 90) {
                clearInterval(interval);
            }
        }, 2500 / 100);

        const response = await postManual("/manual-calc", argModel, dataForm);

        const indikatorResult = {
            Poisson: ["Economic Order Quantity (EOQ) Lot Optimum (qo1)", "Nilai Alpha", "Ongkos Inventori (OT) /Tahun", "Reorder Point (ROP) Unit", "Safety Stock (SS) Unit", "Service Level (%)", "Standar Deviasi Waktu Ancang - Ancang (SL) Unit/Tahun"],
            Wilson: ["Frequensi Pemesanan (f)", "Lot Pengadaan (EOQ) Unit/Pesanan", "Ongkos Inventori (OT) /Tahun", "Ongkos Pembelian (Ob) /Tahun", "Ongkos Pemesanan (Op) /Tahun", "Ongkos Penyimpanan (Os) /Tahun", "Reorder Point (ROP) Unit", "Selang Waktu Pesan Kembali (Bulan)", "Selang Waktu Pesan Kembali (Hari)", "Selang Waktu Pesan Kembali (Tahun)"],
            Tchebycheff: ["Lot Pemesanan Optimal (q0)", "Nilai K Model Tchebycheff"],
            Regret: ["Harga Resale Komponen (O)", "Minimum Regret (Rp )", "Strategi Penyediaan Optimal (Unit)"],
            Linear: ["Harga Resale Komponen (O)", "Ongkos Model Probabilistik Kerusakan", "Strategi Penyediaan Optimal (Unit)"],
            NonLinear: ["Harga Resale Komponen (O)", "Ongkos Model Probabilistik Kerusakan", "Strategi Penyediaan Optimal (Unit)"],
            BCR: ["Benefit-Cost Ratio (BCR)", "Strategi Penyediaan Optimal (Tahun)", "Jenis Probabilitas", "Pesan"],
        };

        if (response[0] === "success") {
            let contentResult = ``;

            indikatorResult[argModel].map((item) => {
                if (response[1][item]) {
                    const value = response[1][item];

                    contentResult += `
                        <div class="flex gap-4 items-center justify-between">
                            <span>${item}</span>
                            <div class="bg-white min-w-[20%] max-w-[75%] text-end py-1 px-2 border rounded">${typeof value === "number" ? value.toFixed(2) : value !== undefined ? value : "N/A"}</div>
                        </div>
                    `;
                }
            });

            document.getElementById(`result${argModel}`).innerHTML = contentResult;

            scrollableDiv.scrollTop = scrollableDiv.scrollHeight;
        } else {
            notifShow("Gagal Proses", response[1]);
        }

        if (response) {
            barPersen.style.transitionDuration = "0ms";
            barPersen.style.width = "100%";

            boxLoadingUpload.classList.add("hidden");
            boxLoadingUpload.classList.remove("flex");
        }
    }
};

paramsContent === "manual" ? tabsContent(headerTabsManual) : tabsContent(headerTabsInput);
urlParams.get("m") ? manualCalc(document.getElementById(`slc${urlParams.get("m")}`), `calc${urlParams.get("m")}`) : "";

btnProses.addEventListener("click", () => prosesFile());
inpAmbil.addEventListener("change", () => (textAmbil.textContent = `${inpAmbil.files[0].name.substring(0, 10)}...${inpAmbil.files[0].name.split(".").pop()}`));
btnTemplate.addEventListener("click", () => downloadTemplate());
headerTabsInput.addEventListener("click", (event) => tabsContent(event.target));
headerTabsManual.addEventListener("click", (event) => tabsContent(event.target));
slcQ.addEventListener("click", () => manualCalc(slcQ, "calcQ"));
slcPoisson.addEventListener("click", () => manualCalc(slcPoisson, "calcPoisson"));
slcWilson.addEventListener("click", () => manualCalc(slcWilson, "calcWilson"));
slcTchebycheff.addEventListener("click", () => manualCalc(slcTchebycheff, "calcTchebycheff"));
slcRegret.addEventListener("click", () => manualCalc(slcRegret, "calcRegret"));
slcLinear.addEventListener("click", () => manualCalc(slcLinear, "calcLinear"));
slcNonLinear.addEventListener("click", () => manualCalc(slcNonLinear, "calcNonLinear"));
slcBCR.addEventListener("click", () => manualCalc(slcBCR, "calcBCR"));
btnHitung.addEventListener("click", () => calcManual(paramsPast));

setupAgGrid();
