-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Servidor: 127.0.0.1
-- Tiempo de generación: 27-08-2026 a las 18:38:13
-- Versión del servidor: 10.4.32-MariaDB
-- Versión de PHP: 8.2.12

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
  `id_alerta_origen` int(11) DEFAULT NULL,
  `estado_alerta` varchar(50) DEFAULT NULL,
  `confirmacion` varchar(50) DEFAULT NULL,
  `mensaje` text DEFAULT NULL,
  `fecha_alerta` datetime DEFAULT NULL,
  `estado_alerta_registro` tinyint(1) NOT NULL DEFAULT 1
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `alerta`
--

INSERT INTO `alerta` (`id_alerta`, `id_usuario`, `id_mascota`, `id_alerta_origen`, `estado_alerta`, `confirmacion`, `mensaje`, `fecha_alerta`, `estado_alerta_registro`) VALUES
(1, 7, 5, NULL, 'mascota_registrada', 'no', NULL, '2026-08-19 00:00:00', 1),
(2, 7, 6, NULL, 'mascota_registrada', 'no', NULL, '2026-08-19 00:00:00', 1),
(3, 7, 7, NULL, 'mascota_registrada', 'no', NULL, '2026-08-19 00:00:00', 1),
(4, 7, 8, NULL, 'mascota_registrada', 'no', NULL, '2026-08-19 00:00:00', 1),
(5, 7, 9, NULL, 'mascota_registrada', 'no', NULL, '2026-08-19 00:00:00', 1),
(6, 7, NULL, NULL, 'perfil_actualizado', 'no', NULL, '2026-08-19 00:00:00', 1),
(7, 7, 10, NULL, 'mascota_registrada', 'no', NULL, '2026-08-19 00:00:00', 1),
(8, 11, 11, NULL, 'mascota_registrada', 'no', NULL, '2026-08-27 00:00:00', 1),
(9, 11, 12, NULL, 'mascota_registrada', 'no', NULL, '2026-08-27 00:00:00', 1),
(10, 12, 11, NULL, 'coincidencia_encontrada', 'si', NULL, '2026-08-27 00:00:00', 1),
(11, 11, 11, NULL, 'mensaje_recibido', 'no', NULL, '2026-08-27 00:00:00', 1),
(12, 12, 11, NULL, 'mensaje_recibido', 'no', NULL, '2026-08-27 00:00:00', 1),
(13, 12, 11, NULL, 'mensaje_recibido', 'no', NULL, '2026-08-27 00:00:00', 1),
(14, 11, 11, NULL, 'mensaje_recibido', 'no', NULL, '2026-08-27 00:00:00', 1),
(15, 11, 11, NULL, 'mensaje_recibido', 'no', NULL, '2026-08-27 00:00:00', 1),
(16, 11, 11, NULL, 'mensaje_recibido', 'no', NULL, '2026-08-27 00:00:00', 1),
(17, 11, 11, NULL, 'mensaje_recibido', 'no', NULL, '2026-08-27 00:00:00', 1),
(18, 11, 11, NULL, 'mensaje_recibido', 'no', NULL, '2026-08-27 00:00:00', 1),
(19, 13, 12, NULL, 'coincidencia_encontrada', 'si', NULL, '2026-08-27 00:00:00', 1),
(20, 11, 12, NULL, 'mensaje_recibido', 'no', NULL, '2026-08-27 00:00:00', 1),
(21, 11, 12, NULL, 'mensaje_recibido', 'no', NULL, '2026-08-27 00:00:00', 1),
(22, 13, 11, NULL, 'coincidencia_encontrada', 'si', NULL, '2026-08-27 00:00:00', 1),
(23, 11, 11, NULL, 'mensaje_recibido', 'no', NULL, '2026-08-27 00:00:00', 1),
(24, 11, 11, NULL, 'mensaje_recibido', 'no', NULL, '2026-08-27 00:00:00', 1),
(25, 11, 11, NULL, 'mensaje_recibido', 'no', NULL, '2026-08-27 00:00:00', 1),
(26, 13, 11, NULL, 'coincidencia_encontrada', 'si', NULL, '2026-08-27 00:00:00', 1),
(27, 11, 11, NULL, 'mensaje_recibido', 'no', NULL, '2026-08-27 00:00:00', 1),
(28, 13, 12, NULL, 'coincidencia_encontrada', 'si', NULL, '2026-08-27 00:00:00', 1),
(29, 11, 12, NULL, 'mensaje_recibido', 'no', NULL, '2026-08-27 00:00:00', 1),
(30, 13, 11, NULL, 'coincidencia_encontrada', 'si', NULL, '2026-08-27 00:00:00', 1),
(31, 11, 11, NULL, 'mensaje_recibido', 'no', NULL, '2026-08-27 00:00:00', 1),
(32, 13, 11, NULL, 'coincidencia_encontrada', 'si', NULL, '2026-08-27 00:00:00', 1),
(33, 13, 11, NULL, 'coincidencia_encontrada', 'si', NULL, '2026-08-27 00:00:00', 1),
(34, 13, 11, NULL, 'coincidencia_encontrada', 'si', 'Nueva coincidencia encontrada: posible coincidencia con Sara.', '2026-08-27 11:19:03', 1);

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
  `fecha_publicacion` date DEFAULT NULL,
  `estado_articulo` tinyint(1) NOT NULL DEFAULT 1
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `articulo`
--

