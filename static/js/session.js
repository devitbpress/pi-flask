const formatDateToCustomString = (date) => {
    const year = date.getFullYear();
    const month = String(date.getMonth() + 1).padStart(2, "0");
    const day = String(date.getDate()).padStart(2, "0");
    const hours = String(date.getHours()).padStart(2, "0");
    const minutes = String(date.getMinutes()).padStart(2, "0");

    return `${year}${month}${day}${hours}${minutes}`;
};

const datetime = new Date();
const formattedDate = formatDateToCustomString(datetime);
sessionStorage.setItem("id", formattedDate);
