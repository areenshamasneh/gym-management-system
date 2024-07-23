CREATE TABLE HallType (
    id INT PRIMARY KEY AUTO_INCREMENT,
    type_description VARCHAR(255),
    type ENUM('sauna', 'training', 'yoga', 'swimming') NOT NULL
);