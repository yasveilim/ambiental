var myChart = null;

function createChart(labels, values) {
    const ctx = document.getElementById("nvivoBarChart").getContext("2d");
    if (myChart) {
        myChart.clear();
        myChart.destroy();
    }

    myChart = new Chart(ctx, {
        type: "bar",
        data: {
            labels: labels,
            datasets: [
                {
                    label: "Avances en la entrega de documentos",
                    data: values,
                    borderWidth: 1,
                },
            ],
        },
        options: {
            scales: {
                y: {
                    beginAtZero: true,
                },
            },
        },
    });
}

function SetChart(categoryAndTotal) {
    const canvasStats = document.querySelector("#nvivoBarChart");
    const context = canvasStats.getContext("2d");
    context.clearRect(0, 0, canvasStats.width, canvasStats.height);

    let labels = [];
    let values = [];

    categoryAndTotal.forEach((item) => {
        labels.push(item.category);
        values.push(item.total);
    });


    createChart(labels, values);

}

async function setAdvanceTable(categories) {
    let loaderDiv = document.querySelector("div.loader-div");
    loaderDiv.style.display = "block";
    const tableBody = document.querySelector(".tbody-advance");
    const { targetUser } = getCtx();
    const request = await axios.get(
        `/api/statistics/materials/${targetUser.id}`
    );
    const materialData = Object.values(request.data);
    const categoryAndTotal = [];

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

            let totalRequired = parseFloat(currentMaterialData["total_required"]);
            let na = parseFloat(currentMaterialData["na"]);
            let totalPercentage = parseFloat(currentMaterialData["total"].replace('%', ''));


            let applicableRequirements = totalRequired - na;
            let absoluteTotal = (totalPercentage / 100) * applicableRequirements;

            categoryAndTotal.push({
                category: categorName,
                total: absoluteTotal,
            });
        }
    );

    SetChart(categoryAndTotal);

    loaderDiv.style.display = "none";
}

axios.get("/api/category/").then(async (response) => {
    const categories = response.data;

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




