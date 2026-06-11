-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Servidor: 127.0.0.1
-- Tiempo de generación: 04-12-2025 a las 12:24:12
-- Versión del servidor: 10.4.32-MariaDB
-- Versión de PHP: 8.1.25

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Base de datos: `busca_huellas_db`
--

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `alerta`
--

CREATE TABLE `alerta` (
  `id_alerta` int(11) NOT NULL,
  `id_avistamiento` int(11) DEFAULT NULL,
  `id_mascota` int(11) DEFAULT NULL,
  `fecha_alerta` datetime DEFAULT NULL,
  `confirmacion` enum('si','no') DEFAULT NULL,
  `mensaje` text DEFAULT NULL,
  `estado_alerta` enum('pendiente','enviada','vista') DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `alerta`
--

INSERT INTO `alerta` (`id_alerta`, `id_avistamiento`, `id_mascota`, `fecha_alerta`, `confirmacion`, `mensaje`, `estado_alerta`) VALUES
(1, 1, 1, '2025-11-10 10:00:00', 'si', 'Se ha detectado una posible coincidencia con Firulais.', 'enviada'),
(2, 2, 2, '2025-12-01 19:00:00', 'no', 'Avistamiento sin alta similitud, revisar imagen.', 'pendiente'),
(3, 3, 2, '2025-01-05 08:00:00', 'si', 'Coincidencia moderada con Max.', 'vista'),
(4, 4, 4, '2025-02-14 15:00:00', 'si', 'Alerta: posible match con Tommy.', 'enviada'),
(5, 5, 6, '2025-03-02 21:00:00', 'no', 'Imagen poco clara, confirmar si es Nala.', 'pendiente'),
(6, 6, 7, '2025-03-15 12:00:00', 'si', 'Coincidencia aceptable con Bruno.', 'enviada'),
(7, 7, NULL, '2025-04-01 17:00:00', 'no', 'Avistamiento sin mascota asignada.', 'pendiente'),
(8, 8, 9, '2025-04-10 09:00:00', 'si', 'Alerta enviada por posible Simba.', 'enviada'),
(9, 9, 3, '2025-04-12 20:00:00', 'si', 'Coincidencia alta con Luna.', 'vista'),
(10, 10, NULL, '2025-04-15 13:00:00', 'no', 'No hay mascota asignada en el avistamiento.', 'pendiente'),
(11, 11, 11, '2025-04-20 10:00:00', 'si', 'Toby podría ser el reportado.', 'enviada'),
(12, 12, NULL, '2025-04-21 08:00:00', 'no', 'Revisar imagen, baja similitud.', 'pendiente'),
(13, 13, 12, '2025-04-22 19:00:00', 'si', 'Coincidencia con Kira, confirmar dueño.', 'enviada'),
(14, 14, NULL, '2025-04-23 11:00:00', 'no', 'Alerta generada sin posible mascota.', 'pendiente'),
(15, 15, 15, '2025-04-24 22:00:00', 'si', 'Thor coincide parcialmente.', 'enviada'),
(16, 16, NULL, '2025-04-25 07:00:00', 'no', 'Avistamiento sin asignación.', 'pendiente'),
(17, 17, 17, '2025-04-26 14:00:00', 'si', 'Lola parece encontrada.', 'vista'),
(18, 18, 18, '2025-04-27 16:00:00', 'si', 'Rex coincide en gran medida.', 'enviada'),
(19, 19, NULL, '2025-04-28 18:00:00', 'no', 'Imagen borrosa, no se identifica mascota.', 'pendiente'),
(20, 20, 20, '2025-04-29 21:00:00', 'si', 'Apolo podría corresponder al avistamiento.', 'enviada');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `avistamiento`
--

CREATE TABLE `avistamiento` (
  `id_avistamiento` int(11) NOT NULL,
  `id_usuario` int(11) DEFAULT NULL,
  `id_mascota` int(11) DEFAULT NULL,
  `foto_avistamiento` varchar(255) DEFAULT NULL,
  `ubicación` varchar(150) DEFAULT NULL,
  `fecha` datetime DEFAULT NULL,
  `porcentaje_similitud` decimal(5,2) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `avistamiento`
--

INSERT INTO `avistamiento` (`id_avistamiento`, `id_usuario`, `id_mascota`, `foto_avistamiento`, `ubicación`, `fecha`, `porcentaje_similitud`) VALUES
(1, 5, 1, 'https://cdn.example.com/avistamientos/1.jpg', 'Parque Central, Suba', '2024-11-10 09:23:00', 78.50),
(2, 8, NULL, 'https://cdn.example.com/avistamientos/2.jpg', 'Calle 70, Chapinero', '2024-12-01 18:10:00', 45.00),
(3, 3, 2, 'https://cdn.example.com/avistamientos/3.jpg', 'Plaza Mayor, Centro', '2025-01-05 07:40:00', 66.20),
(4, 11, 4, 'https://cdn.example.com/avistamientos/4.jpg', 'Centro Comercial Laureles', '2025-02-14 14:12:00', 88.10),
(5, 6, NULL, 'https://cdn.example.com/avistamientos/5.jpg', 'Avenida 3N, Cali', '2025-03-02 20:00:00', 32.75),
(6, 13, 7, 'https://cdn.example.com/avistamientos/6.jpg', 'Parque de la 80, Medellín', '2025-03-15 11:37:00', 71.00),
(7, 2, NULL, 'https://cdn.example.com/avistamientos/7.jpg', 'Río Cali, Paseo', '2025-04-01 16:05:00', 50.00),
(8, 19, 9, 'https://cdn.example.com/avistamientos/8.jpg', 'Sector Norte, Barranquilla', '2025-04-10 08:20:00', 82.60),
(9, 7, 3, 'https://cdn.example.com/avistamientos/9.jpg', 'Parque de la 93, Bogotá', '2025-04-12 19:50:00', 90.00),
(10, 4, NULL, 'https://cdn.example.com/avistamientos/10.jpg', 'Centro Histórico, Cartagena', '2025-04-15 12:00:00', 27.30),
(11, 15, 11, 'https://cdn.example.com/avistamientos/11.jpg', 'Parque del Café, Pereira', '2025-04-20 09:09:00', 73.40),
(12, 10, NULL, 'https://cdn.example.com/avistamientos/12.jpg', 'Circunvalar, Pereira', '2025-04-21 07:07:00', 40.00),
(13, 14, 12, 'https://cdn.example.com/avistamientos/13.jpg', 'Cable, Manizales', '2025-04-22 18:18:00', 60.00),
(14, 18, NULL, 'https://cdn.example.com/avistamientos/14.jpg', 'Barrio Centro, Manizales', '2025-04-23 10:10:00', 55.55),
(15, 12, 15, 'https://cdn.example.com/avistamientos/15.jpg', 'Popayán - Centro', '2025-04-24 21:21:00', 66.20),
(16, 16, NULL, 'https://cdn.example.com/avistamientos/16.jpg', 'Popayán - Norte', '2025-04-25 06:06:00', 49.90),
(17, 17, 17, 'https://cdn.example.com/avistamientos/17.jpg', 'Cúcuta - Centro', '2025-04-26 13:13:00', 87.90),
(18, 9, 18, 'https://cdn.example.com/avistamientos/18.jpg', 'Cúcuta - La Riviera', '2025-04-27 15:15:00', 91.30),
(19, 20, NULL, 'https://cdn.example.com/avistamientos/19.jpg', 'Villavicencio - Siete de Agosto', '2025-04-28 17:17:00', 48.50),
(20, 1, 20, 'https://cdn.example.com/avistamientos/20.jpg', 'Villavicencio - Centro', '2025-04-29 20:20:00', 99.10);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `foto_adopcion`
--

CREATE TABLE `foto_adopcion` (
  `id_foto_publicacion` int(11) NOT NULL,
  `id_publicacion` int(11) DEFAULT NULL,
  `url_imagen` varchar(255) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `foto_adopcion`
--

INSERT INTO `foto_adopcion` (`id_foto_publicacion`, `id_publicacion`, `url_imagen`) VALUES
(1, 1, 'https://cdn.example.com/fotos_adopcion/pub_1.jpg'),
(2, 2, 'https://cdn.example.com/fotos_adopcion/pub_2.jpg'),
(3, 3, 'https://cdn.example.com/fotos_adopcion/pub_3.jpg'),
(4, 4, 'https://cdn.example.com/fotos_adopcion/pub_4.jpg'),
(5, 5, 'https://cdn.example.com/fotos_adopcion/pub_5.jpg'),
(6, 6, 'https://cdn.example.com/fotos_adopcion/pub_6.jpg'),
(7, 7, 'https://cdn.example.com/fotos_adopcion/pub_7.jpg'),
(8, 8, 'https://cdn.example.com/fotos_adopcion/pub_8.jpg'),
(9, 9, 'https://cdn.example.com/fotos_adopcion/pub_9.jpg'),
(10, 10, 'https://cdn.example.com/fotos_adopcion/pub_10.jpg'),
(11, 11, 'https://cdn.example.com/fotos_adopcion/pub_11.jpg'),
(12, 12, 'https://cdn.example.com/fotos_adopcion/pub_12.jpg'),
(13, 13, 'https://cdn.example.com/fotos_adopcion/pub_13.jpg'),
(14, 14, 'https://cdn.example.com/fotos_adopcion/pub_14.jpg'),
(15, 15, 'https://cdn.example.com/fotos_adopcion/pub_15.jpg'),
(16, 16, 'https://cdn.example.com/fotos_adopcion/pub_16.jpg'),
(17, 17, 'https://cdn.example.com/fotos_adopcion/pub_17.jpg'),
(18, 18, 'https://cdn.example.com/fotos_adopcion/pub_18.jpg'),
(19, 19, 'https://cdn.example.com/fotos_adopcion/pub_19.jpg'),
(20, 20, 'https://cdn.example.com/fotos_adopcion/pub_20.jpg');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `foto_mascota`
--

CREATE TABLE `foto_mascota` (
  `id_foto_mascota` int(11) NOT NULL,
  `id_mascota` int(11) DEFAULT NULL,
  `url_imagen` varchar(255) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `foto_mascota`
--

INSERT INTO `foto_mascota` (`id_foto_mascota`, `id_mascota`, `url_imagen`) VALUES
(1, 1, 'https://cdn.example.com/fotos/mascota_1.jpg'),
(2, 2, 'https://cdn.example.com/fotos/mascota_2.jpg'),
(3, 3, 'https://cdn.example.com/fotos/mascota_3.jpg'),
(4, 4, 'https://cdn.example.com/fotos/mascota_4.jpg'),
(5, 5, 'https://cdn.example.com/fotos/mascota_5.jpg'),
(6, 6, 'https://cdn.example.com/fotos/mascota_6.jpg'),
(7, 7, 'https://cdn.example.com/fotos/mascota_7.jpg'),
(8, 8, 'https://cdn.example.com/fotos/mascota_8.jpg'),
(9, 9, 'https://cdn.example.com/fotos/mascota_9.jpg'),
(10, 10, 'https://cdn.example.com/fotos/mascota_10.jpg'),
(11, 11, 'https://cdn.example.com/fotos/mascota_11.jpg'),
(12, 12, 'https://cdn.example.com/fotos/mascota_12.jpg'),
(13, 13, 'https://cdn.example.com/fotos/mascota_13.jpg'),
(14, 14, 'https://cdn.example.com/fotos/mascota_14.jpg'),
(15, 15, 'https://cdn.example.com/fotos/mascota_15.jpg'),
(16, 16, 'https://cdn.example.com/fotos/mascota_16.jpg'),
(17, 17, 'https://cdn.example.com/fotos/mascota_17.jpg'),
(18, 18, 'https://cdn.example.com/fotos/mascota_18.jpg'),
(19, 19, 'https://cdn.example.com/fotos/mascota_19.jpg'),
(20, 20, 'https://cdn.example.com/fotos/mascota_20.jpg');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `mascota`
--

CREATE TABLE `mascota` (
  `id_mascota` int(11) NOT NULL,
  `id_usuario` int(11) DEFAULT NULL,
  `nombre_mascota` varchar(80) DEFAULT NULL,
  `raza` varchar(80) DEFAULT NULL,
  `tamaño` varchar(40) DEFAULT NULL,
  `caracteristicas` text DEFAULT NULL,
  `edad` int(11) DEFAULT NULL,
  `ubicación` varchar(150) DEFAULT NULL,
  `estado` enum('perdida','encontrada','en proceso','adoptada','retirada') DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `mascota`
--

INSERT INTO `mascota` (`id_mascota`, `id_usuario`, `nombre_mascota`, `raza`, `tamaño`, `caracteristicas`, `edad`, `ubicación`, `estado`) VALUES
(1, 1, 'Firulais', 'Labrador', 'Grande', 'Pelaje corto, color amarillo', 5, 'Suba, Bogotá', 'perdida'),
(2, 2, 'Max', 'Pitbull', 'Mediano', 'Musculoso, mancha blanca en pecho', 6, 'Chapinero, Bogotá', 'encontrada'),
(3, 3, 'Luna', 'Criollo', 'Pequeño', 'Orejas puntiagudas, tatuaje', 3, 'Centro, Bogotá', 'en proceso'),
(4, 4, 'Tommy', 'Poodle', 'Pequeño', 'Rizado, necesita corte frecuente', 7, 'Laureles, Medellín', 'adoptada'),
(5, 5, 'Rocky', 'Bulldog', 'Mediano', 'Cara arrugada, tranquilo', 4, 'El Poblado, Medellín', 'retirada'),
(6, 6, 'Nala', 'Beagle', 'Mediano', 'Olor fuerte, ojos expresivos', 6, 'Norte, Cali', 'perdida'),
(7, 7, 'Bruno', 'Pastor Alemán', 'Grande', 'Muy activo, collar negro', 8, 'Centro, Cali', 'encontrada'),
(8, 8, 'Maya', 'Golden Retriever', 'Grande', 'Amigable, nada en agua', 3, 'Cabecera, Bucaramanga', 'en proceso'),
(9, 9, 'Simba', 'Husky', 'Grande', 'Ojos azules, pelaje grueso', 4, 'Norte, Barranquilla', 'perdida'),
(10, 10, 'Coco', 'Chihuahua', 'Pequeño', 'Muy nervioso, color café', 6, 'Centro, Barranquilla', 'en proceso'),
(11, 11, 'Toby', 'Rottweiler', 'Grande', 'Fuerte, protector', 9, 'Centro, Pereira', 'adoptada'),
(12, 12, 'Kira', 'Dálmata', 'Mediano', 'Manchas negras, enérgica', 2, 'Circunvalar, Pereira', 'perdida'),
(13, 13, 'Zeus', 'Boxer', 'Grande', 'Cabeza ancha, juguetón', 6, 'Cable, Manizales', 'encontrada'),
(14, 14, 'Molly', 'Shih Tzu', 'Pequeño', 'Pelaje largo, cariñosa', 5, 'Manizales - Centro', 'en proceso'),
(15, 15, 'Thor', 'Doberman', 'Grande', 'Ágil, orejas cortadas', 4, 'Popayán - Centro', 'perdida'),
(16, 16, 'Boby', 'Border Collie', 'Mediano', 'Muy inteligente, obediente', 10, 'Popayán - Norte', 'adoptada'),
(17, 17, 'Lola', 'Schnauzer', 'Pequeño', 'Barba característica', 1, 'Cúcuta - Centro', 'retirada'),
(18, 18, 'Rex', 'Pug', 'Pequeño', 'Cara chata, ronca al dormir', 7, 'Cúcuta - La Riviera', 'encontrada'),
(19, 19, 'Olivia', 'Cocker Spaniel', 'Mediano', 'Orejas largas, dócil', 3, 'Villavicencio - Siete', 'perdida'),
(20, 20, 'Apolo', 'Maltés', 'Pequeño', 'Blanco, muy pequeño', 2, 'Villavicencio - Centro', 'en proceso');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `mensaje_seguro`
--

CREATE TABLE `mensaje_seguro` (
  `id_mensaje` int(11) NOT NULL,
  `id_solicitud` int(11) DEFAULT NULL,
  `id_usuario` int(11) DEFAULT NULL,
  `mensaje_predefinido` varchar(255) DEFAULT NULL,
  `tipo_mensaje` varchar(80) DEFAULT NULL,
  `fecha` datetime DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `mensaje_seguro`
--

INSERT INTO `mensaje_seguro` (`id_mensaje`, `id_solicitud`, `id_usuario`, `mensaje_predefinido`, `tipo_mensaje`, `fecha`) VALUES
(1, 1, 2, 'Hola, recibimos tu solicitud. Pronto la revisamos.', 'info', '2025-04-01 10:05:00'),
(2, 2, 5, 'Tu solicitud fue aprobada, por favor enviar documentos.', 'accion', '2025-04-02 11:05:00'),
(3, 3, 9, 'Estamos revisando tus referencias.', 'info', '2025-04-03 12:05:00'),
(4, 4, 12, 'Gracias por postular, falta una entrevista.', 'info', '2025-04-04 13:05:00'),
(5, 5, 7, 'Lo sentimos, tu solicitud fue rechazada.', 'error', '2025-04-05 14:05:00'),
(6, 6, 14, 'Solicitud aprobada, coordinar entrega.', 'accion', '2025-04-06 15:05:00'),
(7, 7, 1, 'Recibimos tu formulario, pronto te contactamos.', 'info', '2025-04-07 16:05:00'),
(8, 8, 3, 'Por favor completa el formulario adjunto.', 'accion', '2025-04-08 17:05:00'),
(9, 9, 11, 'Felicitaciones, tu solicitud avanza a entrevista.', 'info', '2025-04-09 18:05:00'),
(10, 10, 4, 'Tu solicitud está en revisión por el equipo.', 'info', '2025-04-10 19:05:00'),
(11, 11, 6, 'Necesitamos más información sobre tu hogar.', 'accion', '2025-04-11 08:35:00'),
(12, 12, 13, 'Falta un documento para continuar.', 'accion', '2025-04-12 09:35:00'),
(13, 13, 16, 'Tu solicitud fue aprobada con condiciones.', 'info', '2025-04-13 10:35:00'),
(14, 14, 18, 'Por favor confirma tu disponibilidad para visita.', 'accion', '2025-04-14 11:35:00'),
(15, 15, 15, 'Documentos recibidos, procedemos.', 'info', '2025-04-15 12:35:00'),
(16, 16, 17, 'Tu solicitud está siendo evaluada.', 'info', '2025-04-16 13:35:00'),
(17, 17, 8, 'Se programó la visita para la próxima semana.', 'info', '2025-04-17 14:35:00'),
(18, 18, 10, 'Necesitamos confirmar horario de entrega.', 'accion', '2025-04-18 15:35:00'),
(19, 19, 19, 'Solicitud aprobada, bienvenido como adoptante.', 'info', '2025-04-19 16:35:00'),
(20, 20, 20, 'Gracias por postular, te contactaremos pronto.', 'info', '2025-04-20 17:35:00');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `publicacion_adopcion`
--

CREATE TABLE `publicacion_adopcion` (
  `id_publicacion` int(11) NOT NULL,
  `id_mascota` int(11) DEFAULT NULL,
  `id_usuario` int(11) DEFAULT NULL,
  `descripcion` text DEFAULT NULL,
  `estado_adopcion` enum('Disponible','En proceso','Adoptada','Retirada') DEFAULT NULL,
  `fecha_publicacion` datetime DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `publicacion_adopcion`
--

INSERT INTO `publicacion_adopcion` (`id_publicacion`, `id_mascota`, `id_usuario`, `descripcion`, `estado_adopcion`, `fecha_publicacion`) VALUES
(1, 4, 4, 'Tommy busca nuevo hogar, buen con niños.', 'Disponible', '2025-01-10 09:00:00'),
(2, 5, 5, 'Rocky necesita familia con jardín.', 'Disponible', '2025-01-15 10:30:00'),
(3, 11, 11, 'Toby está en proceso de adopción familiar.', 'En proceso', '2025-02-01 11:11:00'),
(4, 16, 16, 'Boby busca hogar por cambio de ciudad.', 'Disponible', '2025-02-05 12:00:00'),
(5, 8, 8, 'Maya se da en adopción por problemas de espacio.', 'Disponible', '2025-02-10 13:00:00'),
(6, 2, 2, 'Max necesita hogar responsable.', 'Disponible', '2025-02-20 14:00:00'),
(7, 13, 13, 'Zeus es muy activo y necesita ejercicio diario.', 'Disponible', '2025-03-01 15:00:00'),
(8, 14, 14, 'Molly es cariñosa y tranquila.', 'Adoptada', '2025-03-05 16:00:00'),
(9, 9, 9, 'Simba busca familia que le guste el agua.', 'Disponible', '2025-03-10 17:00:00'),
(10, 15, 15, 'Thor necesita dueño con experiencia.', 'Disponible', '2025-03-15 18:00:00'),
(11, 1, 1, 'Firulais está perdido; se necesita hogar temporal.', 'Retirada', '2025-03-20 09:00:00'),
(12, 3, 3, 'Luna disponible para adopción responsable.', 'En proceso', '2025-03-22 09:30:00'),
(13, 6, 6, 'Nala necesita familia amante de paseos largos.', 'Disponible', '2025-03-25 10:30:00'),
(14, 7, 7, 'Bruno, protector y leal.', 'Disponible', '2025-03-28 11:30:00'),
(15, 10, 10, 'Coco es pequeño y necesita hogar tranquilo.', 'Disponible', '2025-04-01 12:30:00'),
(16, 12, 12, 'Kira busca hogar que cuide su energía.', 'Disponible', '2025-04-05 13:30:00'),
(17, 17, 17, 'Lola disponible para adopción responsable.', 'Adoptada', '2025-04-10 14:30:00'),
(18, 18, 18, 'Rex en adopción por cambio de dueño.', 'En proceso', '2025-04-12 15:30:00'),
(19, 19, 19, 'Olivia necesita espacio amplio para correr.', 'Disponible', '2025-04-15 16:30:00'),
(20, 20, 20, 'Apolo, cachorro de casa, busca hogar.', 'Disponible', '2025-04-20 17:30:00');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `solicitud_adopcion`
--

CREATE TABLE `solicitud_adopcion` (
  `id_solicitud` int(11) NOT NULL,
  `id_usuario` int(11) DEFAULT NULL,
  `id_mascota` int(11) DEFAULT NULL,
  `motivo_adopcion` text DEFAULT NULL,
  `formulario_adopcion` text DEFAULT NULL,
  `estado_solicitud` enum('Pendiente','Aprobada','Rechazada','En revisión') DEFAULT NULL,
  `fecha_solicitud` datetime DEFAULT NULL,
  `comentario_admin` text DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `solicitud_adopcion`
--

INSERT INTO `solicitud_adopcion` (`id_solicitud`, `id_usuario`, `id_mascota`, `motivo_adopcion`, `formulario_adopcion`, `estado_solicitud`, `fecha_solicitud`, `comentario_admin`) VALUES
(1, 2, 4, 'Quiero un perro para compañía familiar.', '{\"preguntas\":\"sí\"}', 'Pendiente', '2025-04-01 10:00:00', NULL),
(2, 5, 5, 'Busco un perro para actividades al aire libre.', '{\"preguntas\":\"sí\"}', 'Aprobada', '2025-04-02 11:00:00', 'Revisado y aprobado.'),
(3, 9, 11, 'Interesado por compañía y guardia.', '{\"preguntas\":\"sí\"}', 'En revisión', '2025-04-03 12:00:00', NULL),
(4, 12, 16, 'Cambio de casa, puedo cuidar bien a la mascota.', '{\"preguntas\":\"sí\"}', 'Pendiente', '2025-04-04 13:00:00', NULL),
(5, 7, 8, 'Familia con niños pequeños, buscamos mascota calmada.', '{\"preguntas\":\"sí\"}', 'Rechazada', '2025-04-05 14:00:00', 'No cumple requisitos.'),
(6, 14, 2, 'Vivo en casa con jardín amplio.', '{\"preguntas\":\"sí\"}', 'Aprobada', '2025-04-06 15:00:00', 'Entrevista exitosa.'),
(7, 1, 13, 'Me gustan perros activos para deporte.', '{\"preguntas\":\"sí\"}', 'Pendiente', '2025-04-07 16:00:00', NULL),
(8, 3, 10, 'Busco compañía para apartamento.', '{\"preguntas\":\"sí\"}', 'Pendiente', '2025-04-08 17:00:00', NULL),
(9, 11, 15, 'Experiencia previa con razas grandes.', '{\"preguntas\":\"sí\"}', 'Aprobada', '2025-04-09 18:00:00', 'Ok para adopción.'),
(10, 4, 1, 'Quiero un perro para acompañar a mis hijos.', '{\"preguntas\":\"sí\"}', 'En revisión', '2025-04-10 19:00:00', NULL),
(11, 6, 6, 'Necesito una mascota para paseos diarios.', '{\"preguntas\":\"sí\"}', 'Pendiente', '2025-04-11 08:30:00', NULL),
(12, 13, 7, 'Busco un perro para seguridad de la casa.', '{\"preguntas\":\"sí\"}', 'Rechazada', '2025-04-12 09:30:00', 'Falta documentación.'),
(13, 16, 3, 'Quiero mascota para terapias y compañía.', '{\"preguntas\":\"sí\"}', 'Aprobada', '2025-04-13 10:30:00', 'Aprobada con condiciones.'),
(14, 18, 9, 'Familia amante del agua y actividades.', '{\"preguntas\":\"sí\"}', 'Pendiente', '2025-04-14 11:30:00', NULL),
(15, 15, 12, 'Busco perro para mi finca.', '{\"preguntas\":\"sí\"}', 'Aprobada', '2025-04-15 12:30:00', 'Documentos OK.'),
(16, 17, 14, 'Quiero perro pequeño para apartamento.', '{\"preguntas\":\"sí\"}', 'Pendiente', '2025-04-16 13:30:00', NULL),
(17, 8, 18, 'Puedo darle tiempo y cuidados especiales.', '{\"preguntas\":\"sí\"}', 'En revisión', '2025-04-17 14:30:00', NULL),
(18, 10, 19, 'Necesito perro para compañía durante la jubilación.', '{\"preguntas\":\"sí\"}', 'Pendiente', '2025-04-18 15:30:00', NULL),
(19, 19, 20, 'Busco cachorro para socializar en familia.', '{\"preguntas\":\"sí\"}', 'Aprobada', '2025-04-19 16:30:00', 'Aprobada.'),
(20, 20, 17, 'Quiero un perro para terapia y paseos.', '{\"preguntas\":\"sí\"}', 'Pendiente', '2025-04-20 17:30:00', NULL);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `usuario`
--

CREATE TABLE `usuario` (
  `id_usuario` int(11) NOT NULL,
  `nombre_completo` varchar(120) DEFAULT NULL,
  `telefono` varchar(20) DEFAULT NULL,
  `correo` varchar(120) DEFAULT NULL,
  `fecha_nacimiento` date DEFAULT NULL,
  `contraseña` varchar(255) DEFAULT NULL,
  `rol` enum('usuario','admin') DEFAULT 'usuario'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `usuario`
--

INSERT INTO `usuario` (`id_usuario`, `nombre_completo`, `telefono`, `correo`, `fecha_nacimiento`, `contraseña`, `rol`) VALUES
(1, 'Carlos Pérez', '3001110001', 'carlos.perez@example.com', '1985-05-10', 'hashed_pwd_1', 'usuario'),
(2, 'Ana Gómez', '3001110002', 'ana.gomez@example.com', '1990-02-21', 'hashed_pwd_2', 'usuario'),
(3, 'Luis Martínez', '3001110003', 'luis.martinez@example.com', '1982-08-14', 'hashed_pwd_3', 'usuario'),
(4, 'María Rodríguez', '3001110004', 'maria.rodriguez@example.com', '1995-11-05', 'hashed_pwd_4', 'usuario'),
(5, 'Juan Hernández', '3001110005', 'juan.hernandez@example.com', '1979-12-30', 'hashed_pwd_5', 'usuario'),
(6, 'Paula Sánchez', '3001110006', 'paula.sanchez@example.com', '1992-07-18', 'hashed_pwd_6', 'usuario'),
(7, 'Andrés López', '3001110007', 'andres.lopez@example.com', '1988-03-02', 'hashed_pwd_7', 'usuario'),
(8, 'Laura Torres', '3001110008', 'laura.torres@example.com', '1994-09-09', 'hashed_pwd_8', 'usuario'),
(9, 'Ricardo Ruiz', '3001110009', 'ricardo.ruiz@example.com', '1980-06-22', 'hashed_pwd_9', 'usuario'),
(10, 'Valentina Castro', '3001110010', 'valentina.castro@example.com', '1996-01-15', 'hashed_pwd_10', 'usuario'),
(11, 'Camilo Vargas', '3001110011', 'camilo.vargas@example.com', '1987-10-03', 'hashed_pwd_11', 'usuario'),
(12, 'Sebastián Mora', '3001110012', 'sebastian.mora@example.com', '1991-04-27', 'hashed_pwd_12', 'usuario'),
(13, 'Daniela Ríos', '3001110013', 'daniela.rios@example.com', '1993-08-12', 'hashed_pwd_13', 'usuario'),
(14, 'Felipe Duarte', '3001110014', 'felipe.duarte@example.com', '1986-02-02', 'hashed_pwd_14', 'usuario'),
(15, 'Carolina León', '3001110015', 'carolina.leon@example.com', '1998-07-07', 'hashed_pwd_15', 'usuario'),
(16, 'Manuel Ortiz', '3001110016', 'manuel.ortiz@example.com', '1983-11-20', 'hashed_pwd_16', 'usuario'),
(17, 'Juliana Peña', '3001110017', 'juliana.pena@example.com', '1997-05-25', 'hashed_pwd_17', 'usuario'),
(18, 'Diego Salazar', '3001110018', 'diego.salazar@example.com', '1989-09-30', 'hashed_pwd_18', 'usuario'),
(19, 'Natalia Prieto', '3001110019', 'natalia.prieto@example.com', '1994-12-12', 'hashed_pwd_19', 'usuario'),
(20, 'Santiago Cárdenas', '3001110020', 'santiago.cardenas@example.com', '1981-03-18', 'hashed_pwd_20', 'admin');

--
-- Índices para tablas volcadas
--

--
-- Indices de la tabla `alerta`
--
ALTER TABLE `alerta`
  ADD PRIMARY KEY (`id_alerta`),
  ADD KEY `fk_alerta_avist` (`id_avistamiento`),
  ADD KEY `fk_alerta_mascota` (`id_mascota`);

--
-- Indices de la tabla `avistamiento`
--
ALTER TABLE `avistamiento`
  ADD PRIMARY KEY (`id_avistamiento`),
  ADD KEY `fk_avist_usuario` (`id_usuario`),
  ADD KEY `fk_avist_mascota` (`id_mascota`);

--
-- Indices de la tabla `foto_adopcion`
--
ALTER TABLE `foto_adopcion`
  ADD PRIMARY KEY (`id_foto_publicacion`),
  ADD KEY `fk_foto_adopcion` (`id_publicacion`);

--
-- Indices de la tabla `foto_mascota`
--
ALTER TABLE `foto_mascota`
  ADD PRIMARY KEY (`id_foto_mascota`),
  ADD KEY `fk_foto_mascota` (`id_mascota`);

--
-- Indices de la tabla `mascota`
--
ALTER TABLE `mascota`
  ADD PRIMARY KEY (`id_mascota`),
  ADD KEY `fk_mascota_usuario` (`id_usuario`);

--
-- Indices de la tabla `mensaje_seguro`
--
ALTER TABLE `mensaje_seguro`
  ADD PRIMARY KEY (`id_mensaje`),
  ADD KEY `fk_mensaje_solicitud` (`id_solicitud`),
  ADD KEY `fk_mensaje_usuario` (`id_usuario`);

--
-- Indices de la tabla `publicacion_adopcion`
--
ALTER TABLE `publicacion_adopcion`
  ADD PRIMARY KEY (`id_publicacion`),
  ADD KEY `fk_publi_mascota` (`id_mascota`),
  ADD KEY `fk_publi_usuario` (`id_usuario`);

--
-- Indices de la tabla `solicitud_adopcion`
--
ALTER TABLE `solicitud_adopcion`
  ADD PRIMARY KEY (`id_solicitud`),
  ADD KEY `fk_solicitud_usuario` (`id_usuario`),
  ADD KEY `fk_solicitud_mascota` (`id_mascota`);

--
-- Indices de la tabla `usuario`
--
ALTER TABLE `usuario`
  ADD PRIMARY KEY (`id_usuario`),
  ADD UNIQUE KEY `correo` (`correo`);

--
-- AUTO_INCREMENT de las tablas volcadas
--

--
-- AUTO_INCREMENT de la tabla `alerta`
--
ALTER TABLE `alerta`
  MODIFY `id_alerta` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=21;

--
-- AUTO_INCREMENT de la tabla `avistamiento`
--
ALTER TABLE `avistamiento`
  MODIFY `id_avistamiento` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=21;

--
-- AUTO_INCREMENT de la tabla `foto_adopcion`
--
ALTER TABLE `foto_adopcion`
  MODIFY `id_foto_publicacion` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=21;

--
-- AUTO_INCREMENT de la tabla `foto_mascota`
--
ALTER TABLE `foto_mascota`
  MODIFY `id_foto_mascota` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=21;

--
-- AUTO_INCREMENT de la tabla `mascota`
--
ALTER TABLE `mascota`
  MODIFY `id_mascota` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=21;

--
-- AUTO_INCREMENT de la tabla `mensaje_seguro`
--
ALTER TABLE `mensaje_seguro`
  MODIFY `id_mensaje` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=21;

--
-- AUTO_INCREMENT de la tabla `publicacion_adopcion`
--
ALTER TABLE `publicacion_adopcion`
  MODIFY `id_publicacion` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=21;

--
-- AUTO_INCREMENT de la tabla `solicitud_adopcion`
--
ALTER TABLE `solicitud_adopcion`
  MODIFY `id_solicitud` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=21;

--
-- AUTO_INCREMENT de la tabla `usuario`
--
ALTER TABLE `usuario`
  MODIFY `id_usuario` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=21;

--
-- Restricciones para tablas volcadas
--

--
-- Filtros para la tabla `alerta`
--
ALTER TABLE `alerta`
  ADD CONSTRAINT `fk_alerta_avist` FOREIGN KEY (`id_avistamiento`) REFERENCES `avistamiento` (`id_avistamiento`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `fk_alerta_mascota` FOREIGN KEY (`id_mascota`) REFERENCES `mascota` (`id_mascota`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Filtros para la tabla `avistamiento`
--
ALTER TABLE `avistamiento`
  ADD CONSTRAINT `fk_avist_mascota` FOREIGN KEY (`id_mascota`) REFERENCES `mascota` (`id_mascota`) ON DELETE SET NULL ON UPDATE CASCADE,
  ADD CONSTRAINT `fk_avist_usuario` FOREIGN KEY (`id_usuario`) REFERENCES `usuario` (`id_usuario`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Filtros para la tabla `foto_adopcion`
--
ALTER TABLE `foto_adopcion`
  ADD CONSTRAINT `fk_foto_adopcion` FOREIGN KEY (`id_publicacion`) REFERENCES `publicacion_adopcion` (`id_publicacion`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Filtros para la tabla `foto_mascota`
--
ALTER TABLE `foto_mascota`
  ADD CONSTRAINT `fk_foto_mascota` FOREIGN KEY (`id_mascota`) REFERENCES `mascota` (`id_mascota`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Filtros para la tabla `mascota`
--
ALTER TABLE `mascota`
  ADD CONSTRAINT `fk_mascota_usuario` FOREIGN KEY (`id_usuario`) REFERENCES `usuario` (`id_usuario`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Filtros para la tabla `mensaje_seguro`
--
ALTER TABLE `mensaje_seguro`
  ADD CONSTRAINT `fk_mensaje_solicitud` FOREIGN KEY (`id_solicitud`) REFERENCES `solicitud_adopcion` (`id_solicitud`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `fk_mensaje_usuario` FOREIGN KEY (`id_usuario`) REFERENCES `usuario` (`id_usuario`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Filtros para la tabla `publicacion_adopcion`
--
ALTER TABLE `publicacion_adopcion`
  ADD CONSTRAINT `fk_publi_mascota` FOREIGN KEY (`id_mascota`) REFERENCES `mascota` (`id_mascota`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `fk_publi_usuario` FOREIGN KEY (`id_usuario`) REFERENCES `usuario` (`id_usuario`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Filtros para la tabla `solicitud_adopcion`
--
ALTER TABLE `solicitud_adopcion`
  ADD CONSTRAINT `fk_solicitud_mascota` FOREIGN KEY (`id_mascota`) REFERENCES `mascota` (`id_mascota`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `fk_solicitud_usuario` FOREIGN KEY (`id_usuario`) REFERENCES `usuario` (`id_usuario`) ON DELETE CASCADE ON UPDATE CASCADE;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
