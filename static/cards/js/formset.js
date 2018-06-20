let formfields = document.getElementById('inputs'),
    lastform = formfields.lastElementChild,
    addBtn = document.getElementById('addBtn'),
    formnum = document.getElementById('id_form-TOTAL_FORMS');


addBtn.addEventListener('click', function () {
    let num = formfields.childElementCount;
    let newNode = lastform.cloneNode(true);
    let newInput = newNode.firstElementChild;
    newInput.value = '';
    newInput.name = 'form-' + num + '-option';
    newInput.id = 'id_' + newInput.name;
    formfields.appendChild(newNode);
    formnum.value++;
});

function delRequest(button) {
    let forDelete = button.parentElement;
    forDelete.remove();
    formnum.value--;
    let childrens = formfields.children;
    for (let i=0; i < childrens.length; i++) {
        childrens[i].firstElementChild.name = 'form-' + i + '-option';
        childrens[i].firstElementChild.id = 'id_' + childrens[i].firstElementChild.name;
    }
}
