CREATE DATABASE IF NOT EXISTS cletaeats
  CHARACTER SET utf8mb4
  COLLATE utf8mb4_unicode_ci;

USE cletaeats;

CREATE TABLE Usuario (
    id          INT AUTO_INCREMENT PRIMARY KEY,
    cedula      VARCHAR(20)  NOT NULL UNIQUE,
    nombre      VARCHAR(100) NOT NULL,
    correo      VARCHAR(100) NOT NULL UNIQUE,
    contrasena  VARCHAR(255) NOT NULL,
    telefono    VARCHAR(20),
    rol         ENUM('ADMIN','CLIENTE','REPARTIDOR','ENCARGADO') NOT NULL,
    latitud     DECIMAL(10,7),
    longitud    DECIMAL(10,7)
);

CREATE TABLE Cliente (
    id_usuario      INT PRIMARY KEY,
    numero_tarjeta  VARCHAR(20),
    estado          ENUM('ACTIVO','SUSPENDIDO') NOT NULL DEFAULT 'ACTIVO',
    FOREIGN KEY (id_usuario) REFERENCES Usuario(id)
);

CREATE TABLE Repartidor (
    id_usuario       INT PRIMARY KEY,
    numero_tarjeta   VARCHAR(20),
    estado           ENUM('DISPONIBLE','OCUPADO','SUSPENDIDO') NOT NULL DEFAULT 'DISPONIBLE',
    kilometros_diarios DECIMAL(8,2) NOT NULL DEFAULT 0,
    FOREIGN KEY (id_usuario) REFERENCES Usuario(id)
);

CREATE TABLE Restaurante (
    id              INT AUTO_INCREMENT PRIMARY KEY,
    nombre          VARCHAR(100) NOT NULL,
    cedula_juridica VARCHAR(20)  NOT NULL UNIQUE,
    direccion       VARCHAR(255),
    tipo_comida     VARCHAR(100),
    latitud         DECIMAL(10,7),
    longitud        DECIMAL(10,7),
    imagen          VARCHAR(255),
    id_encargado    INT,
    FOREIGN KEY (id_encargado) REFERENCES Usuario(id)
);

CREATE TABLE EncargadoRestaurante (
    id_usuario      INT PRIMARY KEY,
    id_restaurante  INT,
    FOREIGN KEY (id_usuario)     REFERENCES Usuario(id),
    FOREIGN KEY (id_restaurante) REFERENCES Restaurante(id)
);

CREATE TABLE Combo (
    id              INT AUTO_INCREMENT PRIMARY KEY,
    id_restaurante  INT NOT NULL,
    nombre          VARCHAR(100) NOT NULL,
    descripcion     TEXT,
    numero          TINYINT NOT NULL CHECK (numero BETWEEN 1 AND 9),
    precio          DECIMAL(8,2) NOT NULL,
    imagen          VARCHAR(255),
    FOREIGN KEY (id_restaurante) REFERENCES Restaurante(id)
);

CREATE TABLE OpcionCombo (
    id        INT AUTO_INCREMENT PRIMARY KEY,
    id_combo  INT NOT NULL,
    nombre    VARCHAR(100) NOT NULL,
    tipo      ENUM('SELECCION_UNICA','MULTIPLE','BOOLEANO') NOT NULL,
    FOREIGN KEY (id_combo) REFERENCES Combo(id)
);

CREATE TABLE ValorOpcion (
    id               INT AUTO_INCREMENT PRIMARY KEY,
    id_opcion        INT NOT NULL,
    descripcion      VARCHAR(100) NOT NULL,
    costo_adicional  DECIMAL(8,2) NOT NULL DEFAULT 0,
    FOREIGN KEY (id_opcion) REFERENCES OpcionCombo(id)
);

CREATE TABLE Pedido (
    id                INT AUTO_INCREMENT PRIMARY KEY,
    id_cliente        INT NOT NULL,
    id_restaurante    INT NOT NULL,
    id_repartidor     INT,
    estado            ENUM('EN_PREPARACION','EN_CAMINO','ENTREGADO','CANCELADO') NOT NULL DEFAULT 'EN_PREPARACION',
    hora_creacion     DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    hora_entrega      DATETIME,
    latitud_destino   DECIMAL(10,7) NOT NULL,
    longitud_destino  DECIMAL(10,7) NOT NULL,
    distancia_km      DECIMAL(8,2)  NOT NULL,
    costo_envio       DECIMAL(8,2)  NOT NULL,
    FOREIGN KEY (id_cliente)     REFERENCES Cliente(id_usuario),
    FOREIGN KEY (id_restaurante) REFERENCES Restaurante(id),
    FOREIGN KEY (id_repartidor)  REFERENCES Repartidor(id_usuario)
);

CREATE TABLE DetallePedido (
    id          INT AUTO_INCREMENT PRIMARY KEY,
    id_pedido   INT NOT NULL,
    id_combo    INT NOT NULL,
    cantidad    INT NOT NULL DEFAULT 1,
    FOREIGN KEY (id_pedido) REFERENCES Pedido(id),
    FOREIGN KEY (id_combo)  REFERENCES Combo(id)
);

