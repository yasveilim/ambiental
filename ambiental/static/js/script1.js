const sidebar = document.querySelector(".sidebar");
const sidebarClose = document.querySelector("#sidebar-close");
const menu = document.querySelector(".menu-content");
const menuItems = document.querySelectorAll(".submenu-item");
const subMenuTitles = document.querySelectorAll(".submenu .menu-title");



console.log('sectionName: asd');
console.log('sectionName: ', sectionName);
// axios.get('https://google.com')

sidebarClose.addEventListener("click", () => sidebar.classList.toggle("close"));

menuItems.forEach((item, index) => {
  item.addEventListener("click", () => {
    menu.classList.add("submenu-active");
    item.classList.add("show-submenu");
    menuItems.forEach((item2, index2) => {
      if (index !== index2) {
        item2.classList.remove("show-submenu");
      }
    });
  });
});

subMenuTitles.forEach((title) => {
  title.addEventListener("click", () => {
    menu.classList.remove("submenu-active");
  });
});

console.log(menuItems, subMenuTitles);

function configOptionElement(className, materials) {


  const wrapper = document.querySelector(className), // ".wrapper"
    selectBtn = wrapper.querySelector(".select-btn"),
    searchInp = wrapper.querySelector("input"),
    options = wrapper.querySelector(".options");

  // let materials = [];
  // ["Agua", "Aire y ruído", "Residuos", "RECNAT y riesgos", "Otros"];

  function addMaterial(selectedCountry) {
    options.innerHTML = "";
    materials.forEach(material => {
      let isSelected = material == selectedCountry ? "selected" : "";
      let li = `<li onclick="updateName(this)" class="${isSelected}">${material}</li>`;
      options.insertAdjacentHTML("beforeend", li);
    });
  }

  function updateName(selectedLi) {
    searchInp.value = "";
    addMaterial(selectedLi.innerText);
    wrapper.classList.remove("active");
    selectBtn.firstElementChild.innerText = selectedLi.innerText;
  }

  searchInp.addEventListener("keyup", () => {
    console.log(" On keyup ");
    let arr = [];
    let searchWord = searchInp.value.toLowerCase();
    arr = materials.filter(data => {
      return data.toLowerCase().startsWith(searchWord);
    }).map(data => {
      let isSelected = data == selectBtn.firstElementChild.innerText ? "selected" : "";
      return `<li onclick="updateName(this)" class="${isSelected}">${data}</li>`;
    }).join("");
    options.innerHTML = arr ? arr : `<p style="margin-top: 10px;">Oops! Country not found</p>`;
  });

  selectBtn.addEventListener("click", () => wrapper.classList.toggle("active"));
  addMaterial();
}

axios.get('/api/material/').then((response) => {
  let materialNames = response.data;
  // console.log('myMaterials: ', Object.values(response.data));
  let materials = Object.values(materialNames);
  configOptionElement(".wrapper", materials);

  
  // configOptionElement(".wrapper", materials);

  
});