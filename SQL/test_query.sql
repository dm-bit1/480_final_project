insert ignore into Hospital.myTable (myName) values ('First');

insert ignore into Hospital.myTable (myName) values ('second');

INSERT IGNORE INTO Hospital.login (username, password, user_type) VALUES ('Admin', 'password', 'admin');

INSERT IGNORE INTO Hospital.login (username, password, user_type) VALUES ('Nurse1', 'password', 'nurse');
INSERT IGNORE INTO Hospital.login (username, password, user_type) VALUES ('Nurse2', 'password', 'nurse');
INSERT IGNORE INTO Hospital.login (username, password, user_type) VALUES ('Nurse3', 'password', 'nurse');

INSERT IGNORE INTO Hospital.login (username, password, user_type) VALUES ('Patient1', 'password', 'patient');
INSERT IGNORE INTO Hospital.login (username, password, user_type) VALUES ('Patient2', 'password', 'patient');
INSERT IGNORE INTO Hospital.login (username, password, user_type) VALUES ('Patient3', 'password', 'patient');

INSERT IGNORE INTO Hospital.nurse (EmployeeID, Fname, MI, Lname, Age, Gender, Phone, Address) VALUES (2, 'Bob', 'N', 'Roberts', 20, 'M', '3121112222', '123 Broadway St');

INSERT IGNORE INTO Hospital.nurse (EmployeeID, Fname, MI, Lname, Age, Gender, Phone, Address) VALUES (3, 'Jane', 'N', 'Grant', 30, 'F', '1234567891', '44 Virginia Ave');

INSERT IGNORE INTO Vaccine (VaccineID, Name, Company, DosesRequired, Description, Availability, OnHold) VALUES (1, 'VaxA', 'PharmaCo', 2, 'Description of VaxA', 100, 0);
INSERT IGNORE INTO Vaccine (VaccineID, Name, Company, DosesRequired, Description, Availability, OnHold) VALUES (2, 'VaxB', 'MediCorp', 1, 'Description of VaxB', 150, 10);
INSERT IGNORE INTO Vaccine (VaccineID, Name, Company, DosesRequired, Description, Availability, OnHold) VALUES (3, 'VaxC', 'HealthInc', 2, 'Description of VaxC', 200, 5);

INSERT IGNORE INTO TimeSlot (TimeSlotID, StartTime, EndTime, MaxPatients) VALUES (1, '2023-12-01 08:00:00', '2023-12-01 12:00:00', 30);
INSERT IGNORE INTO TimeSlot (TimeSlotID, StartTime, EndTime, MaxPatients) VALUES (2, '2023-12-01 13:00:00', '2023-12-01 17:00:00', 25);
INSERT IGNORE INTO TimeSlot (TimeSlotID, StartTime, EndTime, MaxPatients) VALUES (3, '2023-12-02 08:00:00', '2023-12-02 12:00:00', 20);

INSERT IGNORE INTO Hospital.Patient (SSN, Fname, MI, Lname, Age, Gender, Race, OccupationClass, MedicalHistory, Phone, Address, username) VALUES ('123-45-6789', 'David', 'E', 'Wilson', 50, 'M', 'Caucasian', 'Engineer', 'No history', '456-789-0123', '101 Elm St', 'Patient1');
INSERT IGNORE INTO Hospital.Patient (SSN, Fname, MI, Lname, Age, Gender, Race, OccupationClass, MedicalHistory, Phone, Address, username) VALUES ('987-65-4321', 'Emma', 'F', 'Brown', 28, 'F', 'Hispanic', 'Teacher', 'Allergic to penicillin', '567-890-1234', '202 Maple Ave', 'Patient2');
INSERT IGNORE INTO Hospital.Patient (SSN, Fname, MI, Lname, Age, Gender, Race, OccupationClass, MedicalHistory, Phone, Address, username) VALUES ('555-00-1111', 'Frank', 'G', 'Martinez', 36, 'M', 'Black', 'Artist', 'Diabetic', '678-901-2345', '303 Birch Rd', 'Patient3');

INSERT IGNORE INTO VaccinationScheduling (ScheduleID, SSN, VaccineID, TimeSlotID) VALUES (1, '123-45-6789', 1, 1);
INSERT IGNORE INTO VaccinationScheduling (ScheduleID, SSN, VaccineID, TimeSlotID) VALUES (2, '987-65-4321', 2, 2);
INSERT IGNORE INTO VaccinationScheduling (ScheduleID, SSN, VaccineID, TimeSlotID) VALUES (3, '555-00-1111', 3, 3);

INSERT IGNORE INTO Hospital.Nurse (EmployeeID, Fname, MI, Lname, Age, Gender, Phone, Address, username) VALUES (101, 'Alice', 'B', 'Smith', 30, 'F', '123-456-7890', '123 Main St', 'Nurse1');
INSERT IGNORE INTO Hospital.Nurse (EmployeeID, Fname, MI, Lname, Age, Gender, Phone, Address, username) VALUES (102, 'Bob', 'C', 'Johnson', 35, 'M', '234-567-8901', '456 Oak St', 'Nurse2');
INSERT IGNORE INTO Hospital.Nurse (EmployeeID, Fname, MI, Lname, Age, Gender, Phone, Address, username) VALUES (103, 'Carol', 'D', 'Davis', 40, 'F', '345-678-9012', '789 Pine St', 'Nurse3');



INSERT IGNORE INTO NurseScheduling (ScheduleID, EmployeeID, TimeSlotID) VALUES (1, 101, 1);
INSERT IGNORE INTO NurseScheduling (ScheduleID, EmployeeID, TimeSlotID) VALUES (2, 102, 2);
INSERT IGNORE INTO NurseScheduling (ScheduleID, EmployeeID, TimeSlotID) VALUES (3, 103, 3);


INSERT IGNORE INTO VaccineDelivery (DeliveryID, VaccineID, Quantity) VALUES (1, 1, 500);
INSERT IGNORE INTO VaccineDelivery (DeliveryID, VaccineID, Quantity) VALUES (2, 2, 300);
INSERT IGNORE INTO VaccineDelivery (DeliveryID, VaccineID, Quantity) VALUES (3, 3, 400);

INSERT IGNORE INTO VaccinationRecord (RecordID, SSN, EmployeeID, VaccineID, Dose, TimeSlotID) VALUES (1, '123-45-6789', 101, 1, 1, 1);
INSERT IGNORE INTO VaccinationRecord (RecordID, SSN, EmployeeID, VaccineID, Dose, TimeSlotID) VALUES (2, '987-65-4321', 102, 2, 1, 2);
INSERT IGNORE INTO VaccinationRecord (RecordID, SSN, EmployeeID, VaccineID, Dose, TimeSlotID) VALUES (3, '555-00-1111', 103, 3, 1, 3);


