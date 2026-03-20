CREATE DATABASE CletaEats_DB ;
USE CletaEats_DB;
CREATE TABLE usuario (
    id INT AUTO_INCREMENT PRIMARY KEY,
    correo VARCHAR(100) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    rol ENUM('cliente', 'repartidor', 'admin') NOT NULL
);

CREATE TABLE cliente (
    id INT AUTO_INCREMENT PRIMARY KEY,
    usuario_id INT NOT NULL,
    cedula VARCHAR(20) NOT NULL UNIQUE,
    nombre VARCHAR(100) NOT NULL,
    direccion TEXT NOT NULL,
    tarjeta VARCHAR(20) NOT NULL,
    telefono VARCHAR(20) NOT NULL,
    estado ENUM('activo', 'suspendido') DEFAULT 'activo',
    FOREIGN KEY (usuario_id) REFERENCES usuario(id)
);

CREATE TABLE restaurante (
    id INT AUTO_INCREMENT PRIMARY KEY,
    cedula_juridica VARCHAR(20) NOT NULL UNIQUE,
    nombre VARCHAR(100) NOT NULL,
    direccion TEXT NOT NULL,
    tipo_comida VARCHAR(50) NOT NULL
);

CREATE TABLE combo (
    id INT AUTO_INCREMENT PRIMARY KEY,
    restaurante_id INT NOT NULL,
    numero INT NOT NULL CHECK (numero BETWEEN 1 AND 9),
    nombre VARCHAR(100) NOT NULL,
    precio DECIMAL(10,2) NOT NULL,
    FOREIGN KEY (restaurante_id) REFERENCES restaurante(id)
);

CREATE TABLE repartidor (
    id INT AUTO_INCREMENT PRIMARY KEY,
    usuario_id INT NOT NULL,
    cedula VARCHAR(20) NOT NULL UNIQUE,
    nombre VARCHAR(100) NOT NULL,
    correo VARCHAR(100) NOT NULL,
    direccion TEXT NOT NULL,
    telefono VARCHAR(20) NOT NULL,
    tarjeta VARCHAR(20) NOT NULL,
    estado ENUM('disponible', 'ocupado') DEFAULT 'disponible',
    amonestaciones INT DEFAULT 0,
    km_diarios DECIMAL(10,2) DEFAULT 0,
    FOREIGN KEY (usuario_id) REFERENCES usuario(id)
);


SHOW TABLES;