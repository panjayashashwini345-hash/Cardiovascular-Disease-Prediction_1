function predict() {
    const resultElement = document.getElementById("result");
    const data = {};
    const fields = ['age', 'gender', 'height', 'weight', 'ap_hi', 'ap_lo', 'cholesterol', 'gluc', 'smoke', 'alco', 'active'];

    fields.forEach(id => {
        data[id] = document.getElementById(id).value;
    });

    if (Object.values(data).some(val => val === "")) {
        resultElement.style.color = "orange";
        resultElement.innerText = "⚠️ Please fill all fields";
        return;
    }

    // BP Validation
    if (Number(data.ap_lo) >= Number(data.ap_hi)) {
        resultElement.style.color = "orange";
        resultElement.innerText = "⚠️ Diastolic BP cannot be higher than Systolic";
        return;
    }

    resultElement.style.color = "black";
    resultElement.innerText = "⏳ Predicting...";

    fetch("http://127.0.0.1:10000/predict", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(data)
    })
    .then(res => res.json())
    .then(res => {
        if (res.risk === "High") {
            resultElement.style.color = "red";
            resultElement.innerText = `❤️ High Risk of Heart Disease (${res.percentage}%)`;
        } else {
            resultElement.style.color = "green";
            resultElement.innerText = `💚 Low Risk of Heart Disease (${res.percentage}%)`;
        }
    })
    .catch(() => {
        resultElement.style.color = "red";
        resultElement.innerText = "❌ Backend Error";
    });
}