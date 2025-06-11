# Job Application Management System (In Development)

### Current Version (Prototype)

* **Main Page (for now):**
    ![image](https://github.com/user-attachments/assets/77a12d99-cbf8-4e9a-989c-77fba1a7e779)

* **Main Page with Vacancy Details:**
    ![image](https://github.com/user-attachments/assets/34fb2d31-f8d5-4923-90c7-86c92a16f56f)

## Project Overview

This project is a personal web application designed to **automate and streamline the job search process**. Its primary goal is to provide a convenient tool for tracking job vacancies, managing interactions with employers, and simplifying resume submissions.

### Current Status & Development

The project is in an **active development phase**. The screenshots provided illustrate an early iteration of the application, showcasing basic concepts and a portion of the planned functionality. Currently, the application is **actively being rewritten using React.js** to create a more modern, scalable, and intuitive user interface. This process also serves as a practical learning experience for me to deepen my understanding of React.js.

## Current Functionality (What's Already Implemented)

* **Loading Newest Vacancies:** Loads the most recent job vacancies from Gmail (if available).
* **Basic Information Display:** Vacancies are displayed as interactive cards, showing essential details.
* **Detailed Vacancy Analysis:** After clicking a "Details" button, if information doesn't exist in database, the application scrapes and parses the full vacancy description via its link and uses the **Gemini API for summarization** of the job requirements, knowledges etc.
* **Vacancy Management:** Users can star (save basically) and delete vacancies from their view.
* **Basic Filter Options:** Implemented basic filtering capabilities to narrow down job listings.
* **Database Integration:** Functionality for writing and updating vacancy data within a **SQL Server database**.

## Planned Functionality (Development Goals)

These features will be implemented as the project evolves, particularly after the transition to React.js:

* **Intelligent Job Vacancy Parsing:** Automatic loading of newest job vacancies data from Gmail emails sent by popular job search websites (e.g., Profesia.sk and some more).
* **Automated Resume Submission:** Functionality for simplified or fully automated submission of resumes to suitable job vacancies, minimizing manual input.
* **Employer Response Tracking:** A system for monitoring application statuses and categorizing responses from potential employers (e.g., "Under Review," "Interview Invitation," "Rejected").
* **Gamification of the Process:** Integration of gaming elements (e.g., progress bars, achievements, challenges) to increase motivation and engagement throughout the job search process.
* **Integration of Tinder-like Job Searcing:** Posibility for users to apply fast on newest vacancies using Tinder-like swipe functionality.
* **Modern User Interface:** Development of a modern, responsive, and intuitive interface using React.js to ensure the best user experience.

## Technologies Used (Current Version)

* **Frontend:** Vanilla HTML/CSS/JS (now switching to React)
* **Backend:** Python/Flask
* **Database:** MS SQL Server
* **API's:** Gmail (simplegmail), Gemini (google.generativeai)

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.
