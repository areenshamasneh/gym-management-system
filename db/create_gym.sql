CREATE TABLE Gym (
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(255) NOT NULL,
    type VARCHAR(100) NOT NULL,
    description TEXT,
    address_city VARCHAR(255) NOT NULL,
    address_street VARCHAR(255) NOT NULL
);