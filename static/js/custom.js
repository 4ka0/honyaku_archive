// Function to show a spinner in an upload button when the upload button is
// clicked. Used on the glossary and translation upload forms.

function showSpinner() {
    var btn = document.getElementById('upload-button');
    btn.innerHTML =
        '<span class="spinner-border spinner-border-sm"></span>&nbspアップロード中';
    btn.classList.add('disabled');
}

function showSearchSpinner() {
    var btn = document.getElementById('search-button');
    btn.innerHTML =
        '<span class="spinner-border spinner-border-sm"></span>&nbsp検索中';
    btn.classList.add('disabled');
}
