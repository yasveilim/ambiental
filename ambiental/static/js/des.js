
const ALL_OPTION_MENU = document.querySelectorAll(".select-menu");
let currentIndex = null;

ALL_OPTION_MENU.forEach((optionMenu, indexOptionMenu) => {
    let selectBtn = optionMenu.querySelector(".select-btn"),
        options = optionMenu.querySelectorAll(".option"),
        sbtnText  = optionMenu.querySelector(".sBtn-text");


    selectBtn.addEventListener("click", () => {
        console.log("click: ", indexOptionMenu);
        optionMenu.classList.toggle("active")
    });       

    options.forEach((option, optionIndex) => {
        option.addEventListener("click", ()=> {
            let selectedOption = option.querySelector(".option-text").innerText;
           
            if (selectedOption.length > 64) {
                selectedOption = selectedOption.slice(0, 64) + '...';
            }

            if (indexOptionMenu == 0) {
                if (currentIndex != null) {
                    ALL_OPTION_MENU[currentIndex].classList.toggle("select-menu-hidden");
                }
                
                currentIndex = optionIndex + 1;
                console.log([selectedOption])
                console.log("indexOptionMenu: ", ALL_OPTION_MENU[optionIndex + 1]);
                ALL_OPTION_MENU[currentIndex].classList.toggle("select-menu-hidden");
            }

            sbtnText.innerText = selectedOption;

            optionMenu.classList.remove("active");


            //ALL_OPTION_MENU.forEach((optionMenu, indexOptionMenu) => {
            //    optionMenu
            //});

        });
    });

    console.log(options[0])
    options[0].click()
});
