-- Esquema unico de Busca Huellas.
-- Solo estructura y catalogo de roles. Sin datos personales (Ley 1581 de 2012).

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

-- --------------------------------------------------------
-- Tabla `rol`
-- --------------------------------------------------------

CREATE TABLE `rol` (
  `id_rol` int(11) NOT NULL,
  `nombre_rol` varchar(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

INSERT INTO `rol` (`id_rol`, `nombre_rol`) VALUES
(1, 'Usuario'),
(2, 'Administrador');

-- --------------------------------------------------------
-- Tabla `usuario`
-- --------------------------------------------------------

CREATE TABLE `usuario` (
  `id_usuario` int(11) NOT NULL,
  `id_rol` int(11) DEFAULT NULL,
  `nombre_completo` varchar(100) NOT NULL,
  `telefono` varchar(20) DEFAULT NULL,
  `correo` varchar(100) NOT NULL,
  `correo_verificado` tinyint(1) NOT NULL DEFAULT 0,
  `contraseña` varchar(255) NOT NULL,
  `foto_perfil` varchar(255) DEFAULT NULL,
  `google_id` varchar(100) DEFAULT NULL,
  `facebook_id` varchar(100) DEFAULT NULL,
  `fecha_registro` date DEFAULT NULL,
  `preferencias` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL CHECK (json_valid(`preferencias`)),
  `estado_usuario` tinyint(1) NOT NULL DEFAULT 1
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------
-- Tabla `mascota`
-- --------------------------------------------------------

CREATE TABLE `mascota` (
  `id_mascota` int(11) NOT NULL,
  `id_usuario` int(11) DEFAULT NULL,
  `nombre_mascota` varchar(100) NOT NULL,
  `raza` varchar(100) DEFAULT NULL,
  `edad` int(11) DEFAULT NULL,
  `color` varchar(50) DEFAULT NULL,
  `pelaje` varchar(50) DEFAULT NULL,
  `tamaño` varchar(50) DEFAULT NULL,
  `descripcion` text DEFAULT NULL,
  `ubicacion` varchar(255) DEFAULT NULL,
  `estado` varchar(50) DEFAULT NULL,
  `fecha_registro` datetime DEFAULT NULL,
  `estado_mascota` tinyint(1) NOT NULL DEFAULT 1
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------
-- Tabla `foto_mascota`
-- --------------------------------------------------------

CREATE TABLE `foto_mascota` (
  `id_foto` int(11) NOT NULL,
  `id_mascota` int(11) DEFAULT NULL,
  `url_imagen` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------
-- Tabla `alerta`
-- --------------------------------------------------------

CREATE TABLE `alerta` (
  `id_alerta` int(11) NOT NULL,
  `id_usuario` int(11) DEFAULT NULL,
  `id_mascota` int(11) DEFAULT NULL,
  `id_alerta_origen` int(11) DEFAULT NULL,
  `estado_alerta` varchar(50) DEFAULT NULL,
  `confirmacion` varchar(50) DEFAULT NULL,
  `mensaje` text DEFAULT NULL,
  `fecha_alerta` datetime DEFAULT NULL,
  `estado_alerta_registro` tinyint(1) NOT NULL DEFAULT 1
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------
-- Tabla `avistamiento`
-- --------------------------------------------------------

CREATE TABLE `avistamiento` (
  `id_avistamiento` int(11) NOT NULL,
  `id_alerta` int(11) DEFAULT NULL,
  `id_mascota` int(11) DEFAULT NULL,
  `ubicacion` varchar(255) DEFAULT NULL,
  `descripcion_avistamiento` text DEFAULT NULL,
  `url_imagen` varchar(255) DEFAULT NULL,
  `fecha_avistamiento` datetime DEFAULT NULL,
  `estado_avistamiento` tinyint(1) NOT NULL DEFAULT 1
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------
-- Tabla `avistamiento_confirmado`
-- --------------------------------------------------------

CREATE TABLE `avistamiento_confirmado` (
  `id_confirmacion` int(11) NOT NULL,
  `id_avistamiento` int(11) NOT NULL,
  `id_usuario_alerto` int(11) NOT NULL,
  `id_usuario_dueno` int(11) NOT NULL,
  `id_mascota` int(11) NOT NULL,
  `fecha_confirmacion` datetime NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------
-- Tabla `mensaje`
-- --------------------------------------------------------

CREATE TABLE `mensaje` (
  `id_mensaje` int(11) NOT NULL,
  `id_alerta` int(11) DEFAULT NULL,
  `usuario_emisor` int(11) DEFAULT NULL,
  `usuario_receptor` int(11) DEFAULT NULL,
  `mensaje_chat` text DEFAULT NULL,
  `url_imagen` varchar(255) DEFAULT NULL,
  `fecha_envio` datetime DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------
-- Tabla `chat_eliminado`
-- --------------------------------------------------------

CREATE TABLE `chat_eliminado` (
  `id_chat_eliminado` int(11) NOT NULL,
  `id_alerta` int(11) NOT NULL,
  `id_usuario` int(11) NOT NULL,
  `fecha_eliminacion` datetime NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------
-- Tabla `articulo`
-- --------------------------------------------------------

CREATE TABLE `articulo` (
  `id_articulo` int(11) NOT NULL,
  `id_usuario` int(11) DEFAULT NULL,
  `titulo` varchar(255) DEFAULT NULL,
  `contenido` text DEFAULT NULL,
  `url_imagen` varchar(255) DEFAULT NULL,
  `fecha_publicacion` date DEFAULT NULL,
  `estado_articulo` tinyint(1) NOT NULL DEFAULT 1
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------
-- Tabla `informe`
-- --------------------------------------------------------

CREATE TABLE `informe` (
  `id_informe` int(11) NOT NULL,
  `id_usuario` int(11) DEFAULT NULL,
  `titulo` varchar(120) DEFAULT NULL,
  `tipo_informe` varchar(100) DEFAULT NULL,
  `descripcion` text DEFAULT NULL,
  `ruta_pdf` varchar(255) DEFAULT NULL,
  `ruta_excel` varchar(255) DEFAULT NULL,
  `fecha_generacion` date DEFAULT NULL,
  `estado_informe` tinyint(1) NOT NULL DEFAULT 1
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------
-- Indices
-- --------------------------------------------------------

ALTER TABLE `rol`
  ADD PRIMARY KEY (`id_rol`);

ALTER TABLE `usuario`
  ADD PRIMARY KEY (`id_usuario`),
  ADD UNIQUE KEY `correo` (`correo`),
  ADD UNIQUE KEY `google_id` (`google_id`),
  ADD UNIQUE KEY `facebook_id` (`facebook_id`),
  ADD KEY `id_rol` (`id_rol`),
  ADD KEY `idx_usuario_estado` (`estado_usuario`);

ALTER TABLE `mascota`
  ADD PRIMARY KEY (`id_mascota`),
  ADD KEY `id_usuario` (`id_usuario`),
  ADD KEY `idx_mascota_estado` (`estado_mascota`);

ALTER TABLE `foto_mascota`
  ADD PRIMARY KEY (`id_foto`),
  ADD KEY `id_mascota` (`id_mascota`);

ALTER TABLE `alerta`
  ADD PRIMARY KEY (`id_alerta`),
  ADD KEY `id_usuario` (`id_usuario`),
  ADD KEY `id_mascota` (`id_mascota`),
  ADD KEY `idx_alerta_origen` (`id_alerta_origen`),
  ADD KEY `idx_alerta_estado_registro` (`estado_alerta_registro`);

ALTER TABLE `avistamiento`
  ADD PRIMARY KEY (`id_avistamiento`),
  ADD KEY `id_mascota` (`id_mascota`),
  ADD KEY `idx_avistamiento_alerta` (`id_alerta`),
  ADD KEY `idx_avistamiento_estado` (`estado_avistamiento`);

ALTER TABLE `avistamiento_confirmado`
  ADD PRIMARY KEY (`id_confirmacion`),
  ADD UNIQUE KEY `uq_confirmacion_avistamiento` (`id_avistamiento`),
  ADD KEY `idx_confirmacion_alerto` (`id_usuario_alerto`),
  ADD KEY `idx_confirmacion_dueno` (`id_usuario_dueno`),
  ADD KEY `idx_confirmacion_mascota` (`id_mascota`);

ALTER TABLE `mensaje`
  ADD PRIMARY KEY (`id_mensaje`),
  ADD KEY `id_alerta` (`id_alerta`),
  ADD KEY `usuario_emisor` (`usuario_emisor`),
  ADD KEY `usuario_receptor` (`usuario_receptor`);

ALTER TABLE `chat_eliminado`
  ADD PRIMARY KEY (`id_chat_eliminado`),
  ADD UNIQUE KEY `uq_chat_eliminado_usuario` (`id_alerta`,`id_usuario`),
  ADD KEY `fk_chat_eliminado_usuario` (`id_usuario`);

ALTER TABLE `articulo`
  ADD PRIMARY KEY (`id_articulo`),
  ADD KEY `id_usuario` (`id_usuario`),
  ADD KEY `idx_articulo_estado` (`estado_articulo`);

ALTER TABLE `informe`
  ADD PRIMARY KEY (`id_informe`),
  ADD KEY `id_usuario` (`id_usuario`),
  ADD KEY `idx_informe_estado` (`estado_informe`);

-- --------------------------------------------------------
-- AUTO_INCREMENT
-- --------------------------------------------------------

ALTER TABLE `rol`
  MODIFY `id_rol` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

ALTER TABLE `usuario`
  MODIFY `id_usuario` int(11) NOT NULL AUTO_INCREMENT;

ALTER TABLE `mascota`
  MODIFY `id_mascota` int(11) NOT NULL AUTO_INCREMENT;

ALTER TABLE `foto_mascota`
  MODIFY `id_foto` int(11) NOT NULL AUTO_INCREMENT;

ALTER TABLE `alerta`
  MODIFY `id_alerta` int(11) NOT NULL AUTO_INCREMENT;

ALTER TABLE `avistamiento`
  MODIFY `id_avistamiento` int(11) NOT NULL AUTO_INCREMENT;

ALTER TABLE `avistamiento_confirmado`
  MODIFY `id_confirmacion` int(11) NOT NULL AUTO_INCREMENT;

ALTER TABLE `mensaje`
  MODIFY `id_mensaje` int(11) NOT NULL AUTO_INCREMENT;

ALTER TABLE `chat_eliminado`
  MODIFY `id_chat_eliminado` int(11) NOT NULL AUTO_INCREMENT;

ALTER TABLE `articulo`
  MODIFY `id_articulo` int(11) NOT NULL AUTO_INCREMENT;

ALTER TABLE `informe`
  MODIFY `id_informe` int(11) NOT NULL AUTO_INCREMENT;

-- --------------------------------------------------------
-- Claves foraneas
-- --------------------------------------------------------

ALTER TABLE `usuario`
  ADD CONSTRAINT `usuario_ibfk_1` FOREIGN KEY (`id_rol`) REFERENCES `rol` (`id_rol`);

ALTER TABLE `mascota`
  ADD CONSTRAINT `mascota_ibfk_1` FOREIGN KEY (`id_usuario`) REFERENCES `usuario` (`id_usuario`);

ALTER TABLE `foto_mascota`
  ADD CONSTRAINT `foto_mascota_ibfk_1` FOREIGN KEY (`id_mascota`) REFERENCES `mascota` (`id_mascota`);

ALTER TABLE `alerta`
  ADD CONSTRAINT `alerta_ibfk_1` FOREIGN KEY (`id_usuario`) REFERENCES `usuario` (`id_usuario`),
  ADD CONSTRAINT `alerta_ibfk_2` FOREIGN KEY (`id_mascota`) REFERENCES `mascota` (`id_mascota`),
  ADD CONSTRAINT `alerta_ibfk_3` FOREIGN KEY (`id_alerta_origen`) REFERENCES `alerta` (`id_alerta`);

ALTER TABLE `avistamiento`
  ADD CONSTRAINT `avistamiento_ibfk_1` FOREIGN KEY (`id_mascota`) REFERENCES `mascota` (`id_mascota`),
  ADD CONSTRAINT `avistamiento_ibfk_2` FOREIGN KEY (`id_alerta`) REFERENCES `alerta` (`id_alerta`);

ALTER TABLE `avistamiento_confirmado`
  ADD CONSTRAINT `fk_confirmacion_avistamiento` FOREIGN KEY (`id_avistamiento`) REFERENCES `avistamiento` (`id_avistamiento`),
  ADD CONSTRAINT `fk_confirmacion_mascota` FOREIGN KEY (`id_mascota`) REFERENCES `mascota` (`id_mascota`),
  ADD CONSTRAINT `fk_confirmacion_usuario_alerto` FOREIGN KEY (`id_usuario_alerto`) REFERENCES `usuario` (`id_usuario`),
  ADD CONSTRAINT `fk_confirmacion_usuario_dueno` FOREIGN KEY (`id_usuario_dueno`) REFERENCES `usuario` (`id_usuario`);

ALTER TABLE `mensaje`
  ADD CONSTRAINT `mensaje_ibfk_1` FOREIGN KEY (`id_alerta`) REFERENCES `alerta` (`id_alerta`),
  ADD CONSTRAINT `mensaje_ibfk_2` FOREIGN KEY (`usuario_emisor`) REFERENCES `usuario` (`id_usuario`),
  ADD CONSTRAINT `mensaje_ibfk_3` FOREIGN KEY (`usuario_receptor`) REFERENCES `usuario` (`id_usuario`);

ALTER TABLE `chat_eliminado`
  ADD CONSTRAINT `fk_chat_eliminado_alerta` FOREIGN KEY (`id_alerta`) REFERENCES `alerta` (`id_alerta`),
  ADD CONSTRAINT `fk_chat_eliminado_usuario` FOREIGN KEY (`id_usuario`) REFERENCES `usuario` (`id_usuario`);

ALTER TABLE `articulo`
  ADD CONSTRAINT `articulo_ibfk_1` FOREIGN KEY (`id_usuario`) REFERENCES `usuario` (`id_usuario`);

ALTER TABLE `informe`
  ADD CONSTRAINT `informe_ibfk_1` FOREIGN KEY (`id_usuario`) REFERENCES `usuario` (`id_usuario`);

COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
