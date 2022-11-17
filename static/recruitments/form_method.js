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
        form.action = "{% url 'events:event_invite' event.id %}";
        form.method = "post";
    }
});