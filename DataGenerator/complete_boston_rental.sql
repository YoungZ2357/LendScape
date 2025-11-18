-- COMPLETE BOSTON RENTAL PLATFORM DATA
-- Generated with geographically accurate Boston addresses

-- LOCATIONS

INSERT INTO lendscapev1."Location" (locationId, address, city, state, country, postcode, is_default) VALUES
  (1, '829 Boylston Street', 'Boston', 'MA', 'USA', '02116', true);
INSERT INTO lendscapev1."Location" (locationId, address, city, state, country, postcode, is_default) VALUES
  (2, '1784 Washington Street, Apt 3D', 'Boston', 'MA', 'USA', '02118', true);
INSERT INTO lendscapev1."Location" (locationId, address, city, state, country, postcode, is_default) VALUES
  (3, '82 Fenway, Apt 3B', 'Boston', 'MA', 'USA', '02215', true);
INSERT INTO lendscapev1."Location" (locationId, address, city, state, country, postcode, is_default) VALUES
  (4, '128 Charles Street, Apt 1D', 'Boston', 'MA', 'USA', '02114', true);
INSERT INTO lendscapev1."Location" (locationId, address, city, state, country, postcode, is_default) VALUES
  (5, '183 Garden Street, Apt 2C', 'Cambridge', 'MA', 'USA', '02138', true);
INSERT INTO lendscapev1."Location" (locationId, address, city, state, country, postcode, is_default) VALUES
  (6, '257 Brighton Avenue, Apt 3D', 'Boston', 'MA', 'USA', '02134', true);
INSERT INTO lendscapev1."Location" (locationId, address, city, state, country, postcode, is_default) VALUES
  (7, '24 Pond Street, Apt 1B', 'Boston', 'MA', 'USA', '02130', true);
INSERT INTO lendscapev1."Location" (locationId, address, city, state, country, postcode, is_default) VALUES
  (8, '50 Prince Street', 'Boston', 'MA', 'USA', '02113', true);
INSERT INTO lendscapev1."Location" (locationId, address, city, state, country, postcode, is_default) VALUES
  (9, '297 Newbury Street, Apt 1D', 'Boston', 'MA', 'USA', '02116', true);
INSERT INTO lendscapev1."Location" (locationId, address, city, state, country, postcode, is_default) VALUES
  (10, '263 Shawmut Avenue, Apt 1A', 'Boston', 'MA', 'USA', '02118', true);
INSERT INTO lendscapev1."Location" (locationId, address, city, state, country, postcode, is_default) VALUES
  (11, '1349 Boylston Street, Apt 3D', 'Boston', 'MA', 'USA', '02215', true);
INSERT INTO lendscapev1."Location" (locationId, address, city, state, country, postcode, is_default) VALUES
  (12, '123 Charles Street, Apt 3D', 'Boston', 'MA', 'USA', '02114', true);
INSERT INTO lendscapev1."Location" (locationId, address, city, state, country, postcode, is_default) VALUES
  (13, '1577 Massachusetts Avenue', 'Cambridge', 'MA', 'USA', '02138', true);
INSERT INTO lendscapev1."Location" (locationId, address, city, state, country, postcode, is_default) VALUES
  (14, '162 Harvard Avenue', 'Boston', 'MA', 'USA', '02134', true);
INSERT INTO lendscapev1."Location" (locationId, address, city, state, country, postcode, is_default) VALUES
  (15, '54 South Street, Apt 1C', 'Boston', 'MA', 'USA', '02130', true);
INSERT INTO lendscapev1."Location" (locationId, address, city, state, country, postcode, is_default) VALUES
  (16, '62 Prince Street, Apt 4C', 'Boston', 'MA', 'USA', '02113', true);
INSERT INTO lendscapev1."Location" (locationId, address, city, state, country, postcode, is_default) VALUES
  (17, '42 Newbury Street, Apt 1B', 'Boston', 'MA', 'USA', '02116', true);
INSERT INTO lendscapev1."Location" (locationId, address, city, state, country, postcode, is_default) VALUES
  (18, '561 Columbus Avenue, Apt 4D', 'Boston', 'MA', 'USA', '02118', true);
INSERT INTO lendscapev1."Location" (locationId, address, city, state, country, postcode, is_default) VALUES
  (19, '75 Fenway', 'Boston', 'MA', 'USA', '02215', true);
INSERT INTO lendscapev1."Location" (locationId, address, city, state, country, postcode, is_default) VALUES
  (20, '139 Charles Street, Apt 1B', 'Boston', 'MA', 'USA', '02114', true);

-- USERS

INSERT INTO lendscapev1."User" (userId, firstName, lastName, email, locationId, phoneNumber, class, pwd, status) VALUES
  (1, 'Christopher', 'Williams', 'cwilliams@outlook.com', 1, 8573244764, 'active', '7c6a180b36896a0a8c02', 'active');
INSERT INTO lendscapev1."User" (userId, firstName, lastName, email, locationId, phoneNumber, class, pwd, status) VALUES
  (2, 'Jacob', 'Sullivan', 'jacob17@hotmail.com', 2, 8573244764, 'admin', '6cb75f652a9b52798eb6', 'active');
INSERT INTO lendscapev1."User" (userId, firstName, lastName, email, locationId, phoneNumber, class, pwd, status) VALUES
  (3, 'Austin', 'Wong', 'austin.wong@hotmail.com', 3, 8573244764, 'active', '819b0643d6b89dc9b579', 'active');
