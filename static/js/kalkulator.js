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
        <div id="notif${idNotifNow}" class="py-2 px-4 bg-white shadow-xl border rounded-lg flex gap-4 items-center w-fit max-w-[50vw]">
            <img src="static/assets/error.png" alt="error" class="h-6 w-6" />
            <div class="flex flex-col">
                <h1 id="notifStatus" class="text-sm font-semibold">${argStatus}</h1>
                <p id="notifMessage" class="text-xs">${argMessage}</p>
            </div>
            <h1 onclick="removeNotif('notif${idNotifNow}')" class="cursor-pointer text-red-500 font-semibold pl-4">X</h1>
        </div>`;

    setTimeout(() => {
        removeNotif(`notif${idNotifNow}`);
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

    document.querySelectorAll(`#calc${argModel} input`).forEach((element) => {
        if (element.value === "") {
            if (element.name !== "material_code" && element.name !== "material_description" && element.name !== "abc_indikator") {
                element.classList.add("placeholder-red-500");
                status = "failed";
            }
        }

        dataForm[element.name] = element.value ? element.value : "";
    });

    if (status === "success") {
        const response = await postManual("/manual-calc", argModel, dataForm);
        console.log(response);
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

// const lblAmbil = document.getElementById("lblAmbil");

// const setupAgGrid = (data_grid) => {
//     const dom_grid = document.getElementById("aggrid");
//     dom_grid.classList.remove("hidden");
//     dom_grid.innerHTML = ``;
//     let data = [];
//     let columnDefs = [];

//     if (data_grid) {
//         const dataframe = data_grid;
//         data = dataframe.map((row) => {
//             let newRow = {};
//             for (let key in row) {
//                 newRow[key] = key === "Posting Date" ? row[key] : String(row[key]);
//             }
//             return newRow;
//         });

//         Object.keys(data[0]).map((entry) => {
//             columnDefs.push({
//                 headerName: entry,
//                 field: entry,
//                 filter: false,
//                 minWidth: entry.length * 10 < 90 ? 90 : entry.length * 10,
//                 maxWidth: 700,
//             });
//         });
//     }

//     const gridOptions = {
//         defaultColDef: {
//             flex: 1,
//         },
//         columnDefs: columnDefs,
//         rowData: data,
//         pagination: true,
//         paginationPageSize: 100,
//     };

//     gridApi = agGrid.createGrid(dom_grid, gridOptions);
// };

// setupAgGrid();

// lblAmbil.addEventListener("click", () => {
//     document.getElementById("domAggrid").classList.remove("hidden");
//     setupAgGrid([
//         {
//             Material: 6072060,
//             Kategori: "Pola Deterministik",
//             Rata_Rata: 59000000,
//             Standar_Deviasi: 94000000,
//             Material_Code: 6072060,
//             Material_description: "BOLT,MACHINE:5/8IN UNCX50.8MM;HEX;B7",
//             Unit_Price: 35000000,
//             ABC_Indicator: "B",
//             Estimasi_Lead_Time_Mon: 3,
//             Estimasi_Lead_Time_Day: 90,
//             Estimasi_Lead_Time_Year: 246575,
//             Ongkos_Pesan_deterministik: 1000000,
//             Ongkos_Simpan_Barang_deterministik: 5250000,
//         },
//         {
//             Material: 6026100,
//             Kategori: "Pola Deterministik",
//             Rata_Rata: 727272727,
//             Standar_Deviasi: 445176165,
//             Material_Code: 6026100,
//             Material_description: "TIE,CABLE:LOCK;2.5X100MM;PVC;PK/100",
//             Unit_Price: 110000000,
//             ABC_Indicator: "A",
//             Estimasi_Lead_Time_Mon: 1496548,
//             Estimasi_Lead_Time_Day: 44896429,
//             Estimasi_Lead_Time_Year: 123004,
//             Ongkos_Pesan_deterministik: 1000000,
//             Ongkos_Simpan_Barang_deterministik: 16500000,
//         },
//         {
//             Material: 6025576,
//             Kategori: "Pola Deterministik",
//             Rata_Rata: 266666667,
//             Standar_Deviasi: 144337567,
//             Material_Code: 6025576,
//             Material_description: "TERMINAL,LUG:I;2MM2XCU;RED",
//             Unit_Price: 200000000,
//             ABC_Indicator: "B",
//             Estimasi_Lead_Time_Mon: 3401429,
//             Estimasi_Lead_Time_Day: 102042857,
//             Estimasi_Lead_Time_Year: 279569,
//             Ongkos_Pesan_deterministik: 1000000,
//             Ongkos_Simpan_Barang_deterministik: 30000000,
//         },
//     ]);
// });

// const manualCalc = (event, argModel, argColor) => {
//     document.getElementById("domAggrid").classList.add("hidden");
//     const calcModel = document.querySelectorAll(".calc-model");
//     Object.values(calcModel).map((item) => {
//         item.classList.add("hidden");
//     });

//     document.getElementById("boxManual").classList.remove("hidden");
//     document.getElementById("boxManual").classList.add("flex");

//     document.getElementById(argModel).classList.remove("hidden");
//     document.getElementById(argModel).classList.add("flex");

//     document.querySelector(".hover\\:bg-\\[\\#1A8FCB\\]").classList.remove("bg-[#1A8FCB]");
//     document.querySelector(".hover\\:bg-\\[\\#47AD41\\]").classList.remove("bg-[#47AD41]");
//     document.querySelector(".hover\\:bg-\\[\\#F9CD2B\\]").classList.remove("bg-[#F9CD2B]");
//     document.querySelector(".hover\\:bg-\\[\\#F68B33\\]").classList.remove("bg-[#F68B33]");
//     document.querySelector(".hover\\:bg-\\[\\#7961F2\\]").classList.remove("bg-[#7961F2]");
//     document.querySelector(".hover\\:bg-\\[\\#F33D3D\\]").classList.remove("bg-[#F33D3D]");
//     document.querySelector(".hover\\:bg-\\[\\#E667E6\\]").classList.remove("bg-[#E667E6]");
//     document.querySelector(".hover\\:bg-\\[\\#FF5975\\]").classList.remove("bg-[#FF5975]");

//     document.querySelector(".hover\\:bg-\\[\\#1A8FCB\\]").classList.remove("text-white");
//     document.querySelector(".hover\\:bg-\\[\\#47AD41\\]").classList.remove("text-white");
//     document.querySelector(".hover\\:bg-\\[\\#F9CD2B\\]").classList.remove("text-white");
//     document.querySelector(".hover\\:bg-\\[\\#F68B33\\]").classList.remove("text-white");
//     document.querySelector(".hover\\:bg-\\[\\#7961F2\\]").classList.remove("text-white");
//     document.querySelector(".hover\\:bg-\\[\\#F33D3D\\]").classList.remove("text-white");
//     document.querySelector(".hover\\:bg-\\[\\#E667E6\\]").classList.remove("text-white");
//     document.querySelector(".hover\\:bg-\\[\\#FF5975\\]").classList.remove("text-white");

//     document.getElementById(`${argModel}N`).classList.add(`bg-[#${argColor}]`);
//     document.getElementById(`${argModel}N`).classList.add("text-white");
// };

// const viewResult = () => {
//     boxLoadingUpload.classList.remove("hidden");
//     boxLoadingUpload.classList.add("flex");
// };

// const closeLoad = () => {
//     boxLoadingUpload.classList.add("hidden");
//     boxLoadingUpload.classList.remove("flex");
// };
