const deleteIcons = document.querySelectorAll(".fa-xmark");
const saveIcons = document.querySelectorAll(".fa-star");

deleteIcons.forEach((icon) => {
  icon.addEventListener("click", async (event) => {
    const id = event.currentTarget.dataset.vac_id;
    const card = event.target.closest(".card"); // Находим родительскую карточку

    try {
      const response = await fetch(
        `/vacancies/${encodeURIComponent(id)}/delete`,
        {
          method: "DELETE", // Явно указываем метод DELETE
        }
      );

      const result = await response.json();

      if (response.ok && result.hasExecuted && result.isDeleted) {
        // Плавно скрываем и удаляем карточку
        card.style.transition = "opacity 0.3s";
        card.style.opacity = "0";
        setTimeout(() => card.remove(), 300); // Удаляем после анимации
      } else {
        alert(`Failed to delete vacancy: ${result.error || "Unknown error"}`);
      }
    } catch (error) {
      alert("Error deleting vacancy: " + error);
    }
  });
});

const changeIcon = (icon, isSaved) => {
  if (isSaved) {
    icon.classList.replace("fa-regular", "fa-solid");
  } else {
    icon.classList.replace("fa-solid", "fa-regular");
  }
};

const updateAllIcons = (vacancyId, isSaved) => {
  const allIcons = document.querySelectorAll(
    `[data-vac_id="${encodeURIComponent(vacancyId)}"].fa-star`
  );
  console.log(allIcons);
  allIcons.forEach((icon) => changeIcon(icon, isSaved));
};

/*
saveIcons.forEach((icon) => {
  icon.addEventListener("click", async (event) => {
    const id = event.currentTarget.dataset.vac_id;
    try {
      const response = await fetch(`/${id}/save`);
      if (response.ok) {
        const result = await response.json();
        if (result.executed) {
          changeIcon(icon, result.starred);
        }
      }
    } catch (error) {
      alert("Error fetching deleting: " + error);
    }
  });
});
*/

document.addEventListener("click", async (event) => {
  const saveIcon = event.target.closest(".fa-star");
  if (!saveIcon) return;

  const vacancyId = saveIcon.dataset.vac_id;
  if (!vacancyId) return console.error("Vacancy ID not found! (funcs)");

  try {
    const response = await fetch(
      `/vacancies/${encodeURIComponent(vacancyId)}/star`,
      {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
      }
    );
    if (response.ok) {
      const result = await response.json();
      if (result.executed) {
        updateAllIcons(vacancyId, result.starred);
      }
    }
  } catch (error) {
    console.error("Error saving vacancy:", error);
  }
});

const addToggleHandlers = () => {
  const detailsCards = document.querySelectorAll(".details-card-name");

  // Инициализация состояния всех карточек
  detailsCards.forEach((cardName, index) => {
    const content = cardName.nextElementSibling;
    const card = cardName.parentElement;

    // Устанавливаем начальную высоту для всех открытых карточек
    if (!card.classList.contains("collapsed")) {
      content.style.maxHeight = content.scrollHeight + "px";
    }

    // Скрываем первую карточку (Summary) по умолчанию
    if (index === 0) {
      card.classList.add("collapsed");
      // cardName.querySelector(".unfold-arrow-icon").classList.add("rotated");
      content.style.maxHeight = "0px";
    }
  });

  detailsCards.forEach((cardName) => {
    cardName.addEventListener("click", (e) => {
      const arrow = cardName.querySelector(".unfold-arrow-icon");
      const content = cardName.nextElementSibling;
      const card = cardName.parentElement;

      // Toggle класса для анимации стрелочки
      arrow.classList.toggle("rotated");

      // Toggle класса для скрытия контента
      card.classList.toggle("collapsed");

      // Управление высотой для плавной анимации
      if (card.classList.contains("collapsed")) {
        content.style.maxHeight = "0px";
      } else {
        content.style.maxHeight = content.scrollHeight + "px";
      }
    });
  });
};

export { updateAllIcons, addToggleHandlers };
