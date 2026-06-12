-- Crear tabla productos
CREATE TABLE IF NOT EXISTS productos (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    precio NUMERIC(10, 2) NOT NULL,
    stock INT NOT NULL
);

-- Insertar registros iniciales
INSERT INTO productos (nombre, precio, stock) VALUES 
('Laptop', 1200.50, 10),
('Mouse Óptico', 25.00, 50),
('Teclado Mecánico', 45.00, 30),
('Monitor 24"', 180.00, 15),
('Audífonos Gamer', 60.00, 25);