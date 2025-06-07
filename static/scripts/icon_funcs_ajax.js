const deleteIcons = document.querySelectorAll(".fa-xmark");
const saveIcons = document.querySelectorAll(".fa-star");

deleteIcons.forEach((icon) => {
  icon.addEventListener("click", async (event) => {
    const id = event.currentTarget.dataset.vac_id;
    try {
      const response = await fetch(`/vacancies/${id}/delete`);
      if (response.ok) {
        const { hasExecuted, isDeleted } = await response.json();
        alert(
          `Vacancy deleted: ${
            hasExecuted && isDeleted ? "successfuly" : "failed"
          }!`
        );
      }
    } catch (error) {
      alert("Error fetching deleting: " + error);
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
    `[data-vac_id="${vacancyId}"].fa-star`
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
  const saveIcon = event.target.closest(".fa-star"); // Ловим клик по звездочке
  if (!saveIcon) return;

  const vacancyId = saveIcon.dataset.vac_id; // Получаем ID вакансии
  if (!vacancyId) return console.error("Vacancy ID not found! (funcs)");

  try {
    const response = await fetch(`/vacancies/${vacancyId}/star`);
    if (response.ok) {
      const result = await response.json();
      if (result.executed) {
        updateAllIcons(vacancyId, result.starred); // Обновляем все иконки с этим ID
      }
    }
  } catch (error) {
    console.error("Error saving vacancy:", error);
  }
});

export { updateAllIcons };
