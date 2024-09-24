const setHeight = () => document.getElementById("container").style.setProperty("--vh", `${window.innerHeight * 0.01}px`);

window.addEventListener("resize", setHeight);
