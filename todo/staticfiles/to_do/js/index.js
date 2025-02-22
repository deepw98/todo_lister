document.addEventListener('DOMContentLoaded', function() {
    const homeButton = document.getElementById('bh');
    const aboutButton = document.getElementById('ba');
    const contactButton = document.getElementById('bc');
    // const registerButton = document.getElementsByName('register');
    // const loginButton = document.getElementsByName('login');


    homeButton.addEventListener('click', function() {
        window.location.href = ''; 

    });

    aboutButton.addEventListener('click', function() {
        window.location.href = '/about'; 
    });

    contactButton.addEventListener('click', function() {
        window.location.href = '/contact'; 
    });
    // registerButton.addEventListener('click', function() {
    //     window.location.href = '/home'; 
    // });
    // loginButton.addEventListener('click', function() {
    //     window.location.href = '/home'; 
    // });
});

function validatePassword() {
    const password = document.getElementById('password').value;
    const error = document.getElementById('password-error');

    // Regex to enforce a strong password
    const strongPasswordRegex = /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$/;

    if (!strongPasswordRegex.test(password)) {
        error.style.display = 'block';
        return false; // Prevent form submission
    }

    error.style.display = 'none';
    return true; // Allow form submission
}