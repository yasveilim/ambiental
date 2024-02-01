function validarClave(cadena1, cadena2){
    if(cadena1 != cadena2) {
        return "Different";
    }
    if(cadena1.length < 8) {
        return "Short";
    }
    
    let mayusculas1 = (cadena1.match(/[A-Z]/g) || []).length;
    if(mayusculas1 < 2 ) {
        return "NoCapital";
    }
    if(! /[!@#$%^&*(),.?":{}|<>]/.test(cadena1)) {
        return "NoSpecial";
    }
    
    return "Okay";
}
