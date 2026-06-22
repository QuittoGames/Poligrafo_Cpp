window.addEventListener("DOMContentLoaded", () => {
    const API_URL = "http://localhost:8001/api/state";
    const MAX_POINTS = 80;

    function safe(v ) {
        const n = Number(v);
        return Number.isFinite(n) ? n : 0;
    }

    const canvas = document.getElementById("liveChart");
    if (!canvas) {
        console.error("❌ Erro: Canvas 'liveChart' não encontrado.");
        return;
    }

    const ctx = canvas.getContext("2d");

    const gsrHistory = [];
    const baselineHistory = [];
    const labels = [];

    const chart = new Chart(ctx, {
        type: "line",
        data: {
            labels: labels,
            datasets: [
                {
                    label: "GSR",
                    borderColor: "#3b82f6",
                    backgroundColor: "rgba(59, 130, 246, 0.1)",
                    data: gsrHistory,
                    pointRadius: 0,
                    tension: 0.4,
                    fill: true
                },
                {
                    label: "Baseline",
                    borderColor: "#64748b",
                    data: baselineHistory,
                    pointRadius: 0,
                    tension: 0.4
                }
            ]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            animation: false,
            plugins: { legend: { labels: { color: "#fff" } } },
            scales: {
                x: { display: false },
                y: {
                    ticks: { color: "#aaa" },
                    grid: { color: "rgba(255,255,255,0.1)" }
                }
            }
        }
    });

    async function update() {
        try {
            const res = await fetch(API_URL);
            if (!res.ok) throw new Error(`Status: ${res.status}`);

            const data = await res.json();
            // Log para debug (aperte F12 no navegador para ver)
            console.log("Dados recebidos:", data);

            if (!data) return;

            const last = Array.isArray(data) ? data[data.length - 1] : data;
            if (!last) return;

            const gsrVal = safe(last.gsr);
            const baseVal = safe(last.baseline);
            const diffVal = safe(last.diff);

            gsrHistory.push(gsrVal);
            baselineHistory.push(baseVal);
            labels.push(""); 

            if (gsrHistory.length > MAX_POINTS) {
                gsrHistory.shift();
                baselineHistory.shift();
                labels.shift();
            }

            chart.update("none");

            const updateText = (id, val) => {
                const el = document.getElementById(id);
                if (el) el.innerText = val.toFixed(2);
            };

            updateText("val-gsr", gsrVal);
            updateText("val-baseline", baseVal);
            updateText("val-diff", diffVal);

            const statusBox = document.getElementById("status-box");
            const statusLabel = document.getElementById("status-label");

            if (statusBox && statusLabel) {
                const state = last.state || "ESTAVEL";
                statusBox.className = `status-box state-${state}`;
                statusLabel.innerText = state;
            }

        } catch (e) {
            console.warn("⚠️ Falha na conexão com a API. Verifique se o backend está rodando.", e);
        }
    }

    update();
    setInterval(update, 800);
});
