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
let dataClass = [];
let dataModel = {};
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
                <div>Subset Data</div>
            </div>
            <div id="aggrid-website" class="ag-theme-quartz w-full h-full"></div>
        </div>`;

        columnDefs.subset = [
            { headerName: "Posting Date", field: "Posting Date", minWidth: 150 },
            { headerName: "Material Code", field: "Material_Code", minWidth: 150 },
            { headerName: "Material Description", field: "Material Description", minWidth: 150 },
            { headerName: "Quantity(EA)", field: "Quantity(EA)", minWidth: 150 },
            { headerName: "Movement Type", field: "Movement Type", minWidth: 150 },
        ];

        setupAggrid(dataSubset, columnDefs.subset, false);
    }

    if (agT === "class") {
        header.textContent = "Data Klasifikasi";
        headerAction.innerHTML = "";

        childContent.innerHTML = `<div class="w-full h-full bg-white rounded-xl shadow p-3 flex flex-col gap-3">
            <div class="w-full flex justify-between text-sm">
                <div>Data Klasifikasi</div>
            </div>
            <div id="aggrid-website" class="ag-theme-quartz w-full h-full"></div>
        </div>`;

        columnDefs.filtered = [
            { headerName: "Material Code", field: "Material_Code", minWidth: 150 },
            { headerName: "Material Description", field: "Material Description", minWidth: 150 },
            { headerName: "Kategori", field: "Kategori", minWidth: 150 },
            { headerName: "Proses 1", field: "Proses1", minWidth: 150 },
            { headerName: "Proses 2", field: "Proses2", minWidth: 150 },
            { headerName: "Jumlah Data", field: "Jumlah_Data", minWidth: 150 },
            { headerName: "Rata-Rata", field: "Rata_Rata", minWidth: 150 },
            { headerName: "Variansi", field: "Variansi", minWidth: 150 },
            { headerName: "Standar Deviasi", field: "Standar_Deviasi", minWidth: 150 },
            { headerName: "P Value", field: "P_Value", minWidth: 150 },
            { headerName: "Deskripsi Pengujian Statistik", field: "Deskripsi_Pengujian_Statistik", minWidth: 150 },
            { headerName: "Hasil Uji", field: "Hasil_uji", minWidth: 150 },
        ];

        try {
            headerAction.innerHTML = `<button id="btn-process-model" class="bg-transparent hover:bg-blue-500 text-blue-700 font-semibold hover:text-white py-2 px-4 border border-blue-500 hover:border-transparent rounded text-xs">Proses Tiap Kategori</button>`;
            document.getElementById("btn-process-model").addEventListener("click", () => model());
        } catch (error) {
            void 0;
        }

        setupAggrid(dataClass, columnDefs.filtered, false);
    }

    if (agT === "q") {
        header.textContent = "Model Q (Pola Normal)";
        headerAction.innerHTML = "";

        childContent.innerHTML = `<div class="w-full h-full bg-white rounded-xl shadow p-3 flex flex-col gap-3">
            <div class="w-full flex justify-between text-sm">
                <div>Data Hasil Model Q</div>
            </div>
            <div id="aggrid-website" class="ag-theme-quartz w-full h-full"></div>
        </div>`;

        columnDefs.q = [
            { headerName: "Material Code", field: "Material Code", minWidth: 150 },
            { headerName: "Material Description", field: "Material Description", minWidth: 150 },
            { headerName: "ABC Indicator", field: "ABC Indicator", minWidth: 150 },
            { headerName: "Rata - Rata Permintaan Barang (D) Unit/Tahun", field: "Rata - Rata Permintaan Barang (D) Unit/Tahun", minWidth: 150 },
            { headerName: "Standar Deviasi Permintaan Barang (s) Unit/Tahun", field: "Standar Deviasi Permintaan Barang (s) Unit/Tahun", minWidth: 150 },
            { headerName: "Lead Time (L) Tahun", field: "Lead Time (L) Tahun", minWidth: 150 },
            { headerName: "Ongkos Pesan (A) /Pesan", field: "Ongkos Pesan (A) /Pesan", minWidth: 150 },
            { headerName: "Harga Barang (p) /Unit", field: "Harga Barang (p) /Unit", minWidth: 150 },
            { headerName: "Ongkos Simpan (h) /Unit/Tahun", field: "Ongkos Simpan (h) /Unit/Tahun", minWidth: 150 },
            { headerName: "Ongkos Kekurangan Inventori (Cu) /Unit/Tahun", field: "Ongkos Kekurangan Inventori (Cu) /Unit/Tahun", minWidth: 150 },
            { headerName: "Standar Deviasi Permintaan Barang Waktu Lead Time (SL) Unit/Tahun", field: "Standar Deviasi Permintaan Barang Waktu Lead Time (SL) Unit/Tahun", minWidth: 150 },
            { headerName: "Rata - Rata Permintaan Barang Waktu Lead Time (DL) Unit/Tahun", field: "Rata - Rata Permintaan Barang Waktu Lead Time (DL) Unit/Tahun", minWidth: 150 },
            { headerName: "Lot Pengadaan Optimum Barang (EOQ) Unit/Pesanan", field: "Lot Pengadaan Optimum Barang (EOQ) Unit/Pesanan", minWidth: 150 },
            { headerName: "Reorder Point (ROP) Unit", field: "Reorder Point (ROP) Unit", minWidth: 150 },
            { headerName: "Safety Stock (SS) Unit", field: "Safety Stock (SS) Unit", minWidth: 150 },
            { headerName: "Frequensi Pemesanan (f)", field: "Frequensi Pemesanan (f)", minWidth: 150 },
            { headerName: "Ongkos Pembelian (Ob) /Tahun", field: "Ongkos Pembelian (Ob) /Tahun", minWidth: 150 },
            { headerName: "Ongkos Pemesanan (Op) /Tahun", field: "Ongkos Pemesanan (Op) /Tahun", minWidth: 150 },
            { headerName: "Ongkos Penyimpanan (Os) /Tahun", field: "Ongkos Penyimpanan (Os) /Tahun", minWidth: 150 },
            { headerName: "Ongkos Kekurangan Inventori (Ok) /Tahun", field: "Ongkos Kekurangan Inventori (Ok) /Tahun", minWidth: 150 },
            { headerName: "Ongkos Inventori (OT) /Tahun", field: "Ongkos Inventori (OT) /Tahun", minWidth: 150 },
        ];

        setupAggrid(dataModel.q, columnDefs.q, false);
    }

    if (agT === "wilson") {
        header.textContent = "Model Wilson (Pola Deterministik)";
        headerAction.innerHTML = "";

        childContent.innerHTML = `<div class="w-full h-full bg-white rounded-xl shadow p-3 flex flex-col gap-3">
            <div class="w-full flex justify-between text-sm">
                <div>Data Hasil Model Wilson</div>
            </div>
            <div id="aggrid-website" class="ag-theme-quartz w-full h-full"></div>
        </div>`;

        columnDefs.wilson = [
            { headerName: "Material Code", field: "Material Code", minWidth: 150 },
            { headerName: "Material Description", field: "Material Description", minWidth: 150 },
            { headerName: "ABC Indicator", field: "ABC Indicator", minWidth: 150 },
            { headerName: "Permintaan Barang (D) Unit/Tahun", field: "Permintaan Barang (D) Unit/Tahun", minWidth: 150 },
            { headerName: "Harga Barang (p) /Unit", field: "Harga Barang (p) /Unit", minWidth: 150 },
            { headerName: "Ongkos Pesan (A) /Pesan", field: "Ongkos Pesan (A) /Pesan", minWidth: 150 },
            { headerName: "Lead Time (L) Tahun", field: "Lead Time (L) Tahun", minWidth: 150 },
            { headerName: "Ongkos Simpan (h) /Unit/Tahun", field: "Ongkos Simpan (h) /Unit/Tahun", minWidth: 150 },
            { headerName: "Lot Pengadaan (EOQ) Unit/Pesanan", field: "Lot Pengadaan (EOQ) Unit/Pesanan", minWidth: 150 },
            { headerName: "Reorder Point (ROP) Unit", field: "Reorder Point (ROP) Unit", minWidth: 150 },
            { headerName: "Selang Waktu Pesan Kembali (Tahun)", field: "Selang Waktu Pesan Kembali (Tahun)", minWidth: 150 },
            { headerName: "Selang Waktu Pesan Kembali (Bulan)", field: "Selang Waktu Pesan Kembali (Bulan)", minWidth: 150 },
            { headerName: "Selang Waktu Pesan Kembali (Hari)", field: "Selang Waktu Pesan Kembali (Hari)", minWidth: 150 },
            { headerName: "Frequensi Pemesanan (f)", field: "Frequensi Pemesanan (f)", minWidth: 150 },
            { headerName: "Ongkos Pembelian (Ob) /Tahun", field: "Ongkos Pembelian (Ob) /Tahun", minWidth: 150 },
            { headerName: "Ongkos Pemesanan (Op) /Tahun", field: "Ongkos Pemesanan (Op) /Tahun", minWidth: 150 },
            { headerName: "Ongkos Penyimpanan (Os) /Tahun", field: "Ongkos Penyimpanan (Os) /Tahun", minWidth: 150 },
            { headerName: "Ongkos Inventori (OT) /Tahun", field: "Ongkos Inventori (OT) /Tahun", minWidth: 150 },
        ];

        setupAggrid(dataModel.wilson, columnDefs.wilson, false);
    }

    if (agT === "poisson") {
        header.textContent = "Model Poisson (Pola Poisson)";
        headerAction.innerHTML = "";

        childContent.innerHTML = `<div class="w-full h-full bg-white rounded-xl shadow p-3 flex flex-col gap-3">
            <div class="w-full flex justify-between text-sm">
                <div>Data Hasil Model Poisson</div>
            </div>
            <div id="aggrid-website" class="ag-theme-quartz w-full h-full"></div>
        </div>`;

        columnDefs.poisson = [
            { headerName: "Material Code", field: "Material Code", minWidth: 150 },
            { headerName: "Material Description", field: "Material Description", minWidth: 150 },
            { headerName: "ABC Indicator", field: "ABC Indicator", minWidth: 150 },
            { headerName: "Rata - Rata Permintaan Barang (D) Unit/Tahun", field: "Rata - Rata Permintaan Barang (D) Unit/Tahun", minWidth: 150 },
            { headerName: "Standar Deviasi Permintaan Barang (s) Unit/Tahun", field: "Standar Deviasi Permintaan Barang (s) Unit/Tahun", minWidth: 150 },
            { headerName: "Lead Time (L) Tahun", field: "Lead Time (L) Tahun", minWidth: 150 },
            { headerName: "Ongkos Pesan (A) /Pesan", field: "Ongkos Pesan (A) /Pesan", minWidth: 150 },
            { headerName: "Harga Barang (p) /Unit", field: "Harga Barang (p) /Unit", minWidth: 150 },
            { headerName: "Ongkos Simpan (h) /Unit/Tahun", field: "Ongkos Simpan (h) /Unit/Tahun", minWidth: 150 },
            { headerName: "Ongkos Kekurangan Inventori (Cu) /Unit/Tahun", field: "Ongkos Kekurangan Inventori (Cu) /Unit/Tahun", minWidth: 150 },
            { headerName: "Nilai Alpha", field: "Nilai Alpha", minWidth: 150 },
            { headerName: "Standar Deviasi Waktu Ancang - Ancang (SL) Unit/Tahun", field: "Standar Deviasi Waktu Ancang - Ancang (SL) Unit/Tahun", minWidth: 150 },
            { headerName: "Economic Order Quantity (EOQ) Lot Optimum (qo1)", field: "Economic Order Quantity (EOQ) Lot Optimum (qo1)", minWidth: 150 },
            { headerName: "Reorder Point (ROP) Unit", field: "Reorder Point (ROP) Unit", minWidth: 150 },
            { headerName: "Safety Stock (SS) Unit", field: "Safety Stock (SS) Unit", minWidth: 150 },
            { headerName: "Service Level (%)", field: "Service Level (%)", minWidth: 150 },
            { headerName: "Ongkos Inventori (OT) /Tahun", field: "Ongkos Inventori (OT) /Tahun", minWidth: 150 },
        ];

        setupAggrid(dataModel.poisson, columnDefs.poisson, false);
    }

    if (agT === "tchebycheff") {
        header.textContent = "Model Tchebycheff (Pola Tak - Tentu)";
        headerAction.innerHTML = "";

        childContent.innerHTML = `<div class="w-full h-full bg-white rounded-xl shadow p-3 flex flex-col gap-3">
            <div class="w-full flex justify-between text-sm">
                <div>Data Hasil Model Tchebycheff</div>
            </div>
            <div id="aggrid-website" class="ag-theme-quartz w-full h-full"></div>
        </div>`;

        columnDefs.tchebycheff = [
            { headerName: "Material Code", field: "Material Code", minWidth: 150 },
            { headerName: "Material Description", field: "Material Description", minWidth: 150 },
            { headerName: "ABC Indicator", field: "ABC Indicator", minWidth: 150 },
            { headerName: "Harga Barang (p) /Unit", field: "Harga Barang (p) /Unit", minWidth: 150 },
            { headerName: "Kerugian Ketidakadaan Barang (Cu) /Unit", field: "Kerugian Ketidakadaan Barang (Cu) /Unit", minWidth: 150 },
            { headerName: "Standar Deviasi Permintaan Barang (s)", field: "Standar Deviasi Permintaan Barang (s)", minWidth: 150 },
            { headerName: "Rata - Rata Permintaan Barang (alpha)", field: "Rata - Rata Permintaan Barang (alpha)", minWidth: 150 },
            { headerName: "Nilai K Model Tchebycheff", field: "Nilai K Model Tchebycheff", minWidth: 150 },
            { headerName: "Lot Pemesanan Optimal (q0)", field: "Lot Pemesanan Optimal (q0)", minWidth: 150 },
        ];

        setupAggrid(dataModel.tchebycheff, columnDefs.tchebycheff, false);
    }

    if (agT === "regret") {
        header.textContent = "Model Regret (Pola Non Moving)";
        headerAction.innerHTML = "";

        childContent.innerHTML = `<div class="w-full h-full bg-white rounded-xl shadow p-3 flex flex-col gap-3">
            <div class="w-full flex justify-between text-sm">
                <div>Data Hasil Model Regret</div>
            </div>
            <div id="aggrid-website" class="ag-theme-quartz w-full h-full"></div>
        </div>`;

        columnDefs.regret = [
            { headerName: "Material Code", field: "Material Code", minWidth: 150 },
            { headerName: "Material Description", field: "Material Description", minWidth: 150 },
            { headerName: "ABC Indicator", field: "ABC Indicator", minWidth: 150 },
            { headerName: "Ongkos Pemakaian Komponen (H)", field: "Ongkos Pemakaian Komponen (H)", minWidth: 150 },
            { headerName: "Ongkos Kerugian Akibat Kerusakan (L)", field: "Ongkos Kerugian Akibat Kerusakan (L)", minWidth: 150 },
            { headerName: "Jumlah Komponen Terpasang (m)", field: "Jumlah Komponen Terpasang (m)", minWidth: 150 },
            { headerName: "Harga Resale Komponen (O)", field: "Harga Resale Komponen (O)", minWidth: 150 },
            { headerName: "Minimum Regret (Rp )", field: "Minimum Regret (Rp )", minWidth: 150 },
            { headerName: "Strategi Penyediaan Optimal (Unit)", field: "Strategi Penyediaan Optimal (Unit)", minWidth: 150 },
        ];

        setupAggrid(dataModel.regret, columnDefs.regret, false);
    }

    if (agT === "linear") {
        header.textContent = "Model Linear (Pola Non Moving)";
        headerAction.innerHTML = "";

        childContent.innerHTML = `<div class="w-full h-full bg-white rounded-xl shadow p-3 flex flex-col gap-3">
            <div class="w-full flex justify-between text-sm">
                <div>Data Hasil Model Linear</div>
            </div>
            <div id="aggrid-website" class="ag-theme-quartz w-full h-full"></div>
        </div>`;

        columnDefs.linear = [
            { headerName: "Material Code", field: "Material Code", minWidth: 150 },
            { headerName: "Material Description", field: "Material Description", minWidth: 150 },
            { headerName: "ABC Indicator", field: "ABC Indicator", minWidth: 150 },
            { headerName: "Ongkos Pemakaian Komponen (H)", field: "Ongkos Pemakaian Komponen (H)", minWidth: 150 },
            { headerName: "Ongkos Kerugian Akibat Kerusakan (L)", field: "Ongkos Kerugian Akibat Kerusakan (L)", minWidth: 150 },
            { headerName: "Jumlah Komponen Terpasang (m)", field: "Jumlah Komponen Terpasang (m)", minWidth: 150 },
            { headerName: "Harga Resale Komponen (O)", field: "Harga Resale Komponen (O)", minWidth: 150 },
            { headerName: "Ongkos Model Probabilistik Kerusakan", field: "Ongkos Model Probabilistik Kerusakan", minWidth: 150 },
            { headerName: "Strategi Penyediaan Optimal (Unit)", field: "Strategi Penyediaan Optimal (Unit)", minWidth: 150 },
        ];

        setupAggrid(dataModel.linear, columnDefs.linear, false);
    }

    if (agT === "non-linear") {
        header.textContent = "Model Non Linear (Pola Non Moving)";
        headerAction.innerHTML = "";

        childContent.innerHTML = `<div class="w-full h-full bg-white rounded-xl shadow p-3 flex flex-col gap-3">
            <div class="w-full flex justify-between text-sm">
                <div>Data Hasil Model Non Linear</div>
            </div>
            <div id="aggrid-website" class="ag-theme-quartz w-full h-full"></div>
        </div>`;

        columnDefs.nonlinear = [
            { headerName: "Material Code", field: "Material Code", minWidth: 150 },
            { headerName: "Material Description", field: "Material Description", minWidth: 150 },
            { headerName: "ABC Indicator", field: "ABC Indicator", minWidth: 150 },
            { headerName: "Ongkos Pemakaian Komponen (H)", field: "Ongkos Pemakaian Komponen (H)", minWidth: 150 },
            { headerName: "Ongkos Kerugian Akibat Kerusakan (L)", field: "Ongkos Kerugian Akibat Kerusakan (L)", minWidth: 150 },
            { headerName: "Jumlah Komponen Terpasang (m)", field: "Jumlah Komponen Terpasang (m)", minWidth: 150 },
            { headerName: "Harga Resale Komponen (O)", field: "Harga Resale Komponen (O)", minWidth: 150 },
            { headerName: "Ongkos Model Probabilistik Kerusakan", field: "Ongkos Model Probabilistik Kerusakan", minWidth: 150 },
            { headerName: "Strategi Penyediaan Optimal (Unit)", field: "Strategi Penyediaan Optimal (Unit)", minWidth: 150 },
        ];

        setupAggrid(dataModel.nonlinear, columnDefs.nonlinear, false);
    }

    if (agT === "bcr") {
        header.textContent = "Model BCR (Pola BCR)";
        headerAction.innerHTML = "";

        childContent.innerHTML = `<div class="w-full h-full bg-white rounded-xl shadow p-3 flex flex-col gap-3">
            <div class="w-full flex justify-between text-sm">
                <div>Data Hasil Model BCR</div>
            </div>
            <div id="aggrid-website" class="ag-theme-quartz w-full h-full"></div>
        </div>`;

        columnDefs.bcr = [
            { headerName: "Material Code", field: "Material Code", minWidth: 150 },
            { headerName: "Material Description", field: "Material Description", minWidth: 150 },
            { headerName: "ABC Indicator", field: "ABC Indicator", minWidth: 150 },
            { headerName: "Harga Komponen (Ho)", field: "Harga Komponen (Ho)", minWidth: 150 },
            { headerName: "Kerugian Komponen (Co)", field: "Kerugian Komponen (Co)", minWidth: 150 },
            { headerName: "Suku Bunga (i)", field: "Suku Bunga (i)", minWidth: 150 },
            { headerName: "Waktu Sisa Operasi (tahun)", field: "Waktu Sisa Operasi (tahun)", minWidth: 150 },
            { headerName: "Benefit-Cost Ratio (BCR)", field: "Benefit-Cost Ratio (BCR)", minWidth: 150 },
            { headerName: "Strategi Penyediaan Optimal (Tahun)", field: "Strategi Penyediaan Optimal (Tahun)", minWidth: 150 },
            { headerName: "Jenis Probabilitas", field: "Jenis Probabilitas", minWidth: 150 },
            { headerName: "Pesan", field: "Pesan", minWidth: 150 },
        ];

        setupAggrid(dataModel.bcr, columnDefs.bcr, false);
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

        fileIdNow < [...inpFile.files].length - 1 ? uploadFile(fileIdNow + 1) : tools("mentah");
    } catch (error) {
        void 0;
    }
};

const subset = async () => {
    let lengData = 0;

    Object.values(dataMentah).map((item) => (lengData += item.length));

    let times = Object.values(dataMentah).reduce((sum, data) => sum + data.length, 0);
    const idProgress = progresBar("Filterisasi Data", "Normalisasi data Input Histori Good Issue (GI)", times);

    const responseSubset = await postFetch("subset", { session: sId });

    if (responseSubset[0] !== "success") {
        notification("show", "Gagal mengolah data");
        sInterval[idProgress] = "done";
        return;
    }

    sInterval[idProgress] === "done" ? progresBarStatus(idProgress) : (sInterval[idProgress] = "done");

    dataSubset = responseSubset[1];
    tools("subset");
    filtered();
};

const filtered = async () => {
    let times = dataSubset.length;

    const idProgress = progresBar("Filterisasi Data", "Filtering data Histori Good Issue (GI)", times);

    const responseClass = await postFetch("classification", { session: sId });

    if (responseClass[0] !== "success") {
        notification("show", "Gagal mengolah data");
        sInterval[idProgress] = "done";
        return;
    }

    sInterval[idProgress] === "done" ? progresBarStatus(idProgress) : (sInterval[idProgress] = "done");

    dataClass = responseClass[1];
    tools("class");
};

const model = async () => {
    let times = dataClass.length;

    const idProgress = progresBar("Filterisasi Data", "Filtering data Histori Good Issue (GI)", times);

    const responseModel = await postFetch("model-to-calc", { session: sId });

    if (responseModel[0] !== "success") {
        notification("show", "Gagal mengolah data");
        sInterval[idProgress] = "done";
        return;
    }

    sInterval[idProgress] === "done" ? progresBarStatus(idProgress) : (sInterval[idProgress] = "done");

    dataModel = responseModel[1];
    tools("q");
};

const setHeight = () => document.getElementById("container").style.setProperty("--vh", `${window.innerHeight * 0.01}px`);
const setLoading = (value) => gridApi.setGridOption("loading", value);

childTools.querySelectorAll(".tools").forEach((element) => element.addEventListener("click", () => tools(element.getAttribute("data-tools"))));
inpFile.addEventListener("change", () => uploadFile(fileId));
btnChevron.addEventListener("click", () => miniNav());
window.addEventListener("resize", setHeight);

document.addEventListener("DOMContentLoaded", async () => {
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
