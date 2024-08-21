USE bus;

CREATE TABLE student(
    AdmissionId INT PRIMARY KEY,
    Name VARCHAR(20),
    Email VARCHAR(255),
    Photo VARCHAR(50),
    Department VARCHAR(30),
    Pass VARCHAR(20)
);

CREATE TABLE admin(
    Email VARCHAR(255) PRIMARY KEY,
    Name VARCHAR(20),
    Pass VARCHAR(20)
);

CREATE TABLE pass(
    AdmissionId INT,
    FromPlace VARCHAR(20),
    Validity INT,
    UKey VARCHAR(20),
    FOREIGN KEY(AdmissionId) REFERENCES student(AdmissionId)
);