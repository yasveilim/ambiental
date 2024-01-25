
const ALL_OPTION_MENU = document.querySelectorAll(".select-menu");

ALL_OPTION_MENU.forEach(optionMenu => {
    let selectBtn = optionMenu.querySelector(".select-btn"),
        options = optionMenu.querySelectorAll(".option"),
        sbtnText  = optionMenu.querySelector(".sBtn-text");


    selectBtn.addEventListener("click", () => optionMenu.classList.toggle("active"));       

    options.forEach(option => {
        option.addEventListener("click", ()=> {
            let selectedOption = option.querySelector(".option-text").innerText;
            console.log([selectedOption])
            if (selectedOption.length > 64) {
                selectedOption = selectedOption.slice(0, 64) + '...';
            }

            sbtnText.innerText = selectedOption;

            optionMenu.classList.remove("active");
        });
    });

    console.log(options[0])
    options[0].click()
});

OPTIONS[0].click()