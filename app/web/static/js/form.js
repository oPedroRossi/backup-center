const form = document.getElementById("deviceForm");
const ipInput = form.querySelector("[name='ip_address']");

document.addEventListener("DOMContentLoaded", function () {

    const deviceType = document.getElementById("deviceType");
    const modelSelect = document.getElementById("modelSelect");

    const models = {
        firewall: ["Sophos", "Fortinet"],
        switch: ["HPE", "Huawei"],
        telefonia: ["Elastix", "Issabel", "UCM"]
    };

    deviceType.addEventListener("change", function () {

        const selectedType = this.value;

        // limpa modelos anteriores
        modelSelect.innerHTML = '<option value="">Selecione...</option>';

        if (models[selectedType]) {
            models[selectedType].forEach(function (model) {
                const option = document.createElement("option");
                option.value = model.toLowerCase();
                option.textContent = model;
                modelSelect.appendChild(option);
            });
        }
    });

});

function validateIP(ip) {
    const regex = /^(25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)\.(25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)\.(25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)\.(25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)$/;
    return regex.test(ip);
}

function validateField(field) {

    if (field.name === "ip_address") {
        if (!validateIP(field.value)) {
            field.classList.add("is-invalid");
            field.classList.remove("is-valid");
            return false;
        }
    }

    if (!field.checkValidity()) {
        field.classList.add("is-invalid");
        field.classList.remove("is-valid");
        return false;
    }

    field.classList.remove("is-invalid");
    field.classList.add("is-valid");
    return true;
}

form.querySelectorAll("input").forEach(input => {
    input.addEventListener("input", () => {
        validateField(input);
    });
});

form.querySelectorAll("select").forEach(select => {
    select.addEventListener("change", () => {
        validateField(select);
    });
});

form.addEventListener("submit", async function (e) {
    e.preventDefault();

    let isValid = true;

    form.querySelectorAll("input, select").forEach(field => {
        if (!validateField(field)) {
            isValid = false;
        }
    });

    if (!isValid) return;

    const button = form.querySelector("button");
    button.disabled = true;
    button.innerHTML = `
        <span class="spinner-border spinner-border-sm me-2"></span>
        Cadastrando...
    `;

    const formData = new FormData(form);
    const data = Object.fromEntries(formData.entries());

    try {
        const response = await fetch("/api/create_device", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(data)
        });

        const result = await response.json();

        if (response.ok) {
            showToast("Dispositivo criado com sucesso!", true);
            form.reset();
            form.querySelectorAll(".is-valid").forEach(el => el.classList.remove("is-valid"));
        } else {
            showToast(result.error || "Erro ao cadastrar.", false);
        }

    } catch {
        showToast("Erro de conexão com servidor.", false);
    }

    button.disabled = false;
    button.innerHTML = "Cadastrar Device";
});


function showToast(message, success) {
    const toast = document.createElement("div");
    toast.className = `toast-apple ${success ? "toast-success" : "toast-error"}`;
    toast.innerText = message;

    document.body.appendChild(toast);

    setTimeout(() => {
        toast.style.opacity = "0";
        toast.style.transform = "translateX(20px)";
        setTimeout(() => toast.remove(), 300);
    }, 3500);
}


