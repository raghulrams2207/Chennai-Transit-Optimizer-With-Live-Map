-- ============================================================
-- CHENNAI MULTI-MODAL TRANSIT OPTIMIZER
-- REAL CHENNAI METRO / SUBURBAN RAIL CORRIDORS
-- BUS LINKS ARE REPRESENTATIVE DEMO LINKS, NOT LIVE MTC DATA
-- ============================================================

CREATE DATABASE IF NOT EXISTS transit_optimizer;
USE transit_optimizer;

SET FOREIGN_KEY_CHECKS = 0;
DROP TABLE IF EXISTS bookings;
DROP TABLE IF EXISTS connections;
DROP TABLE IF EXISTS stations;
DROP TABLE IF EXISTS routes;
DROP TABLE IF EXISTS fare_zones;
SET FOREIGN_KEY_CHECKS = 1;

-- ============================================================
-- FARE ZONES
-- ============================================================
CREATE TABLE fare_zones (
    zone_id INT PRIMARY KEY,
    zone_name VARCHAR(100) NOT NULL,
    penalty_multiplier DECIMAL(5,2) NOT NULL DEFAULT 1.00
) ENGINE=InnoDB;

INSERT INTO fare_zones VALUES
(1,'Central Chennai',1.00),
(2,'Inner Chennai',1.15),
(3,'Outer Chennai',1.30);

-- ============================================================
-- ROUTES
-- ============================================================
CREATE TABLE routes (
    route_id INT PRIMARY KEY,
    route_name VARCHAR(100) NOT NULL,
    mode ENUM('Bus','Metro','Rail') NOT NULL,
    base_fare DECIMAL(10,2) NOT NULL
) ENGINE=InnoDB;

INSERT INTO routes VALUES
(1,'Chennai Metro Blue Line','Metro',30.00),
(2,'Chennai Metro Green Line','Metro',30.00),
(3,'Chennai Beach - Tambaram Suburban','Rail',15.00),
(4,'Chennai Central - Avadi Suburban','Rail',15.00),
(5,'Chennai Beach - Chengalpattu Suburban','Rail',20.00),
(6,'MRTS Chennai Beach - Velachery','Rail',15.00),
(7,'MTC Central City Connector','Bus',10.00),
(8,'MTC Anna Nagar - CMBT Connector','Bus',12.00),
(9,'MTC Guindy - Velachery Connector','Bus',15.00),
(10,'MTC OMR Connector','Bus',18.00),
(11,'MTC West Chennai Connector','Bus',15.00);

-- ============================================================
-- STATIONS / LOCATIONS
-- 60 real Chennai locations / transit points
-- ============================================================
CREATE TABLE stations (
    station_id INT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    mode ENUM('Bus','Metro','Rail') NOT NULL,
    zone_id INT NOT NULL,
    status TINYINT(1) NOT NULL DEFAULT 1,
    FOREIGN KEY (zone_id) REFERENCES fare_zones(zone_id)
) ENGINE=InnoDB;

INSERT INTO stations VALUES
-- BLUE LINE / CENTRAL
(1,'Wimco Nagar','Metro',3,1),
(2,'Tiruvottiyur','Metro',2,1),
(3,'Tiruvottiyur Theradi','Metro',2,1),
(4,'Kaladipet','Metro',2,1),
(5,'Tollgate','Metro',1,1),
(6,'New Washermenpet','Metro',1,1),
(7,'Tondiarpet','Metro',1,1),
(8,'Sri Theagaraya College','Metro',1,1),
(9,'Washermenpet','Metro',1,1),
(10,'Mannadi','Metro',1,1),
(11,'High Court','Metro',1,1),
(12,'Chennai Central Metro','Metro',1,1),
(13,'Government Estate','Metro',1,1),
(14,'LIC','Metro',1,1),
(15,'Thousand Lights','Metro',1,1),
(16,'AG-DMS','Metro',2,1),
(17,'Teynampet','Metro',2,1),
(18,'Nandanam','Metro',2,1),
(19,'Saidapet Metro','Metro',2,1),
(20,'Little Mount','Metro',2,1),
(21,'Alandur Metro','Metro',2,1),

