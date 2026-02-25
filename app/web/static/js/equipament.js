let allEquipaments = [];
let filteredEquipaments = [];
let currentPage = 1;
const rowsPerPage = 10;

function loadEquipaments(equipamentType) {
    fetch(`/api/equipaments/${equipamentType}`)
        .then(response => {
            if (response.status === 401) {
                window.location.href = "/login";
                return;
            }
            return response.json();
        })
        .then(data => {
            allEquipaments = data.data;
            applyFilters();
        })
        .catch(err => {
            console.error("Erro ao carregar equipamentos:", err);
        });
}

function updateEquipaments(equipaments) {
    const tbody = document.getElementById("equipamentTableBody");
    tbody.innerHTML = "";

    equipaments.forEach(equipament => {

        const tr = document.createElement("tr");

        tr.innerHTML = `
    <td>${equipament.name}</td>
    <td>${equipament.model}</td>
    <td>${equipament.last_backup ?? "Nunca"}</td>
    <td class="${equipament.last_status === "OK" ? "status-ok" : "status-error"}">
        ${equipament.last_status ?? "Sem status"}
    </td>
    <td class="d-flex gap-2">

        <a href="/equipamento/${equipament.id}" 
           class="btn btn-sm btn-primary">
           Ver backups
        </a>

        <button class="btn btn-sm btn-danger"
                onclick="deleteDevice(${equipament.id})">
            Deletar
        </button>

    </td>
`;

        tbody.appendChild(tr);
    });
}

function updateKPIs(equipaments) {

    const total = equipaments.length;

    const okCount = equipaments.filter(e => e.last_status === "OK").length;

    const failCount = equipaments.filter(e => e.last_status === "FAILED").length;

    const lastBackups = equipaments
        .map(e => e.last_backup)
        .filter(date => date !== null);

    let lastBackupFormatted = "Nunca";

    if (lastBackups.length > 0) {
        const latest = new Date(Math.max(...lastBackups.map(d => new Date(d))));
        lastBackupFormatted = latest.toLocaleString("pt-BR");
    }

    document.getElementById("kpiTotal").innerText = total;
    document.getElementById("kpiOk").innerText = okCount;
    document.getElementById("kpiFail").innerText = failCount;
    document.getElementById("kpiLastBackup").innerText = lastBackupFormatted;
}

function applyFilters() {

    const searchValue = document
        .getElementById("searchInput")
        .value
        .toLowerCase();

    filteredEquipaments = allEquipaments.filter(e =>
        e.name.toLowerCase().includes(searchValue)
    );

    currentPage = 1;
    renderPage();
}

function renderPage() {

    const totalPages = Math.ceil(filteredEquipaments.length / rowsPerPage);

    const start = (currentPage - 1) * rowsPerPage;
    const end = start + rowsPerPage;

    const paginated = filteredEquipaments.slice(start, end);

    updateEquipaments(paginated);
    updateKPIs(filteredEquipaments);

    document.getElementById("pageInfo").innerText =
        `Página ${currentPage} de ${totalPages || 1}`;
}

document.getElementById("searchInput")
    .addEventListener("input", applyFilters);

document.getElementById("prevPage")
    .addEventListener("click", () => {
        if (currentPage > 1) {
            currentPage--;
            renderPage();
        }
    });

document.getElementById("nextPage")
    .addEventListener("click", () => {
        const totalPages = Math.ceil(filteredEquipaments.length / rowsPerPage);
        if (currentPage < totalPages) {
            currentPage++;
            renderPage();
        }
    });

function deleteDevice(id) {

    if (!confirm("Tem certeza que deseja deletar este equipamento?")) return;

    fetch(`/api/equipaments/${id}`, {
        method: "DELETE"
    })
    .then(res => res.json())
    .then(data => {
        alert("Equipamento deletado!");
        location.reload();
    })
    .catch(err => {
        console.error(err);
        alert("Erro ao deletar equipamento");
    });
}