const detailsButtons = document.querySelectorAll(".card-buttons .details-btn");

const createCardDetailsSection = async (cardData) => {
  const detailsCardTitles = `
    <div style="width: 100%; display: flex; flex-direction: column; gap: 15px">
      <h1 class="details-card-position">${cardData.Position}</h1>
      <h3 class="details-card-location">${cardData.Location}</h3>
      <div class="additional-info">
        ${cardData.hasExpired ? "<h5 id='hasExpired'>Expired</h5>" : ""}
        ${
          cardData.haveApplied
            ? "<h5 id='haveApplied'>Already applied</h5>"
            : ""
        }
      </div>
    </div>
  `;
  const buttons = `
    <!-- Buttons part -->
    <div class="side-btn-container">
      <i class="fa-solid fa-xmark"></i>
      <a href=${cardData.Link} class="button apply-btn" target="_blank">Apply</a>
      <!-- <i class="fa-solid fa-star"></i> -->
      <i class="fa-regular fa-star"></i>
    </div>
  `;

  let rowK = "";
  for (const knowledge of cardData.Knowledges) {
    rowK += `
      <p>${knowledge.Field}</p>
    `;
  }

  let rowF = "";
  for (const framework of cardData.Frameworks) {
    rowF += `
      <p>${framework.Name}</p>
    `;
  }
  let cardHTML = `
      <!-- Card -->
      <div class="details-card">
        <div class="details-card-name">
          <h3><i class="fa-solid fa-gear"></i>Knowledges</h3>
          <i class="fa-solid fa-chevron-down"></i>
        </div>
        <div class="details-card-info">
          ${rowK}
        </div>
      </div>
      <!-- Card -->
      <div class="details-card">
        <div class="details-card-name">
          <h3><i class="fa-solid fa-gear"></i>Frameworks</h3>
          <i class="fa-solid fa-chevron-down"></i>
        </div>
        <div class="details-card-info">
          ${rowF.length > 0 ? rowF : "No data found("}
        </div>
      </div>
      <!-- Card -->
      <div class="details-card">
        <div class="details-card-name">
          <h3><i class="fa-solid fa-gear"></i>Salary</h3>
          <i class="fa-solid fa-chevron-down"></i>
        </div>
        <div class="details-card-info">
          <p>${
            cardData.Salary > 30
              ? cardData.Salary + "EUR/mesiac"
              : cardData.Salary + "EUR/hod"
          }</p>
        </div>
      </div>
    `;
  return { cardHTML, detailsCardTitles, buttons };
};

detailsButtons.forEach((button) => {
  button.addEventListener("click", async (event) => {
    try {
      const id = event.currentTarget.dataset.vac_id;
      const response = await fetch(`/${id}/details`);
      if (response.ok) {
        const cardDetails = await response.json();
        console.log(cardDetails);
        const details = await createCardDetailsSection(cardDetails);

        const detailsCardPlace = document.getElementById("details-panel");
        detailsCardPlace.innerHTML = `
          ${details.detailsCardTitles}
          ${details.cardHTML}
          ${details.buttons}
        `;
      }
    } catch (error) {
      alert(error.message);
    }
  });
});