INSERT INTO lendscapev1."User" (userId, firstName, lastName, email, locationId, phoneNumber, class, pwd, status) VALUES
  (4, 'Tina', 'Reed', 'tinar@hotmail.com', 4, 8573244764, 'admin', '34cc93ece0ba9e3f6f23', 'active');
INSERT INTO lendscapev1."User" (userId, firstName, lastName, email, locationId, phoneNumber, class, pwd, status) VALUES
  (5, 'Kimberly', 'Miller', 'kmiller@hotmail.com', 5, 8573244764, 'active', 'db0edd04aaac4506f7ed', 'active');
INSERT INTO lendscapev1."User" (userId, firstName, lastName, email, locationId, phoneNumber, class, pwd, status) VALUES
  (6, 'Kaitlin', 'Reid', 'kaitlin.reid@gmail.com', 6, 8573244764, 'inactive', '218dd27aebeccecae69a', 'banned');
INSERT INTO lendscapev1."User" (userId, firstName, lastName, email, locationId, phoneNumber, class, pwd, status) VALUES
  (7, 'Danielle', 'James', 'danielle.james@gmail.com', 7, 8573244764, 'inactive', '00cdb7bb942cf6b290ce', 'active');
INSERT INTO lendscapev1."User" (userId, firstName, lastName, email, locationId, phoneNumber, class, pwd, status) VALUES
  (8, 'Miguel', 'Johnson', 'mjohnson@yahoo.com', 8, 8573244764, 'inactive', 'b25ef06be3b6948c0bc4', 'active');
INSERT INTO lendscapev1."User" (userId, firstName, lastName, email, locationId, phoneNumber, class, pwd, status) VALUES
  (9, 'Johnny', 'Andrews', 'jandrews@outlook.com', 9, 8573244764, 'inactive', '5d69dd95ac183c964378', 'active');
INSERT INTO lendscapev1."User" (userId, firstName, lastName, email, locationId, phoneNumber, class, pwd, status) VALUES
  (10, 'Aaron', 'Allen', 'aarona@gmail.com', 10, 8573244764, 'inactive', '87e897e3b54a405da144', 'active');
INSERT INTO lendscapev1."User" (userId, firstName, lastName, email, locationId, phoneNumber, class, pwd, status) VALUES
  (11, 'William', 'Meadows', 'william21@gmail.com', 11, 8573244764, 'inactive', '1e5c2776cf544e213c3d', 'active');
INSERT INTO lendscapev1."User" (userId, firstName, lastName, email, locationId, phoneNumber, class, pwd, status) VALUES
  (12, 'Alexander', 'Murphy', 'alexanderm@outlook.com', 12, 8573244764, 'inactive', 'c24a542f884e144451f9', 'active');
INSERT INTO lendscapev1."User" (userId, firstName, lastName, email, locationId, phoneNumber, class, pwd, status) VALUES
  (13, 'Paul', 'Walsh', 'paul84@outlook.com', 13, 8573244764, 'inactive', 'ee684912c7e588d03ccb', 'active');
INSERT INTO lendscapev1."User" (userId, firstName, lastName, email, locationId, phoneNumber, class, pwd, status) VALUES
  (14, 'Jason', 'Henderson', 'jason.henderson@gmail.com', 14, 8573244764, 'admin', '8ee736784ce419bd1655', 'active');
INSERT INTO lendscapev1."User" (userId, firstName, lastName, email, locationId, phoneNumber, class, pwd, status) VALUES
  (15, 'Mike', 'Jones', 'mikej@gmail.com', 15, 8573244764, 'inactive', '9141fea0574f83e190ab', 'active');
INSERT INTO lendscapev1."User" (userId, firstName, lastName, email, locationId, phoneNumber, class, pwd, status) VALUES
  (16, 'Courtney', 'Gonzalez', 'courtneyg@gmail.com', 16, 8573244764, 'active', '2b40aaa979727c43411c', 'active');
INSERT INTO lendscapev1."User" (userId, firstName, lastName, email, locationId, phoneNumber, class, pwd, status) VALUES
  (17, 'Jennifer', 'Espinoza', 'jennifer87@outlook.com', 17, 8573244764, 'inactive', 'a63f9709abc75bf8bd8f', 'active');
INSERT INTO lendscapev1."User" (userId, firstName, lastName, email, locationId, phoneNumber, class, pwd, status) VALUES
  (18, 'Ashley', 'Goodman', 'ashleyg@hotmail.com', 18, 8573244764, 'inactive', '80b8bdceb474b5127b6a', 'active');
INSERT INTO lendscapev1."User" (userId, firstName, lastName, email, locationId, phoneNumber, class, pwd, status) VALUES
  (19, 'Todd', 'Mccormick', 'toddm@gmail.com', 19, 8573244764, 'inactive', 'e532ae6f28f4c2be70b5', 'active');
INSERT INTO lendscapev1."User" (userId, firstName, lastName, email, locationId, phoneNumber, class, pwd, status) VALUES
  (20, 'Christine', 'Bailey', 'christine.bailey@gmail.com', 20, 8573244764, 'inactive', 'aee67d9bb569ad1562f7', 'active');

-- ITEMS

INSERT INTO lendscapev1."Item" (itemId, itemName, userId, description, price, image_url, is_available) VALUES
  (1, 'Singing Machine Karaoke Machine', 16, 'Singing Machine Karaoke Machine in like new condition. Well maintained and ready to rent.', 52.76, 'https://example.com/images/party/1.jpg', false);
