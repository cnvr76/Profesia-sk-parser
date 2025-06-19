import React, { useState, useEffect } from "react";
import VacanciesContainer from "./VacanciesContainer";
import DetailsPanel from "./DetailsPanel";
import Header from "./Header";
import { api } from "../../services/api";

const Layout = () => {
  const [vacancies, setVacancies] = useState([]);
  const [selectedVacancyId, setSelectedVacancyId] = useState(null);
  const [currentFilter, setCurrentFilter] = useState("All");
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [retryAttempt, setRetryAttempt] = useState(0);
  const [isNewestFetching, setIsNewestFetching] = useState(false);

  useEffect(() => {
    const savedFilter = localStorage.getItem("selectedFilter");
    if (savedFilter && savedFilter !== currentFilter) {
      setCurrentFilter(savedFilter);
    }
  }, []);

  useEffect(() => {
    loadVacancies(getApiCurrentFilter());
  }, [currentFilter]);

  const getApiCurrentFilter = () => {
    const filter = currentFilter || "All";
    return filter.replace(" ", "_").toLocaleLowerCase();
  };

  const loadVacancies = async (filter, retryCount = 0, maxRetries = 3) => {
    setRetryAttempt(retryCount);

    if (retryCount === 0) {
      await new Promise((resolve) => setTimeout(resolve, 300));
    }

    setLoading(true);
    setError(null);

    try {
      const data = await api.getVacancies(filter);

      if (Array.isArray(data)) {
        setVacancies(data);
        setRetryAttempt(0);
        return;
      }

      if (data && typeof data === "object" && data.error) {
        if (retryCount < maxRetries && data.retry) {
          await new Promise((resolve) => setTimeout(resolve, 1000));
          return loadVacancies(retryCount + 1, maxRetries);
        } else {
          throw new Error(`Ошибка сервера: ${data.error}`);
        }
      }
    } catch (error) {
      // Сетевые ошибки
      if (
        retryCount < maxRetries &&
        (error.message.includes("Сервер не отвечает") ||
          error.message.includes("ERR_NETWORK") ||
          error.message.includes("timeout") ||
          error.message.includes("Timeout"))
      ) {
        await new Promise((resolve) => setTimeout(resolve, 2000));
        return loadVacancies(retryCount + 1, maxRetries);
      }

      setError(
        `${error.message} (attempt ${retryCount + 1}/${maxRetries + 1})`
      );
      setVacancies([]);
      setRetryAttempt(0);
    } finally {
      setLoading(false);
    }
  };

  // Обработчик клика по деталям вакансии
  const handleDetailsClick = (vacancyId) => {
    setSelectedVacancyId(vacancyId);
  };

  const selectedVacancy = vacancies.find((v) => v.V_id === selectedVacancyId);

  // Обработчик закрытия панели деталей
  const handleDetailsClose = () => {
    setSelectedVacancyId(null);
  };

  // Обработчик обновления вакансии (звездочка)
  const handleVacancyUpdate = (vacancyId, updates) => {
    setVacancies((prev) =>
      prev.map((vacancy) =>
        vacancy.V_id === vacancyId ? { ...vacancy, ...updates } : vacancy
      )
    );
  };

  // Обработчик удаления вакансии
  const handleVacancyDelete = (vacancyId) => {
    setVacancies((prev) =>
      prev.filter((vacancy) => vacancy.V_id !== vacancyId)
    );

    // Закрываем детали если была открыта удаленная вакансия
    if (selectedVacancyId === vacancyId) {
      setSelectedVacancyId(null);
    }
  };

  // Обработчик смены фильтра
  const handleFilterChange = (newFilter) => {
    setCurrentFilter(newFilter);
    setSelectedVacancyId(null); // Закрываем детали при смене фильтра
    setRetryAttempt(0);
  };

  // Обработчик ручного retry
  const handleRetry = () => {
    loadVacancies(getApiCurrentFilter(), 0);
  };

  const handleFetchingNewestVacancies = async () => {
    setIsNewestFetching(true);
    try {
      const result = await api.getNewestVacancies();
      if (result.success) {
        await loadVacancies(getApiCurrentFilter(), 0);
      }
    } catch (error) {
      console.error("Ошибка при парсинге новых вакансий:", error);
      setError(`Parsing error: ${error.message}`);
    } finally {
      setIsNewestFetching(false);
    }
  };

  return (
    <div className="App">
      {/* Фоновый паттерн */}
      <div className="pattern"></div>

      <div className="everything">
        {/* ========== БОКОВАЯ ПАНЕЛЬ ========== */}
        <section className="side-panel">
          {/* Панель деталей вакансии */}
          <DetailsPanel
            vacancyId={selectedVacancyId}
            vacancy={selectedVacancy}
            isVisible={!!selectedVacancyId}
            onClose={handleDetailsClose}
            onVacancyUpdate={handleVacancyUpdate}
          />

          {/* Zzzzz */}
          <div className="zzzz-container">
            <span className="z-letter" id="z1">
              Z
            </span>
            <span className="z-letter" id="z2">
              Z
            </span>
            <span className="z-letter" id="z3">
              Z
            </span>
            <span className="z-letter" id="z4">
              Z
            </span>
            <span className="z-letter" id="z5">
              Z
            </span>
          </div>
        </section>

        {/* ========== ОСНОВНАЯ ПАНЕЛЬ ========== */}
        <section className="main-panel">
          {/* Верхняя панель навигации */}
          <Header
            currentFilter={currentFilter}
            currentIconPage={null}
            onFilterChange={handleFilterChange}
            onNewestFetching={handleFetchingNewestVacancies}
            isNewestFetching={isNewestFetching}
          />

          {/* Контейнер с вакансиями - выделен в отдельный компонент */}
          <VacanciesContainer
            vacancies={vacancies}
            loading={loading}
            error={error}
            retryAttempt={retryAttempt}
            onRetry={handleRetry}
            onVacancyUpdate={handleVacancyUpdate}
            onVacancyDelete={handleVacancyDelete}
            onDetailsClick={handleDetailsClick}
          />
        </section>
      </div>
    </div>
  );
};

export default Layout;
