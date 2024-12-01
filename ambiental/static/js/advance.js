async function setAdvanceTable(categories) {
    console.log();
    let loaderDiv = document.querySelector("div.loader-div");
    loaderDiv.style.display = "block";
    const tableBody = document.querySelector(".tbody-advance");
    const { targetUser } = getCtx();
    const request = await axios.get(
        `/api/statistics/materials/${targetUser.id}`
    );
    const materialData = Object.values(request.data);

    Object.entries(categories).forEach(
        ([category, categorName], index) => {
            const currentMaterialData = materialData[index];

            const tr = document.createElement("tr");
            tr.innerHTML = `
                      <td>${categorName}</td>
                      <td>${currentMaterialData["total_required"]}</td>
                      <td>${currentMaterialData["na"]}</td>
                      <td>${currentMaterialData["applicable_requirements"]}</td>
                      <td>
                          <table>
                              <tbody>
                                  <tr>
                                      <td>${currentMaterialData["delivered"]}</td>
                                      <td>${currentMaterialData["pending"]}</td>
                                  </tr>
                              </tbody>
                          </table>
                      </td>
                      <td>${currentMaterialData["total"]}</td>
                  `;
            tableBody.appendChild(tr);
        }
    );

    loaderDiv.style.display = "none";
}

axios.get("/api/category/").then(async (response) => {
    const categories = response.data;
    console.log(categories);


    /**/

    let selectUser = document.querySelector("#users-list");
    if (selectUser !== null && selectUser !== undefined) {
        await setAdvanceTable(categories);
        selectUser.addEventListener("change", async () => {
            const tableBody = document.querySelector(".tbody-advance");
            tableBody.innerHTML = "";
            await setAdvanceTable(categories);
        });
    }
});