INSERT INTO lendscapev1."Item" (itemId, itemName, userId, description, price, image_url, is_available) VALUES
  (2, 'Canon DSLR Camera', 10, 'Canon DSLR Camera in like new condition. Well maintained and ready to rent.', 60.29, 'https://example.com/images/electronics/2.jpg', true);
INSERT INTO lendscapev1."Item" (itemId, itemName, userId, description, price, image_url, is_available) VALUES
  (3, 'Milwaukee Nail Gun', 5, 'Rent my Milwaukee Nail Gun! Good condition, perfect for your needs.', 33.6, 'https://example.com/images/tools/3.jpg', false);
INSERT INTO lendscapev1."Item" (itemId, itemName, userId, description, price, image_url, is_available) VALUES
  (4, 'REI Hiking Backpack', 3, 'Rent my REI Hiking Backpack! Excellent condition, perfect for your needs.', 26.7, 'https://example.com/images/outdoor/4.jpg', false);
INSERT INTO lendscapev1."Item" (itemId, itemName, userId, description, price, image_url, is_available) VALUES
  (5, 'Callaway Golf Clubs', 16, 'Callaway Golf Clubs in excellent condition. Well maintained and ready to rent.', 74.37, 'https://example.com/images/sports/5.jpg', true);
INSERT INTO lendscapev1."Item" (itemId, itemName, userId, description, price, image_url, is_available) VALUES
  (6, 'Wilson Tennis Racket', 10, 'Rent my Wilson Tennis Racket! Like New condition, perfect for your needs.', 20.52, 'https://example.com/images/sports/6.jpg', true);
INSERT INTO lendscapev1."Item" (itemId, itemName, userId, description, price, image_url, is_available) VALUES
  (7, 'Coleman Camping Stove', 13, 'Rent my Coleman Camping Stove! Like New condition, perfect for your needs.', 26.82, 'https://example.com/images/outdoor/7.jpg', true);
INSERT INTO lendscapev1."Item" (itemId, itemName, userId, description, price, image_url, is_available) VALUES
  (8, 'Yeti Cooler', 1, '2019 Yeti Cooler. Good condition, includes all accessories.', 30.08, 'https://example.com/images/outdoor/8.jpg', true);
INSERT INTO lendscapev1."Item" (itemId, itemName, userId, description, price, image_url, is_available) VALUES
  (9, 'Trek Mountain Bike', 16, 'Rent my Trek Mountain Bike! Very Good condition, perfect for your needs.', 37.5, 'https://example.com/images/outdoor/9.jpg', true);
INSERT INTO lendscapev1."Item" (itemId, itemName, userId, description, price, image_url, is_available) VALUES
  (10, 'Singing Machine Karaoke Machine', 5, '2023 Singing Machine Karaoke Machine. Like New condition, includes all accessories.', 79.6, 'https://example.com/images/party/10.jpg', true);
INSERT INTO lendscapev1."Item" (itemId, itemName, userId, description, price, image_url, is_available) VALUES
  (11, 'Epson Projector', 1, 'Rent my Epson Projector! Excellent condition, perfect for your needs.', 67.92, 'https://example.com/images/electronics/11.jpg', true);
INSERT INTO lendscapev1."Item" (itemId, itemName, userId, description, price, image_url, is_available) VALUES
  (12, 'REI Hiking Backpack', 10, 'REI Hiking Backpack in like new condition. Well maintained and ready to rent.', 27.8, 'https://example.com/images/outdoor/12.jpg', true);
INSERT INTO lendscapev1."Item" (itemId, itemName, userId, description, price, image_url, is_available) VALUES
  (13, 'Coleman Camping Stove', 13, 'Coleman Camping Stove in good condition. Well maintained and ready to rent.', 23.58, 'https://example.com/images/outdoor/13.jpg', true);
INSERT INTO lendscapev1."Item" (itemId, itemName, userId, description, price, image_url, is_available) VALUES
  (14, 'Rossignol Ski Equipment', 3, 'Rossignol Ski Equipment in like new condition. Well maintained and ready to rent.', 57.08, 'https://example.com/images/sports/14.jpg', true);
INSERT INTO lendscapev1."Item" (itemId, itemName, userId, description, price, image_url, is_available) VALUES
  (15, 'Burton Snowboard', 3, 'Burton Snowboard in good condition. Well maintained and ready to rent.', 50.7, 'https://example.com/images/sports/15.jpg', true);
INSERT INTO lendscapev1."Item" (itemId, itemName, userId, description, price, image_url, is_available) VALUES
  (16, 'Black & Decker Sander', 5, '2021 Black & Decker Sander. Very Good condition, includes all accessories.', 19.94, 'https://example.com/images/tools/16.jpg', true);
INSERT INTO lendscapev1."Item" (itemId, itemName, userId, description, price, image_url, is_available) VALUES
  (17, 'Catch Surf Surfboard', 16, 'Rent my Catch Surf Surfboard! Excellent condition, perfect for your needs.', 54.27, 'https://example.com/images/sports/17.jpg', true);
INSERT INTO lendscapev1."Item" (itemId, itemName, userId, description, price, image_url, is_available) VALUES
  (18, 'REI Hiking Backpack', 3, 'Rent my REI Hiking Backpack! Good condition, perfect for your needs.', 33.51, 'https://example.com/images/outdoor/18.jpg', true);