-- GREEN LINE
(22,'Egmore Metro','Metro',1,1),
(23,'Nehru Park','Metro',1,1),
(24,'Kilpauk','Metro',1,1),
(25,'Pachaiyappas College','Metro',1,1),
(26,'Shenoy Nagar','Metro',2,1),
(27,'Anna Nagar East','Metro',2,1),
(28,'Anna Nagar Tower','Metro',2,1),
(29,'Thirumangalam','Metro',2,1),
(30,'Koyambedu','Metro',2,1),
(31,'CMBT Metro','Metro',2,1),
(32,'Arumbakkam','Metro',2,1),
(33,'Vadapalani','Metro',2,1),
(34,'Ashok Nagar','Metro',2,1),
(35,'Ekkatuthangal','Metro',2,1),
(36,'St Thomas Mount Metro','Metro',2,1),

-- AIRPORT CORRIDOR
(37,'OTA Nanganallur Road','Metro',3,1),
(38,'Meenambakkam','Metro',3,1),
(39,'Chennai International Airport','Metro',3,1),

-- SUBURBAN RAIL
(40,'Chennai Beach','Rail',1,1),
(41,'Chennai Fort','Rail',1,1),
(42,'Chennai Park','Rail',1,1),
(43,'Chennai Egmore','Rail',1,1),
(44,'Chetpet','Rail',1,1),
(45,'Nungambakkam','Rail',1,1),
(46,'Kodambakkam','Rail',2,1),
(47,'Mambalam','Rail',2,1),
(48,'Guindy Railway','Rail',2,1),
(49,'St Thomas Mount Railway','Rail',2,1),
(50,'Tirusulam','Rail',3,1),
(51,'Pallavaram','Rail',3,1),
(52,'Chromepet','Rail',3,1),
(53,'Tambaram','Rail',3,1),
(54,'Perungalathur','Rail',3,1),
(55,'Vandalur','Rail',3,1),
(56,'Avadi','Rail',3,1),
(57,'Ambattur','Rail',3,1),
(58,'Tiruvallur','Rail',3,1),

-- BUS / INTERCHANGE LOCATIONS
(59,'Porur','Bus',3,1),
(60,'Sholinganallur','Bus',3,1);

-- ============================================================
-- CONNECTIONS
-- ============================================================
CREATE TABLE connections (
    connection_id INT PRIMARY KEY AUTO_INCREMENT,
    source_id INT NOT NULL,
    destination_id INT NOT NULL,
    route_id INT NOT NULL,
    travel_time INT NOT NULL,
    distance DECIMAL(6,2) NOT NULL,
    status TINYINT(1) NOT NULL DEFAULT 1,
    FOREIGN KEY (source_id) REFERENCES stations(station_id),
    FOREIGN KEY (destination_id) REFERENCES stations(station_id),
    FOREIGN KEY (route_id) REFERENCES routes(route_id)
) ENGINE=InnoDB;

-- ============================================================
-- BLUE LINE: real station order
-- ============================================================
INSERT INTO connections(source_id,destination_id,route_id,travel_time,distance) VALUES
(1,2,1,3,1.2),(2,3,1,3,1.1),(3,4,1,3,1.0),
(4,5,1,3,1.2),(5,6,1,3,1.1),(6,7,1,3,1.1),
(7,8,1,2,0.9),(8,9,1,2,0.9),(9,10,1,3,1.0),
(10,11,1,3,1.0),(11,12,1,3,1.1),(12,13,1,3,1.0),
(13,14,1,2,0.8),(14,15,1,3,1.0),(15,16,1,3,1.1),
(16,17,1,3,1.0),(17,18,1,3,1.0),(18,19,1,3,1.1),
(19,20,1,3,1.0),(20,21,1,3,1.1);

-- ============================================================
-- GREEN LINE: real station order
-- ============================================================
INSERT INTO connections(source_id,destination_id,route_id,travel_time,distance) VALUES
(12,22,2,4,1.4),(22,23,2,3,1.0),(23,24,2,3,1.0),
(24,25,2,3,1.0),(25,26,2,3,1.1),(26,27,2,3,1.0),
(27,28,2,2,0.8),(28,29,2,3,1.1),(29,30,2,4,1.4),
(30,31,2,3,1.1),(31,32,2,3,1.0),(32,33,2,3,1.0),
(33,34,2,3,1.1),(34,35,2,3,1.0),(35,21,2,4,1.5),
(21,36,2,3,1.2);

