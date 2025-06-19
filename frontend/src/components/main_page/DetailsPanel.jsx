import React, { useState, useEffect } from "react";
import { api } from "../../services/api";
import DetailsSection from "./DetailsSection";

const DetailsPanel = ({
  vacancyId,
  vacancy,
  isVisible,
  onClose,
  onVacancyUpdate,
}) => {
  const [vacancyDetails, setVacancyDetails] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const [collapsedSections, setCollapsedSections] = useState({
    summary: true,
    knowledges: false,
    frameworks: false,
    salary: false,
  });

  // Загружаем детали при изменении vacancyId
  useEffect(() => {
    if (vacancyId && isVisible) {
      loadVacancyDetails();
    } else {
      setVacancyDetails(null);
    }
  }, [vacancyId, isVisible]);

  useEffect(() => {
    if (vacancyDetails && vacancy && vacancy.V_id == vacancyDetails.V_id) {
      if (vacancyDetails.isStarred !== vacancy.isStarred) {
        setVacancyDetails((prev) => ({
          ...prev,
          isStarred: vacancy.isStarred,
        }));
      }
    }
  }, [vacancy?.isStarred, vacancyDetails?.V_id]);

  // Функция загрузки деталей (заменяет details_ajax.js fetch)
  const loadVacancyDetails = async () => {
    setLoading(true);
    setError(null);

    try {
      const details = await api.getVacancyDetails(vacancyId);
      setVacancyDetails(details);
    } catch (error) {
      setError(error.message);
    } finally {
      setLoading(false);
    }
  };

  // Функция переключения секций (заменяет addToggleHandlers из details_ajax.js)
  const toggleSection = (sectionName) => {
    setCollapsedSections((prev) => ({
      ...prev,
      [sectionName]: !prev[sectionName],
    }));
  };

  // Обработчик звездочки в деталях
  const handleStarToggle = async () => {
    if (!vacancyDetails) return;

    try {
      const result = await api.toggleStar(vacancyDetails.V_id);

      if (result.success) {
        setVacancyDetails((prev) => ({
          ...prev,
          isStarred: result.isStarred,
        }));

        onVacancyUpdate(vacancyDetails.V_id, { isStarred: result.isStarred });
      }
    } catch (error) {
      console.error("Ошибка изменения звездочки в деталях:", error);
    }
  };

  // Если не видна - не рендерим
  if (!isVisible) return null;

  return (
    <div className="details-panel shown">
      {loading && (
        <div className="details-loading">
          <i class="fa-solid fa-spinner fa-spin-pulse"></i>
          <p>Загружаем детали...</p>
        </div>
      )}

      {error && (
        <div className="details-error">
          <p>❌ Ошибка: {error}</p>
          <button onClick={loadVacancyDetails} className="retry-btn">
            🔄 Попробовать снова
          </button>
        </div>
      )}
      {console.log(vacancyDetails)}
      {vacancyDetails && (
        <>
          {/* Заголовок деталей */}
          <div
            style={{
              width: "100%",
              display: "flex",
              flexDirection: "column",
              gap: "15px",
            }}
          >
            <h1 className="details-card-position">{vacancyDetails.Position}</h1>
            <h3 className="details-card-location">{vacancyDetails.Location}</h3>

            <div className="additional-info">
              {vacancyDetails.hasExpired && <h5 id="hasExpired">Expired</h5>}
              {vacancyDetails.haveApplied && <h5 id="haveApplied">Applied</h5>}
            </div>
          </div>

          {/* Секции деталей */}
          <DetailsSection
            title="Summary"
            icon="fa-gear"
            sectionKey="summary"
            isCollapsed={collapsedSections.summary}
            toggleSection={toggleSection}
          >
            <b>
              <span style={{ color: "white", fontSize: "1.1rem" }}>
                {vacancyDetails.Company}
              </span>
            </b>
            <br />
            {vacancyDetails.Summary || "No data found"}
          </DetailsSection>

          <DetailsSection
            title="Knowledges"
            icon="fa-gear"
            sectionKey="knowledges"
            isCollapsed={collapsedSections.knowledges}
            toggleSection={toggleSection}
          >
            {vacancyDetails.Knowledges?.length > 0
              ? vacancyDetails.Knowledges.map((knowledge, index) => (
                  <p key={index}>{knowledge.Field}</p>
                ))
              : "No data found"}
          </DetailsSection>

          <DetailsSection
            title="Frameworks"
            icon="fa-gear"
            sectionKey="frameworks"
            isCollapsed={collapsedSections.frameworks}
            toggleSection={toggleSection}
          >
            {vacancyDetails.Frameworks?.length > 0
              ? vacancyDetails.Frameworks.map((framework, index) => (
                  <p key={index}>{framework.Name}</p>
                ))
              : "No data found"}
          </DetailsSection>

          <DetailsSection
            title="Salary"
            icon="fa-gear"
            sectionKey="salary"
            isCollapsed={collapsedSections.salary}
            toggleSection={toggleSection}
          >
            <p>
              {vacancyDetails.Salary > 100
                ? `${vacancyDetails.Salary}EUR/mesiac`
                : `${vacancyDetails.Salary}EUR/hod`}
            </p>
          </DetailsSection>

          {/* Кнопки управления */}
          <div className="side-btn-container">
            <i
              className="fa-solid fa-xmark"
              onClick={onClose}
              title="Закрыть"
            ></i>

            <a
              href={vacancyDetails.Link}
              className="button apply-btn"
              target="_blank"
              rel="noopener noreferrer"
            >
              Apply
            </a>

            <i
              className={`fa-${
                vacancyDetails.isStarred ? "solid" : "regular"
              } fa-star star-icon`}
              onClick={handleStarToggle}
              style={{
                cursor: "pointer",
                color: vacancyDetails.isStarred ? "#ffe863" : "white",
              }}
              title={
                vacancyDetails.isStarred
                  ? "Убрать из избранного"
                  : "Добавить в избранное"
              }
            />
          </div>
        </>
      )}
    </div>
  );
};

export default DetailsPanel;
