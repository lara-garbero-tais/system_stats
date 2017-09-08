--Database, table and user creation script

CREATE DATABASE IF NOT EXISTS ltais;

USE ltais;

CREATE TABLE IF NOT EXISTS client_stats (
	date TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    ip VARCHAR(255),
    cpu DECIMAL(33,30),
    memory DECIMAL(33,30),
    uptime DECIMAL(40,30)
);

CREATE USER IF NOT EXISTS ltais@localhost IDENTIFIED BY 'password';
GRANT ALL PRIVILEGES ON ltais.* TO ltais@localhost;
FLUSH PRIVILEGES;