CREATE TABLE PreferenciaDetalle (
    id                INT AUTO_INCREMENT PRIMARY KEY,
    id_detalle_pedido INT NOT NULL,
    id_valor_opcion   INT NOT NULL,
    FOREIGN KEY (id_detalle_pedido) REFERENCES DetallePedido(id),
    FOREIGN KEY (id_valor_opcion)   REFERENCES ValorOpcion(id)
);

CREATE TABLE Calificacion (
    id            INT AUTO_INCREMENT PRIMARY KEY,
    id_pedido     INT NOT NULL,
    id_evaluador  INT NOT NULL,
    id_evaluado   INT NOT NULL,
    rol_evaluador ENUM('CLIENTE','REPARTIDOR') NOT NULL,
    tipo          ENUM('BUENO','REGULAR','MALO') NOT NULL,
    opinion       TEXT,
    fecha         DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    UNIQUE KEY uq_calificacion (id_pedido, id_evaluador),
    FOREIGN KEY (id_pedido)    REFERENCES Pedido(id),
    FOREIGN KEY (id_evaluador) REFERENCES Usuario(id),
    FOREIGN KEY (id_evaluado)  REFERENCES Usuario(id)
);


-- ============================================================
--  DATOS DE PRUEBA
-- ============================================================

INSERT INTO Usuario (cedula, nombre, correo, contrasena, telefono, rol, latitud, longitud) VALUES
-- Admin
('100000001', 'Admin Sistema',       'admin@cletaeats.com',       'hashed_password', '88880000', 'ADMIN',      9.9981,  -84.1167),
-- Encargados
('200000001', 'Mario Picado',        'mario@burguer.com',         'hashed_password', '88881111', 'ENCARGADO',  9.9990,  -84.1160),
('200000002', 'Luisa Mora',          'luisa@pizzaheredia.com',    'hashed_password', '88882222', 'ENCARGADO',  10.0010, -84.1180),
-- Clientes
('300000001', 'Ana González',        'ana@mail.com',              'hashed_password', '88883333', 'CLIENTE',    9.9975,  -84.1150),
('300000002', 'Carlos Jiménez',      'carlos@mail.com',           'hashed_password', '88884444', 'CLIENTE',    9.9965,  -84.1140),
('300000003', 'Sofía Ramírez',       'sofia@mail.com',            'hashed_password', '88885555', 'CLIENTE',    10.0020, -84.1200),
-- Repartidores
('400000001', 'Diego Vargas',        'diego@cletaeats.com',       'hashed_password', '88886666', 'REPARTIDOR', 9.9985,  -84.1165),
('400000002', 'Fernanda Ulate',      'fernanda@cletaeats.com',    'hashed_password', '88887777', 'REPARTIDOR', 10.0005, -84.1175),
('400000003', 'Roberto Chaves',      'roberto@cletaeats.com',     'hashed_password', '88888888', 'REPARTIDOR', 9.9960,  -84.1145);

INSERT INTO Cliente (id_usuario, numero_tarjeta, estado) VALUES
(4, '4111111111111111', 'ACTIVO'),
(5, '4222222222222222', 'ACTIVO'),
(6, '4333333333333333', 'ACTIVO');

INSERT INTO Repartidor (id_usuario, numero_tarjeta, estado, kilometros_diarios) VALUES
(7, '5111111111111111', 'DISPONIBLE', 12.5),
(8, '5222222222222222', 'DISPONIBLE',  8.0),
(9, '5333333333333333', 'OCUPADO',    15.3);

INSERT INTO Restaurante (nombre, cedula_juridica, direccion, tipo_comida, latitud, longitud, imagen, id_encargado) VALUES
('Burguer Tico',     '3-101-000001', 'Heredia Centro, 100m norte del parque', 'Hamburguesas', 9.9990, -84.1160, NULL, 2),
('Pizza Heredia',    '3-101-000002', 'Barrio Los Ángeles, Heredia',           'Pizza',        10.0010, -84.1180, NULL, 3);

INSERT INTO EncargadoRestaurante (id_usuario, id_restaurante) VALUES
(2, 1),
(3, 2);

-- Burguer Tico
INSERT INTO Combo (id_restaurante, nombre, descripcion, numero, precio, imagen) VALUES
(1, 'Classic Burger',      'Hamburguesa clásica con papas y refresco',        1, 4000.00, NULL),
(1, 'Double Smash',        'Doble carne, queso cheddar, papas y refresco',    2, 5000.00, NULL),
(1, 'Chicken Crispy',      'Pollo crujiente, ensalada, papas y refresco',     3, 6000.00, NULL),
-- Pizza Heredia
(2, 'Pizza Personal',      'Pizza personal de 6 pulgadas al gusto',           1, 4000.00, NULL),
(2, 'Pizza Mediana',       'Pizza mediana 10 pulgadas + refresco',            3, 6000.00, NULL),
(2, 'Combo Familiar',      'Pizza grande 14 pulgadas + 2 refrescos',          5, 8000.00, NULL);

