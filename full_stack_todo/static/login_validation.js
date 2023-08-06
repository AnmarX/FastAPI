
const email = document.getElementById("email");
const password = document.getElementById("passwordd");
const passwordMatchError = document.getElementById("passwordMatchError");
const emailMatchError = document.getElementById("emailMatchError");
const btn = document.getElementById("btn");

function isValidEmail(email) {
  // A simple email validation regex
  const emailPattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  return emailPattern.test(email);
}

function updateButtonAndErrors() {
  const emailValid = isValidEmail(email.value);
  const emailValid2 = email.value.length > 0;
  const passwordValid = password.value.length > 0;

  btn.disabled = !(emailValid && passwordValid && emailValid2);

  // Show/hide errors for password match and email
  passwordMatchError.style.display = passwordValid ? "none" : "block";
  emailMatchError.style.display = emailValid ? "none" : "block";
}

function restrictSpecialChars(event) {
    const char = event.key;
    const emailRegex = /^[a-zA-Z0-9@.]*$/;
    if (!emailRegex.test(char) && char !== '@' && char !== '.') {
      event.preventDefault();
    }
  }


email.addEventListener("input", updateButtonAndErrors);
email.addEventListener("blur", updateButtonAndErrors);
email.addEventListener("keypress", restrictSpecialChars);

password.addEventListener("input", updateButtonAndErrors);
password.addEventListener("blur", updateButtonAndErrors);
