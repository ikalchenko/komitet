function manageUser(btn) {
    let btnParent = btn.parentElement;
    let hiddenInput = btnParent.children[3];
    hiddenInput.value = btn.value;
    btnParent.submit();
}
