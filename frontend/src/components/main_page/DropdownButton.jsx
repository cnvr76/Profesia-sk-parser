import React, { useState, useEffect } from "react";

const DropdownButton = ({
  title,
  icon,
  options,
  selectedOption,
  onOptionChange,
}) => {
  const [isDropdownOpen, setIsDropdownOpen] = useState(false);

  const handleOptionSelect = (optionName) => {
    setIsDropdownOpen(false);

    if (onOptionChange && typeof onOptionChange == "function")
      onOptionChange(optionName);
  };

  const handleMouseEnter = () => {
    setIsDropdownOpen(true);
  };

  const handleMouseLeave = () => {
    setIsDropdownOpen(false);
  };

  return (
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
        <i className={`fa-solid ${icon}`}></i> {title}
      </button>

      <span id="selected">{selectedOption}</span>

      <div
        className="dropdown-content"
        style={{
          display: isDropdownOpen ? "flex" : "none",
        }}
      >
        {options.map((option) => (
          <a
            key={option}
            href="#"
            onClick={(e) => {
              e.preventDefault();
              handleOptionSelect(option);
            }}
            className={selectedOption === option ? "selected-in-dropdown" : ""}
          >
            {option}
          </a>
        ))}
      </div>
    </div>
  );
};

export default DropdownButton;
