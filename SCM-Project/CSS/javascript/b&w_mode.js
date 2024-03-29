document.addEventListener('DOMContentLoaded', function () {
    var dbContainer = document.getElementById('DB');
    var darkModeToggle = document.getElementById('dark_change');
    var themes = document.getElementById('theme');

    // Check if dark mode preference is stored and apply it
    var darkModeEnabled = sessionStorage.getItem('darkModeEnabled');
    if (darkModeEnabled === 'true') {
        enableDarkMode();
    }

    // Dark mode toggle event listener
    darkModeToggle.addEventListener('click', function(){
        toggleDarkMode();
    });

    // Theme click event listener
    themes.addEventListener('click', function() {
        toggleDarkMode();
    });

    // Function to toggle dark mode
    function toggleDarkMode() {
        var darkModeEnabled = sessionStorage.getItem('darkModeEnabled');
        if (darkModeEnabled === 'true') {
            disableDarkMode();
        } else {
            enableDarkMode();
        }
    }

    // Function to enable dark mode
    function enableDarkMode() {
        darkModeToggle.classList.add('activee');
        dbContainer.classList.add('night');
        sessionStorage.setItem('darkModeEnabled', 'true');
    }

    // Function to disable dark mode
    function disableDarkMode() {
        darkModeToggle.classList.remove('activee');
        dbContainer.classList.remove('night');
        sessionStorage.setItem('darkModeEnabled', 'false');
    }
});

function logout() {
    sessionStorage.removeItem('darkModeEnabled');
    localStorage.removeItem('darkModeEnabled')
}
