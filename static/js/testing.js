const slcModel = document.getElementById("slcModel");

const process = async (event) => {
  const url = "http://127.0.0.1:8080/calc";

  const fileInput = event.target;
  const formData = new FormData();
  formData.append("file", fileInput.files[0]);
  formData.append("model", slcModel.value);

  try {
    const response = await fetch(url, {
      method: "POST",
      body: formData,
    });

    if (!response.ok) {
      const errorData = await response.json();
      console.error("Error:", errorData.error);
      return;
    }

    const result = await response.json();
    console.log("Response:", result);
  } catch (error) {
    console.error("Error:", error);
  }
};
