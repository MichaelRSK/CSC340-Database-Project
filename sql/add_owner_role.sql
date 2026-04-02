USE store_db;

ALTER TABLE Users
MODIFY COLUMN role ENUM('owner', 'manager', 'employee') NOT NULL;
