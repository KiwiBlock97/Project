USE bus;

CREATE TABLE student (
    AdminNo INT PRIMARY KEY,
    Name VARCHAR(20),
    Photo VARCHAR(50),
    Department VARCHAR(30),
    Pass VARCHAR(20)
);

CREATE TABLE admin (
    Name VARCHAR(20) PRIMARY KEY,
    Pass VARCHAR(20)
);

CREATE TABLE pass (
    PassID INT AUTO_INCREMENT PRIMARY KEY,
    AdminNo INT,
    FromPlace VARCHAR(20),
    Validity INT,
    UKey varchar(20),
    FOREIGN KEY (AdminNo) REFERENCES student(AdminNo)
);