-- Combo 1: Classic Burger
INSERT INTO OpcionCombo (id_combo, nombre, tipo) VALUES
(1, 'Salsa',            'SELECCION_UNICA'),
(1, 'Tamaño de refresco', 'SELECCION_UNICA'),
(1, 'Extras',           'MULTIPLE');

-- Combo 4: Pizza Personal
INSERT INTO OpcionCombo (id_combo, nombre, tipo) VALUES
(4, 'Masa',             'SELECCION_UNICA'),
(4, 'Salsa de soya',    'BOOLEANO'),
(4, 'Ingredientes extra', 'MULTIPLE');

-- Salsa (id_opcion=1)
INSERT INTO ValorOpcion (id_opcion, descripcion, costo_adicional) VALUES
(1, 'BBQ',         0),
(1, 'Ranch',       0),
(1, 'Mostaza',     0),
(1, 'Sin salsa',   0);

-- Tamaño de refresco (id_opcion=2)
INSERT INTO ValorOpcion (id_opcion, descripcion, costo_adicional) VALUES
(2, 'Regular',     0),
(2, 'Grande',    300),
(2, 'Extra grande', 600);

-- Extras burger (id_opcion=3)
INSERT INTO ValorOpcion (id_opcion, descripcion, costo_adicional) VALUES
(3, 'Doble carne', 800),
(3, 'Extra queso', 400),
(3, 'Aguacate',    500),
(3, 'Sin cebolla',   0);

-- Masa pizza (id_opcion=4)
INSERT INTO ValorOpcion (id_opcion, descripcion, costo_adicional) VALUES
(4, 'Delgada',     0),
(4, 'Gruesa',      0);

-- Salsa de soya (id_opcion=5) — BOOLEANO
INSERT INTO ValorOpcion (id_opcion, descripcion, costo_adicional) VALUES
(5, 'Incluir',     0),
(5, 'No incluir',  0);

-- Ingredientes extra pizza (id_opcion=6)
INSERT INTO ValorOpcion (id_opcion, descripcion, costo_adicional) VALUES
(6, 'Pepperoni extra', 500),
(6, 'Champiñones',     400),
(6, 'Jalapeños',       300);

-- Pedido 1: Ana → Burguer Tico, entregado por Diego
INSERT INTO Pedido (id_cliente, id_restaurante, id_repartidor, estado, hora_creacion, hora_entrega,
                    latitud_destino, longitud_destino, distancia_km, costo_envio) VALUES
(4, 1, 7, 'ENTREGADO', '2026-04-28 12:00:00', '2026-04-28 12:35:00',
 9.9975, -84.1150, 2.1, 400.00);  -- 10% de ₡4000

-- Pedido 2: Carlos → Pizza Heredia, en camino con Fernanda
INSERT INTO Pedido (id_cliente, id_restaurante, id_repartidor, estado, hora_creacion, hora_entrega,
                    latitud_destino, longitud_destino, distancia_km, costo_envio) VALUES
(5, 2, 8, 'EN_CAMINO', '2026-04-28 13:10:00', NULL,
 9.9965, -84.1140, 4.5, 1200.00); -- 20% de ₡6000

-- Pedido 3: Sofía → Burguer Tico, en preparación (sin repartidor aún)
INSERT INTO Pedido (id_cliente, id_restaurante, id_repartidor, estado, hora_creacion, hora_entrega,
                    latitud_destino, longitud_destino, distancia_km, costo_envio) VALUES
(6, 1, NULL, 'EN_PREPARACION', '2026-04-28 14:00:00', NULL,
 10.0020, -84.1200, 1.8, 600.00); -- 10% de ₡6000

INSERT INTO DetallePedido (id_pedido, id_combo, cantidad) VALUES
(1, 1, 1),   -- Pedido 1: 1x Classic Burger
(2, 5, 2),   -- Pedido 2: 2x Pizza Mediana
(3, 2, 1),   -- Pedido 3: 1x Double Smash
(3, 1, 2);   -- Pedido 3: 2x Classic Burger

INSERT INTO PreferenciaDetalle (id_detalle_pedido, id_valor_opcion) VALUES
(1, 1),   -- Pedido 1, Classic Burger → Salsa BBQ
(1, 5),   -- Pedido 1, Classic Burger → Refresco Regular
(1, 10),  -- Pedido 1, Classic Burger → Doble carne
(3, 2),   -- Pedido 3, Double Smash → Salsa Ranch
(3, 6);   -- Pedido 3, Double Smash → Refresco Grande

-- Cliente Ana califica a Diego
INSERT INTO Calificacion (id_pedido, id_evaluador, id_evaluado, rol_evaluador, tipo, opinion) VALUES
(1, 4, 7, 'CLIENTE', 'BUENO', 'Llegó rápido y amable');

-- Diego califica a Ana
INSERT INTO Calificacion (id_pedido, id_evaluador, id_evaluado, rol_evaluador, tipo, opinion) VALUES
(1, 7, 4, 'REPARTIDOR', 'BUENO', 'Dirección clara, fácil de encontrar');