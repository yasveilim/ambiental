const sidebar = document.querySelector(".sidebar");
const sidebarClose = document.querySelector("#sidebar-close");
const menu = document.querySelector(".menu-content");
const menuItems = document.querySelectorAll(".submenu-item");
const subMenuTitles = document.querySelectorAll(".submenu .menu-title");
const mainModal = () => document.querySelector("div.modal");

var globalBookSelect = null;

function closeModal() {
  mainModal().style.display = "none";
}

sidebarClose.addEventListener("click", () => {
  let tags = ["fa-xmark", "fa-bars"];
  if (sidebarClose.classList.contains("fa-bars")) {
    tags = ["fa-bars", "fa-xmark"];
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
  if (str === null || str === "") return false;
  else str = str.toString();

  return str.replace(/\w\S*/g, function (txt) {
    return txt.charAt(0).toUpperCase() + txt.substr(1).toLowerCase();
  });
}

function configOptionElement(className, itemNamesList, callback) {
  console.log("configOptionElement: ", className);

  let loaderDiv = document.querySelector("div.loader-div");
  console.log("loaderDiv: ", loaderDiv);
  loaderDiv.style.display = "none";

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
      let index = selectedItem.getAttribute("idx");
      loaderDiv.style.display = "flex";
      callback(selectedItem.innerText, index, wrapper);
    }

    itemNamesList.forEach((itemName, idx) => {
      let isSelected =
        selectedItem && itemName == selectedItem.innerText ? "selected" : "";

      let newOpt = document.createElement("li");
      newOpt.onclick = updateName;
      newOpt.className = `${isSelected}`;
      newOpt.textContent = titleCase(itemName);
      newOpt.setAttribute("idx", idx);
      // return `<li onclick="updateName(this)" class="${isSelected}">${data}</li>`;
      options.appendChild(newOpt);
    });
  }

  searchInp.addEventListener("keyup", () => {
    let searchWord = searchInp.value.toLowerCase();
    document.querySelector(`${className} .options`).innerHTML = "";

    itemNamesList
      .filter((itemName) => {
        return itemName.toLowerCase().startsWith(searchWord);
      })
      .forEach((filteredItemName) => {
        let isSelected =
          filteredItemName == selectBtn.firstElementChild.innerText
            ? "selected"
            : "";

        let newOpt = document.createElement("li");
        newOpt.onclick = updateName;
        newOpt.className = `${isSelected}`;
        newOpt.textContent = titleCase(filteredItemName);

        options.appendChild(newOpt);
      })
      .join("");

    // options.innerHTML = arr ? arr : `<p style="margin-top: 10px;">Oops! Country not found</p>`;
  });

  selectBtn.addEventListener("click", () => wrapper.classList.toggle("active"));
  addMaterial();
}

function collectBookNames(data) {
  // Buscamos la primera clave en el objeto (puede ser 'AGUA' u otra)
  const key = Object.keys(data)[0];
  // Extraemos los nombres de los libros
  const bookNames = data[key].map((book) => book.name);
  return bookNames;
}

function trimText(text) {
  const limit = 80;
  return text.length > limit ? text.substring(0, limit - 3) + "..." : text;
}

function invertObject(obj) {
  return Object.fromEntries(
    Object.entries(obj).map(([key, value]) => [value, key])
  );
}

function setCommentsModal(newValue) {
  let commentsModal = document.querySelector("div.modal-comments");
  commentsModal.classList.toggle("hidden");

  let commentsModalText = commentsModal.querySelector(".modal-comments-textarea");
  commentsModalText.value = newValue;
  return commentsModal;
}

document.querySelector("div.modal-comments .close-modal-btn").onclick = () => {
  setCommentsModal("");
};


function showComments() {
  let commentsModal = setCommentsModal("This is a comment from the admin");

}

