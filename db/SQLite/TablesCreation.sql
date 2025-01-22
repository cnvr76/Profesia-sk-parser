CREATE TABLE Companies (
  C_id INTEGER NOT NULL PRIMARY KEY,
  Name TEXT NOT NULL UNIQUE
);

CREATE TABLE Resumes (
  Res_id INTEGER NOT NULL PRIMARY KEY,
  Position TEXT NOT NULL,
  File TEXT NOT NULL UNIQUE,
  Language TEXT NOT NULL
);

CREATE TABLE Locations (
  L_id INTEGER NOT NULL PRIMARY KEY,
  City TEXT NOT NULL UNIQUE
);

CREATE TABLE Vacancies (
  V_id INTEGER NOT NULL PRIMARY KEY,
  Position TEXT NOT NULL,
  Link TEXT NOT NULL,
  Salary REAL NOT NULL,
  Description TEXT NOT NULL,
  Company INTEGER NOT NULL,
  Resume INTEGER,
  Location INTEGER NOT NULL,
  FOREIGN KEY (Company) REFERENCES Companies (C_id),
  FOREIGN KEY (Resume) REFERENCES Resumes (Res_id),
  FOREIGN KEY (Location) REFERENCES Locations (L_id)
);

CREATE TABLE Responses (
  Resp_id INTEGER NOT NULL PRIMARY KEY,
  isPositive INTEGER NOT NULL,
  EmailHR TEXT NOT NULL,
  V_id INTEGER NOT NULL,
  FOREIGN KEY (V_id) REFERENCES Vacancies (V_id)
);