INSERT INTO `articulo` (`id_articulo`, `id_usuario`, `titulo`, `contenido`, `url_imagen`, `fecha_publicacion`, `estado_articulo`) VALUES
(3, 2, 'Este es un texto de prueba para saber la eficiencia de el creador de articulos', 'El Lorem Ipsum fue concebido como un texto de relleno, formateado de una cierta manera para permitir la presentación de elementos gráficos en documentos, sin necesidad de una copia formal. El uso de Lorem Ipsum permite a los diseñadores reunir los diseños y la forma del contenido antes de que el contenido se haya creado, dando al diseño y al proceso de producción más libertad.\r\n\r\nSe cree ampliamente que la historia de Lorem Ipsum se origina con Cicerón en el siglo I aC y su texto De Finibus bonorum et malorum. Esta obra filosófica, también conocida como En los extremos del bien y del mal, se dividió en cinco libros. El Lorem Ipsum que conocemos hoy se deriva de partes del primer libro Liber Primus y su discusión sobre el hedonismo, cuyas palabras habían sido alteradas, añadidas y eliminadas para convertirlas en un latín sin sentido e impropio. No se sabe exactamente cuándo el texto recibió su forma tradicional actual. Sin embargo, las referencias a la frase \"Lorem Ipsum\" se pueden encontrar en la Edición de la Biblioteca Clásica Loeb de 1914 del De Finibus en las secciones 32 y 33. Fue en esta edición del De Finibus en la que H. Rackman tradujo el texto. El siguiente fragmento se selecciona de la sección 32:\r\n\r\n\"qui dolorem ipsum, quia dolor sit amet consectetur adipisci velit, sed quia non numquam eius modi tempora incidunt, ut labore et dolore magnam aliquam quaerat voluptatem\".\r\n\r\nEsto es reconocible, en parte, como el estándar del Lorem Ipsum de hoy y fue traducido a:\r\n\r\n\"Nor again is there anyone who loves or pursues or desires to obtain pain of itself, because it is pain, but occasionally circumstances occur in which toil and pain can procure him some great pleasure\".\r\n\r\nPasando a la década de 1960, el Lorem Ipsum fue popularizado por el fabricante de tipografía Letraset, que lo utilizó en sus campañas publicitarias. Letraset ofrecía páginas de Lorem Ipsum como hojas de transferencia, que fueron ampliamente utilizadas en la era anterior a los ordenadores para los diseños. Estas páginas de transferencia, conocidas como Letraset Body Type, se incluyeron en la publicidad de la compañía y en su popular catálogo.\r\n\r\nEl Lorem Ipsum fue reintroducido en la década de 1980 por Aldus Corporation, una empresa que desarrolló Software de Publicación de Escritorio. Su producto más conocido PageMaker viene con gráficos y plantillas de procesamiento de textos previamente instaladas que contienen una versión del lenguaje latín falso.', 'https://ichef.bbci.co.uk/ace/ws/640/amz/worldservice/live/assets/images/2011/07/25/110725144827_sp_question_mark_304x171_other_nocredit.jpg.webp', '2026-05-20', 1),
(4, 7, '💡 Cinco claves para cuidar a tu perro en casa', 'Alimentación sana: Da a tu perro comida de buena calidad según su edad y tamaño.Agua limpia: Cambia el agua de su plato varias veces al día para que siempre esté fresca.Paseos diarios: Saca a tu mascota a caminar para que haga ejercicio y queme energía.Visita al veterinario: Lleva a tu animal al doctor al menos una vez al año para poner sus vacunas.Amor y juego: Dedica tiempo todos los días a jugar y acariciar a tu fiel compañero', '/static/uploads/articulos/c968c927c40e45fcad0079dbc81708ae.jpg', '2026-08-19', 1);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `avistamiento`
--

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

