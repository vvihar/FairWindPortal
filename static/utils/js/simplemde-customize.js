// 参考：
// https://github.com/sparksuite/simplemde-markdown-editor

const simplemde = new SimpleMDE({
    element: document.getElementById("id_memo"),
    renderingConfig: {
        codeSyntaxHighlighting: true,
    },
    toolbar: ["bold", "italic", "heading", "|", "quote", "unordered-list", "ordered-list", "|", "link", "table", "horizontal-rule", "|", "preview", "side-by-side", "fullscreen", "|", "guide"],
});
const form = document.getElementById("form");
window.onload = () => {
    form.style.visibility = "visible";
}