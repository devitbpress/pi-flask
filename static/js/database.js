let gridApi;

const postData = async (argUrl, argData) => {
    try {
        const response = await fetch(argUrl, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify(argData),
        });

        if (!response.ok) {
            const errorData = await response.json();
            return ["failed", errorData.error];
        }

        const result = await response.json();
        return ["success", result];
    } catch (error) {
        return ["failed", error.message];
    }
};

const setupAggrid = async (agData, agLoad) => {
    const eGrid = document.getElementById("aggrid");
    let formatter = new Intl.NumberFormat("id-ID", { style: "currency", currency: "IDR", currencyDisplay: "symbol" });

    const columnDefs = [
        { headerName: "Material Code", field: "p_code", filter: true, minWidth: 170, maxWidth: 200, headerCheckboxSelection: true, checkboxSelection: true },
        { headerName: "Material Description", field: "p_description", filter: true, minWidth: 200, maxWidth: 250 },
        {
            headerName: "Unit Price",
            field: "p_price",
            filter: true,
            minWidth: 150,
            maxWidth: 200,
            cellStyle: { textAlign: "end" },
            filter: "agNumberColumnFilter",
            // valueFormatter: (params) => currencyFormatter(params.data.currency, "$"),
            // filter: "agNumberColumnFilter",
            // filterParams: {
            //     suppressAndOrCondition: true,
            //     filterOptions: ["greaterThan"],
            // },
        },
        { headerName: "Estimasi Lead Time (Mon)", field: "p_lead_m", filter: true, minWidth: 200, maxWidth: 300, cellStyle: { textAlign: "center" } },
        { headerName: "Estimasi Lead Time (Day)", field: "p_lead_d", filter: true, minWidth: 200, maxWidth: 300, cellStyle: { textAlign: "center" } },
    ];

    const rowData = agData.map((item) => {
        item.p_price = formatter.format(parseInt(item.p_price));
        return item;
    });

    defaultColDef = { flex: 1 };
    const selectBox = (event) => (orderSelected = event.api.getSelectedRows());

    const gridOptions = {
        columnDefs: columnDefs,
        rowData: rowData,
        defaultColDef: defaultColDef,
        onCellDoubleClicked: (event) => (event.colDef.field === "order" ? window.open(`https://www.itbpress.id/wp-admin/post.php?post=${event.value}&action=edit`, "_blank") : ""),
        // selecting
        rowSelection: "multiple",
        onSelectionChanged: selectBox,
        suppressRowClickSelection: true,
        // pagination
        pagination: true,
        paginationPageSize: 25,
        paginationPageSizeSelector: [10, 25, 50, 100, 300],
    };

    eGrid.innerHTML = "";
    gridApi = agGrid.createGrid(eGrid, gridOptions);

    document.querySelectorAll(".ag-header-cell").forEach((element) => {
        element.style.height = "35px";
    });

    document.querySelectorAll(".ag-header").forEach((element) => {
        element.style.minHeight = "38px";
        element.style.height = "38px";
    });

    document.querySelectorAll(".ag-row-even").forEach((element) => {
        element.style.minHeight = "38px";
        element.style.height = "38px";
        element.style.fontSize = "12px";
    });

    document.querySelectorAll(".ag-row-odd").forEach((element) => {
        element.style.minHeight = "38px";
        element.style.height = "38px";
        element.style.fontSize = "12px";
    });

    setLoading(agLoad);
    document.querySelectorAll(".ag-header-cell-label").forEach((element) => {
        element.textContent.trim() === "Unit Price" ? element.classList.add("justify-end", "pr-2") : "";
    });
};

const setLoading = (value) => gridApi.setGridOption("loading", value);

setupAggrid([{}], true);

const onSetup = async () => {
    const [status, data] = await postData("/get-product", { params: "product" });
    setupAggrid(data.orders, false);
};

document.addEventListener("DOMContentLoaded", () => onSetup());
