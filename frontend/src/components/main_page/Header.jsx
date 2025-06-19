import React, { useState } from "react";
import avatar from "../../static/images/avatar.jpg";
import { useNavigate } from "react-router-dom";
import DropdownButton from "./DropdownButton";

const Header = ({
  currentFilter,
  currentIconPage,
  onFilterChange,
  onNewestFetching,
  isNewestFetching,
}) => {
  const [selectedIcon, setSelectedIcon] = useState(null || currentIconPage);

  const navigator = useNavigate();

  const filterOptions = [
    "All",
    "Fetched",
    "Problematic",
    "Expired",
    "Most recent",
  ];

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
        <DropdownButton
          title={"Filters"}
          icon={"fa-filter"}
          options={filterOptions}
          selectedOption={currentFilter}
          onOptionChange={onFilterChange}
        />
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
          onClick={() => navigator("/starred")}
          title="Избранные вакансии"
        >
          <i
            className="fa-solid fa-star"
            style={{ color: "white", fontSize: "1rem" }}
          ></i>
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
