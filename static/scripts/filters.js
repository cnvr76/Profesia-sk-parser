const filtersButton = document.getElementById("filters-btn");
const selectedFilter = document.getElementById("selected");
const dropdownContentBlock = document.querySelector(
  ".dropdown .dropdown-content"
);
const dropdownBlock = document.querySelector(".dropdown");

const options = ["All", "Fetched", "Expired", "Most recent"];

function initFilters() {
  dropdownContentBlock.innerHTML = "";

  options.forEach((option) => {
    const link = document.createElement("a");
    link.href = "#";
    link.textContent = option;

    link.addEventListener("click", (e) => {
      e.preventDefault();
      const filterName = e.target.textContent;
      selectedFilter.textContent = filterName;
      localStorage.setItem("selectedFilter", filterName);
      const correctName = correctFilterName(filterName);
      window.location.href = `/bar/filters/${correctName}`;
    });

    dropdownContentBlock.appendChild(link);
  });

  const savedFilter = localStorage.getItem("selectedFilter");
  selectedFilter.textContent = savedFilter || options[0];
}

function correctFilterName(filterName) {
  return filterName.replace(" ", "_").toLowerCase();
}

filtersButton.addEventListener("mouseenter", () => {
  dropdownContentBlock.style.display = "flex";
  filtersButton.style.borderRadius = "10px 10px 0 0";
});

dropdownBlock.addEventListener("mouseleave", () => {
  dropdownContentBlock.style.display = "none";
  filtersButton.style.borderRadius = "10px";
});

document.addEventListener("DOMContentLoaded", initFilters);
