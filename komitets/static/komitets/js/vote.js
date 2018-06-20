function vote(btn) {
    let btnParent = btn.parentElement;
    let hiddenInput = btnParent.children[1];
    if (btn.value === 'yes') {
        hiddenInput.value = 'yes';
    } else {
        hiddenInput.value = 'no';
    }
            btnParent.submit();


}
