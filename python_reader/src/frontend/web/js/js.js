/* =============================================================================
   Polígrafo — live dashboard
   Rules:
     1. Data updates every poll tick (cheap, always).
     2. Color/DOM updates ONLY on state transition (tracked, deduped).
     3. All non-chart visuals driven by [data-state] on .app-container —
        no inline style mutations.
   ============================================================================= */

window.addEventListener("DOMContentLoaded", () => {

    //---------------------------------------
    // CONSTANTS
    //---------------------------------------

    const API_URL = "http://localhost:8001/api/state";
    const POLL_INTERVAL_MS = 800;
    const MAX_POINTS = 80;

    // Neutral palette (state-independent).
    const BASELINE_COLOR = "#64748b";

    // State palette. Mirrors style.css [data-state] tokens — keep in sync.
    const STATE_STYLE = {
        ESTAVEL:         { color: "#10b981", background: "rgba(16,185,129,.15)",  text: "ESTÁVEL" },
        NONE:            { color: "#10b981", background: "rgba(16,185,129,.15)",  text: "ESTÁVEL" },
        VARIACAO_LEVE:   { color: "#facc15", background: "rgba(250,204,21,.15)",  text: "LEVE ALTERAÇÃO" },
        LEVE:            { color: "#facc15", background: "rgba(250,204,21,.15)",  text: "LEVE ALTERAÇÃO" },
        ALTERACAO:       { color: "#facc15", background: "rgba(250,204,21,.15)",  text: "LEVE ALTERAÇÃO" },
        LEVE_ALTERACAO:  { color: "#facc15", background: "rgba(250,204,21,.15)",  text: "LEVE ALTERAÇÃO" },
        PICO_DETECTADO:  { color: "#ef4444", background: "rgba(239,68,68,.15)",   text: "PICO" },
        PICO:            { color: "#ef4444", background: "rgba(239,68,68,.15)",   text: "PICO" },
        ALERT:           { color: "#ef4444", background: "rgba(239,68,68,.15)",   text: "PICO" },
        NOT_CONNECTED:   { color: "#ef4444", background: "rgba(239,68,68,.15)",   text: "SEM CONTATO" },
        NO_CONTACT:      { color: "#ef4444", background: "rgba(239,68,68,.15)",   text: "SEM CONTATO" },
        SEM_CONTATO:     { color: "#ef4444", background: "rgba(239,68,68,.15)",   text: "SEM CONTATO" }
    };

    const DEFAULT_STYLE = STATE_STYLE.ESTAVEL;

    //---------------------------------------
    // DOM
    //---------------------------------------

    const canvas = document.getElementById("liveChart");

    if (!canvas) {
        console.error("Canvas não encontrada.");
        return;
    }

    const ctx = canvas.getContext("2d");
    const appContainer = document.querySelector(".app-container");
    const statusLabel = document.getElementById("status-label");
    const stateText = document.getElementById("state-text");

    const gsrHistory = [];
    const baselineHistory = [];
    const labels = [];

    //---------------------------------------
    // CHART
    //---------------------------------------

    const chart = new Chart(ctx, {
        type: "line",
        data: {
            labels,
            datasets: [
                {
                    label: "GSR",
                    data: gsrHistory,
                    borderColor: DEFAULT_STYLE.color,
                    backgroundColor: DEFAULT_STYLE.background,
                    pointRadius: 0,
                    tension: 0.35,
                    fill: true
                },
                {
                    label: "Baseline",
                    data: baselineHistory,
                    borderColor: BASELINE_COLOR,
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

    //---------------------------------------
    // STATE TRANSITION (the ONLY path that mutates visuals)
    //---------------------------------------

    let currentState = null;
    let currentChartColor = null;

    function applyStateVisuals(stateRaw) {

        const state = (stateRaw || "ESTAVEL").toUpperCase();

        // Deduplicate: nothing changes unless the state actually transitioned.
        if (state === currentState) return;

        currentState = state;
        const cfg = STATE_STYLE[state] || DEFAULT_STYLE;

        // 1. DOM state — drives ALL CSS ([data-state] tokens in style.css).
        if (appContainer) appContainer.dataset.state = state;

        // 2. Text labels (only fire on transition).
        if (statusLabel) statusLabel.textContent = cfg.text;
        if (stateText) stateText.textContent = cfg.text;

        // 3. Chart color — Chart.js needs JS mutation; gate on color diff
        //    so equal-palette transitions (PICO -> ALERT) don't redraw.
        if (cfg.color !== currentChartColor) {
            chart.data.datasets[0].borderColor = cfg.color;
            chart.data.datasets[0].backgroundColor = cfg.background;
            currentChartColor = cfg.color;
            chart.update("none");
        }
    }

    //---------------------------------------
    // DATA (every tick — no visual mutation)
    //---------------------------------------

    function safe(v) {
        const n = Number(v);
        return Number.isFinite(n) ? n : 0;
    }

    function updateText(id, value) {
        const el = document.getElementById(id);

        if (el)
            el.innerText = value.toFixed(2);
    }

    function pushData(last) {

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

        chart.update("none");
    }

    //---------------------------------------
    // POLL LOOP
    //---------------------------------------

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
            // DATA: every tick, cheap, no color touch
            //---------------------------------------

            pushData(last);

            //---------------------------------------
            // STATE: only mutates visuals on change
            //---------------------------------------

            applyStateVisuals(last.state);

        }
        catch (e) {

            console.warn("Falha na API", e);

        }
        finally {

            updating = false;

        }

    }

    async function loop() {

        await update();

        setTimeout(loop, POLL_INTERVAL_MS);
    }

    loop();

});
