const toggleBtn = document.getElementById('darkModeToggle');
const icon = document.getElementById('darkModeIcon');
const body = document.body;

if(localStorage.getItem('darkMode') === 'enabled'){
    body.classList.add('dark-mode');
    icon.textContent = '☀️';
} else {
    icon.textContent = '🌙';
}

toggleBtn.addEventListener('click', () => {
    body.classList.toggle('dark-mode');

    if(body.classList.contains('dark-mode')){
        localStorage.setItem('darkMode', 'enabled');
        icon.textContent = '☀️';
    } else {
        localStorage.setItem('darkMode', 'disabled');
        icon.textContent = '🌙';
    }
});
