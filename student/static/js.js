function checkpass{
        if(document.signup.password.value!=document.signup.cpwd.value){
            alert("Password doesn't match!");
            document.signup.cpwd.focus();
            return false;
        }
        return true;
    }