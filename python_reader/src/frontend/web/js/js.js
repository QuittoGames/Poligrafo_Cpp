window.addEventListener("DOMContentLoaded", () => {

    const API_URL = "http://localhost:8001/api/state";
    const MAX_POINTS = 80;

    function safe(v) {
        const n = Number(v);
        return Number.isFinite(n) ? n : 0;
    }

    const canvas = document.getElementById("liveChart");

    if (!canvas) {
        console.error("Canvas não encontrada.");
        return;
    }

    const ctx = canvas.getContext("2d");

    const gsrHistory = [];
    const baselineHistory = [];
    const labels = [];

    const chart = new Chart(ctx, {
        type: "line",
        data: {
            labels,
            datasets: [
                {
                    label: "GSR",
                    data: gsrHistory,
                    borderColor: "#10b981",
                    backgroundColor: "rgba(16,185,129,.15)",
                    pointRadius: 0,
                    tension: 0.35,
                    fill: true
                },
                {
                    label: "Baseline",
                    data: baselineHistory,
                    borderColor: "#64748b",
                    pointRadius: 0,
                    tension: 0.35
                }
            ]
        },

        options: {
            responsive: true,
            maintainAspectRatio: false,
            animation: false,

            plugins: {
                legend: {
                    labels: {
                        color: "#ffffff"
                    }
                }
            },

            scales: {
                x: {
                    display: false
                },

                y: {
                    ticks: {
                        color: "#94a3b8"
                    },

                    grid: {
                        color: "rgba(255,255,255,.08)"
                    }
                }
            }
        }
    });

    function updateText(id, value) {
        const el = document.getElementById(id);

        if (el)
            el.innerText = value.toFixed(2);
    }

    let updating = false;

    async function update() {

        if (updating)
            return;

        updating = true;

        try {

            const res = await fetch(API_URL, {
                cache: "no-store"
            });

            if (!res.ok)
                throw new Error(`HTTP ${res.status}`);

            const data = await res.json();

            if (!Array.isArray(data) || data.length === 0)
                return;

            const last = data.at(-1);

            if (!last)
                return;

            //---------------------------------------
            // DADOS
            //---------------------------------------

            const gsrVal = safe(last.gsr);
            const baseVal = safe(last.baseline);
            const diffVal = safe(last.diff);

            gsrHistory.push(gsrVal);
            baselineHistory.push(baseVal);
            labels.push("");

            while (gsrHistory.length > MAX_POINTS) {
                gsrHistory.shift();
                baselineHistory.shift();
                labels.shift();
            }

            updateText("val-gsr", gsrVal);
            updateText("val-baseline", baseVal);
            updateText("val-diff", diffVal);

            //---------------------------------------
            // ESTADOS
            //---------------------------------------

            const state = (last.state || "ESTAVEL").toUpperCase();

            let color = "#10b981";
            let background = "rgba(16,185,129,.15)";
            let stateText = "ESTÁVEL";

            switch (state) {

                case "LEVE":
                case "ALTERACAO":
                case "LEVE_ALTERACAO":

                    color = "#facc15";
                    background = "rgba(250,204,21,.15)";
                    stateText = "LEVE ALTERAÇÃO";

                    break;

                case "PICO":
                case "ALERT":

                    color = "#ef4444";
                    background = "rgba(239,68,68,.15)";
                    stateText = "PICO";

                    break;

                default:

                    color = "#10b981";
                    background = "rgba(16,185,129,.15)";
                    stateText = "ESTÁVEL";
            }

            //---------------------------------------
            // GRAFICO
            //---------------------------------------

            chart.data.datasets[0].borderColor = color;
            chart.data.datasets[0].backgroundColor = background;

            chart.update("none");

            //---------------------------------------
            // HEADER
            //---------------------------------------

            const statusBox = document.getElementById("status-box");
            const statusLabel = document.getElementById("status-label");
            const led = document.querySelector(".led");

            if (statusBox && statusLabel && led) {

                statusBox.style.borderColor = color;
                statusBox.style.background = background;
                statusBox.style.boxShadow = `0 0 15px ${background}`;

                statusLabel.innerText = stateText;
                statusLabel.style.color = color;

                led.style.backgroundColor = color;
                led.style.boxShadow = `0 0 15px ${color}`;

                if (state === "PICO" || state === "ALERT") {
                    led.style.animation = "pulse .8s infinite";
                } else {
                    led.style.animation = "";
                }
            }

            //---------------------------------------
            // TEXTO GRANDE
            //---------------------------------------

            const stateInfo = document.getElementById("state-text");

            if (stateInfo) {
                stateInfo.innerText = stateText;
                stateInfo.style.color = color;
                stateInfo.style.textShadow = `0 0 10px ${color}`;
            }

            //---------------------------------------
            // CARDS
            //---------------------------------------

            document.querySelectorAll(".card").forEach(card => {

                card.style.borderColor = color;
                card.style.boxShadow = `0 0 10px ${background}`;
            });

        }
        catch (e) {

            console.warn("Falha na API", e);

        }
        finally {

            updating = false;

        }

    }

    //---------------------------------------
    // LOOP
    //---------------------------------------

    async function loop() {

        await update();

        setTimeout(loop, 800);
    }

    loop();

});