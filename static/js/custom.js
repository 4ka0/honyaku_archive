// Functions to show spinners in the search and upload buttons upon being
// clicked. Used in the navbar search form and the glossary and translation
// upload forms.
function showUploadSpinner() {
    var btn = document.getElementById('upload-button');
    btn.innerHTML =
        '<span class="spinner-border spinner-border-sm"></span>&nbspアップロード中';
    btn.classList.add('disabled');
}

function showSearchSpinner() {

    // Show the spinner within the button when clicked.
    var btn = document.getElementById('search-button');
    btn.innerHTML =
        '&nbsp<span class="spinner-border spinner-border-sm"></span>&nbsp';

    // Reset the content of the button when leaving the page.
    // Prevents the spinner still being shown when returning to a previous page
    // by using the browser back button.
    document.onvisibilitychange = () => {
        if (document.visibilityState === "hidden") {
            btn.innerHTML = "検索";
        }
    };
}

// Function to copy text to the clipboard.
function copyText(text) {
    navigator.clipboard.writeText(text);
}

// Function to insert table cell text into the search field in the navbar.
function searchText(text) {
    var searchField = document.getElementById("search-input-field");
    searchField.value = text
    searchField.select()
}

// Function to select text in the search field in the navbar.
function selectSearchInputText() {
    document.getElementById("search-input-field").select();
}