--
-- Volcado de datos para la tabla `avistamiento`
--

INSERT INTO `avistamiento` (`id_avistamiento`, `id_alerta`, `id_mascota`, `ubicacion`, `descripcion_avistamiento`, `url_imagen`, `fecha_avistamiento`, `estado_avistamiento`) VALUES
(1, 34, 11, 'Carrera 14A · 4.6564517, -74.0634267', 'Avistamiento reportado por Joan Guerrero.', '/static/uploads/capturas/b4d22413c3594b01aa5f992e382c6a6b.jpg', '2026-08-27 11:19:03', 1);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `foto_mascota`
--

CREATE TABLE `foto_mascota` (
  `id_foto` int(11) NOT NULL,
  `id_mascota` int(11) DEFAULT NULL,
  `url_imagen` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `foto_mascota`
--

INSERT INTO `foto_mascota` (`id_foto`, `id_mascota`, `url_imagen`) VALUES
(1, 5, '/static/uploads/mascotas/e1ec9f7cb3b84377bd4f0266ad388bee.jpg'),
(2, 5, '/static/uploads/mascotas/a500819edf13422495969cfaeb431599.jpg'),
(3, 6, '/static/uploads/mascotas/5ea21bd320d7419185378403602cc1ec.jpg'),
(4, 6, '/static/uploads/mascotas/de2433a20d7d4d71b5d5e40099237858.jpg'),
(5, 7, '/static/uploads/mascotas/56f1cf4ae58e412bb95984e2dd90e097.jpg'),
(6, 7, '/static/uploads/mascotas/b07fac64c93540afa5c5fa11e23e7ef6.jpg'),
(7, 8, '/static/uploads/mascotas/30e2c59954014f308ea45c824faa5663.jpg'),
(8, 8, '/static/uploads/mascotas/1a39581e66f64e7fb524d4145b6e1f9a.jpg'),
(9, 9, '/static/uploads/mascotas/c7805596a02b4607ac8b5753b7a7fbbf.jpg'),
(10, 9, '/static/uploads/mascotas/a4ca245f780b41ad97ea21efb356b784.jpg'),
(11, 10, '/static/uploads/mascotas/e71ea5b7d5f94046b77312c33c5b10dc.jpg'),
(12, 10, '/static/uploads/mascotas/6fbf602a36784577918207f5fdd2772c.jpg'),
(13, 11, '/static/uploads/mascotas/c3973bbb8f6b4895917c6e08ce31e055.png'),
(14, 11, '/static/uploads/mascotas/4f47b01d13bc4e90bafb08ad876debed.png'),
(15, 11, '/static/uploads/mascotas/ba096d57f7434d01b5ded8a1583a5ec0.png'),
(16, 12, '/static/uploads/mascotas/1a319b793d5a4d7e9503b144e401007b.png'),
(17, 12, '/static/uploads/mascotas/2f355a97a5d645e0affd2df421d709f9.png'),
(18, 12, '/static/uploads/mascotas/15d85450bbb440459c7e65da739567dc.png');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `informe`
--

CREATE TABLE `informe` (
  `id_informe` int(11) NOT NULL,
  `id_usuario` int(11) DEFAULT NULL,
  `tipo_informe` varchar(100) DEFAULT NULL,
  `descripcion` text DEFAULT NULL,
  `fecha_generacion` date DEFAULT NULL,
  `estado_informe` tinyint(1) NOT NULL DEFAULT 1
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `informe`
--

INSERT INTO `informe` (`id_informe`, `id_usuario`, `tipo_informe`, `descripcion`, `fecha_generacion`, `estado_informe`) VALUES
(1, 7, 'mascotas_por_fecha', 'Informe personalizado\nTipo: mascotas_por_fecha\n\n1. id_mascota: 10 | nombre_mascota: nana | estado: perdida | raza: pomeranian | fecha_registro: 2026-08-19 | usuario: Juan David\n2. id_mascota: 9 | nombre_mascota: nana | estado: en proceso | raza: pomeranian | fecha_registro: 2026-08-19 | usuario: Juan David\n3. id_mascota: 8 | nombre_mascota: dfgh | estado: perdida | raza: dfghd | fecha_registro: 2026-08-19 | usuario: Juan David\n4. id_mascota: 7 | nombre_mascota: zzzz | estado: perdida | raza: dfghdfg | fecha_registro: 2026-08-19 | usuario: Juan David\n5. id_mascota: 6 | nombre_mascota: hola | estado: perdida | raza: dfgh | fecha_registro: 2026-08-19 | usuario: Juan David\n6. id_mascota: 5 | nombre_mascota: hola | estado: perdida | raza: sdf | fecha_registro: 2026-08-19 | usuario: Juan David', '2026-08-19', 1);

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
  `estado` varchar(50) DEFAULT NULL,
  `fecha_registro` datetime DEFAULT NULL,
  `estado_mascota` tinyint(1) NOT NULL DEFAULT 1
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `mascota`
--

INSERT INTO `mascota` (`id_mascota`, `id_usuario`, `nombre_mascota`, `raza`, `edad`, `color`, `pelaje`, `tamaño`, `descripcion`, `estado`, `fecha_registro`, `estado_mascota`) VALUES
(5, 7, 'hola', 'sdf', 2, 'azul', 'corto', 'mediano', 'sdfg', 'perdida', '2026-08-19 00:00:00', 0),
(6, 7, 'hola', 'dfgh', 6, 'dgh', 'dgh', 'mediano', 'dgh', 'perdida', '2026-08-19 00:00:00', 0),
(7, 7, 'zzzz', 'dfghdfg', 12, 'dfgh', 'dfgh', 'mediano', 'dfgh', 'perdida', '2026-08-19 00:00:00', 0),
(8, 7, 'dfgh', 'dfghd', 30, 'dfgh', 'dfgh', 'mediano', 'dfgh', 'perdida', '2026-08-19 00:00:00', 0),
(9, 7, 'nana', 'pomeranian', 15, 'cafe oscuro', 'medio', 'pequeño', 'la perra es ciega,y no tiene dientes', 'en proceso', '2026-08-19 00:00:00', 0),
(10, 7, 'nana', 'pomeranian', 12, 'cafe oscuro', 'corto', 'pequeño', 'no tiene muelas', 'perdida', '2026-08-19 00:00:00', 0),
(11, 11, 'Sara', 'Criolla', 2, 'Negro', 'Liza', 'mediano', 'Tiene manchas en las patas', 'perdida', '2026-08-27 00:00:00', 1),
(12, 11, 'Pam', 'criolla', 1, 'cafe', 'corto', 'mediano', 'tiene ojos', 'perdida', '2026-08-27 00:00:00', 1);

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
  `url_imagen` varchar(255) DEFAULT NULL,
  `fecha_envio` datetime DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `mensaje`
--

INSERT INTO `mensaje` (`id_mensaje`, `id_alerta`, `usuario_emisor`, `usuario_receptor`, `mensaje_chat`, `url_imagen`, `fecha_envio`) VALUES
(1, 10, 12, 11, 'Hola bro, tu perra esta  en la casa ñ', NULL, '2026-08-27 09:44:56'),
(2, 10, 11, 12, 'Holi bro, como vas?', NULL, '2026-08-27 09:46:21'),
(3, 10, 11, 12, 'Si si, ya la encontre', NULL, '2026-08-27 09:46:33'),
(4, 10, 12, 11, 'Cll 49 C bis A sur #2D-09 Este', NULL, '2026-08-27 09:47:15'),
(5, 10, 12, 11, 'Hijueputa', NULL, '2026-08-27 09:47:28'),
(6, 10, 12, 11, 'Perra', NULL, '2026-08-27 09:47:38'),
(7, 10, 12, 11, 'hola', NULL, '2026-08-27 09:47:56'),
(8, 10, 12, 11, 'Estupidoo', NULL, '2026-08-27 09:48:10'),
(9, 19, 13, 11, 'Hola', NULL, '2026-08-27 09:54:31'),
(10, 19, 13, 11, 'Hi', NULL, '2026-08-27 09:54:36'),
(11, 22, 13, 11, 'Hi', NULL, '2026-08-27 09:54:50'),
(12, 22, 13, 11, 'Hola', NULL, '2026-08-27 09:55:42'),
(13, 10, 12, 11, 'uykhjjh', NULL, '2026-08-27 10:47:28'),
(14, 26, 13, 11, 'Compartió una foto tomada para la alerta sobre Sara.', NULL, '2026-08-27 11:03:55'),
(15, 26, 13, 11, 'Sara', NULL, '2026-08-27 11:04:00'),
(16, 28, 13, 11, 'Compartió una foto tomada para la alerta sobre Pam.', NULL, '2026-08-27 11:04:12'),
(17, 28, 13, 11, 'Pam', NULL, '2026-08-27 11:04:16'),
(18, 30, 13, 11, 'Compartió una foto tomada para la alerta sobre Sara.', NULL, '2026-08-27 11:04:54'),
(19, 30, 13, 11, 'Sara', NULL, '2026-08-27 11:04:59'),
(20, 32, 13, 11, 'Compartió una foto tomada para la alerta sobre Sara.', NULL, '2026-08-27 11:12:26'),
(21, 34, 13, 11, 'Compartió una foto tomada para la alerta sobre Sara.', '/static/uploads/capturas/b4d22413c3594b01aa5f992e382c6a6b.jpg', '2026-08-27 11:19:03');

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
  `foto_perfil` varchar(255) DEFAULT NULL,
  `google_id` varchar(100) DEFAULT NULL,
  `facebook_id` varchar(100) DEFAULT NULL,
  `fecha_registro` date DEFAULT NULL,
  `preferencias` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL CHECK (json_valid(`preferencias`)),
  `estado_usuario` tinyint(1) NOT NULL DEFAULT 1
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `usuario`
--

INSERT INTO `usuario` (`id_usuario`, `id_rol`, `nombre_completo`, `telefono`, `correo`, `contraseña`, `foto_perfil`, `google_id`, `facebook_id`, `fecha_registro`, `preferencias`, `estado_usuario`) VALUES
(2, 1, 'Sebastian', '1234567891', 'holi@gmail.com', 'scrypt:32768:8:1$TDcUsvkYyP1WzW9q$f3fce03b73283ba6d34a2a2c125582cfdb97bd0f9de98ef24b1921306940297a7e3a3f1499ad278b975d787f469fe5de137e491de9b14a945dc8377df7a6ec7f', NULL, NULL, NULL, NULL, '{\"tema\": \"claro\", \"reducir_movimiento\": false}', 0),
(5, 2, 'Juan Davñ+id', '1234567891', 'julian1233@gmail.com', 'scrypt:32768:8:1$i73NWbdyfMGi1PE3$16ed09b31535149ca86a6c029e460b8c5a5fc19d22e886519542df0058673ade8df5c477c283bd121929167e72609f1932fff8f6fef4967c2719d653973b6c1e', NULL, NULL, NULL, NULL, '{\"tema\": \"claro\", \"reducir_movimiento\": false}', 0),
(7, 2, 'Juan David', '3168110222', 'davidrigrillo10@gmail.com', 'scrypt:32768:8:1$Wzp24f0VcfSUy57y$0a13bdb870551e6779fff9afb842d03cceb59fb275cc3e2862920d3db3d4a814ea29287684aa863f7fb5d7ffb8f71ec9528250355ad67e30bdcaf7ecc58f6de4', '/static/uploads/perfiles/5210dc31f9b24765a2e8e82d8e88e721.jpg', '103992112638203136698', NULL, NULL, '{\"tema\": \"sepia\", \"reducir_movimiento\": true}', 1),
(8, 1, 'david', '3249304044', 'davidgrillo1499@gmail.com', 'scrypt:32768:8:1$YYxyVvUmkEqV9JCB$485208e321b783695b31de8d87b3214e777605ff336684d192555e14f2b82403249c7a86e0263956abd86331c2c062b4139eb30f49d226d2db24cbede4f07651', NULL, NULL, '122230511810281715', NULL, '{\"tema\": \"claro\", \"reducir_movimiento\": false}', 1),
(9, 1, 'Juan', '3138373593', 'softmode1422@gmail.com', 'scrypt:32768:8:1$9t31ZXQyj8pFk6EF$b38e733dd0808cdc45575139e87f025df4a23eda32515aa5160d762fee95eb8e33c1a2f4d84065f82b34e6fb874ed8a85757e4a5dae474a52c8e24fcd4ae7e42', NULL, NULL, NULL, NULL, '{\"tema\": \"claro\", \"reducir_movimiento\": false}', 1),
(11, 1, 'Joan Sebastian Guerrero Cristancho', NULL, 'joanguerrero913@gmail.com', 'scrypt:32768:8:1$mEQX4012oRoJOmqY$ebc2261edbb407b3f0db269ab895af85d94480ba5cf3711a1a0db68876bbe9312441e999391afafee4f5ae59710f601c5eb98ead9ff15f8ac191aa6c7a6758b3', 'https://lh3.googleusercontent.com/a/ACg8ocJ-YQKaSs_bJ_dsN4qnjlcx_9zoQj2essiNtn5Ng6ochb0IGHs=s96-c', '104708668906736913529', NULL, '2026-08-19', '{\"tema\": \"claro\", \"reducir_movimiento\": false}', 1),
(12, 1, 'Daniel Londoño', NULL, 'danielondono08@gmail.com', 'scrypt:32768:8:1$6QpnwYG0a00dZjVw$9182c0a20600df69a5b73c6c5b66a21c70fbdc8eafd7577089c40bd304f3cba39cf64344abb2e7914ec343aba5dd19f041fd3a4bb5df66f44de9b813b0c211e2', 'https://lh3.googleusercontent.com/a/ACg8ocLZL0yMbSR0c8nfGFrmMKdVLMq17JhnvsO57oDA-Lw8uob00w=s96-c', '101233084825760661237', NULL, '2026-08-27', NULL, 1),
(13, 2, 'Joan Guerrero', '1234567891', 'joansguerreroc2007@gmail.com', 'scrypt:32768:8:1$GtqmtVBP7oql0gVv$08d22868f22fd37e3fd16c24aabce8d7bd12d82fbdfba443ecf09e28d9840e7bb8f96ee62851135a1ec69fdb13dd10f6e34e8ce38200ff37cb7885dd8c70a5c1', NULL, NULL, NULL, '2026-08-27', NULL, 1);

--
-- Índices para tablas volcadas
--

--
-- Indices de la tabla `alerta`
--
ALTER TABLE `alerta`
  ADD PRIMARY KEY (`id_alerta`),
  ADD KEY `id_usuario` (`id_usuario`),
  ADD KEY `id_mascota` (`id_mascota`),
  ADD KEY `idx_alerta_origen` (`id_alerta_origen`);

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
  ADD KEY `id_mascota` (`id_mascota`),
  ADD KEY `idx_avistamiento_alerta` (`id_alerta`);

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
  ADD UNIQUE KEY `google_id` (`google_id`),
  ADD UNIQUE KEY `facebook_id` (`facebook_id`),
  ADD KEY `id_rol` (`id_rol`);

--
-- AUTO_INCREMENT de las tablas volcadas
--

--
-- AUTO_INCREMENT de la tabla `alerta`
--
ALTER TABLE `alerta`
  MODIFY `id_alerta` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=35;

--
-- AUTO_INCREMENT de la tabla `articulo`
--
ALTER TABLE `articulo`
  MODIFY `id_articulo` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- AUTO_INCREMENT de la tabla `avistamiento`
--
ALTER TABLE `avistamiento`
  MODIFY `id_avistamiento` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT de la tabla `foto_mascota`
--
ALTER TABLE `foto_mascota`
  MODIFY `id_foto` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=19;

--
-- AUTO_INCREMENT de la tabla `informe`
--
ALTER TABLE `informe`
  MODIFY `id_informe` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT de la tabla `mascota`
--
ALTER TABLE `mascota`
  MODIFY `id_mascota` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=13;

--
-- AUTO_INCREMENT de la tabla `mensaje`
--
ALTER TABLE `mensaje`
  MODIFY `id_mensaje` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=22;

--
-- AUTO_INCREMENT de la tabla `rol`
--
ALTER TABLE `rol`
  MODIFY `id_rol` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT de la tabla `usuario`
--
ALTER TABLE `usuario`
  MODIFY `id_usuario` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=14;

--
-- Restricciones para tablas volcadas
--

--
-- Filtros para la tabla `alerta`
--
ALTER TABLE `alerta`
  ADD CONSTRAINT `alerta_ibfk_1` FOREIGN KEY (`id_usuario`) REFERENCES `usuario` (`id_usuario`),
  ADD CONSTRAINT `alerta_ibfk_2` FOREIGN KEY (`id_mascota`) REFERENCES `mascota` (`id_mascota`),
  ADD CONSTRAINT `alerta_ibfk_3` FOREIGN KEY (`id_alerta_origen`) REFERENCES `alerta` (`id_alerta`);

--
-- Filtros para la tabla `articulo`
--
ALTER TABLE `articulo`
  ADD CONSTRAINT `articulo_ibfk_1` FOREIGN KEY (`id_usuario`) REFERENCES `usuario` (`id_usuario`);

--
-- Filtros para la tabla `avistamiento`
--
ALTER TABLE `avistamiento`
  ADD CONSTRAINT `avistamiento_ibfk_1` FOREIGN KEY (`id_mascota`) REFERENCES `mascota` (`id_mascota`),
  ADD CONSTRAINT `avistamiento_ibfk_2` FOREIGN KEY (`id_alerta`) REFERENCES `alerta` (`id_alerta`);

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
