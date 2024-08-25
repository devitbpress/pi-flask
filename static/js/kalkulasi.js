const domUnggah = document.getElementById("domUnggah");
const domAggrid = document.getElementById("domAggrid");
const listFile = document.getElementById("listFile");
const listModel = document.getElementById("listModel");
const boxBtnKlasifikasi = document.getElementById("boxBtnKlasifikasi");
const btnKlasifikasi = document.getElementById("btnKlasifikasi");
const spinKlasifikasi = document.getElementById("spinKlasifikasi");
const boxBtnModel = document.getElementById("boxBtnModel");
const btnModel = document.getElementById("btnModel");
const slcDataMentah = document.getElementById("slcDataMentah");
const slcKalkulator = document.getElementById("slcKalkulator");
const boxListUploaded = document.getElementById("boxListUploaded");
const lblFile = document.getElementById("lblFile");
const btnUnggah = document.getElementById("btnUnggah");
const boxLoadingUpload = document.getElementById("boxLoadingUpload");

let gridApi;
let dataFrameAll = {};
const url = {
    df2016: `https://script.googleusercontent.com/macros/echo?user_content_key=LapeqqujSCVeQvmpzT5bkMgzXWkxwgiu1mURRM-isA7bygQPmY_RZm60CWSziiKYTmAZpdMfy43Rxh9ZLE6-MhKVo_UWvr9xm5_BxDlH2jW0nuo2oDemN9CCS2h10ox_1xSncGQajx_ryfhECjZEnGuO4qDBLlAQWG3HIimfwOnfbTaRnZZ6p2dRBUozm3HtuS7akCaZpH19msygRfVm6PmaP9D1eKTXkUPqQxDsfEQwoK-KYyzZsw&lib=MPESXYQJhVskUi_ALc6m-eCI2ydRSHzvq`,
    df2017: `https://script.googleusercontent.com/macros/echo?user_content_key=XaWyXGs6pAzckkvNYAPH872HBjmf8OGqWCAOkRTvOfQLEMeWz6WOa8mEriAE36F6LlhQqVrZfV0ZpO5NWYNbmQnngGj7mkoKm5_BxDlH2jW0nuo2oDemN9CCS2h10ox_1xSncGQajx_ryfhECjZEnD96G-rnTZVZWVFeAXwnGo2n28Wp3Ma6gwZkxmdRhTA3URxiSvgzUCpHQ3vZNCE26EHgXbaYjhT8WpCe3tkmz8Yy3BlvxlezCg&lib=MNGASYCfPbrrldgWvv5FC9yI2ydRSHzvq`,
    df2018: `https://script.googleusercontent.com/macros/echo?user_content_key=OtjOmAn4DKa8pj-UIvdwZ-_ab4u0YIMpk9v52aKDpl6TtH-j6r1W4wsUtrbAb203mtUmMubmarzZ8vq8C_6SiMkhmxa_NKuTm5_BxDlH2jW0nuo2oDemN9CCS2h10ox_1xSncGQajx_ryfhECjZEnCChdS3B0SKOyu3FPoPejWdJTy2H7CZ6gyPuoHxKd1_z332WkDTbqy1FpncTkkIm8cRAFp1mT9fjy-ue-R8wLpNpANH6yBi_3Q&lib=MMFFfMc36Tz7gdAWaZVhwnyI2ydRSHzvq`,
    df2019: `https://script.googleusercontent.com/macros/echo?user_content_key=PqhKJ8x_8iuVLQj8sy40ECBrCUSDUa8SXeLO2XycHIHYcd2Xw0_NSmxdzYcKZLDhUd7yFuPbeLeP2ARztW-cnbjcCf7nRIyLm5_BxDlH2jW0nuo2oDemN9CCS2h10ox_1xSncGQajx_ryfhECjZEnF8BewZjzFdU--TqpTHYU4NcBiCRoW8hS_q8gfwHMJrIOYCYsqoXWEODnOC4_yChAyUdW5ckvAeYgkzvY8zy2X6MHARCYiyXAA&lib=MWINTYQUnhvaXxg6pVnWt3yI2ydRSHzvq`,
    df2020: `https://script.googleusercontent.com/macros/echo?user_content_key=iKtBwsDz9yHBRN83bIvSDGyb3DluuOsrtVk-IMpPozv7Eq9n07c3Knqd3KYS1rHOxj_rwQo2lUyOpLdcs8mL8Qbs7D-u6R9Cm5_BxDlH2jW0nuo2oDemN9CCS2h10ox_1xSncGQajx_ryfhECjZEnMfhlPR8yprj3k-xB9tvquy_2wS0AWoYNWq_QjXVJR4g8OO9AvZHFdPXnqqgncEkSxba90-zg_rvtzLP4PgEs7Hb3lj62okUAQ&lib=MBb1WDrCLO3r8IjyZ4G3XuCI2ydRSHzvq`,
    df2021: `https://script.googleusercontent.com/macros/echo?user_content_key=7kyP4tbZ8gBjakK9LGfW-KoCmSqYmgv9I2WLYswvmvmeMoRonDp2d9gTB31weoQAZ6vK_i6LBZR5ws8vjMF9k1ljTGraIr2tm5_BxDlH2jW0nuo2oDemN9CCS2h10ox_1xSncGQajx_ryfhECjZEnP8coveGuXE2AdxQawEnZTQ_IlCcHl1HWmq8DA9DgXFtUdpDr2LhuEyY8BHGfD3ccAl6KIEdtudlVTWaYE7XZUXm_sh2_xlnMtz9Jw9Md8uu&lib=MdfDIPYIJ0m28seyijUDXJ6rp9mNFFq5w`,
    df2022: `https://script.googleusercontent.com/macros/echo?user_content_key=RJKrM8Z6mlYJw4Ib6Sea07J3flozNefKLyQWcQUGU93GPieen3W8iSAOgEqxojof9Ju_1dhFdqTbdnVsb9H18B9zxvCZrPZvm5_BxDlH2jW0nuo2oDemN9CCS2h10ox_1xSncGQajx_ryfhECjZEnNvGsJwTcFaW8j0bYOSi-hVKqizubQ5-7aq5rxt_eW_1PjwwVIBR5oJNmPyjP5PFbm0BYC5MmGpSBQr1iihMKFsm0gf0HLNCcQ&lib=MSYiCRwB9yk0AIa3uQGf7EiI2ydRSHzvq`,
    subset: `https://script.googleusercontent.com/macros/echo?user_content_key=LN6S6G4NoYPaI3ZMc8jXGJDrf3zY6mcAo-A1wS4NfaDzw_cEW4ZJ_QgjtDW-NeDPNbk_s4Tdu16hDqR2Hr64rUeUzjCVI4BEm5_BxDlH2jW0nuo2oDemN9CCS2h10ox_1xSncGQajx_ryfhECjZEnCZMSbKOriGDzCmAJzm0MPI6UMtnK9tTHVg_O9kLldhtfBiNqqKayMQ5_T3gqrlBqVJNoyZFPgzbO0cA-KM6pvxHw8t15glPrA&lib=MT6rcwllOd5tojifwud_qBCI2ydRSHzvq`,
    klasifikasi: `https://script.googleusercontent.com/macros/echo?user_content_key=RmiOuOvhnP-aO7QGulCMRyp05IZPT0DK1r2hrPMVkQQZeYz4Yr8jKEZtyt0g_JqTllvDjgIUwXKp5E53UkUDt82rpr7IRpPZm5_BxDlH2jW0nuo2oDemN9CCS2h10ox_1xSncGQajx_ryfhECjZEnPZZOrz8dqh2kLEV0Ss8b7C1chdi-JrQdv-hk8jivYQ7XTUDzM24GMvSfUL5gog476NN2ymws2VhInPA0r9S42t_Y-z0UIk399z9Jw9Md8uu&lib=MVTkoRexjagTHjHPsH-tfGqrp9mNFFq5w`,
    poisson: `https://script.googleusercontent.com/macros/echo?user_content_key=Zn2u8gPRHRBI6MUvnMdN7KWJNPd6jmtoA255Zkz-RFqJJXk3-4puAyG6NCln5nknnIB2KSwMQURSQvttRttuFn60cglgXypmm5_BxDlH2jW0nuo2oDemN9CCS2h10ox_1xSncGQajx_ryfhECjZEnLC2FM618Wk4ltzjeqJ7o4Zbr0XY3jS07ty4AO05ben5vuTdi03xoVhrRYOulF8d4wEcRek0DmYA71ELigH1jxCD4ZRneTVC1g&lib=M5oFFvavvXpNxNed9CnsdjiI2ydRSHzvq`,
    wilson: `https://script.googleusercontent.com/macros/echo?user_content_key=qjRFLKuQuJ2izkPvr3cbh-TqhOmJfVnyuJwq0qy0vp6F1Kmh17SiFAbJvdnda3cFNAZ1zcxuo-lSQvttRttuFrfxE8PTwNcbm5_BxDlH2jW0nuo2oDemN9CCS2h10ox_1xSncGQajx_ryfhECjZEnC6WcADXlS3Yz8UPMqXuHkpl1aeWXVjgC_syd-OdRp89Kwvqrt3sv0DDP5pUUUG9J20uKdyLZ7oABIhdHzhoIhE9ziJv9OQCog&lib=MnJn45aJNy0DKQMIlmFJ_lSI2ydRSHzvq`,
    q: `https://script.googleusercontent.com/macros/echo?user_content_key=iYVA00aYqCsT_4J8y5KEjIce8Re3cavzwNZLO2uIfW5VBklkf-uUynMSLe0fxBpzAqcoLzUeQSFSQvttRttuFjs_yIRjYhr7m5_BxDlH2jW0nuo2oDemN9CCS2h10ox_1xSncGQajx_ryfhECjZEnMj-ude2OAl6f-5ziaH5qbEaHMsiwAN7rp-UvtxQdOz_0kKE_c8ZK0AtLKGiUK7FvIhX-2M6tinfOVLT9Zwa4SrVR3ojIhiyxtz9Jw9Md8uu&lib=MI-FsJ9-71eoGw3FLA6ZHwKrp9mNFFq5w`,
    tchebycheff: `https://script.googleusercontent.com/macros/echo?user_content_key=c3983MJnmsWcMAFce87zt1tSaYd0uUVqcCbUARaEflfNLjPmhlk9msry7JLyrcfGpPcykI4ljHdSQvttRttuFqd7_pgvXFgAm5_BxDlH2jW0nuo2oDemN9CCS2h10ox_1xSncGQajx_ryfhECjZEnL14w6F4pH7o5xrQU2_5Dzipkk-eel3K-F-eUAQ3djNtRCpVKs9UlEeKpCDidiwzLXHFB2Z0DJLct6uWN-8etAjBpr6FYzE-jg&lib=MRcM6G4OwEId7Ewf59E4OiKrp9mNFFq5w`,
    minmaxregret: `https://script.googleusercontent.com/macros/echo?user_content_key=IPvIHEBwtjQ-fPtidsM9Fa4pBCa5EwvPIMeLJbTw9y0GY5BoykZ613DTxUHsRLEBkRR4NTU0VaZSQvttRttuFheWebAHguH1m5_BxDlH2jW0nuo2oDemN9CCS2h10ox_1xSncGQajx_ryfhECjZEnOIbk552ltPz_IBYrWlTcAbbWDbgOjEtqIBDy3ULL-YFsdoDZ0Py6QhbSV_EA7a358VSNUDzfYXfJLOitoVD6PFU8iUmcRhi7g&lib=MGq3AYgEnE7jjxrhqNOcI0yI2ydRSHzvq`,
    kerusakanlinear: `https://script.googleusercontent.com/macros/echo?user_content_key=YOwwpB3Ro6tvLDv5LGTkw5M_MDEWycVu6ypP8BtOxd4un8mC7ZKGmaX4gFFvw5hz0r0MjXS7LKVSQvttRttuFuT4tWDRgd0Im5_BxDlH2jW0nuo2oDemN9CCS2h10ox_1xSncGQajx_ryfhECjZEnN6qks3o3nTRE0EnlEOwwNQNWwjL0FOfVn-7sRrbX8NHZ487lGqUi_rg-LZXcx4kUSogzCL1pnxpvhuulzdSHYRM-AwBlVTIAw&lib=MbVMY4SDAVBfhcfc2wn6OpSI2ydRSHzvq`,
    kerusakannonlinear: `https://script.googleusercontent.com/macros/echo?user_content_key=d4aLrO9nibKf_pmYnJ90tQRg-Blvz1pTl3a-5Im97dab9wwJYRt4PshfMbV6IUa1di4pAp12oYFSQvttRttuFrNQJLkJGelXm5_BxDlH2jW0nuo2oDemN9CCS2h10ox_1xSncGQajx_ryfhECjZEnJ0nVbLxlaDrZA0R7cQRpmTqZQtgUf2cZ-CqXSVtatTzC8cQ19v9jDsz1YWzDwuQbNqYkgUt9T67YJJc38DiKqx2cfief25W5tz9Jw9Md8uu&lib=MDBg5H1jIbXWgJ-t-b5Rbm6rp9mNFFq5w`,
    bcr: `https://script.googleusercontent.com/macros/echo?user_content_key=Onf03N9QtAZRVYTFGJ5V9Y_pkgkwtDk23C3nh427TCZ3Nt9cech0EiYzHpO4eSKqHxCagHOoqbZSQvttRttuFpq2xukyhWc5m5_BxDlH2jW0nuo2oDemN9CCS2h10ox_1xSncGQajx_ryfhECjZEnLyNyGF7t8wrrnmPUTZaepNN_ioCJmaRklJ51LEB5WuzLk5soulfqylSOkkITgXiyvvx797OiO6ralgUtTRuaIZuTi7XbslkRtz9Jw9Md8uu&lib=M0aVgklHhzy5bZ6K0MjjtR6rp9mNFFq5w`,
};