function loadMaterials(categories, materials) {
  configOptionElement(
    "div.wrapper",
    materials,
    (selectedText, index, xwrapper) => {
      console.log("selectedText: ", selectedText, " - ", index);

      //
      if (!selectedText || selectedText === "Categoría") {
        return;
      }

      //let materialSelectedName = materialsFromValues[selectedText];
      //console.log('This is the selected material: ', materialSelectedName);

      // TODO: Esto tiene un errror, cuando se cambia el primer option
      // el segundo se congela aunque carga toda la data
      // Pista: El segundo options no puede cambiar a "activate"

      let fetchData = async () => {
        let ctx = getCtx();
        let csrftoken = Cookies.get("csrftoken");
        let config = {
          headers: {
            "X-CSRFToken": csrftoken,
          },
        };

        try {

          const response = await axios.post(
            `/api/materialbook/${sectionName}/${index}`,
            ctx,
            config
          );

          let documentsData = response.data;
          let documentsNames = collectBookNames(documentsData);

          console.log(
            "div.name_document: ",
            document.querySelector("div.name_document")
          );

          configOptionElement(
            "div.name_document",
            documentsNames,
            (selectedText, index, wrapper) => {
              const statusDocument = {
                DELIVERED: {
                  text: "Entregado",
                  className: "thead-de",
                },
                PENDING: {
                  text: "Pendiente",
                  className: "thead-pe",
                },
                NA: {
                  text: "No Aplica",
                  className: "thead-na",
                },
              };
              // console.log("Estado: ", selectedText, " ", index, " ", wrapper);

              let bookData = documentsData.items[index];
              globalBookSelect = bookData;

              // #246355 #0F362D

              let deliveryProgress = document.querySelector(
                "th#delivery-progress"
              );
              let theadUnique = document.querySelector("thead");

              let dateDelivery = document.querySelector("td#date-delivery");
              let environmentalPerformanceLevel = document.querySelector(
                "td#environmental-performance-level"
              );
              let uploadTotheCloud = document.querySelector(
                "td#upload-tothe-cloud"
              );
              let comments = document.querySelector("td#comments");
              comments.innerHTML = `<button onclick="showComments()">Ver</button>`;

              metadataBar = statusDocument[bookData.advance];
              deliveryProgress.textContent = metadataBar.text; // cambiar color
              theadUnique.classList.forEach((name) =>
                theadUnique.classList.remove(name)
              );
              theadUnique.classList.add(metadataBar.className);
              theadUnique.onclick = (event) => {
                mainModal().style.display = "block";
                console.log(`I clicked here: `, event);
              };

              dateDelivery.textContent = bookData.deliveryDate; //bookData.archives;
              // is_critical
              environmentalPerformanceLevel.textContent = bookData.nda;
              uploadTotheCloud.textContent = bookData.essential_cloud
                ? "Si"
                : "No";
              //comments.textContent = bookData.comments;

              let loaderDiv = document.querySelector("div.loader-div");
              loaderDiv.style.display = "none";
            }
          );
        } catch (error) {
          console.error("Error fetching data: ", error);
        }
      };

      fetchData();
    }
  );
}

if (mainModal().style.display !== "none") {
  mainModal().style.display = "none";
}

function getCtx() {
  let selectUser = document.querySelector("#users-list");
  if (selectUser === null || selectUser === undefined) {
    return null;
  }

  selectUser = selectUser.options[selectUser.selectedIndex];
  return {
    targetUser: {
      username: selectUser.textContent.trim(),
      id: Number(selectUser.value),
    },
  };
}

axios.get("/api/category/").then((response) => {
  function searchMaterialByUser() {
    let categories = response.data;
    let ctx = getCtx();
    let csrftoken = Cookies.get("csrftoken");
    let config = {
      headers: {
        "X-CSRFToken": csrftoken,
      },
    };

    axios.post(`/api/material/${sectionName}`, ctx, config).then((response) => {
      //console.log(categories, " - ", sectionName, " - ", response.data)
      loadMaterials(categories, response.data.names);
    });
  }

  searchMaterialByUser();

  let selectUser = document.querySelector("#users-list");
  if (selectUser !== null && selectUser !== undefined) {
    selectUser.addEventListener("change", searchMaterialByUser);
  }
});