INSERT INTO lendscapev1."Item" (itemId, itemName, userId, description, price, image_url, is_available) VALUES
  (19, 'GoPro Hero', 13, '2021 GoPro Hero. Excellent condition, includes all accessories.', 34.71, 'https://example.com/images/electronics/19.jpg', true);
INSERT INTO lendscapev1."Item" (itemId, itemName, userId, description, price, image_url, is_available) VALUES
  (20, 'Red Paddleboard', 1, '2024 Red Paddleboard. Good condition, includes all accessories.', 47.57, 'https://example.com/images/sports/20.jpg', true);
INSERT INTO lendscapev1."Item" (itemId, itemName, userId, description, price, image_url, is_available) VALUES
  (21, 'Epson Projector', 13, '2023 Epson Projector. Excellent condition, includes all accessories.', 69.79, 'https://example.com/images/electronics/21.jpg', true);
INSERT INTO lendscapev1."Item" (itemId, itemName, userId, description, price, image_url, is_available) VALUES
  (22, 'North Face Sleeping Bag', 10, '2020 North Face Sleeping Bag. Like New condition, includes all accessories.', 27.3, 'https://example.com/images/outdoor/22.jpg', true);
INSERT INTO lendscapev1."Item" (itemId, itemName, userId, description, price, image_url, is_available) VALUES
  (23, 'DeWalt Drill', 16, 'DeWalt Drill in very good condition. Well maintained and ready to rent.', 26.44, 'https://example.com/images/tools/23.jpg', true);
INSERT INTO lendscapev1."Item" (itemId, itemName, userId, description, price, image_url, is_available) VALUES
  (24, 'Coleman Tent', 1, '2023 Coleman Tent. Very Good condition, includes all accessories.', 33.22, 'https://example.com/images/outdoor/24.jpg', true);
INSERT INTO lendscapev1."Item" (itemId, itemName, userId, description, price, image_url, is_available) VALUES
  (25, 'Pioneer DJ Controller', 10, 'Rent my Pioneer DJ Controller! Good condition, perfect for your needs.', 71.04, 'https://example.com/images/electronics/25.jpg', true);
INSERT INTO lendscapev1."Item" (itemId, itemName, userId, description, price, image_url, is_available) VALUES
  (26, 'Pioneer DJ Controller', 16, 'Rent my Pioneer DJ Controller! Excellent condition, perfect for your needs.', 65.32, 'https://example.com/images/electronics/26.jpg', true);
INSERT INTO lendscapev1."Item" (itemId, itemName, userId, description, price, image_url, is_available) VALUES
  (27, 'Ryobi Pressure Washer', 1, 'Rent my Ryobi Pressure Washer! Good condition, perfect for your needs.', 57.46, 'https://example.com/images/tools/27.jpg', true);
INSERT INTO lendscapev1."Item" (itemId, itemName, userId, description, price, image_url, is_available) VALUES
  (28, 'Catch Surf Surfboard', 5, '2019 Catch Surf Surfboard. Excellent condition, includes all accessories.', 54.2, 'https://example.com/images/sports/28.jpg', true);
INSERT INTO lendscapev1."Item" (itemId, itemName, userId, description, price, image_url, is_available) VALUES
  (29, 'Makita Circular Saw', 13, 'Rent my Makita Circular Saw! Like New condition, perfect for your needs.', 38.84, 'https://example.com/images/tools/29.jpg', false);
INSERT INTO lendscapev1."Item" (itemId, itemName, userId, description, price, image_url, is_available) VALUES
  (30, 'Bosch Tile Cutter', 3, 'Bosch Tile Cutter in excellent condition. Well maintained and ready to rent.', 34.58, 'https://example.com/images/tools/30.jpg', true);
INSERT INTO lendscapev1."Item" (itemId, itemName, userId, description, price, image_url, is_available) VALUES
  (31, 'JBL Speaker System', 5, 'JBL Speaker System in good condition. Well maintained and ready to rent.', 87.93, 'https://example.com/images/party/31.jpg', true);
INSERT INTO lendscapev1."Item" (itemId, itemName, userId, description, price, image_url, is_available) VALUES
  (32, 'Trek Mountain Bike', 10, '2021 Trek Mountain Bike. Excellent condition, includes all accessories.', 56.44, 'https://example.com/images/outdoor/32.jpg', false);
INSERT INTO lendscapev1."Item" (itemId, itemName, userId, description, price, image_url, is_available) VALUES
  (33, 'Makita Circular Saw', 16, '2023 Makita Circular Saw. Good condition, includes all accessories.', 30.18, 'https://example.com/images/tools/33.jpg', true);
INSERT INTO lendscapev1."Item" (itemId, itemName, userId, description, price, image_url, is_available) VALUES
  (34, 'Epson Projector', 13, 'Rent my Epson Projector! Good condition, perfect for your needs.', 67.79, 'https://example.com/images/electronics/34.jpg', true);
INSERT INTO lendscapev1."Item" (itemId, itemName, userId, description, price, image_url, is_available) VALUES
  (35, 'Callaway Golf Clubs', 13, 'Callaway Golf Clubs in good condition. Well maintained and ready to rent.', 53.31, 'https://example.com/images/sports/35.jpg', true);
INSERT INTO lendscapev1."Item" (itemId, itemName, userId, description, price, image_url, is_available) VALUES
  (36, 'Rossignol Ski Equipment', 1, 'Rossignol Ski Equipment in excellent condition. Well maintained and ready to rent.', 79.03, 'https://example.com/images/sports/36.jpg', true);
