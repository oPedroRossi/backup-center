document.addEventListener("DOMContentLoaded", () => {
    loadDashboard();
});

function loadDashboard() {
    fetch("/api/dashboard/data", {
        method: "GET",
        credentials: "include"
    })
        .then(response => {
            if (response.status === 401) {
                window.location.href = "/login";
                return;
            }
            return response.json();
        })
        .then(data => {
            if (!data) return;
            console.log(data);
            updateDashboard(data.data);
        })
        .catch(err => {
            console.error("Erro ao carregar dashboard:", err);
        });
}

function updateDashboard(data) {
    // CPU
    if (data.cpu.percent !== undefined) {
        document.getElementById("cpuUsage").innerText =
            data.cpu.percent + " % / " + data.cpu.status;
    } else {
        document.getElementById("cpuUsage").innerText =
            "0%";
    }

    // RAM
    document.getElementById("ramUsage").innerText =
        data.memory.used_gb + " GB";
    document.getElementById("ramTotal").innerText =
        "de " + data.memory.total_gb + " GB";

    // DISK
    document.getElementById("diskUsage").innerText =
        data.disk.free_gb + " GB";
    document.getElementById("diskTotal").innerText =
        "de " + data.disk.total_gb + " GB";

    console.log("Dados do dashboard atualizados:", data);

    // BACKUPS
    if (data.backup_ok_count == null || data.backup_ok_count == undefined) {
        document.getElementById("backupOkCount").innerText = "0";
    } else {
        document.getElementById("backupOkCount").innerText = data.backup_ok_count;
    }

    if (data.backup_failed_count == null || data.backup_failed_count == undefined) {
        document.getElementById("backupFailedCount").innerText = "0";
    } else {
        document.getElementById("backupFailedCount").innerText = data.backup_failed_count;
    }

    // LOGS
    const logsContainer = document.getElementById("logsContainer");
    logsContainer.innerHTML = "";

    // Pega apenas os últimos 5
    const lastLogs = data.logs_device.slice(-5).reverse();

    if (lastLogs.length > 0) {

        lastLogs.forEach(log => {

            const logElement = document.createElement("div");
            logElement.classList.add("log-entry");

            logElement.innerHTML = `
            <strong>${new Date(log.created_at).toLocaleString()} - ${log.entity}:</strong>
            <span>${log.device_name}</span>
            <em>(${log.action})</em>
        `;

            logsContainer.appendChild(logElement);
        });

    } else {
        logsContainer.innerHTML = "<p>Nenhum log encontrado.</p>";
    }

}