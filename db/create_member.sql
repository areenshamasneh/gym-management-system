CREATE TABLE Member (
    id INT PRIMARY KEY AUTO_INCREMENT,
    gym_id INT NOT NULL,
    name VARCHAR(255) NOT NULL,
    birth_date DATE NOT NULL,
    phone_number VARCHAR(20),
    FOREIGN KEY (gym_id) REFERENCES Gym(id) ON DELETE CASCADE
);