INSERT INTO lendscapev1."Item" (itemId, itemName, userId, description, price, image_url, is_available) VALUES
  (37, 'Pelican Kayak', 3, 'Pelican Kayak in like new condition. Well maintained and ready to rent.', 47.08, 'https://example.com/images/outdoor/37.jpg', false);
INSERT INTO lendscapev1."Item" (itemId, itemName, userId, description, price, image_url, is_available) VALUES
  (38, 'Yeti Cooler', 1, 'Rent my Yeti Cooler! Good condition, perfect for your needs.', 31.1, 'https://example.com/images/outdoor/38.jpg', true);
INSERT INTO lendscapev1."Item" (itemId, itemName, userId, description, price, image_url, is_available) VALUES
  (39, 'Bosch Tile Cutter', 3, '2021 Bosch Tile Cutter. Excellent condition, includes all accessories.', 35.14, 'https://example.com/images/tools/39.jpg', false);
INSERT INTO lendscapev1."Item" (itemId, itemName, userId, description, price, image_url, is_available) VALUES
  (40, 'Bosch Tile Cutter', 3, 'Bosch Tile Cutter in like new condition. Well maintained and ready to rent.', 29.51, 'https://example.com/images/tools/40.jpg', true);
INSERT INTO lendscapev1."Item" (itemId, itemName, userId, description, price, image_url, is_available) VALUES
  (41, 'Canon DSLR Camera', 10, '2023 Canon DSLR Camera. Good condition, includes all accessories.', 86.23, 'https://example.com/images/electronics/41.jpg', true);
INSERT INTO lendscapev1."Item" (itemId, itemName, userId, description, price, image_url, is_available) VALUES
  (42, 'Canon DSLR Camera', 10, 'Rent my Canon DSLR Camera! Very Good condition, perfect for your needs.', 68.13, 'https://example.com/images/electronics/42.jpg', true);
INSERT INTO lendscapev1."Item" (itemId, itemName, userId, description, price, image_url, is_available) VALUES
  (43, 'Catch Surf Surfboard', 3, 'Rent my Catch Surf Surfboard! Good condition, perfect for your needs.', 58.49, 'https://example.com/images/sports/43.jpg', true);
INSERT INTO lendscapev1."Item" (itemId, itemName, userId, description, price, image_url, is_available) VALUES
  (44, 'North Face Sleeping Bag', 5, 'Rent my North Face Sleeping Bag! Very Good condition, perfect for your needs.', 26.83, 'https://example.com/images/outdoor/44.jpg', true);
INSERT INTO lendscapev1."Item" (itemId, itemName, userId, description, price, image_url, is_available) VALUES
  (45, 'SnapFloor Dance Floor', 16, '2022 SnapFloor Dance Floor. Like New condition, includes all accessories.', 145.82, 'https://example.com/images/party/45.jpg', true);
INSERT INTO lendscapev1."Item" (itemId, itemName, userId, description, price, image_url, is_available) VALUES
  (46, 'Fun Booth Photo Booth', 16, '2019 Fun Booth Photo Booth. Very Good condition, includes all accessories.', 155.84, 'https://example.com/images/party/46.jpg', true);
INSERT INTO lendscapev1."Item" (itemId, itemName, userId, description, price, image_url, is_available) VALUES
  (47, 'Wilson Tennis Racket', 13, 'Rent my Wilson Tennis Racket! Good condition, perfect for your needs.', 21.27, 'https://example.com/images/sports/47.jpg', false);
INSERT INTO lendscapev1."Item" (itemId, itemName, userId, description, price, image_url, is_available) VALUES
  (48, 'Ryobi Pressure Washer', 1, '2020 Ryobi Pressure Washer. Like New condition, includes all accessories.', 49.9, 'https://example.com/images/tools/48.jpg', true);
INSERT INTO lendscapev1."Item" (itemId, itemName, userId, description, price, image_url, is_available) VALUES
  (49, 'Epson Projector', 1, 'Rent my Epson Projector! Good condition, perfect for your needs.', 64.85, 'https://example.com/images/electronics/49.jpg', true);
INSERT INTO lendscapev1."Item" (itemId, itemName, userId, description, price, image_url, is_available) VALUES
  (50, 'Werner Ladder', 1, '2023 Werner Ladder. Like New condition, includes all accessories.', 17.95, 'https://example.com/images/tools/50.jpg', true);

-- ORDERS

INSERT INTO lendscapev1."Order" (orderId, renterId, borrowerId, reviewId) VALUES
  (1, 13, 15, 8);
INSERT INTO lendscapev1."Order" (orderId, renterId, borrowerId, reviewId) VALUES
  (2, 1, 18, 3);
INSERT INTO lendscapev1."Order" (orderId, renterId, borrowerId, reviewId) VALUES
  (3, 16, 15, NULL);
INSERT INTO lendscapev1."Order" (orderId, renterId, borrowerId, reviewId) VALUES
  (4, 10, 18, NULL);
INSERT INTO lendscapev1."Order" (orderId, renterId, borrowerId, reviewId) VALUES
  (5, 3, 17, NULL);
INSERT INTO lendscapev1."Order" (orderId, renterId, borrowerId, reviewId) VALUES
  (6, 5, 8, 10);
INSERT INTO lendscapev1."Order" (orderId, renterId, borrowerId, reviewId) VALUES
  (7, 3, 11, 26);
