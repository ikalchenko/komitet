function vote(btn) {
    let btnParent = btn.parentElement;
    let hiddenInput = btnParent.children[1];
    hiddenInput.value = btn.value;
    btnParent.submit();
}
