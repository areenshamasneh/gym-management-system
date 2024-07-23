CREATE TABLE Machine (
    serial_number VARCHAR(100) PRIMARY KEY,
    type VARCHAR(100) NOT NULL,
    model VARCHAR(100),
    brand VARCHAR(100),
    status ENUM('operational', 'broken') NOT NULL,
    maintenance_date DATE
);