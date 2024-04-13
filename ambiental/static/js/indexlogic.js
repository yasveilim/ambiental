const sidebar = document.querySelector(".sidebar");
const sidebarClose = document.querySelector("#sidebar-close");
const menu = document.querySelector(".menu-content");
const menuItems = document.querySelectorAll(".submenu-item");
const subMenuTitles = document.querySelectorAll(".submenu .menu-title");


sidebarClose.addEventListener("click", () => {

  let tags = ['fa-xmark', 'fa-bars'];
  if (sidebarClose.classList.contains('fa-bars')) {
    tags = ['fa-bars', 'fa-xmark'];
  }

  sidebarClose.classList.replace(tags[0], tags[1]);
  return sidebar.classList.toggle("close");
});

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

// console.log(menuItems, subMenuTitles);

function configOptionElement(className, itemNamesList, callback) {

  console.log('configOptionElement: ', className);

  const wrapper = document.querySelector(className),
    selectBtn = wrapper.querySelector(".select-btn"),
    searchInp = wrapper.querySelector("input"),
    options = wrapper.querySelector(".options");

  // options.innerHTML = "";
  // searchInp.value = "";

  function updateName(event) {
    console.log(event);
    let selectedLi = event.srcElement;
    searchInp.value = "";
    addMaterial(selectedLi.innerText);
    wrapper.classList.remove("active");
    selectBtn.firstElementChild.innerText = selectedLi.innerText;
  }

  function addMaterial(selectedItem) {
    options.innerHTML = "";
    //console.log("Another item is selected", documentNames);
    callback(selectedItem, wrapper);
    itemNamesList.forEach(itemName => {
      let isSelected = itemName == selectedItem ? "selected" : "";

      let newOpt = document.createElement('li');
      newOpt.onclick = updateName;
      newOpt.className = `${isSelected}`;
      newOpt.textContent = itemName;
      // return `<li onclick="updateName(this)" class="${isSelected}">${data}</li>`;
      options.appendChild(newOpt);

    });
  }


  searchInp.addEventListener("keyup", () => {
    let searchWord = searchInp.value.toLowerCase();
    document.querySelector(`${className} .options`).innerHTML = '';

    itemNamesList.filter(itemName => {
      return itemName.toLowerCase().startsWith(searchWord);
    }).forEach(filteredItemName => {
      let isSelected =
        filteredItemName == selectBtn.firstElementChild.innerText ? "selected" : "";

      let newOpt = document.createElement('li');
      newOpt.onclick = updateName;
      newOpt.className = `${isSelected}`;
      newOpt.textContent = filteredItemName;

      options.appendChild(newOpt);
    }).join("");

    // options.innerHTML = arr ? arr : `<p style="margin-top: 10px;">Oops! Country not found</p>`;
  });

  selectBtn.addEventListener("click", () => wrapper.classList.toggle("active"));
  addMaterial();
}

function collectBookNames(data) {
  // Buscamos la primera clave en el objeto (puede ser 'AGUA' u otra)
  const key = Object.keys(data)[0];
  // Extraemos los nombres de los libros
  const bookNames = data[key].map(book => book.name);
  return bookNames;
}

function invertObject(obj) {
  return Object.fromEntries(Object.entries(obj).map(([key, value]) => [value, key]));
}

axios.get('/api/material/').then((response) => {
  let materialNames = response.data;
  let materialsFromValues = invertObject(materialNames);
  let materials = Object.values(materialNames);

  configOptionElement("div.wrapper", materials, (selectedText, xwrapper) => {

    if (!selectedText || selectedText === 'Categoría') {
      return;
    }

    let materialSelectedName = materialsFromValues[selectedText];
    console.log('This is the selected material: ', materialSelectedName);

    // TODO: Esto tiene un errror, cuando se cambia el primer option
    // el segundo se congela aunque carga toda la data

    let fetchData = async () => {
      try {
        const response = await axios.get(`/api/materialbook/${materialSelectedName}`);
        console.log('My materialSelectedName is: ', materialSelectedName, response.data);

        let documentsData = response.data;
        let documentsNames = collectBookNames(documentsData);

        console.log('div.name_document: ', document.querySelector("div.name_document"))

        configOptionElement("div.name_document", documentsNames, (selectedText, wrapper) => {
          //const wrapper = document.querySelector(className),
          selectBtn = wrapper.querySelector(".select-btn");
          selectBtn.firstElementChild.innerText = "";

          // console.log(`My select: ${selectedText}`)
        });
      } catch (error) {
        console.error('Error fetching data: ', error);
      }
    };

    fetchData()

  });
});
