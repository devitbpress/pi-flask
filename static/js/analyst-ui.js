const btnChevron = document.getElementById("btn-chevron");

let miniNavIndikacator = { status: false, nav: "13rem", tools: "13rem" };

const miniNav = () => {
    const boxNav = document.getElementById("box-nav");
    const boxContent = document.getElementById("box-content");

    if (miniNavIndikacator.status) {
        boxNav.style.width = "13rem";
        miniNavIndikacator.nav = "13rem";
        miniNavIndikacator.status = false;
        btnChevron.querySelector("img").classList.remove("rotate-180");
    } else {
        boxNav.style.width = "4rem";
        miniNavIndikacator.nav = "4rem";
        miniNavIndikacator.status = true;
        btnChevron.querySelector("img").classList.add("rotate-180");
    }

    boxContent.style.width = `calc(100vw - ${miniNavIndikacator.nav} - ${miniNavIndikacator.tools})`;
};

const setHeight = () => document.getElementById("container").style.setProperty("--vh", `${window.innerHeight * 0.01}px`);

btnChevron.addEventListener("click", () => miniNav());

window.addEventListener("resize", setHeight);
setHeight();
