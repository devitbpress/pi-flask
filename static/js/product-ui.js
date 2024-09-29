let datasetProduct = [];

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

    if (agT === "products") {
        header.textContent = "List Produk";
        headerAction.innerHTML = "";

        childContent.innerHTML = `<div class="w-full h-full bg-white rounded-xl shadow p-3 flex flex-col gap-3">
            <div class="w-full flex justify-between text-xs">
                <div>Produk PI</div>
                <div class="flex gap-2 justify-between items-center">
                    <span>Cari Data</span>
                    <input oninput="inpSearch(event)" type="text" placeholder="cari..." class="outline-none border py-1 px-2 rounded border-green-500" />
                    <button onclick="downloadCsv()" class="ml-4 bg-transparent hover:bg-green-500 text-green-700 hover:text-white py-1 px-2 border border-green-500 hover:border-transparent rounded">Export CSV</button>
                </div>
            </div>
            <div id="aggrid-website" class="ag-theme-quartz w-full h-full"></div>
        </div>`;

        columnDefs["products"] = [
            { headerName: "Material Code", field: "p_code", minWidth: 150 },
            { headerName: "Material Description", field: "p_description", minWidth: 100 },
            { headerName: "Unit Price", field: "p_price", minWidth: 100 },
            { headerName: "Estimasi Lead Time (mon)", field: "p_lead_m", minWidth: 150 },
            { headerName: "Estimasi Lead Time (day)", field: "p_lead_d", minWidth: 150 },
        ];

        setupAggrid(datasetProduct, columnDefs.products, false);
    }
};

const setProduct = async () => {
    const idProgress = progresBar("GET Data", `Produk PI`, 15000);

    const responseProduct = await postFetch("get-product");

    sInterval[idProgress] === "done" ? progresBarStatus(idProgress) : (sInterval[idProgress] = "done");

    if (responseProduct[0] !== "success") {
        notification("show", "Gagal ambil data produk", "failed");
        return;
    }

    notification("show", "Berhasil ambil data produk", "success");

    datasetProduct = responseProduct[1].map((prod) => {
        prod.p_price = `Rp ${prod.p_price.toLocaleString("id-ID")}`;
        return prod;
    });

    tools("products");
};

const inpSearch = (event) => searchData(event.target.value);

document.addEventListener("DOMContentLoaded", async () => {
    setHeight();

    const ParamTools = urlParams.get("t");
    if (ParamTools) {
        tools(ParamTools);
    } else {
        url.searchParams.set("t", "products");
        window.history.replaceState({}, "", url.toString());
        tools("products");
    }

    setTimeout(() => miniNav(), 150);

    setProduct();
});
