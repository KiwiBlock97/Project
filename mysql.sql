USE bus;

CREATE TABLE student(
    AdmissionId INT PRIMARY KEY,
    Name VARCHAR(20),
    Email VARCHAR(255),
    Photo VARCHAR(50),
    Department VARCHAR(30),
    Password VARCHAR(20)
);

CREATE TABLE admin(
    Email VARCHAR(255) PRIMARY KEY,
    Name VARCHAR(20),
    Password VARCHAR(20)
);

CREATE TABLE pass(
    AdmissionId INT,
    FromPlace VARCHAR(20),
    Validity INT,
    UKey VARCHAR(255),
    FOREIGN KEY(AdmissionId) REFERENCES student(AdmissionId)
);

CREATE TABLE place(
    Place VARCHAR(30) PRIMARY KEY,
    Price int UNSIGNED
);

SET GLOBAL event_scheduler = ON;

DELIMITER //

CREATE EVENT IF NOT EXISTS auto_remove_expired_records
ON SCHEDULE EVERY 1 MINUTE
DO
BEGIN
  DELETE FROM pass
  WHERE Validity <= UNIX_TIMESTAMP();

  DELETE FROM pass_order
  WHERE Time + 3600 <= UNIX_TIMESTAMP() AND Status IS NULL;
END;
//


-- SET GLOBAL event_scheduler = OFF; 
-- ALTER EVENT auto_remove_expired_records DISABLE;  -- Temporarily disable
-- DROP EVENT auto_remove_expired_records;           -- Permanently remove