INSERT INTO lendscapev1."Order" (orderId, renterId, borrowerId, reviewId) VALUES
  (8, 3, 13, NULL);
INSERT INTO lendscapev1."Order" (orderId, renterId, borrowerId, reviewId) VALUES
  (9, 16, 9, 1);
INSERT INTO lendscapev1."Order" (orderId, renterId, borrowerId, reviewId) VALUES
  (10, 1, 7, 6);
INSERT INTO lendscapev1."Order" (orderId, renterId, borrowerId, reviewId) VALUES
  (11, 1, 11, 23);
INSERT INTO lendscapev1."Order" (orderId, renterId, borrowerId, reviewId) VALUES
  (12, 5, 12, 25);
INSERT INTO lendscapev1."Order" (orderId, renterId, borrowerId, reviewId) VALUES
  (13, 1, 10, 13);
INSERT INTO lendscapev1."Order" (orderId, renterId, borrowerId, reviewId) VALUES
  (14, 3, 12, 9);
INSERT INTO lendscapev1."Order" (orderId, renterId, borrowerId, reviewId) VALUES
  (15, 5, 18, NULL);
INSERT INTO lendscapev1."Order" (orderId, renterId, borrowerId, reviewId) VALUES
  (16, 1, 13, NULL);
INSERT INTO lendscapev1."Order" (orderId, renterId, borrowerId, reviewId) VALUES
  (17, 1, 10, NULL);
INSERT INTO lendscapev1."Order" (orderId, renterId, borrowerId, reviewId) VALUES
  (18, 1, 15, 21);
INSERT INTO lendscapev1."Order" (orderId, renterId, borrowerId, reviewId) VALUES
  (19, 1, 15, NULL);
INSERT INTO lendscapev1."Order" (orderId, renterId, borrowerId, reviewId) VALUES
  (20, 1, 18, 27);
INSERT INTO lendscapev1."Order" (orderId, renterId, borrowerId, reviewId) VALUES
  (21, 1, 20, 4);
INSERT INTO lendscapev1."Order" (orderId, renterId, borrowerId, reviewId) VALUES
  (22, 1, 8, 24);
INSERT INTO lendscapev1."Order" (orderId, renterId, borrowerId, reviewId) VALUES
  (23, 16, 10, 22);
INSERT INTO lendscapev1."Order" (orderId, renterId, borrowerId, reviewId) VALUES
  (24, 3, 18, 2);
INSERT INTO lendscapev1."Order" (orderId, renterId, borrowerId, reviewId) VALUES
  (25, 16, 9, 19);
INSERT INTO lendscapev1."Order" (orderId, renterId, borrowerId, reviewId) VALUES
  (26, 10, 7, NULL);
INSERT INTO lendscapev1."Order" (orderId, renterId, borrowerId, reviewId) VALUES
  (27, 3, 13, 28);
INSERT INTO lendscapev1."Order" (orderId, renterId, borrowerId, reviewId) VALUES
  (28, 10, 9, 16);
INSERT INTO lendscapev1."Order" (orderId, renterId, borrowerId, reviewId) VALUES
  (29, 10, 13, 17);
INSERT INTO lendscapev1."Order" (orderId, renterId, borrowerId, reviewId) VALUES
  (30, 1, 12, 5);
INSERT INTO lendscapev1."Order" (orderId, renterId, borrowerId, reviewId) VALUES
  (31, 13, 12, 18);
INSERT INTO lendscapev1."Order" (orderId, renterId, borrowerId, reviewId) VALUES
  (32, 13, 19, NULL);
INSERT INTO lendscapev1."Order" (orderId, renterId, borrowerId, reviewId) VALUES
  (33, 10, 7, NULL);
INSERT INTO lendscapev1."Order" (orderId, renterId, borrowerId, reviewId) VALUES
  (34, 16, 15, 14);
INSERT INTO lendscapev1."Order" (orderId, renterId, borrowerId, reviewId) VALUES
  (35, 1, 15, 7);
INSERT INTO lendscapev1."Order" (orderId, renterId, borrowerId, reviewId) VALUES
  (36, 13, 10, 20);
INSERT INTO lendscapev1."Order" (orderId, renterId, borrowerId, reviewId) VALUES
  (37, 10, 15, 12);
INSERT INTO lendscapev1."Order" (orderId, renterId, borrowerId, reviewId) VALUES
  (38, 5, 17, 11);
INSERT INTO lendscapev1."Order" (orderId, renterId, borrowerId, reviewId) VALUES
  (39, 13, 20, NULL);
INSERT INTO lendscapev1."Order" (orderId, renterId, borrowerId, reviewId) VALUES
  (40, 1, 7, 15);

-- REVIEWS

INSERT INTO lendscapev1."Review" (reviewId, userId, itemId, orderId, content, rating) VALUES
  (1, 9, 5, 9, 'It was okay. The Callaway Golf Clubs worked adequately but nothing special. Might rent again.', 3);
INSERT INTO lendscapev1."Review" (reviewId, userId, itemId, orderId, content, rating) VALUES
  (2, 18, 15, 24, 'Worked well for my needs. The Burton Snowboard''s base was waxed. Worked for what I needed.', 4);
INSERT INTO lendscapev1."Review" (reviewId, userId, itemId, orderId, content, rating) VALUES
  (3, 18, 49, 2, 'Exactly what I needed! The Epson Projector''s bright clear image. Highly recommend!', 5);
