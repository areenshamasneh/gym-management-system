CREATE TABLE HallMachine (
    hall_id INT NOT NULL,
    machine_id VARCHAR(100) NOT NULL,
    name VARCHAR(255),
    uid VARCHAR(100) NOT NULL,
    PRIMARY KEY (hall_id, machine_id),
    FOREIGN KEY (hall_id) REFERENCES Hall(id) ON DELETE CASCADE,
    FOREIGN KEY (machine_id) REFERENCES Machine(serial_number) ON DELETE CASCADE
);
