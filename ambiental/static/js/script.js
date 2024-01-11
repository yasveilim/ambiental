//Ejecutar función en el evento click
document.getElementById("btn_open").addEventListener("click", open_close_menu);

//Declaramos variables
var side_menu = document.getElementById("menu_side");
var body = document.getElementById("body");

side_menu.classList.add("menu__side_close");

//Evento para mostrar y ocultar menú
function open_close_menu(){
    body.classList.toggle("body_move");
    
    side_menu.classList.toggle("menu__side_close");
    side_menu.classList.toggle("menu__side");
    side_menu.classList.toggle("menu__side_move");
}



//Haciendo el menú responsive(adaptable)

window.addEventListener("resize", function(){

    if (window.innerWidth > 760){

        body.classList.remove("body_move");
        side_menu.classList.remove("menu__side_move");
    }

    if (window.innerWidth < 760){

        body.classList.add("body_move");
        side_menu.classList.add("menu__side_move");
    }

});