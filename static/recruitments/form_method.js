const form = document.getElementById("form");

form.addEventListener("submit", () => {
    const temp = document.getElementsByName("temp")[0];
    const csrfmiddlewaretoken = document.getElementsByName("csrfmiddlewaretoken")[0];
    const inviteCheckbox = document.getElementsByClassName("invite");
    if (temp.checked) { // 仮登録
        csrfmiddlewaretoken.disabled = true;
        for (let i = 0; i < inviteCheckbox.length; i++) {
            inviteCheckbox[i].setAttribute("name", "mid");
        }
        temp.disabled = true;
    } else { // 本登録
        csrfmiddlewaretoken.disabled = false;
        form.action = SUBMIT_PATH;
        form.method = "post";
    }
});

// generate url from checkbox
const generateUrl = () => {
    const inviteCheckbox = document.getElementsByClassName("invite");
    let url = BASE_URL + "?";
    for (let i = 0; i < inviteCheckbox.length; i++) {
        if (inviteCheckbox[i].checked) {
            url += "mid=" + inviteCheckbox[i].value + "&";
        }
    }
    url = url.slice(0, -1);
    return url;
}
// shorten url when the button is clicked
const shortenButton = document.getElementById("shorten-button");
// post request to shorten url
function ShortenURL() {
    const url = generateUrl();
    const shortenForm = document.getElementById("shorten-form");
    // set value to the form before submit the form
    const input = document.createElement("input");
    input.setAttribute("type", "hidden");
    input.setAttribute("name", "redirect_to");
    input.setAttribute("value", url);
    shortenForm.appendChild(input);
    shortenForm.submit();
}