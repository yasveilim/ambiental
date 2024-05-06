const sidebar = document.querySelector(".sidebar");
const sidebarClose = document.querySelector("#sidebar-close");
const menu = document.querySelector(".menu-content");
const menuItems = document.querySelectorAll(".submenu-item");
const subMenuTitles = document.querySelectorAll(".submenu .menu-title");
const mainModal = document.querySelector("div.modal");

var globalBookSelect = null;

function closeModal() {
  mainModal.style.display = "none";
}

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
function titleCase(str) {
  if ((str === null) || (str === ''))
      return false;
  else
      str = str.toString();

  return str.replace(/\w\S*/g,
      function (txt) {
          return txt.charAt(0).toUpperCase() +
              txt.substr(1).toLowerCase();
      });
}

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
    addMaterial(selectedLi);
    wrapper.classList.remove("active");
    selectBtn.firstElementChild.innerText = trimText(selectedLi.innerText);
  }

  function addMaterial(selectedItem) {
    options.innerHTML = "";
    //console.log("Another item is selected", documentNames);

    if (selectedItem !== undefined) {
      //console.log(selectedItem, selectedItem.parentElement);
      let index = selectedItem.getAttribute('idx');
  
      callback(selectedItem.innerText, index, wrapper);
    }

    itemNamesList.forEach((itemName, idx) => {
      let isSelected = (selectedItem && itemName == selectedItem.innerText) ? "selected" : "";

      let newOpt = document.createElement('li');
      newOpt.onclick = updateName;
      newOpt.className = `${isSelected}`;
      newOpt.textContent = titleCase(itemName);
      newOpt.setAttribute('idx', idx)
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
      newOpt.textContent =  titleCase(filteredItemName);

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

function trimText(text) {
  const limit = 80;
  return text.length > limit ? text.substring(0, limit - 3) + '...' : text;
}

function invertObject(obj) {
  return Object.fromEntries(Object.entries(obj).map(([key, value]) => [value, key]));
}


function loadMaterials(categories, materials) {

  configOptionElement("div.wrapper", materials, (selectedText, index, xwrapper) => {
    console.log("selectedText: ", selectedText, " - ", index);

    // 
    if (!selectedText || selectedText === 'Categoría') {
      return;
    }

    //let materialSelectedName = materialsFromValues[selectedText];
    //console.log('This is the selected material: ', materialSelectedName);

    // TODO: Esto tiene un errror, cuando se cambia el primer option
    // el segundo se congela aunque carga toda la data
    // Pista: El segundo options no puede cambiar a "activate"

    let fetchData = async () => {
      try {
        const response = await axios.get(`/api/materialbook/${sectionName}/${index}`);
        console.log('My materialSelectedName is: ', response.data);

        let documentsData = response.data;
        let documentsNames = collectBookNames(documentsData);

        console.log('div.name_document: ', document.querySelector("div.name_document"))

        configOptionElement("div.name_document", documentsNames, (selectedText, index, wrapper) => {
          const statusDocument = {
            'DELIVERED': {
              text: 'Entregado',
              className: 'thead-de',
            },
            'PENDING': {
              text: 'Pendiente',
              className: 'thead-pe',
            },
            'NA': {
              text: 'No Aplica',
              className: 'thead-na',
            } 
        };
          console.log("Estado: ", selectedText, " ", index, " ", wrapper)

          let bookData = documentsData.items[index];
          globalBookSelect = bookData;

          // #246355 #0F362D

          let deliveryProgress = document.querySelector("th#delivery-progress");
          let theadUnique = document.querySelector("thead");

          let dateDelivery = document.querySelector("td#date-delivery");
          let environmentalPerformanceLevel = document.querySelector("td#environmental-performance-level");
          let uploadTotheCloud = document.querySelector("td#upload-tothe-cloud");
          let comments = document.querySelector("td#comments"); 

          metadataBar = statusDocument[bookData.advance];
          deliveryProgress.textContent = metadataBar.text; // cambiar color
          theadUnique.classList.forEach(name => theadUnique.classList.remove(name))
          theadUnique.classList.add(metadataBar.className);
          theadUnique.onclick = (event) => {
            mainModal.style.display = "block";
            console.log(`I clicked here: `, event);
          };

          //theadUnique.innerHTML.



          dateDelivery.textContent = bookData.archives;
          // is_critical
          environmentalPerformanceLevel.textContent = bookData.nda;
          uploadTotheCloud.textContent = bookData.essential_cloud ? "Si" : "No";
          comments.textContent = bookData.comments;

          //const wrapper = document.querySelector(className),
          // selectBtn = wrapper.querySelector(".select-btn");
          // selectBtn.firstElementChild.innerText = "";

          // console.log(`My select: ${selectedText}`)
        });
      } catch (error) {
        console.error('Error fetching data: ', error);
      }
    };

    fetchData()

  });
}


axios.get('/api/category/').then((response) => {
  closeModal();
  let categories = response.data;
  axios.get(`/api/material/${sectionName}`).then((response) => {
    //console.log(categories, " - ", sectionName, " - ", response.data)
    loadMaterials(categories, response.data.names)
  });
});