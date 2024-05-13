CREATE TABLE `acknowledgmentContexts` (
  `id` bigint(20) unsigned NOT NULL AUTO_INCREMENT,
  `ackid` bigint(20) unsigned NOT NULL,
  `context` text NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `id` (`id`),
  KEY `ackid` (`ackid`),
  CONSTRAINT `acknowledgmentContexts_ibfk_1` FOREIGN KEY (`ackid`) REFERENCES `acknowledgments` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
CREATE TABLE `acknowledgments` (
  `id` bigint(20) unsigned NOT NULL AUTO_INCREMENT,
  `cluster` bigint(20) unsigned DEFAULT NULL,
  `name` varchar(255) NOT NULL,
  `entType` varchar(20) DEFAULT NULL,
  `ackType` varchar(20) DEFAULT NULL,
  `paperid` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `id` (`id`),
  KEY `cluster` (`cluster`),
  KEY `name` (`name`),
  KEY `entType` (`entType`),
  KEY `ackType` (`ackType`),
  KEY `paperid` (`paperid`),
  CONSTRAINT `acknowledgments_ibfk_1` FOREIGN KEY (`paperid`) REFERENCES `papers` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
CREATE TABLE `acknowledgments_versionShadow` (
  `id` bigint(20) unsigned NOT NULL,
  `name` varchar(100) DEFAULT NULL,
  `entType` varchar(100) DEFAULT NULL,
  `ackType` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`id`),
  CONSTRAINT `acknowledgments_versionShadow_ibfk_1` FOREIGN KEY (`id`) REFERENCES `acknowledgments` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
CREATE TABLE `authors` (
  `id` bigint(20) unsigned NOT NULL AUTO_INCREMENT,
  `cluster` bigint(20) unsigned DEFAULT NULL,
  `name` varchar(100) NOT NULL,
  `affil` varchar(255) DEFAULT NULL,
  `address` varchar(255) DEFAULT NULL,
  `email` varchar(100) DEFAULT NULL,
  `ord` int(11) NOT NULL,
  `paperid` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `id` (`id`),
  KEY `cluster` (`cluster`),
  KEY `name` (`name`),
  KEY `paperid` (`paperid`),
  CONSTRAINT `authors_ibfk_1` FOREIGN KEY (`paperid`) REFERENCES `papers` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=17423653 DEFAULT CHARSET=utf8;
CREATE TABLE `authors_versionShadow` (
  `id` bigint(20) unsigned NOT NULL,
  `name` varchar(100) DEFAULT NULL,
  `affil` varchar(100) DEFAULT NULL,
  `address` varchar(100) DEFAULT NULL,
  `email` varchar(100) DEFAULT NULL,
  `ord` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`id`),
  CONSTRAINT `authors_versionShadow_ibfk_1` FOREIGN KEY (`id`) REFERENCES `authors` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
CREATE TABLE `cannames` (
  `id` bigint(20) unsigned NOT NULL AUTO_INCREMENT,
  `canname` varchar(100) DEFAULT NULL,
  `fname` varchar(30) DEFAULT NULL,
  `mname` varchar(30) DEFAULT NULL,
  `lname` varchar(30) DEFAULT NULL,
  `ndocs` int(11) DEFAULT NULL,
  `ncites` int(10) unsigned NOT NULL DEFAULT '0',
  `url` varchar(250) DEFAULT NULL,
  `affil` varchar(255) DEFAULT NULL,
  `affil2` varchar(255) DEFAULT NULL,
  `affil3` varchar(255) DEFAULT NULL,
  `address` varchar(255) DEFAULT NULL,
  `email` varchar(100) DEFAULT NULL,
  `hindex` int(10) unsigned NOT NULL DEFAULT '0',
  PRIMARY KEY (`id`),
  KEY `canname_lname` (`lname`),
  KEY `canname_fname` (`fname`)
) ENGINE=InnoDB AUTO_INCREMENT=1316233 DEFAULT CHARSET=utf8;
CREATE TABLE `checksum` (
  `sha1` varchar(100) NOT NULL,
  `paperid` varchar(100) NOT NULL,
  `filetype` varchar(10) NOT NULL,
  PRIMARY KEY (`sha1`),
  KEY `paperid` (`paperid`),
  KEY `filetype` (`filetype`),
  CONSTRAINT `checksum_ibfk_1` FOREIGN KEY (`paperid`) REFERENCES `papers` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
CREATE TABLE `citationContexts` (
  `id` bigint(20) unsigned NOT NULL AUTO_INCREMENT,
  `citationid` bigint(20) unsigned NOT NULL,
  `context` text NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `id` (`id`),
  KEY `citationid` (`citationid`),
  CONSTRAINT `citationContexts_ibfk_1` FOREIGN KEY (`citationid`) REFERENCES `citations` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=83626949 DEFAULT CHARSET=utf8;
CREATE TABLE `citations` (
  `id` bigint(20) unsigned NOT NULL AUTO_INCREMENT,
  `cluster` bigint(20) unsigned DEFAULT NULL,
  `authors` text,
  `title` varchar(255) DEFAULT NULL,
  `venue` varchar(255) DEFAULT NULL,
  `venueType` varchar(20) DEFAULT NULL,
  `year` int(11) DEFAULT NULL,
  `pages` varchar(20) DEFAULT NULL,
  `editors` text,
  `publisher` varchar(100) DEFAULT NULL,
  `pubAddress` varchar(100) DEFAULT NULL,
  `volume` int(11) DEFAULT NULL,
  `number` int(11) DEFAULT NULL,
  `tech` varchar(100) DEFAULT NULL,
  `raw` text,
  `paperid` varchar(100) NOT NULL,
  `self` tinyint(4) NOT NULL DEFAULT '0',
  PRIMARY KEY (`id`),
  UNIQUE KEY `id` (`id`),
  KEY `cluster` (`cluster`),
  KEY `title` (`title`),
  KEY `venue` (`venue`),
  KEY `venueType` (`venueType`),
  KEY `year` (`year`),
  KEY `publisher` (`publisher`),
  KEY `paperid` (`paperid`),
  KEY `self` (`self`),
  CONSTRAINT `citations_ibfk_1` FOREIGN KEY (`paperid`) REFERENCES `papers` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=86941372 DEFAULT CHARSET=utf8;
CREATE TABLE `citecharts` (
  `id` varchar(100) NOT NULL,
  `lastNcites` int(10) unsigned NOT NULL,
  `citechartData` text,
  PRIMARY KEY (`id`),
  KEY `lastNcites` (`lastNcites`),
  CONSTRAINT `citecharts_ibfk_1` FOREIGN KEY (`id`) REFERENCES `papers` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
CREATE TABLE `eTables` (
  `id` varchar(100) NOT NULL,
  `caption` varchar(200) DEFAULT NULL,
  `content` text,
  `footNote` varchar(200) DEFAULT NULL,
  `refText` varchar(200) DEFAULT NULL,
  `paperid` varchar(100) NOT NULL,
  `pageNum` int(11) NOT NULL,
  `proxyID` varchar(100) NOT NULL,
  `inDocID` int(11) DEFAULT '0',
  `updateTime` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
CREATE TABLE `elinks` (
  `paperid` varchar(100) NOT NULL,
  `label` varchar(50) NOT NULL,
  `url` varchar(255) NOT NULL,
  PRIMARY KEY (`paperid`,`label`),
  KEY `paperid` (`paperid`),
  KEY `label` (`label`),
  CONSTRAINT `elinks_ibfk_1` FOREIGN KEY (`paperid`) REFERENCES `papers` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `elinks_ibfk_2` FOREIGN KEY (`label`) REFERENCES `link_types` (`label`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
CREATE TABLE `hubMap` (
  `id` bigint(20) unsigned NOT NULL AUTO_INCREMENT,
  `urlid` bigint(20) unsigned NOT NULL,
  `hubid` bigint(20) unsigned NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `id` (`id`),
  KEY `urlid` (`urlid`),
  KEY `hubid` (`hubid`),
  CONSTRAINT `hubMap_ibfk_1` FOREIGN KEY (`urlid`) REFERENCES `urls` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `hubMap_ibfk_2` FOREIGN KEY (`hubid`) REFERENCES `hubUrls` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=5320739 DEFAULT CHARSET=utf8;
CREATE TABLE `hubUrls` (
  `id` bigint(20) unsigned NOT NULL AUTO_INCREMENT,
  `url` varchar(255) NOT NULL,
  `lastCrawl` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `repositoryID` varchar(15) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `id` (`id`),
  UNIQUE KEY `url` (`url`),
  KEY `url_2` (`url`),
  KEY `lastCrawl` (`lastCrawl`),
  KEY `repositoryID` (`repositoryID`)
) ENGINE=InnoDB AUTO_INCREMENT=1192691 DEFAULT CHARSET=utf8;
CREATE TABLE `keywords` (
  `id` bigint(20) unsigned NOT NULL AUTO_INCREMENT,
  `keyword` varchar(100) NOT NULL,
  `paperid` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `id` (`id`),
  KEY `keyword` (`keyword`),
  KEY `paperid` (`paperid`),
  CONSTRAINT `keywords_ibfk_1` FOREIGN KEY (`paperid`) REFERENCES `papers` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=4892357 DEFAULT CHARSET=utf8;
CREATE TABLE `keywords_versionShadow` (
  `id` bigint(20) unsigned NOT NULL,
  `keyword` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`id`),
  CONSTRAINT `keywords_versionShadow_ibfk_1` FOREIGN KEY (`id`) REFERENCES `keywords` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
CREATE TABLE `legacyIDMap` (
  `id` bigint(20) unsigned NOT NULL AUTO_INCREMENT,
  `paperid` varchar(100) NOT NULL,
  `legacyid` int(10) unsigned NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `id` (`id`),
  KEY `paperid` (`paperid`),
  KEY `legacyid` (`legacyid`),
  CONSTRAINT `legacyIDMap_ibfk_1` FOREIGN KEY (`paperid`) REFERENCES `papers` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=736194 DEFAULT CHARSET=utf8;
CREATE TABLE `link_types` (
  `label` varchar(50) NOT NULL,
  `baseURL` varchar(255) NOT NULL,
  PRIMARY KEY (`label`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
CREATE TABLE `paperVersions` (
  `id` bigint(20) unsigned NOT NULL AUTO_INCREMENT,
  `name` varchar(20) DEFAULT NULL,
  `paperid` varchar(100) NOT NULL,
  `version` int(11) NOT NULL,
  `repositoryID` varchar(15) NOT NULL,
  `path` varchar(255) NOT NULL,
  `deprecated` tinyint(4) NOT NULL DEFAULT '0',
  `spam` tinyint(4) NOT NULL DEFAULT '0',
  `time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `id` (`id`),
  KEY `name` (`name`),
  KEY `paperid` (`paperid`),
  KEY `version` (`version`),
  KEY `repositoryID` (`repositoryID`),
  KEY `deprecated` (`deprecated`),
  KEY `spam` (`spam`),
  CONSTRAINT `paperVersions_ibfk_1` FOREIGN KEY (`paperid`) REFERENCES `papers` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=2429269 DEFAULT CHARSET=utf8;
CREATE TABLE `paper_listing` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `paperid` varchar(100) DEFAULT NULL,
  `dates` date DEFAULT NULL,
  `operation` enum('REMOVE','LIST') DEFAULT NULL,
  `requester` varchar(100) DEFAULT NULL,
  `email` varchar(256) DEFAULT NULL,
  `reason` varchar(256) DEFAULT NULL,
  `operator` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `paperid_dates` (`paperid`,`dates`)
) ENGINE=InnoDB AUTO_INCREMENT=327774 DEFAULT CHARSET=utf8;
CREATE TABLE `papers` (
  `id` varchar(100) NOT NULL,
  `version` int(10) unsigned NOT NULL,
  `cluster` bigint(20) unsigned DEFAULT NULL,
  `title` varchar(255) DEFAULT NULL,
  `abstract` text,
  `year` int(11) DEFAULT NULL,
  `venue` varchar(255) DEFAULT NULL,
  `venueType` varchar(20) DEFAULT NULL,
  `pages` varchar(20) DEFAULT NULL,
  `volume` int(11) DEFAULT NULL,
  `number` int(11) DEFAULT NULL,
  `publisher` varchar(100) DEFAULT NULL,
  `pubAddress` varchar(100) DEFAULT NULL,
  `tech` varchar(100) DEFAULT NULL,
  `public` tinyint(4) NOT NULL DEFAULT '1',
  `ncites` int(10) unsigned NOT NULL DEFAULT '0',
  `versionName` varchar(20) DEFAULT NULL,
  `crawlDate` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `repositoryID` varchar(15) DEFAULT NULL,
  `conversionTrace` varchar(255) DEFAULT NULL,
  `selfCites` int(10) unsigned NOT NULL DEFAULT '0',
  `versionTime` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `version` (`version`),
  KEY `cluster` (`cluster`),
  KEY `title` (`title`),
  KEY `year` (`year`),
  KEY `versionName` (`versionName`),
  KEY `crawlDate` (`crawlDate`),
  KEY `repositoryID` (`repositoryID`),
  KEY `selfCites` (`selfCites`),
  KEY `versionTime` (`versionTime`),
  KEY `ncites` (`ncites`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
CREATE TABLE `papers_versionShadow` (
  `id` varchar(100) NOT NULL,
  `title` varchar(100) DEFAULT NULL,
  `abstract` varchar(100) DEFAULT NULL,
  `year` varchar(100) DEFAULT NULL,
  `venue` varchar(100) DEFAULT NULL,
  `venueType` varchar(100) DEFAULT NULL,
  `pages` varchar(100) DEFAULT NULL,
  `volume` varchar(100) DEFAULT NULL,
  `number` varchar(100) DEFAULT NULL,
  `publisher` varchar(100) DEFAULT NULL,
  `pubAddress` varchar(100) DEFAULT NULL,
  `tech` varchar(100) DEFAULT NULL,
  `citations` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`id`),
  CONSTRAINT `papers_versionShadow_ibfk_1` FOREIGN KEY (`id`) REFERENCES `papers` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
CREATE TABLE `pdfTables` (
  `id` varchar(100) NOT NULL,
  `caption` varchar(200) DEFAULT NULL,
  `content` text,
  `footNote` varchar(200) DEFAULT NULL,
  `refText` varchar(200) DEFAULT NULL,
  `paperid` varchar(100) NOT NULL,
  `pageNum` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `paperid` (`paperid`),
  CONSTRAINT `pdfTables_ibfk_1` FOREIGN KEY (`paperid`) REFERENCES `papers` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
CREATE TABLE `redirectpdf` (
  `paperid` varchar(100) NOT NULL,
  `label` varchar(20) NOT NULL,
  `externalrepoid` varchar(255) DEFAULT NULL,
  `url` varchar(1024) DEFAULT NULL,
  PRIMARY KEY (`paperid`),
  KEY `paperid` (`paperid`),
  KEY `externalrepoid` (`externalrepoid`),
  KEY `label` (`label`),
  CONSTRAINT `redirectpdf_ibfk_1` FOREIGN KEY (`paperid`) REFERENCES `papers` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `redirectpdf_ibfk_2` FOREIGN KEY (`label`) REFERENCES `redirecttemplates` (`label`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
CREATE TABLE `redirecttemplates` (
  `label` varchar(20) NOT NULL DEFAULT '',
  `urltemplate` varchar(1024) DEFAULT NULL,
  PRIMARY KEY (`label`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
CREATE TABLE `tags` (
  `id` bigint(20) unsigned NOT NULL AUTO_INCREMENT,
  `paperid` varchar(100) NOT NULL,
  `tag` varchar(50) NOT NULL,
  `count` int(10) unsigned NOT NULL DEFAULT '0',
  PRIMARY KEY (`id`),
  UNIQUE KEY `id` (`id`),
  KEY `paperid` (`paperid`),
  KEY `tag` (`tag`),
  CONSTRAINT `tags_ibfk_1` FOREIGN KEY (`paperid`) REFERENCES `papers` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=3164 DEFAULT CHARSET=utf8;
CREATE TABLE `textSources` (
  `name` varchar(50) NOT NULL,
  `content` text,
  PRIMARY KEY (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
CREATE TABLE `urls` (
  `id` bigint(20) unsigned NOT NULL AUTO_INCREMENT,
  `url` varchar(255) NOT NULL,
  `paperid` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `id` (`id`),
  KEY `url` (`url`),
  KEY `paperid` (`paperid`),
  CONSTRAINT `urls_ibfk_1` FOREIGN KEY (`paperid`) REFERENCES `papers` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=5199504 DEFAULT CHARSET=utf8;
CREATE TABLE `userCorrections` (
  `id` bigint(20) unsigned NOT NULL AUTO_INCREMENT,
  `userid` varchar(100) NOT NULL,
  `paperid` varchar(100) NOT NULL,
  `version` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `id` (`id`),
  KEY `userid` (`userid`),
  KEY `paperid` (`paperid`),
  KEY `version` (`version`),
  CONSTRAINT `userCorrections_ibfk_1` FOREIGN KEY (`paperid`) REFERENCES `papers` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=892656 DEFAULT CHARSET=utf8;
