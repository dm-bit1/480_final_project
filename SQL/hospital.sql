create schema if not exists Hospital;

create table if not exists Hospital.Login (
    username VARCHAR(255) primary key,
    password VARCHAR(255),
    user_type ENUM('admin', 'nurse', 'patient')
);

create table if not exists Hospital.myTable (
	myName varchar(20) 
);

CREATE TABLE IF NOT EXISTS Vaccine (
    VaccineID INT PRIMARY KEY,
    Name VARCHAR(255),
    Company VARCHAR(255),
    DosesRequired INT,
    Description TEXT,
    Availability INT,
    OnHold INT
);

CREATE TABLE IF NOT EXISTS Nurse (
    EmployeeID INT PRIMARY KEY,
    Fname VARCHAR(255),
    MI CHAR(1),
    Lname VARCHAR(255),
    Age INT,
    Gender CHAR(1),
    Phone VARCHAR(15),
    Address VARCHAR(255),
    username VARCHAR(255),
    FOREIGN KEY (username) REFERENCES login(username)
);


CREATE TABLE IF NOT EXISTS TimeSlot (
    TimeSlotID INT PRIMARY KEY,
    StartTime DATETIME,
    EndTime DATETIME,
    MaxPatients INT
);

CREATE TABLE IF NOT EXISTS Patient (
    SSN VARCHAR(11) PRIMARY KEY,
    Fname VARCHAR(255),
    MI CHAR(1),
    Lname VARCHAR(255),
    Age INT,
    Gender CHAR(1),
    Race VARCHAR(255),
    OccupationClass VARCHAR(255),
    MedicalHistory TEXT,
    Phone VARCHAR(15),
    Address VARCHAR(255),
    username VARCHAR(255),  -- Match the type and size with the login table
    FOREIGN KEY (username) REFERENCES login(username)
);


CREATE TABLE IF NOT EXISTS VaccineDelivery (
    DeliveryID INT PRIMARY KEY,
    VaccineID INT,
    Quantity INT,
    FOREIGN KEY (VaccineID) REFERENCES Vaccine(VaccineID)
);

CREATE TABLE IF NOT EXISTS NurseScheduling (
    ScheduleID INT PRIMARY KEY,
    EmployeeID INT,
    TimeSlotID INT,
    FOREIGN KEY (EmployeeID) REFERENCES Nurse(EmployeeID),
    FOREIGN KEY (TimeSlotID) REFERENCES TimeSlot(TimeSlotID)
);

CREATE TABLE IF NOT EXISTS VaccinationScheduling (
    ScheduleID INT PRIMARY KEY,
    SSN VARCHAR(255),
    VaccineID INT,
    TimeSlotID INT,
    FOREIGN KEY (SSN) REFERENCES Patient(SSN),
    FOREIGN KEY (VaccineID) REFERENCES Vaccine(VaccineID),
    FOREIGN KEY (TimeSlotID) REFERENCES TimeSlot(TimeSlotID)
);

CREATE TABLE IF NOT EXISTS VaccinationRecord (
    RecordID INT PRIMARY KEY,
    SSN VARCHAR(255),
    EmployeeID INT,
    VaccineID INT,
    Dose INT,
    TimeSlotID INT,
    FOREIGN KEY (SSN) REFERENCES Patient(SSN),
    FOREIGN KEY (EmployeeID) REFERENCES Nurse(EmployeeID),
    FOREIGN KEY (VaccineID) REFERENCES Vaccine(VaccineID),
    FOREIGN KEY (TimeSlotID) REFERENCES TimeSlot(TimeSlotID)
);