INSERT INTO lendscapev1."Review" (reviewId, userId, itemId, orderId, content, rating) VALUES
  (4, 20, 48, 21, 'Good rental overall. The Ryobi Pressure Washer''s cleaned everything easily. Worked for what I needed.', 4);
INSERT INTO lendscapev1."Review" (reviewId, userId, itemId, orderId, content, rating) VALUES
  (5, 12, 49, 30, 'Terrible experience. The Epson Projector dim image. Total waste!', 1);
INSERT INTO lendscapev1."Review" (reviewId, userId, itemId, orderId, content, rating) VALUES
  (6, 7, 36, 10, 'Worked well for my needs. Worked for what I needed.', 4);
INSERT INTO lendscapev1."Review" (reviewId, userId, itemId, orderId, content, rating) VALUES
  (7, 15, 11, 35, 'Did the job. The Epson Projector worked adequately but nothing special. Might rent again.', 3);
INSERT INTO lendscapev1."Review" (reviewId, userId, itemId, orderId, content, rating) VALUES
  (8, 15, 21, 1, 'Pretty disappointed. The Epson Projector wouldn''t focus. Look elsewhere.', 2);
INSERT INTO lendscapev1."Review" (reviewId, userId, itemId, orderId, content, rating) VALUES
  (9, 12, 15, 14, 'Perfect rental experience! The Burton Snowboard''s base was waxed. Perfect for my project!', 5);
INSERT INTO lendscapev1."Review" (reviewId, userId, itemId, orderId, content, rating) VALUES
  (10, 8, 16, 6, 'Couldn''t be happier! Perfect for my project!', 5);
INSERT INTO lendscapev1."Review" (reviewId, userId, itemId, orderId, content, rating) VALUES
  (11, 17, 28, 38, 'Perfect rental experience! The Catch Surf Surfboard''s wax was fresh. Perfect for my project!', 5);
INSERT INTO lendscapev1."Review" (reviewId, userId, itemId, orderId, content, rating) VALUES
  (12, 15, 42, 37, 'Exactly what I needed! The Canon DSLR Camera''s amazing image quality. Will definitely rent again!', 5);
INSERT INTO lendscapev1."Review" (reviewId, userId, itemId, orderId, content, rating) VALUES
  (13, 10, 48, 13, 'Good rental overall. The Ryobi Pressure Washer''s all attachments included. Worked for what I needed.', 4);
INSERT INTO lendscapev1."Review" (reviewId, userId, itemId, orderId, content, rating) VALUES
  (14, 15, 26, 34, 'Average experience. The Pioneer DJ Controller worked adequately but nothing special. It was fine.', 3);
INSERT INTO lendscapev1."Review" (reviewId, userId, itemId, orderId, content, rating) VALUES
  (15, 7, 11, 40, 'Pretty disappointed. The Epson Projector wouldn''t focus. Won''t rent again.', 2);
INSERT INTO lendscapev1."Review" (reviewId, userId, itemId, orderId, content, rating) VALUES
  (16, 9, 22, 28, 'Exactly what I needed! Perfect for my project!', 5);
INSERT INTO lendscapev1."Review" (reviewId, userId, itemId, orderId, content, rating) VALUES
  (17, 13, 25, 29, 'Couldn''t be happier! Will definitely rent again!', 5);
INSERT INTO lendscapev1."Review" (reviewId, userId, itemId, orderId, content, rating) VALUES
  (18, 12, 13, 31, 'Exactly what I needed! The Coleman Camping Stove''s boiled water quickly. Will definitely rent again!', 5);
INSERT INTO lendscapev1."Review" (reviewId, userId, itemId, orderId, content, rating) VALUES
  (19, 9, 26, 25, 'Pretty disappointed. Not recommended.', 2);
INSERT INTO lendscapev1."Review" (reviewId, userId, itemId, orderId, content, rating) VALUES
  (20, 10, 21, 36, 'It was okay. The Epson Projector worked adequately but nothing special. Did the job.', 3);
INSERT INTO lendscapev1."Review" (reviewId, userId, itemId, orderId, content, rating) VALUES
  (21, 15, 27, 18, 'Pretty disappointed. The Ryobi Pressure Washer hose was cracked. Won''t rent again.', 2);
INSERT INTO lendscapev1."Review" (reviewId, userId, itemId, orderId, content, rating) VALUES
  (22, 10, 9, 23, 'Good rental overall. The Trek Mountain Bike''s comfortable ride. Worked for what I needed.', 4);
INSERT INTO lendscapev1."Review" (reviewId, userId, itemId, orderId, content, rating) VALUES
  (23, 11, 27, 11, 'Pretty satisfied. The Ryobi Pressure Washer''s all attachments included. Worked for what I needed.', 4);
INSERT INTO lendscapev1."Review" (reviewId, userId, itemId, orderId, content, rating) VALUES
  (24, 8, 24, 22, 'Average experience. The Coleman Tent worked adequately but nothing special. Did the job.', 3);
INSERT INTO lendscapev1."Review" (reviewId, userId, itemId, orderId, content, rating) VALUES
  (25, 12, 3, 12, 'Couldn''t be happier! Perfect for my project!', 5);
INSERT INTO lendscapev1."Review" (reviewId, userId, itemId, orderId, content, rating) VALUES
  (26, 11, 14, 7, 'Perfect rental experience! Highly recommend!', 5);
