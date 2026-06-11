-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Servidor: 127.0.0.1
-- Tiempo de generación: 25-05-2026 a las 14:22:09
-- Versión del servidor: 10.4.32-MariaDB
-- Versión de PHP: 8.0.30

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Base de datos: `busca_huellas`
--

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `alerta`
--

CREATE TABLE `alerta` (
  `id_alerta` int(11) NOT NULL,
  `id_usuario` int(11) DEFAULT NULL,
  `id_mascota` int(11) DEFAULT NULL,
  `estado_alerta` varchar(50) DEFAULT NULL,
  `confirmacion` varchar(50) DEFAULT NULL,
  `fecha_alerta` date DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `articulo`
--

CREATE TABLE `articulo` (
  `id_articulo` int(11) NOT NULL,
  `id_usuario` int(11) DEFAULT NULL,
  `titulo` varchar(255) DEFAULT NULL,
  `contenido` text DEFAULT NULL,
  `url_imagen` varchar(255) DEFAULT NULL,
  `fecha_publicacion` date DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `articulo`
--

INSERT INTO `articulo` (`id_articulo`, `id_usuario`, `titulo`, `contenido`, `url_imagen`, `fecha_publicacion`) VALUES
(3, 2, 'Este es un texto de prueba para saber la eficiencia de el creador de articulos', 'El Lorem Ipsum fue concebido como un texto de relleno, formateado de una cierta manera para permitir la presentación de elementos gráficos en documentos, sin necesidad de una copia formal. El uso de Lorem Ipsum permite a los diseñadores reunir los diseños y la forma del contenido antes de que el contenido se haya creado, dando al diseño y al proceso de producción más libertad.\r\n\r\nSe cree ampliamente que la historia de Lorem Ipsum se origina con Cicerón en el siglo I aC y su texto De Finibus bonorum et malorum. Esta obra filosófica, también conocida como En los extremos del bien y del mal, se dividió en cinco libros. El Lorem Ipsum que conocemos hoy se deriva de partes del primer libro Liber Primus y su discusión sobre el hedonismo, cuyas palabras habían sido alteradas, añadidas y eliminadas para convertirlas en un latín sin sentido e impropio. No se sabe exactamente cuándo el texto recibió su forma tradicional actual. Sin embargo, las referencias a la frase \"Lorem Ipsum\" se pueden encontrar en la Edición de la Biblioteca Clásica Loeb de 1914 del De Finibus en las secciones 32 y 33. Fue en esta edición del De Finibus en la que H. Rackman tradujo el texto. El siguiente fragmento se selecciona de la sección 32:\r\n\r\n\"qui dolorem ipsum, quia dolor sit amet consectetur adipisci velit, sed quia non numquam eius modi tempora incidunt, ut labore et dolore magnam aliquam quaerat voluptatem\".\r\n\r\nEsto es reconocible, en parte, como el estándar del Lorem Ipsum de hoy y fue traducido a:\r\n\r\n\"Nor again is there anyone who loves or pursues or desires to obtain pain of itself, because it is pain, but occasionally circumstances occur in which toil and pain can procure him some great pleasure\".\r\n\r\nPasando a la década de 1960, el Lorem Ipsum fue popularizado por el fabricante de tipografía Letraset, que lo utilizó en sus campañas publicitarias. Letraset ofrecía páginas de Lorem Ipsum como hojas de transferencia, que fueron ampliamente utilizadas en la era anterior a los ordenadores para los diseños. Estas páginas de transferencia, conocidas como Letraset Body Type, se incluyeron en la publicidad de la compañía y en su popular catálogo.\r\n\r\nEl Lorem Ipsum fue reintroducido en la década de 1980 por Aldus Corporation, una empresa que desarrolló Software de Publicación de Escritorio. Su producto más conocido PageMaker viene con gráficos y plantillas de procesamiento de textos previamente instaladas que contienen una versión del lenguaje latín falso.', 'https://ichef.bbci.co.uk/ace/ws/640/amz/worldservice/live/assets/images/2011/07/25/110725144827_sp_question_mark_304x171_other_nocredit.jpg.webp', '2026-05-20');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `avistamiento`
--

CREATE TABLE `avistamiento` (
  `id_avistamiento` int(11) NOT NULL,
  `id_mascota` int(11) DEFAULT NULL,
  `ubicacion` varchar(255) DEFAULT NULL,
  `descripcion_avistamiento` text DEFAULT NULL,
  `url_imagen` varchar(255) DEFAULT NULL,
  `fecha_avistamiento` date DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `foto_mascota`
--

CREATE TABLE `foto_mascota` (
  `id_foto` int(11) NOT NULL,
  `id_mascota` int(11) DEFAULT NULL,
  `url_imagen` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `informe`
--

CREATE TABLE `informe` (
  `id_informe` int(11) NOT NULL,
  `id_usuario` int(11) DEFAULT NULL,
  `tipo_informe` varchar(100) DEFAULT NULL,
  `descripcion` text DEFAULT NULL,
  `fecha_generacion` date DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `mascota`
--

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
  `estado` varchar(50) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `mascota`
--

INSERT INTO `mascota` (`id_mascota`, `id_usuario`, `nombre_mascota`, `raza`, `edad`, `color`, `pelaje`, `tamaño`, `descripcion`, `estado`) VALUES
(1, 1, 'TIti', 'tasita', 2, 'Blanco y gris', 'Largo rizado', 'pequeño', 'Tiene una mancha naranja en la pata derecha', 'perdida');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `mensaje`
--

CREATE TABLE `mensaje` (
  `id_mensaje` int(11) NOT NULL,
  `id_alerta` int(11) DEFAULT NULL,
  `usuario_emisor` int(11) DEFAULT NULL,
  `usuario_receptor` int(11) DEFAULT NULL,
  `mensaje_chat` text DEFAULT NULL,
  `fecha_envio` datetime DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `rol`
--

CREATE TABLE `rol` (
  `id_rol` int(11) NOT NULL,
  `nombre_rol` varchar(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `rol`
--

INSERT INTO `rol` (`id_rol`, `nombre_rol`) VALUES
(1, 'Usuario'),
(2, 'Administrador');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `usuario`
--

CREATE TABLE `usuario` (
  `id_usuario` int(11) NOT NULL,
  `id_rol` int(11) DEFAULT NULL,
  `nombre_completo` varchar(100) NOT NULL,
  `telefono` varchar(20) DEFAULT NULL,
  `correo` varchar(100) NOT NULL,
  `contraseña` varchar(255) NOT NULL,
  `foto_perfil` varchar(255) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `usuario`
--

INSERT INTO `usuario` (`id_usuario`, `id_rol`, `nombre_completo`, `telefono`, `correo`, `contraseña`, `foto_perfil`) VALUES
(1, 1, 'Pepito', '1234567891', 'pepito2214@gmail.com', 'scrypt:32768:8:1$sO7F9IZVA72GBb5O$6936399f298f3d282dfa688d1d198e16f6d76eb8dc1394221d0204ef406cf1f13e83e68f459ad1bb65ddbb973c00b5d326313f040d7f4c382eb84b627c26963c', 'https://ichef.bbci.co.uk/ace/ws/640/amz/worldservice/live/assets/images/2011/07/25/110725144827_sp_question_mark_304x171_other_nocredit.jpg.webp'),
(2, 1, 'Sebastian', '1234567891', 'holi@gmail.com', 'scrypt:32768:8:1$TDcUsvkYyP1WzW9q$f3fce03b73283ba6d34a2a2c125582cfdb97bd0f9de98ef24b1921306940297a7e3a3f1499ad278b975d787f469fe5de137e491de9b14a945dc8377df7a6ec7f', NULL),
(3, 1, 'Camilo Perez', '1234567891', 'camilo1234@gmail.com', 'scrypt:32768:8:1$smOY6VPPMLMdzbkC$a94d0b21282a847836eb333a5a77ed13118ade15c15dcf63a27cb9353b17dbe3a545ca525a87469de9356520515eed0939a0a27aae1bd6d75a5ff21ec4607a02', NULL);

--
-- Índices para tablas volcadas
--

--
-- Indices de la tabla `alerta`
--
ALTER TABLE `alerta`
  ADD PRIMARY KEY (`id_alerta`),
  ADD KEY `id_usuario` (`id_usuario`),
  ADD KEY `id_mascota` (`id_mascota`);

--
-- Indices de la tabla `articulo`
--
ALTER TABLE `articulo`
  ADD PRIMARY KEY (`id_articulo`),
  ADD KEY `id_usuario` (`id_usuario`);

--
-- Indices de la tabla `avistamiento`
--
ALTER TABLE `avistamiento`
  ADD PRIMARY KEY (`id_avistamiento`),
  ADD KEY `id_mascota` (`id_mascota`);

--
-- Indices de la tabla `foto_mascota`
--
ALTER TABLE `foto_mascota`
  ADD PRIMARY KEY (`id_foto`),
  ADD KEY `id_mascota` (`id_mascota`);

--
-- Indices de la tabla `informe`
--
ALTER TABLE `informe`
  ADD PRIMARY KEY (`id_informe`),
  ADD KEY `id_usuario` (`id_usuario`);

--
-- Indices de la tabla `mascota`
--
ALTER TABLE `mascota`
  ADD PRIMARY KEY (`id_mascota`),
  ADD KEY `id_usuario` (`id_usuario`);

--
-- Indices de la tabla `mensaje`
--
ALTER TABLE `mensaje`
  ADD PRIMARY KEY (`id_mensaje`),
  ADD KEY `id_alerta` (`id_alerta`),
  ADD KEY `usuario_emisor` (`usuario_emisor`),
  ADD KEY `usuario_receptor` (`usuario_receptor`);

--
-- Indices de la tabla `rol`
--
ALTER TABLE `rol`
  ADD PRIMARY KEY (`id_rol`);

--
-- Indices de la tabla `usuario`
--
ALTER TABLE `usuario`
  ADD PRIMARY KEY (`id_usuario`),
  ADD UNIQUE KEY `correo` (`correo`),
  ADD KEY `id_rol` (`id_rol`);

--
-- AUTO_INCREMENT de las tablas volcadas
--

--
-- AUTO_INCREMENT de la tabla `alerta`
--
ALTER TABLE `alerta`
  MODIFY `id_alerta` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `articulo`
--
ALTER TABLE `articulo`
  MODIFY `id_articulo` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT de la tabla `avistamiento`
--
ALTER TABLE `avistamiento`
  MODIFY `id_avistamiento` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `foto_mascota`
--
ALTER TABLE `foto_mascota`
  MODIFY `id_foto` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `informe`
--
ALTER TABLE `informe`
  MODIFY `id_informe` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `mascota`
--
ALTER TABLE `mascota`
  MODIFY `id_mascota` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT de la tabla `mensaje`
--
ALTER TABLE `mensaje`
  MODIFY `id_mensaje` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `rol`
--
ALTER TABLE `rol`
  MODIFY `id_rol` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT de la tabla `usuario`
--
ALTER TABLE `usuario`
  MODIFY `id_usuario` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- Restricciones para tablas volcadas
--

--
-- Filtros para la tabla `alerta`
--
ALTER TABLE `alerta`
  ADD CONSTRAINT `alerta_ibfk_1` FOREIGN KEY (`id_usuario`) REFERENCES `usuario` (`id_usuario`),
  ADD CONSTRAINT `alerta_ibfk_2` FOREIGN KEY (`id_mascota`) REFERENCES `mascota` (`id_mascota`);

--
-- Filtros para la tabla `articulo`
--
ALTER TABLE `articulo`
  ADD CONSTRAINT `articulo_ibfk_1` FOREIGN KEY (`id_usuario`) REFERENCES `usuario` (`id_usuario`);

--
-- Filtros para la tabla `avistamiento`
--
ALTER TABLE `avistamiento`
  ADD CONSTRAINT `avistamiento_ibfk_1` FOREIGN KEY (`id_mascota`) REFERENCES `mascota` (`id_mascota`);

--
-- Filtros para la tabla `foto_mascota`
--
ALTER TABLE `foto_mascota`
  ADD CONSTRAINT `foto_mascota_ibfk_1` FOREIGN KEY (`id_mascota`) REFERENCES `mascota` (`id_mascota`);

--
-- Filtros para la tabla `informe`
--
ALTER TABLE `informe`
  ADD CONSTRAINT `informe_ibfk_1` FOREIGN KEY (`id_usuario`) REFERENCES `usuario` (`id_usuario`);

--
-- Filtros para la tabla `mascota`
--
ALTER TABLE `mascota`
  ADD CONSTRAINT `mascota_ibfk_1` FOREIGN KEY (`id_usuario`) REFERENCES `usuario` (`id_usuario`);

--
-- Filtros para la tabla `mensaje`
--
ALTER TABLE `mensaje`
  ADD CONSTRAINT `mensaje_ibfk_1` FOREIGN KEY (`id_alerta`) REFERENCES `alerta` (`id_alerta`),
  ADD CONSTRAINT `mensaje_ibfk_2` FOREIGN KEY (`usuario_emisor`) REFERENCES `usuario` (`id_usuario`),
  ADD CONSTRAINT `mensaje_ibfk_3` FOREIGN KEY (`usuario_receptor`) REFERENCES `usuario` (`id_usuario`);

--
-- Filtros para la tabla `usuario`
--
ALTER TABLE `usuario`
  ADD CONSTRAINT `usuario_ibfk_1` FOREIGN KEY (`id_rol`) REFERENCES `rol` (`id_rol`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
