var bg_default = document.getElementById("id_bgcolor").value;
var qr_default = document.getElementById("id_qrcolor").value;
const pickrBG = new Pickr({
    el: "#colorBG",
    theme: "monolith",
    lockOpacity: true,
    default: bg_default,
    position: "right",

    swatches: [
        "rgb(244, 67, 54)",
        "rgb(233, 30, 99)",
        "rgb(156, 39, 176)",
        "rgb(103, 58, 183)",
        "rgb(63, 81, 181)",
        "rgb(33, 150, 243)",
        "rgb(0, 188, 212)",
        "rgb(0, 150, 136)",
        "rgb(76, 175, 80)",
        "rgb(139, 195, 74)",
        "rgb(205, 220, 57)",
        "rgb(255, 235, 59)",
        "rgb(255, 193, 7)",
        "rgb(255, 255, 255)",
    ],

    components: {
        palette: true,
        // Main components
        preview: true,
        opacity: false,
        hue: true,

        // Input / output Options
        interaction: {
            hex: true,
            rgba: true,
            hsla: false,
            hsva: false,
            cmyk: false,
            input: true,
            clear: true,
            save: true,
        },
    },
    i18n: {
        // Strings visible in the UI
        "btn:save": "保存",
        "btn:cancel": "キャンセル",
        "btn:clear": "クリア",

        // Strings used for aria-labels
        "aria:btn:save": "保存して閉じる",
        "aria:btn:cancel": "キャンセルして閉じる",
        "aria:btn:clear": "クリアして閉じる",
    },
});
pickrBG.on("change", (color, source, instance) => {
    var color = color.toHEXA().toString();
    document.getElementById("id_bgcolor").value = color;
});

const pickrLogo = new Pickr({
    el: "#colorQR",
    theme: "monolith",
    lockOpacity: true,
    default: qr_default,
    position: "right",

    swatches: [
        "rgb(244, 67, 54)",
        "rgb(233, 30, 99)",
        "rgb(156, 39, 176)",
        "rgb(103, 58, 183)",
        "rgb(63, 81, 181)",
        "rgb(33, 150, 243)",
        "rgb(0, 188, 212)",
        "rgb(0, 150, 136)",
        "rgb(76, 175, 80)",
        "rgb(139, 195, 74)",
        "rgb(205, 220, 57)",
        "rgb(255, 235, 59)",
        "rgb(255, 193, 7)",
        "rgb(255, 255, 255)",
    ],

    components: {
        palette: true,
        // Main components
        preview: true,
        opacity: false,
        hue: true,

        // Input / output Options
        interaction: {
            hex: true,
            rgba: true,
            hsla: false,
            hsva: false,
            cmyk: false,
            input: true,
            clear: true,
            save: true,
        },
    },
    i18n: {
        // Strings visible in the UI
        "btn:save": "保存",
        "btn:cancel": "キャンセル",
        "btn:clear": "クリア",

        // Strings used for aria-labels
        "aria:btn:save": "保存して閉じる",
        "aria:btn:cancel": "キャンセルして閉じる",
        "aria:btn:clear": "クリアして閉じる",
    },
});

pickrLogo.on("change", (color, source, instance) => {
    var color = color.toHEXA().toString();
    document.getElementById("id_qrcolor").value = color;
});
