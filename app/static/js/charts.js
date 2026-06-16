document.addEventListener("DOMContentLoaded", async () => {
    const canvas = document.getElementById("employeesByDepartmentChart");
    if (!canvas || typeof Chart === "undefined") {
        return;
    }

    const response = await fetch("/api/charts/employees-by-department");
    const payload = await response.json();

    new Chart(canvas, {
        type: "bar",
        data: {
            labels: payload.labels,
            datasets: [
                {
                    label: "Colaboradores",
                    data: payload.data,
                    backgroundColor: ["#167c6b", "#315a7c", "#986d12", "#6b7280"],
                    borderRadius: 6,
                },
            ],
        },
        options: {
            responsive: true,
            plugins: {
                legend: {
                    display: false,
                },
            },
            scales: {
                y: {
                    beginAtZero: true,
                    ticks: {
                        precision: 0,
                    },
                },
            },
        },
    });
});
