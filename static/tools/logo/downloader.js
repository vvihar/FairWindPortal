const download = () => {
    // svg domを取得
    const svg = document.getElementById("fwlogo");

    // canvasを準備
    let canvas = document.createElement("canvas");
    canvas.width = svg.width.baseVal.value;
    canvas.height = svg.height.baseVal.value;

    // 描画をするための、canvasの組み込みオブジェクトを準備
    const ctx = canvas.getContext("2d");
    // imgオブジェクトを準備
    let image = new Image();

    // imageの読み込みが完了したら、onloadが走る
    image.onload = () => {
        // SVGデータをPNG形式に変換する
        // canvasに描画する drawImage(image, x座標, y座標, 幅, 高さ)
        ctx.drawImage(image, 0, 0, image.width, image.height);

        // ローカルにダウンロード
        let link = document.createElement("a");
        link.href = canvas.toDataURL(); // 描画した画像のURIを返す data:image/png;base64
        link.download = "fairwind.png";
        link.click();
    };
    // 読み込みに失敗したらこっちが走る
    image.onerror = (error) => {
        console.log(error);
    };

    // SVGデータをXMLで取り出す
    const svgData = new XMLSerializer().serializeToString(svg);
    // この時点で、上記のonloadが走る
    image.src =
        "data:image/svg+xml;charset=utf-8;base64," +
        btoa(unescape(encodeURIComponent(svgData)));
};
const downloadButton = document.getElementById("download");
downloadButton.onclick = () => {
    download();
};
