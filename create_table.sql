CREATE TABLE `prom_http_sd_web` (
  `prom_ip` varchar(128) COLLATE utf8_bin NOT NULL,
  `job` varchar(64) COLLATE utf8_bin NOT NULL,
  `app` varchar(128) COLLATE utf8_bin NOT NULL,
  `gp` varchar(64) COLLATE utf8_bin DEFAULT NULL COMMENT 'group',
  `target_ip` varchar(128) COLLATE utf8_bin NOT NULL,
  `target_port` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;
