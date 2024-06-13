-- ROLE TABLE 
CREATE TABLE IF NOT EXISTS `roles`(
    `id` INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    `position` NOT NULL VARCHAR(50),
    `date` TIMESTAMP DEFAULT CURRENT_TIME 
);


CREATE TABLE IF NOT EXISTS `admins`(
    `id` INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    `firstname` NOT NULL VARCHAR(100),
    `lastname` NOT NULL VARCHAR(100),
    `email` NOT NULL VARCHAR(100),
    `password` NOT NULL VARCHAR(100),
    `role_id` INT(11),
    `status` TINYINT(0),
    CONSTRAINT role_auth FOREIGN KEY(`role_id`) REFERENCES `roles`(`id`) ON DELETE CASCADE,
    `registered_at` timestamp DEFAULT CURRENT_TIME
);

-- AUTHOR'S TABLE
CREATE TABLE IF NOT EXISTS `authors`(
    `id` INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    `title` NOT NULL VARCHAR(500),
    `content` NOT NULL LONGTEXT,
    `admin_id` NOT NULL INT,
    CONSTRAINT fk_auth FOREIGN KEY(`admin_id`) REFERENCES `admins`(`id`) ON DELETE CASCADE,
    `registered_at` timestamp DEFAULT CURRENT_TIME
);
-- EDITOR'S TABLE
CREATE TABLE IF NOT EXISTS `editors`(
    `id` INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    `admin_id` INT NOT NULL,
    `title` NOT NULL VARCHAR(200),
    `content` NOT NULL LONGTEXT,
    `author_id` INT NOT NULL,
    CONSTRAINT edit_auth FOREIGN KEY(`admin_id`) REFERENCES `authors`(`id`) ON DELETE CASCADE,
    `edited_date` timestamp DEFAULT CURRENT_TIME
);

-- PUBLISHER'S TABLE
CREATE TABLE IF NOT EXISTS `publishers`(
    `id` INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    `admin_id` INT NOT NULL,
    `editor_id` INT NOT NULL,
    `author_id` INT NOT NULL,
    CONSTRAINT pub_auth FOREIGN KEY(`admin_id`) REFERENCES `admins`(`id`) ON DELETE CASCADE,
    CONSTRAINT pub_edit_auth FOREIGN KEY(`editor_id`) REFERENCES `editors`(`id`) ON DELETE CASCADE,
    CONSTRAINT author_auth FOREIGN KEY(`author_id`) REFERENCES `authors`(`id`) ON DELETE CASCADE,
    `publiahed_date` timestamp DEFAULT CURRENT_TIME
);


