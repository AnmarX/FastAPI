
        const email = document.getElementById("email");
        const password = document.getElementById("passwordd");
        const confirmPassword = document.getElementById("confirmPassword");
        const passwordMatchError = document.getElementById("passwordMatchError");
        const emailMatchError = document.getElementById("emailMatchError");
        const btn = document.getElementById("btn");

        function isValidEmail(email) {
          // A simple email validation regex
          const emailPattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
          return emailPattern.test(email);
        }

        function updateButtonAndErrors() {
          const passwordMatch = confirmPassword.value === password.value;
          const emailValid = isValidEmail(email.value);
          const emailValid2 = email.value.length > 0;
          const passwordValid = password.value.length > 0;

          btn.disabled = !(passwordMatch && emailValid && passwordValid && emailValid2);

          // Show/hide errors for password match and email
          passwordMatchError.style.display = passwordMatch ? "none" : "block";
          emailMatchError.style.display = emailValid ? "none" : "block";
        }

        function restrictSpecialChars(event) {
            const char = event.key;
            const emailRegex = /^[a-zA-Z0-9@.]*$/;
            if (!emailRegex.test(char) && char !== '@' && char !== '.') {
              event.preventDefault();
            }
          }

        // Add event listeners to the input fields for input and blur events
        confirmPassword.addEventListener("input", updateButtonAndErrors);
        confirmPassword.addEventListener("blur", updateButtonAndErrors);

        email.addEventListener("input", updateButtonAndErrors);
        email.addEventListener("blur", updateButtonAndErrors);
        email.addEventListener("keypress", restrictSpecialChars);

        password.addEventListener("input", updateButtonAndErrors);
        password.addEventListener("blur", updateButtonAndErrors);
      

    
      
            // const email = document.getElementById("email");
            // const password = document.getElementById("passwordd");
            // const confirmPassword = document.getElementById("confirmPassword");
            // const passwordMatchError = document.getElementById("passwordMatchError");
            // const emailMatchError = document.getElementById("emailMatchError");
            // const btn = document.getElementById("btn");
          

            // function updateButtonAndErrors() {
            //   const passwordMatch = confirmPassword.value === password.value;
            //   const emailValid = email.value.length > 0;
            //   const passwordValid = password.value.length > 0;

            //   btn.disabled = !(passwordMatch && emailValid && passwordValid);

            //   // Show/hide errors for password match and email
            //   passwordMatchError.style.display = passwordMatch ? "none" : "block";
            //   emailMatchError.style.display = emailValid ? "none" : "block";
            // }

            // // Add event listeners to the input fields for input and blur events
            // confirmPassword.addEventListener("input", updateButtonAndErrors);
            // confirmPassword.addEventListener("blur", updateButtonAndErrors);

            // email.addEventListener("input", updateButtonAndErrors);
            // email.addEventListener("blur", updateButtonAndErrors);

            // password.addEventListener("input", updateButtonAndErrors);
            // password.addEventListener("blur", updateButtonAndErrors);

          // const email =document.getElementById("email")
          // const password = document.getElementById("passwordd");
          // const confirmPassword = document.getElementById("confirmPassword");
          // const passwordMatchError = document.getElementById("passwordMatchError");
          // const btn = document.getElementById("btn");
          // const emailMatchError=document.getElementById("emailMatchError")
          // // const nextButton = document.querySelector("input[name='next']");
         
       

          // confirmPassword.addEventListener("input", () => {
          //   // Check if the input field has any text
          //   if (confirmPassword.value.length > 0 && confirmPassword.value==password.value) {
          //     // If there's text, enable the button
          //     btn.disabled = false;
          //     passwordMatchError.style.display = "none";
          //   } else {
          //     // If there's no text, disable the button
          //     btn.disabled = true;
          //     passwordMatchError.style.display = "block";

          //   }
          // });

