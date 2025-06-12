import axios from "axios";

const API_BASE = "http://localhost:5000";

const apiClient = axios.create({
  baseURL: API_BASE,
  timeout: 10000,
  headers: {
    Accept: "application/json",
    "Content-Type": "application/json",
  },
});

const longApiClient = axios.create({
  baseURL: API_BASE,
  timeout: 60000,
  headers: {
    Accept: "application/json",
    "Content-Type": "application/json",
  },
});

// AJAX calls
export const api = {
  // Получить все вакансии (заменяет загрузку главной страницы)
  getVacancies: async (filter = "all") => {
    try {
      const response = await apiClient.get(`/bar/filters/${filter}`);
      return response.data;
    } catch (error) {
      console.error("Error loading vacancies:", error);
      throw error;
    }
  },

  // Получить детали вакансии (заменяет details_ajax.js)
  getVacancyDetails: async (vacancyId) => {
    try {
      const response = await apiClient.get(`/vacancies/${vacancyId}/details`);
      return response.data;
    } catch (error) {
      console.error(
        `Error fetching details for this V_is = ${vacancyId}:`,
        error
      );
      throw error;
    }
  },

  getNewestVacancies: async () => {
    try {
      const response = await longApiClient.get("/bar/newest");
      console.log(response);
      if (response.data.executed) {
        return {
          success: true,
        };
      } else {
        throw new Error("Loading newest vacancies wasn't processed");
      }
    } catch (error) {
      console.error("Error with newest vacancies: ", error);
      throw error;
    }
  },

  // Переключить звездочку (заменяет icon_funcs_ajax.js)
  toggleStar: async (vacancyId) => {
    try {
      const response = await apiClient.post(`/vacancies/${vacancyId}/star`);

      if (response.data.executed) {
        return {
          success: true,
          isStarred: response.data.starred,
          vacancyId: vacancyId,
        };
      } else {
        throw new Error("Starring operation wasn't processed");
      }
    } catch (error) {
      console.error(`Error in starring ${vacancyId}:`, error);
      throw error;
    }
  },

  // Удалить вакансию (заменяет icon_funcs_ajax.js)
  deleteVacancy: async (vacancyId) => {
    try {
      const response = await apiClient.delete(`/vacancies/${vacancyId}/delete`);

      if (response.data.hasExecuted && response.data.isDeleted) {
        console.log(`Vacancy V_id = ${vacancyId} deleted successfully`);
        return {
          success: true,
          vacancyId: vacancyId,
        };
      } else {
        throw new Error(response.data.error || "Couldn't delete vacancy");
      }
    } catch (error) {
      console.error(`Error while deleting vacancy V_id = ${vacancyId}:`, error);
      throw error;
    }
  },

  // Получить вакансии по фильтру (заменяет filters.js логику)
  getVacanciesByFilter: async (filterName) => {
    try {
      const response = await apiClient.get(`/bar/filters/${filterName}`);
      return response.data;
    } catch (error) {
      console.error(`Error loading data using filter ${filterName}:`, error);
      throw error;
    }
  },
};

export const {
  getVacancies,
  getVacancyDetails,
  toggleStar,
  deleteVacancy,
  getVacanciesByFilter,
} = api;

export default api;
