function togglePasswordVisibility() {
    var passwordInput = document.getElementById("password");
    var passIcon = document.getElementById("pass-icon");
    
    if (passwordInput.type === "password") {
      passwordInput.type = "text";
      passIcon.src = "wed/bx-low-vision.svg"; // Change icon to show
    } else {
      passwordInput.type = "password";
      passIcon.src = "wed/bx-low-vision.svg"; // Change icon to hide
    }
  }