let numUplaoded = 1;
let fileNameAll = [
    { name: "Histori GI SAP 2016.xlsx", size: 255184 },
    { name: "Histori GI SAP 2017.xlsx", size: 132535 },
    { name: "Histori GI SAP 2018 Bulan 1-12.xlsx", size: 1251425 },
    { name: "Histori GI SAP 2019 Bulan 1-12.xlsx", size: 3334554 },
    { name: "Histori GI SAP 2020 Bulan 1-12.xlsx", size: 6542678 },
    { name: "Histori GI SAP 2021 Bulan 1-12.xlsx", size: 631345 },
    { name: "Histori GI SAP 2022 Bulan 1-12.xlsx", size: 316155 },
];
let fileFix = {};

const getData = async (argUrl) => {
    if (dataFrameAll[argUrl]) {
        return dataFrameAll[argUrl];
    } else {
        try {
            const response = await fetch(url[argUrl]);
            const data = await response.json();
            dataFrameAll[argUrl] = data;
            return data;
        } catch (error) {
            console.error(error);
        }
    }
};

const setLoading = (value) => {
    gridApi.setGridOption("loading", value);
};

const filterAgGrid = (event) => {
    gridApi.setGridOption("quickFilterText", event.target.value);
};

const onBtnExport = () => {
    gridApi.exportDataAsCsv();
};

