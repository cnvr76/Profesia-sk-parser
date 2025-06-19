import React from "react";
import VacancyCard from "./VacancyCard";
import sleepyCat from "../../static/images/sleepy_cat.png";

const VacanciesContainer = ({
  vacancies,
  loading,
  error,
  retryAttempt,
  onRetry,
  onVacancyUpdate,
  onVacancyDelete,
  onDetailsClick,
}) => {
  if (loading) {
    return (
      <section className="vacancies-container">
        <div className="loading-container">
          <i className="fa-solid fa-spinner fa-spin"></i>
          <p>
            {retryAttempt > 0
              ? `Retry ${retryAttempt + 1}/4...`
              : "Loading vacancies..."}
          </p>
        </div>
      </section>
    );
  }

  if (error) {
    return (
      <section className="vacancies-container">
        <div className="error-container">
          <p>Error: {error}</p>
          <button onClick={onRetry} className="retry-btn">
            Try again
          </button>
        </div>
      </section>
    );
  }

  if (vacancies.length === 0) {
    return (
      <section className="vacancies-container">
        <div className="nothing-found-container">
          <img src={sleepyCat} alt="Nothing found cat" id="nothing-found-img" />
          <span>Nothing found</span>
        </div>
      </section>
    );
  }

  return (
    <section className="vacancies-container">
      {/* Статистика */}
      <div className="vacancies-stats">
        <p>
          Vacancies: <strong>{vacancies.length}</strong>
        </p>
        <p>
          Starred:{" "}
          <strong>{vacancies.filter((v) => v.isStarred).length}</strong>
        </p>
        <p>
          Companies:{" "}
          <strong>
            {[...new Set(vacancies.map((v) => v.Company))].length}
          </strong>
        </p>
      </div>

      {/* Список вакансий */}
      {vacancies.map((vacancy) => (
        <VacancyCard
          key={vacancy.V_id}
          vacancy={vacancy}
          onDetailsClick={onDetailsClick}
          onVacancyUpdate={onVacancyUpdate}
          onVacancyDelete={onVacancyDelete}
        />
      ))}
    </section>
  );
};

export default VacanciesContainer;
