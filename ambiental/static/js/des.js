const OPTION_MENU = document.querySelector(".select-menu"),
       SELECT_BTN = OPTION_MENU.querySelector(".select-btn"),
       OPTIONS    = OPTION_MENU.querySelectorAll(".option"),
       SBTN_TEXT  = OPTION_MENU.querySelector(".sBtn-text");

SELECT_BTN.addEventListener("click", () => OPTION_MENU.classList.toggle("active"));       

OPTIONS.forEach(option => {
    option.addEventListener("click", ()=> {
        let selectedOption = option.querySelector(".option-text").innerText;
        SBTN_TEXT.innerText = selectedOption;

        OPTION_MENU.classList.remove("active");
    });
});

console.log(OPTIONS[0])
OPTIONS[0].click()
