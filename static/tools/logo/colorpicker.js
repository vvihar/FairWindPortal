const container = document.getElementsByClassName("color-picker");
/*let elementArray = [];
for (let i = 0; i < container.length; i++) {
    const newElement = document.createElement("div");
    container[i].appendChild(newElement);
    elementArray.push(newElement);
}*/
elementArray = Array.from(container);
const pickrBG = new Pickr({
    el: elementArray[1],
    theme: "monolith",
    lockOpacity: true,
    default: "#ffffff",
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
    document.getElementById("logo-bg").style.backgroundColor = color;
});

const pickrLogo = new Pickr({
    el: elementArray[0],
    theme: "monolith",
    lockOpacity: true,
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
    document.getElementById("logoPath").style.fill = color;
});

let backgroundInput = document.getElementById("backgroundColor");
let logoInput = document.getElementById("logoColor");
let reset = document.getElementById("reset");
let logoGrad = document.getElementById("gradient");

/*backgroundInput.onchange = () => {
    var color = backgroundInput.value;
    document.body.style.backgroundColor = color;
};
logoInput.onchange = () => {
    var color = logoInput.value;
    document.getElementById("logoPath").style.fill = color;
};*/

reset.onclick = () => {
    document.getElementById("logoPath").style.fill =
        "url(#linearGradient13147)";
    document.getElementById("logo-bg").style.backgroundColor = "white";
};
logoGrad.onclick = () => {
    document.getElementById("logoPath").style.fill =
        "url(#linearGradient13147)";
};