const setupAgGrid = (data_grid) => {
    const dom_grid = document.getElementById("aggrid");
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

const runLoading = (argType) => {
    boxLoadingUpload.classList.remove("hidden");
    boxLoadingUpload.classList.add("flex");

    document.getElementById("textPersen").textContent = "0 %";
    document.getElementById("barPersen").style.width = "0 %";

    if (argType === "klasifikasi") {
        document.getElementById("statusDown").textContent = "Klasifikasi Data";

        let number = 0;
        const interval = setInterval(() => {
            document.getElementById("textPersen").textContent = `${number + 1}%`;
            document.getElementById("barPersen").style.width = `${number + 1}%`;
            document.getElementById("statusUp").textContent = "Filtering data Histori Good Issue (GI)";
            number += 1;

            if (number >= 25) {
                document.getElementById("statusUp").textContent = "Agregasi Data";
            }

            if (number >= 70) {
                document.getElementById("statusUp").textContent = "Klasifikasi Material";
            }

            if (number >= 85) {
                document.getElementById("statusUp").textContent = "Identifikasi Pola Distribusi";
            }

            if (number >= 100) {
                clearInterval(interval);
                setTimeout(() => {
                    boxLoadingUpload.classList.remove("flex");
                    boxLoadingUpload.classList.add("hidden");
                    document.getElementById(`h5Klasifikasi`).classList.remove("hidden");
                    tabsResutl("", "klasifikasi", "h5Klasifikasi");

                    document.getElementById("textKlasifikasi").textContent = "Done";
                }, 150);
            }
        }, 5000 / 100);
    }

    if (argType === "kalkulator") {
        document.getElementById("statusDown").textContent = "Model Perhitungan";

        let number = 0;
        const interval = setInterval(() => {
            document.getElementById("textPersen").textContent = `${number + 1}%`;
            document.getElementById("barPersen").style.width = `${number + 1}%`;
            document.getElementById("statusUp").textContent = "Pola Normal => Model Q";
            number += 1;

            if (number >= 10) {
                document.getElementById("statusUp").textContent = "Pola Deterministik => Model Wilson";
            }

            if (number >= 30) {
                document.getElementById("statusUp").textContent = "Pola Poisson => Model Poisson";
            }

            if (number >= 50) {
                document.getElementById("statusUp").textContent = "Pola Tak Tentu => Model Tchebycheff";
            }

            if (number >= 70) {
                document.getElementById("statusUp").textContent = "Pola Non Moving => Model MaxMinRegret";
            }

            if (number >= 80) {
                document.getElementById("statusUp").textContent = "Pola Non Moving => Model Kerusakan Linear";
            }

            if (number >= 90) {
                document.getElementById("statusUp").textContent = "Pola Non Moving => Model Kerusakan Non Linear";
            }

            if (number >= 100) {
                clearInterval(interval);
                setTimeout(() => {
                    boxLoadingUpload.classList.remove("flex");
                    boxLoadingUpload.classList.add("hidden");
                    document.getElementById(`h5Kalkulator`).classList.remove("hidden");
                    tabsResutl("", "kalkulator", "h5Kalkulator");

                    document.getElementById("textModel").textContent = "Done";
                }, 150);
            }
        }, 7500 / 100);
    }
};

slcDataMentah.addEventListener("change", async () => {
    setLoading(true);
    setupAgGrid(await getData(slcDataMentah.value));
    setLoading(false);
});

slcKalkulator.addEventListener("change", async () => {
    setLoading(true);
    setupAgGrid(await getData(slcKalkulator.value));
    setLoading(false);
});

const formatFileSize = (size) => {
    const units = ["B", "KB", "MB", "GB", "TB"];
    let unitIndex = 0;
    while (size >= 1024 && unitIndex < units.length - 1) {
        size /= 1024;
        unitIndex++;
    }
    return `${size.toFixed(2)} ${units[unitIndex]}`;
};

const removeUploaded = (argNum, argName) => {
    document.getElementById(`fileUpload${argNum}`).remove();
    delete fileFix[argName];
};

btnUnggah.addEventListener("click", () => {
    let timeLoad = 0;
    let lengtTime = 0;
    Object.values(fileFix).map((item) => {
        setTimeout(() => {
            document.getElementById(`barUpload${item.id}`).style.width = "100%";
            let number = 0;
            const interval = setInterval(() => {
                document.getElementById(`persenUpload${item.id}`).textContent = `${number + 1}% Done`;
                number += 1;

                if (number >= 100) {
                    clearInterval(interval);
                    lengtTime += 1;
                    if (Object.values(fileFix).length === lengtTime) {
                        setTimeout(() => {
                            document.getElementById("h5Mentah").classList.remove("hidden");
                            document.getElementById("h5Subset").classList.remove("hidden");

                            tabsResutl("", "mentah", "h5Mentah");
                        }, 100);
                    }
                }
            }, 2500 / 100);
        }, timeLoad);

        timeLoad += 250;
    });

    btnUnggah.textContent = "Mengunggah ...";
});

lblFile.addEventListener("click", () => {
    fileNameAll.map((item) => {
        boxListUploaded.innerHTML += `
            <div id="fileUpload${numUplaoded}" class="w-full h-fit border-b flex gap-4 py-3 px-4 items-center">
                <img src="static/assets/excel.png" alt="excel" class="h-8" />
                <div class="flex flex-col w-full gap-1">
                    <div class="w-full flex justify-between">
                        <span>${item.name}</span>
                        <img onclick="removeUploaded(${numUplaoded}, '${item.name}')" src="static/assets/delete.png" alt="delete" class="w-5 h-5 cursor-pointer" />
                    </div>
                    <div class="relative w-full">
                        <div class="w-full h-2 bg-[#F68B33] rounded"></div>
                        <div id="barUpload${numUplaoded}" class="w-0 h-2 bg-[#47AD41] absolute top-0 left-0 rounded duration-[2500ms]"></div>
                    </div>
                    <div class="flex justify-between">
                        <span id="persenUpload${numUplaoded}">0% Done</span>
                        <span>${formatFileSize(item.size)}</span>
                    </div>
                </div>
            </div>
        `;

        item["id"] = numUplaoded;
        fileFix[item.name] = item;
        numUplaoded += 1;
    });
});

const tabsResutl = async (event, argTabs, id) => {
    const headers = boxTabs.getElementsByTagName("h5");
    Object.values(headers).map((item) => {
        item.classList.remove("border-b", "border-[#1A8FCB]", "text-[#1A8FCB]");
    });

    if (event === "") {
        document.getElementById(`${id}`).classList.add("border-b", "border-[#1A8FCB]", "text-[#1A8FCB]");
    } else {
        event.target.classList.add("border-b", "border-[#1A8FCB]", "text-[#1A8FCB]");
    }

    if (argTabs === "unggah") {
        // unggah
        domUnggah.classList.add("flex");
        domUnggah.classList.remove("hidden");

        // aggrid
        domAggrid.classList.add("hidden");
        domAggrid.classList.remove("flex");

        setTimeout(() => {
            domAggrid.classList.add("scale-0");
            domUnggah.classList.remove("scale-0");
        }, 150);
    } else {
        // unggah
        domUnggah.classList.remove("flex");
        domUnggah.classList.add("hidden");

        // aggrid
        domAggrid.classList.remove("hidden");
        domAggrid.classList.add("flex");

        // semua
        listFile.classList.add("hidden");
        listFile.classList.remove("flex");
        listModel.classList.add("hidden");
        listModel.classList.remove("flex");
        boxBtnKlasifikasi.classList.add("hidden");
        boxBtnKlasifikasi.classList.remove("flex");
        boxBtnModel.classList.add("hidden");
        boxBtnModel.classList.remove("flex");

        setTimeout(() => {
            domUnggah.classList.add("scale-0");
            domAggrid.classList.remove("scale-0");
        }, 150);

        setLoading(true);

        if (argTabs === "mentah") {
            listFile.classList.remove("hidden");
            listFile.classList.add("flex");
            setupAgGrid(await getData(slcDataMentah.value));
            setLoading(false);
        }
        if (argTabs === "subset") {
            boxBtnKlasifikasi.classList.remove("hidden");
            boxBtnKlasifikasi.classList.add("flex");
            setupAgGrid(await getData("subset"));
            setLoading(false);
        }
        if (argTabs === "klasifikasi") {
            boxBtnModel.classList.remove("hidden");
            boxBtnModel.classList.add("flex");
            setupAgGrid(await getData("klasifikasi"));
            setLoading(false);
        }
        if (argTabs === "kalkulator") {
            listModel.classList.remove("hidden");
            listModel.classList.add("flex");
            setupAgGrid(await getData(slcKalkulator.value));
            setLoading(false);
        }
    }
};

Object.keys(url).map((item) => {
    getData(item);
});
