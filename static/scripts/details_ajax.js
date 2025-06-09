import { addToggleHandlers } from "./icon_funcs_ajax.js";

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
    <div class="side-btn-container">
      <i class="fa-solid fa-xmark" id="delete-btn-details"></i>
      <a href=${
        cardData.Link
      } class="button apply-btn" target="_blank">Apply</a>
      <i class="fa-${cardData.isStarred ? "solid" : "regular"} fa-star"
         id="save-btn-details"
         data-vac_id="${cardData.V_id}"></i>
    </div>
  `;

  let rowK = cardData.Knowledges.map(
    (knowledge) => `<p>${knowledge.Field}</p>`
  ).join("");
  let rowF = cardData.Frameworks.map(
    (framework) => `<p>${framework.Name}</p>`
  ).join("");

  let cardHTML = `
      <div class="details-card">
        <div class="details-card-name">
          <h3><i class="fa-solid fa-gear"></i>Summary</h3>
          <i class="fa-solid fa-chevron-down unfold-arrow-icon"></i>
        </div>
        <div class="details-card-info">
        <b><span style="color: white">${cardData.Company}</span></b><br/>
        ${cardData.Summary || "No data found("}</div>
      </div>
      <div class="details-card">
        <div class="details-card-name">
          <h3><i class="fa-solid fa-gear"></i>Knowledges</h3>
          <i class="fa-solid fa-chevron-down unfold-arrow-icon rotated"></i>
        </div>
        <div class="details-card-info">${rowK || "No data found("}</div>
      </div>
      <div class="details-card">
        <div class="details-card-name">
          <h3><i class="fa-solid fa-gear"></i>Frameworks</h3>
          <i class="fa-solid fa-chevron-down unfold-arrow-icon rotated"></i>
        </div>
        <div class="details-card-info">${rowF || "No data found("}</div>
      </div>
      <div class="details-card">
        <div class="details-card-name">
          <h3><i class="fa-solid fa-gear"></i>Salary</h3>
          <i class="fa-solid fa-chevron-down unfold-arrow-icon rotated"></i>
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
  return { detailsCardTitles, cardHTML, buttons };
};

detailsButtons.forEach((button) => {
  button.addEventListener("click", async (event) => {
    try {
      const id = event.currentTarget.dataset.vac_id;
      const response = await fetch(`/vacancies/${id}/details`);
      if (response.ok) {
        const cardDetails = await response.json();
        console.log(cardDetails);
        const details = await createCardDetailsSection(cardDetails);

        const detailsCardPlace = document.getElementById("details-panel");
        detailsCardPlace.dataset.vac_id = cardDetails.V_id;
        detailsCardPlace.innerHTML = `
          ${details.detailsCardTitles}
          ${details.cardHTML}
          ${details.buttons}
        `;

        addToggleHandlers();
      }
    } catch (error) {
      alert(error.message);
    }
  });
});
