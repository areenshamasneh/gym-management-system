CREATE TABLE Employee (
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(255) NOT NULL,
    gym_id INT NOT NULL,
    manager_id INT,
    address_city VARCHAR(255) NOT NULL,
    address_street VARCHAR(255) NOT NULL,
    phone_number VARCHAR(20),
    email VARCHAR(255) UNIQUE NOT NULL,
    positions SET('cleaner', 'trainer', 'system_worker', 'other') NOT NULL,
    FOREIGN KEY (gym_id) REFERENCES Gym(id) ON DELETE CASCADE,
    FOREIGN KEY (manager_id) REFERENCES Employee(id) ON DELETE SET NULL
);