const lblAmbil = document.getElementById("lblAmbil");

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

setupAgGrid();

lblAmbil.addEventListener("click", () => {
    document.getElementById("domAggrid").classList.remove("hidden");
    setupAgGrid([
        {
            Material: 6072060,
            Kategori: "Pola Deterministik",
            Rata_Rata: 59000000,
            Standar_Deviasi: 94000000,
            Material_Code: 6072060,
            Material_description: "BOLT,MACHINE:5/8IN UNCX50.8MM;HEX;B7",
            Unit_Price: 35000000,
            ABC_Indicator: "B",
            Estimasi_Lead_Time_Mon: 3,
            Estimasi_Lead_Time_Day: 90,
            Estimasi_Lead_Time_Year: 246575,
            Ongkos_Pesan_deterministik: 1000000,
            Ongkos_Simpan_Barang_deterministik: 5250000,
        },
        {
            Material: 6026100,
            Kategori: "Pola Deterministik",
            Rata_Rata: 727272727,
            Standar_Deviasi: 445176165,
            Material_Code: 6026100,
            Material_description: "TIE,CABLE:LOCK;2.5X100MM;PVC;PK/100",
            Unit_Price: 110000000,
            ABC_Indicator: "A",
            Estimasi_Lead_Time_Mon: 1496548,
            Estimasi_Lead_Time_Day: 44896429,
            Estimasi_Lead_Time_Year: 123004,
            Ongkos_Pesan_deterministik: 1000000,
            Ongkos_Simpan_Barang_deterministik: 16500000,
        },
        {
            Material: 6025576,
            Kategori: "Pola Deterministik",
            Rata_Rata: 266666667,
            Standar_Deviasi: 144337567,
            Material_Code: 6025576,
            Material_description: "TERMINAL,LUG:I;2MM2XCU;RED",
            Unit_Price: 200000000,
            ABC_Indicator: "B",
            Estimasi_Lead_Time_Mon: 3401429,
            Estimasi_Lead_Time_Day: 102042857,
            Estimasi_Lead_Time_Year: 279569,
            Ongkos_Pesan_deterministik: 1000000,
            Ongkos_Simpan_Barang_deterministik: 30000000,
        },
    ]);
});

const manualCalc = (event, argModel, argColor) => {
    document.getElementById("domAggrid").classList.add("hidden");
    const calcModel = document.querySelectorAll(".calc-model");
    Object.values(calcModel).map((item) => {
        item.classList.add("hidden");
    });

    document.getElementById("boxManual").classList.remove("hidden");
    document.getElementById("boxManual").classList.add("flex");

    document.getElementById(argModel).classList.remove("hidden");
    document.getElementById(argModel).classList.add("flex");

    document.querySelector(".hover\\:bg-\\[\\#1A8FCB\\]").classList.remove("bg-[#1A8FCB]");
    document.querySelector(".hover\\:bg-\\[\\#47AD41\\]").classList.remove("bg-[#47AD41]");
    document.querySelector(".hover\\:bg-\\[\\#F9CD2B\\]").classList.remove("bg-[#F9CD2B]");
    document.querySelector(".hover\\:bg-\\[\\#F68B33\\]").classList.remove("bg-[#F68B33]");
    document.querySelector(".hover\\:bg-\\[\\#7961F2\\]").classList.remove("bg-[#7961F2]");
    document.querySelector(".hover\\:bg-\\[\\#F33D3D\\]").classList.remove("bg-[#F33D3D]");
    document.querySelector(".hover\\:bg-\\[\\#E667E6\\]").classList.remove("bg-[#E667E6]");
    document.querySelector(".hover\\:bg-\\[\\#FF5975\\]").classList.remove("bg-[#FF5975]");

    document.querySelector(".hover\\:bg-\\[\\#1A8FCB\\]").classList.remove("text-white");
    document.querySelector(".hover\\:bg-\\[\\#47AD41\\]").classList.remove("text-white");
    document.querySelector(".hover\\:bg-\\[\\#F9CD2B\\]").classList.remove("text-white");
    document.querySelector(".hover\\:bg-\\[\\#F68B33\\]").classList.remove("text-white");
    document.querySelector(".hover\\:bg-\\[\\#7961F2\\]").classList.remove("text-white");
    document.querySelector(".hover\\:bg-\\[\\#F33D3D\\]").classList.remove("text-white");
    document.querySelector(".hover\\:bg-\\[\\#E667E6\\]").classList.remove("text-white");
    document.querySelector(".hover\\:bg-\\[\\#FF5975\\]").classList.remove("text-white");

    document.getElementById(`${argModel}N`).classList.add(`bg-[#${argColor}]`);
    document.getElementById(`${argModel}N`).classList.add("text-white");
};

const viewResult = () => {
    boxLoadingUpload.classList.remove("hidden");
    boxLoadingUpload.classList.add("flex");
};

const closeLoad = () => {
    boxLoadingUpload.classList.add("hidden");
    boxLoadingUpload.classList.remove("flex");
};
