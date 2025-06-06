CREATE PROCEDURE GetVacancyDetails(@v_id INT)
AS
BEGIN
    -- �������� ����������
    SELECT 
        v.V_id, v.Position, v.Link, 
        c.Name as 'Company', l.City as 'Location',
        v.Salary, v.haveApplied, v.hasExpired, s.S_id as 'isStarred'
    FROM Vacancies v
    JOIN Companies c ON c.C_id = v.Company
    JOIN Locations l ON l.L_id = v.Location
    LEFT JOIN Starred s ON v.V_id = s.V_id
    WHERE v.V_id = @v_id;
    
    -- ������
    SELECT Field, Description FROM Knowledges WHERE V_id = @v_id;
    
    -- ����������
    SELECT Name FROM Frameworks WHERE V_id = @v_id;
END