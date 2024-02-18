//Ejecutar función en el evento click
const BTN_OPEN = document.getElementById("btn_open");

BTN_OPEN.addEventListener("click", () => {
    BTN_OPEN.classList.toggle("fa-bars");
    BTN_OPEN.classList.toggle("fa-times");

    body.classList.toggle("body_move");

    side_menu.classList.toggle("menu__side_close");
    side_menu.classList.toggle("menu__side");
    side_menu.classList.toggle("menu__side_move");
});

//Declaramos variables
var side_menu = document.getElementById("menu_side");
var body = document.getElementById("body");

side_menu.classList.add("menu__side_close");

//Haciendo el menú responsive(adaptable)

window.addEventListener("resize", function () {

    if (window.innerWidth > 760) {

        body.classList.remove("body_move");
        side_menu.classList.remove("menu__side_move");
    }

    if (window.innerWidth < 760) {

        body.classList.add("body_move");
        side_menu.classList.add("menu__side_move");
    }

});