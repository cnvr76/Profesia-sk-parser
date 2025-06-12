import React, { useEffect, useState } from "react";
import { api } from "../services/api";

const VacancyCard = ({
  vacancy,
  onDetailsClick,
  onVacancyUpdate,
  onVacancyDelete,
}) => {
  const [isDeleting, setIsDeleting] = useState(false);
  const [isStarring, setIsStarring] = useState(false);
  const [isStarred, setIsStarred] = useState(vacancy.isStarred);

  useEffect(() => {
    setIsStarred(vacancy.isStarred);
  }, [vacancy.isStarred]);

  const handleDelete = async () => {
    if (isDeleting) return;

    if (!window.confirm(`Удалить вакансию "${vacancy.Position}"?`)) {
      return;
    }

    setIsDeleting(true);

    try {
      await api.deleteVacancy(vacancy.V_id);

      onVacancyDelete?.(vacancy.V_id);
    } catch (error) {
      alert("Ошибка удаления вакансии: " + error.message);
    } finally {
      setIsDeleting(false);
    }
  };

  const handleStarToggle = async () => {
    if (isStarring) return;

    setIsStarring(true);

    try {
      const result = await api.toggleStar(vacancy.V_id);

      if (result.success) {
        setIsStarred(result.isStarred);
        onVacancyUpdate?.(vacancy.V_id, { isStarred: result.isStarred });
      }
    } catch (error) {
      console.error("Ошибка изменения звездочки:", error);
      alert("Ошибка изменения статуса избранного");
    } finally {
      setIsStarring(false);
    }
  };

  const handleDetailsClick = (e) => {
    e.preventDefault();
    onDetailsClick?.(vacancy.V_id);
  };

  const formatDate = (dateString) => {
    try {
      if (!dateString) return "No date";
      const date = new Date(dateString);
      return date.toLocaleDateString("sk-SK");
    } catch (error) {
      console.error("Ошибка форматирования даты:", error);
      return dateString || "Invalid date";
    }
  };

  return (
    <div className="card">
      <div className="info-text">
        <h1 className="position-title">{vacancy.Position}</h1>
        <h3 className="company-name">{vacancy.Company}</h3>
        <h3 className="location-name">
          {vacancy.Location} - ({formatDate(vacancy.Date)})
        </h3>
      </div>

      <div className="clickables">
        <div className="icons">
          {/* Иконка удаления */}
          <i
            className={`fa-solid fa-xmark ${isDeleting ? "deleting" : ""}`}
            onClick={handleDelete}
            style={{
              cursor: isDeleting ? "wait" : "pointer",
              opacity: isDeleting ? 0.5 : 1,
            }}
            title="Удалить вакансию"
          />

          {/* Иконка звездочки */}
          <i
            className={`fa-${isStarred ? "solid" : "regular"} fa-star ${
              isStarring ? "starring" : ""
            }`}
            onClick={handleStarToggle}
            style={{
              cursor: isStarring ? "wait" : "pointer",
              opacity: isStarring ? 0.5 : 1,
              color: isStarred ? "#FFD700" : "inherit",
            }}
            title={isStarred ? "Убрать из избранного" : "Добавить в избранное"}
          />
        </div>

        <div className="card-buttons">
          {/* Кнопка деталей */}
          <a
            href="#"
            className="button details-btn"
            onClick={handleDetailsClick}
          >
            Details
          </a>

          {/* Кнопка применить */}
          <a
            href={vacancy.Link}
            className="button apply-btn"
            target="_blank"
            rel="noopener noreferrer"
          >
            Apply
          </a>
        </div>
      </div>
    </div>
  );
};

export default VacancyCard;