-- ============================================================
-- AIRPORT METRO EXTENSION / BLUE CORRIDOR
-- ============================================================
INSERT INTO connections(source_id,destination_id,route_id,travel_time,distance) VALUES
(36,37,1,4,1.5),(37,38,1,3,1.2),(38,39,1,4,1.5);

-- ============================================================
-- SUBURBAN RAIL: BEACH -> TAMBARAM
-- based on actual corridor
-- ============================================================
INSERT INTO connections(source_id,destination_id,route_id,travel_time,distance) VALUES
(40,41,3,3,1.0),(41,42,3,3,1.0),(42,43,3,4,1.4),
(43,44,3,4,1.5),(44,45,3,3,1.2),(45,46,3,3,1.2),
(46,47,3,4,1.5),(47,48,3,5,2.0),(48,49,3,4,1.5),
(49,50,3,5,2.0),(50,51,3,5,2.2),(51,52,3,4,1.7),
(52,53,3,5,2.4),(53,54,3,5,2.5),(54,55,3,5,2.5);

-- ============================================================
-- SUBURBAN RAIL: CENTRAL -> AVADI -> TIRUVALLUR
-- ============================================================
INSERT INTO connections(source_id,destination_id,route_id,travel_time,distance) VALUES
(12,42,4,4,1.2),(42,57,4,7,4.0),(57,56,4,6,3.5),
(56,58,4,8,5.0);

-- ============================================================
-- MRTS / BUS REPRESENTATION AROUND VELACHERY IS NOT USED AS
-- A live timetable; these are simplified graph links.
-- ============================================================

-- ============================================================
-- REPRESENTATIVE BUS CONNECTORS
-- These are deliberately labelled as simulated connectors.
-- They make multimodal transfer possible without claiming
-- to reproduce the live MTC timetable.
-- ============================================================
INSERT INTO connections(source_id,destination_id,route_id,travel_time,distance) VALUES
(21,59,9,15,6.0),   -- Alandur -> Porur
(59,60,10,25,12.0), -- Porur -> Sholinganallur
(60,39,10,30,15.0), -- Sholinganallur -> Airport-area connector
(30,59,11,25,11.0), -- Koyambedu -> Porur
(31,59,11,20,9.0),  -- CMBT -> Porur
(36,49,9,12,5.0),   -- St Thomas Mount -> suburban rail
(53,60,10,35,17.0), -- Tambaram -> Sholinganallur
(56,31,11,30,14.0); -- Avadi -> CMBT

-- ============================================================
-- TRANSFER LINKS BETWEEN REAL INTERCHANGE LOCATIONS
-- ============================================================
INSERT INTO connections(source_id,destination_id,route_id,travel_time,distance) VALUES
(12,42,7,5,0.5),    -- Central Metro <-> Park/Central rail area
(22,43,7,4,0.4),    -- Egmore Metro <-> Egmore Rail
(21,49,7,5,0.5),    -- Alandur Metro <-> St Thomas Mount rail area
(36,49,7,3,0.3),    -- St Thomas Mount Metro <-> Rail
(30,31,7,5,0.8),    -- Koyambedu <-> CMBT
(31,33,8,7,2.5);    -- CMBT -> Vadapalani bus/metro connector

-- ============================================================
-- MAKE THE NETWORK BIDIRECTIONAL
-- ============================================================
INSERT INTO connections
(source_id,destination_id,route_id,travel_time,distance,status)
SELECT destination_id,source_id,route_id,travel_time,distance,status
FROM connections;

-- ============================================================
-- BOOKINGS
-- ============================================================
CREATE TABLE bookings (
    booking_id INT PRIMARY KEY AUTO_INCREMENT,
    user_name VARCHAR(100) NOT NULL,
    source_id INT NOT NULL,
    destination_id INT NOT NULL,
    travel_time INT NOT NULL,
    final_cost DECIMAL(10,2) NOT NULL,
    booking_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (source_id) REFERENCES stations(station_id),
    FOREIGN KEY (destination_id) REFERENCES stations(station_id)
) ENGINE=InnoDB;

-- ============================================================
-- VERIFICATION
-- ============================================================
SELECT COUNT(*) AS total_stations FROM stations;
SELECT COUNT(*) AS total_connections FROM connections;

SELECT station_id,name,mode,zone_id
FROM stations
ORDER BY station_id;

SELECT route_id,route_name,mode,base_fare
FROM routes
ORDER BY route_id;