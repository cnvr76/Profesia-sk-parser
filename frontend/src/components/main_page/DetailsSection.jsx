import React from "react";

const DetailsSection = ({
  title,
  icon,
  children,
  sectionKey,
  isCollapsed,
  toggleSection,
}) => {
  return (
    <div className={`details-card ${isCollapsed ? "collapsed" : ""}`}>
      <div
        className="details-card-name"
        onClick={() => toggleSection(sectionKey)}
        style={{ cursor: "pointer" }}
      >
        <h3>
          <i className={`fa-solid ${icon}`}></i>
          {title}
        </h3>
        <i
          className={`fa-solid fa-chevron-down unfold-arrow-icon ${
            isCollapsed ? "rotated" : ""
          }`}
        ></i>
      </div>

      <div
        className="details-card-info"
        style={{
          gridTemplateRows: isCollapsed ? "0fr" : "1fr",
          overflow: "hidden",
        }}
      >
        <span style={{ display: "flex", flexDirection: "column", gap: "7px" }}>
          {children}
        </span>
      </div>
    </div>
  );
};

export default DetailsSection;
