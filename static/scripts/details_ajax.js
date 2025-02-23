const detailsButtons = document.querySelectorAll(".card-buttons .details-btn");

const createCardDetailsSection = async (cardData) => {
  const detailsCardPlace = document.getElementById("details-panel");

  let detailsCardPosition = document.querySelector(".details-card-position");
  let detailsCardLocation = document.querySelector(".details-card-location");

  // фором добавлять <p>, а потом еще одним, но по кол-ву, записывать в шаблон карточки
  let detailsHTML = "";
  for (details in cardDetails.le) {
    cardHTML += `
    <!-- Card -->
    <div class="details-card">
      <div class="details-card-name">
        <h3><i class="fa-solid fa-gear"></i>Salary</h3>
        <i class="fa-solid fa-chevron-down"></i>
      </div>
      <div class="details-card-info">
        <p> <!-- СЮДА ВСТАВИТЬ ИНФО ФОРОМ --> </p>
      </div>
    </div>
    `;
    detailsHTML = `
    
    `;
  }
};

detailsButtons.forEach((button) => {
  button.addEventListener("click", async (event) => {
    try {
      const id = event.currentTarget.dataset.vac_id;
      const response = await fetch(`/${id}/details`);
      if (response.ok) {
        const cardDetails = await response.json();
        console.log(cardDetails);
        createCardDetailsSection(cardDetails);
      }
    } catch (error) {
      alert(error.message);
    }
  });
});
