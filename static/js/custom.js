// Functions to show spinners in the search and upload buttons upon being
// clicked. Used in the navbar search form and the glossary and translation
// upload forms.

function showSpinner() {
    var btn = document.getElementById('upload-button');
    btn.innerHTML =
        '<span class="spinner-border spinner-border-sm"></span>&nbspアップロード中';
    btn.classList.add('disabled');
}

function showSearchSpinner() {
    var btn = document.getElementById('search-button');
    btn.innerHTML =
        '&nbsp<span class="spinner-border spinner-border-sm"></span>&nbsp';
    btn.classList.add('disabled');
}
