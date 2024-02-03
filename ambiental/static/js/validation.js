function validatePassword(str1, str2){
    if(str1 != str2) {
        return "Different";
    }

    if(str1.length < 8) {
        return "Short";
    }
    
    let mayusculas1 = (str1.match(/[A-Z]/g) || []).length;
    if(mayusculas1 < 2 ) {
        return "NoCapital";
    }
    
    if (!/^[a-zA-Z0-9-_]+$/.test(str1)) {
        return "InvalidCharacters";
    }
    
    // if(! /[!@#$%^&*(),.?":{}|<>]/.test(str1)) { return "NoSpecial"; }
    
    return "Okay";
}
