import React, { useState } from "react";
import avatar from "../static/images/avatar.jpg";

const Header = ({
  currentFilter,
  onFilterChange,
  onNewestFetching,
  isNewestFetching,
}) => {
  const [isDropdownOpen, setIsDropdownOpen] = useState(false);
  const [selectedFilter, setSelectedFilter] = useState(currentFilter || "All");

  const filterOptions = ["All", "Fetched", "Expired", "Most recent"];

  const handleFilterSelect = (filterName) => {
    setSelectedFilter(filterName);
    setIsDropdownOpen(false);

    localStorage.setItem("selectedFilter", filterName);

    onFilterChange(filterName);
  };

  const handleMouseEnter = () => {
    setIsDropdownOpen(true);
  };

  const handleMouseLeave = () => {
    setIsDropdownOpen(false);
  };

  return (
    <section className="bar">
      {/* Левая часть навигации */}
      <div className="left-part">
        {/* Кнопка Home */}
        <button
          className="button"
          id="home-btn"
          onClick={() => console.log("Home функциональность в разработке")}
          title="Показать все вакансии"
        >
          <i className="fa-solid fa-house"></i>
        </button>

        {/* Кнопка Newest */}
        <button
          className={`button ${isNewestFetching ? "loading" : ""}`}
          id="newest-btn"
          onClick={onNewestFetching}
          disabled={isNewestFetching}
          title={
            isNewestFetching ? "Парсим новые вакансии..." : "Новейшие вакансии"
          }
        >
          {isNewestFetching ? (
            <>
              <i className="fa-solid fa-spinner fa-spin"></i> Parsing...
            </>
          ) : (
            "Newest"
          )}
        </button>

        {/* Кнопка Matching */}
        <button
          className="button"
          id="tinder-btn"
          onClick={() => console.log("Matching функциональность в разработке")}
          title="Подходящие вакансии"
        >
          Matching
        </button>

        {/* Dropdown фильтры (заменяет filters.js) */}
        <div
          className="dropdown"
          onMouseEnter={handleMouseEnter}
          onMouseLeave={handleMouseLeave}
        >
          <button
            className="button"
            id="filters-btn"
            style={{
              borderRadius: isDropdownOpen ? "10px 10px 0 0" : "10px",
            }}
          >
            <i className="fa-solid fa-arrow-down-wide-short"></i>
            Filters
          </button>

          <span id="selected">{selectedFilter}</span>

          <div
            className="dropdown-content"
            style={{
              display: isDropdownOpen ? "flex" : "none",
            }}
          >
            {filterOptions.map((option) => (
              <a
                key={option}
                href="#"
                onClick={(e) => {
                  e.preventDefault();
                  handleFilterSelect(
                    option.toLocaleLowerCase().replace(" ", "_")
                  );
                }}
                className={selectedFilter === option ? "selected" : ""}
              >
                {option}
              </a>
            ))}
          </div>
        </div>
      </div>

      {/* Правая часть навигации */}
      <div className="right-part">
        {/* Иконки действий */}
        <button
          className="button icon-btn"
          onClick={() => console.log("Send функциональность в разработке")}
          title="Отправить"
        >
          <i className="fa-solid fa-paper-plane"></i>
        </button>

        <button
          className="button icon-btn"
          onClick={() => console.log("Email функциональность в разработке")}
          title="Электронная почта"
        >
          <i className="fa-solid fa-envelope"></i>
        </button>

        {/* Тут скорее всего сделать надо переход на другую страницу со всеми избранными */}
        <button
          className="button icon-btn"
          onClick={() => console.log("Starred функциональность в разработке")}
          title="Избранные вакансии"
        >
          <i className="fa-solid fa-bookmark"></i>
        </button>

        {/* Аватар профиля */}
        <button
          className="profile-btn"
          onClick={() => console.log("Профиль в разработке")}
          title="Профиль пользователя"
        >
          <img src={avatar} alt="Profile picture" id="profile-picture" />
        </button>
      </div>
    </section>
  );
};

export default Header;
