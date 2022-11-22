const totalManageElement = document.getElementById('id_items-TOTAL_FORMS')
// set the number of forms upon page load
totalManageElement.value = document.getElementsByClassName('item-form').length;

let currentItemCount = parseInt(totalManageElement.value)
const addBtn = document.getElementById('add-btn')
addBtn.addEventListener('click', () => {
    // do not allow more than 15 items
    if (currentItemCount >= 15) {
        alert("請求項目は15個までです。")
        return
    }
    const itemForm = document.getElementsByClassName('item-form')[0];
    const clone_itemForm = itemForm.cloneNode(true);
    // change id for cloned form's child elements
    const inputs = clone_itemForm.getElementsByTagName('input');
    for (let i = 0; i < inputs.length; i++) {
        const input = inputs[i];
        const id = input.id;
        const name = input.name;
        input.id = id.replace('0', currentItemCount);
        input.name = name.replace('0', currentItemCount);
    };
    const inputs_text = clone_itemForm.querySelectorAll('input[type="text"]');
    for (let i = 0; i < inputs_text.length; i++) {
        const input = inputs_text[i];
        input.value = '';
    };
    // set value to today's date (YYYY-MM-DD)
    const today = new Date();
    const year = today.getFullYear();
    const month = ('0' + (today.getMonth() + 1)).slice(-2);
    const day = ('0' + today.getDate()).slice(-2);
    const date = year + '-' + month + '-' + day;
    clone_itemForm.querySelector('input[name$="date"]').value = date;
    clone_itemForm.querySelector('input[name$="volume"]').value = 1;
    clone_itemForm.querySelector('input[name$="unit"]').value = "個";
    clone_itemForm.querySelector('input[name$="amount"]').value = 0;
    clone_itemForm.querySelector('input[name$="DELETE"]').checked = false;
    clone_itemForm.querySelector('input[name$="id"]').remove();

    const labels = clone_itemForm.getElementsByTagName('label')
    for (let i = 0; i < labels.length; i++) {
        const label = labels[i];
        const forAttr = label.getAttribute('for');
        label.setAttribute('for', forAttr.replace('0', currentItemCount));
    };
    // insert cloned form after last form
    const lastForm = document.getElementsByClassName('item-form')[currentItemCount - 1];
    lastForm.insertAdjacentElement('afterend', clone_itemForm);
    currentItemCount += 1;
    totalManageElement.value = currentItemCount;
});