INSERT INTO lendscapev1."Review" (reviewId, userId, itemId, orderId, content, rating) VALUES
  (27, 18, 11, 20, 'Good rental overall. The Epson Projector''s worked with my laptop. Worked for what I needed.', 4);
INSERT INTO lendscapev1."Review" (reviewId, userId, itemId, orderId, content, rating) VALUES
  (28, 13, 4, 27, 'Pretty disappointed. Won''t rent again.', 2);

-- USERITEM

INSERT INTO lendscapev1."UserItem" (userId, itemId) VALUES
  (16, 1);
INSERT INTO lendscapev1."UserItem" (userId, itemId) VALUES
  (10, 2);
INSERT INTO lendscapev1."UserItem" (userId, itemId) VALUES
  (5, 3);
INSERT INTO lendscapev1."UserItem" (userId, itemId) VALUES
  (3, 4);
INSERT INTO lendscapev1."UserItem" (userId, itemId) VALUES
  (16, 5);
INSERT INTO lendscapev1."UserItem" (userId, itemId) VALUES
  (10, 6);
INSERT INTO lendscapev1."UserItem" (userId, itemId) VALUES
  (13, 7);
INSERT INTO lendscapev1."UserItem" (userId, itemId) VALUES
  (1, 8);
INSERT INTO lendscapev1."UserItem" (userId, itemId) VALUES
  (16, 9);
INSERT INTO lendscapev1."UserItem" (userId, itemId) VALUES
  (5, 10);
INSERT INTO lendscapev1."UserItem" (userId, itemId) VALUES
  (1, 11);
INSERT INTO lendscapev1."UserItem" (userId, itemId) VALUES
  (10, 12);
INSERT INTO lendscapev1."UserItem" (userId, itemId) VALUES
  (13, 13);
INSERT INTO lendscapev1."UserItem" (userId, itemId) VALUES
  (3, 14);
INSERT INTO lendscapev1."UserItem" (userId, itemId) VALUES
  (3, 15);
INSERT INTO lendscapev1."UserItem" (userId, itemId) VALUES
  (5, 16);
INSERT INTO lendscapev1."UserItem" (userId, itemId) VALUES
  (16, 17);
INSERT INTO lendscapev1."UserItem" (userId, itemId) VALUES
  (3, 18);
INSERT INTO lendscapev1."UserItem" (userId, itemId) VALUES
  (13, 19);
INSERT INTO lendscapev1."UserItem" (userId, itemId) VALUES
  (1, 20);
INSERT INTO lendscapev1."UserItem" (userId, itemId) VALUES
  (13, 21);
INSERT INTO lendscapev1."UserItem" (userId, itemId) VALUES
  (10, 22);
INSERT INTO lendscapev1."UserItem" (userId, itemId) VALUES
  (16, 23);
INSERT INTO lendscapev1."UserItem" (userId, itemId) VALUES
  (1, 24);
INSERT INTO lendscapev1."UserItem" (userId, itemId) VALUES
  (10, 25);
INSERT INTO lendscapev1."UserItem" (userId, itemId) VALUES
  (16, 26);
INSERT INTO lendscapev1."UserItem" (userId, itemId) VALUES
  (1, 27);
INSERT INTO lendscapev1."UserItem" (userId, itemId) VALUES
  (5, 28);
INSERT INTO lendscapev1."UserItem" (userId, itemId) VALUES
  (13, 29);
INSERT INTO lendscapev1."UserItem" (userId, itemId) VALUES
  (3, 30);
INSERT INTO lendscapev1."UserItem" (userId, itemId) VALUES
  (5, 31);
INSERT INTO lendscapev1."UserItem" (userId, itemId) VALUES
  (10, 32);
INSERT INTO lendscapev1."UserItem" (userId, itemId) VALUES
  (16, 33);
INSERT INTO lendscapev1."UserItem" (userId, itemId) VALUES
  (13, 34);
INSERT INTO lendscapev1."UserItem" (userId, itemId) VALUES
  (13, 35);
INSERT INTO lendscapev1."UserItem" (userId, itemId) VALUES
  (1, 36);
INSERT INTO lendscapev1."UserItem" (userId, itemId) VALUES
  (3, 37);
INSERT INTO lendscapev1."UserItem" (userId, itemId) VALUES
  (1, 38);
INSERT INTO lendscapev1."UserItem" (userId, itemId) VALUES
  (3, 39);
INSERT INTO lendscapev1."UserItem" (userId, itemId) VALUES
  (3, 40);
INSERT INTO lendscapev1."UserItem" (userId, itemId) VALUES
  (10, 41);
INSERT INTO lendscapev1."UserItem" (userId, itemId) VALUES
  (10, 42);
INSERT INTO lendscapev1."UserItem" (userId, itemId) VALUES
  (3, 43);
INSERT INTO lendscapev1."UserItem" (userId, itemId) VALUES
  (5, 44);
INSERT INTO lendscapev1."UserItem" (userId, itemId) VALUES
  (16, 45);
INSERT INTO lendscapev1."UserItem" (userId, itemId) VALUES
  (16, 46);
INSERT INTO lendscapev1."UserItem" (userId, itemId) VALUES
  (13, 47);
INSERT INTO lendscapev1."UserItem" (userId, itemId) VALUES
  (1, 48);
INSERT INTO lendscapev1."UserItem" (userId, itemId) VALUES
  (1, 49);
INSERT INTO lendscapev1."UserItem" (userId, itemId) VALUES
  (1, 50);
