SET NAMES utf8mb4;
SET CHARACTER SET utf8mb4;
CREATE DATABASE IF NOT EXISTS sqli_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE sqli_db;

CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY, 
    name VARCHAR(255) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    role INT DEFAULT 0
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS wallpapers (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    image_path VARCHAR(255) NOT NULL,
    category VARCHAR(100),
    uploader_id INT,                    
    is_approved TINYINT(1) DEFAULT 0,   
    is_private TINYINT(1) DEFAULT 0     
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS secret_data (
    id INT AUTO_INCREMENT PRIMARY KEY,
    content VARCHAR(255)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

INSERT INTO secret_data (content) VALUES ('FLAG{SQL_INJECTION_SUCCESS_NHOM7}');

INSERT INTO users (name,email,password,role) VALUES ('admin', 'admin@gmail.com', '123456', 1);

INSERT INTO wallpapers (title, image_path, category, is_approved) VALUES
('Trái đất nền đen 2', 'anh-nen-dien-thoai-hinh-trai-dat-nen-den-2-30-14-03-38.jpg', 'phone',1),
('Trái đất nền đen 1', 'anh-nen-dien-thoai-hinh-trai-dat-nen-den-1-30-14-03-19.jpg', 'phone',1),
('Chill 18', 'hinh-nen-dien-thoai-chill (18).jpg', 'phone',1),
('Chill 8', 'hinh-nen-dien-thoai-chill (8).jpg', 'phone',1),
('Bearbrick 5', 'hinh-nen-dien-thoai-bearbrick (5).jpg', 'phone',1),
('Ngầu 64', 'hinh-nen-dien-thoai-ngau (64).jpg', 'phone',1),
('Ngầu 49', 'hinh-nen-dien-thoai-ngau (49).jpg', 'phone',1),
('Ngầu 29', 'hinh-nen-dien-thoai-ngau (29).jpg', 'phone',1),
('Ngầu 8', 'hinh-nen-dien-thoai-ngau (8).jpg', 'phone',1),
('Ngầu 32', 'hinh-nen-dien-thoai-ngau (32).jpg', 'phone',1),
('Ngầu 11', 'hinh-nen-dien-thoai-ngau (11).jpg', 'phone',1),
('Doraemon Gốc', 'doraemon_full_detail_goc.jpg', 'phone',1),
('Cute 26-2', 'hinh-nen-dien-thoai-cute-26-2.jpg', 'phone',1),
('Cute New 5', 'hinh-nen-dien-thoai-cute-new (5).jpg', 'phone',1),
('Cute New 8', 'hinh-nen-dien-thoai-cute-new (8).jpg', 'phone',1),
('Cute 48', 'hinh-nen-dien-thoai-cute (48).jpg', 'phone',1),
('Cute 4', 'hinh-nen-dien-thoai-cute (4).jpg', 'phone',1),
('Cute 27', 'hinh-nen-dien-thoai-cute (27).jpg', 'phone',1),
('Cute 23', 'hinh-nen-dien-thoai-cute (23).jpg', 'phone',1),
('Cute 13', 'hinh-nen-dien-thoai-cute (13).jpg', 'phone',1),
('Cute 16', 'hinh-nen-dien-thoai-cute (16).jpg', 'phone',1),
('Mùa đông 3', 'hinh-nen-mua-dong-3.png', 'phone',1),
('Mùa đông 2', 'hinh-nen-mua-dong-2.jpg', 'phone',1),
('Mùa đông', 'hinh-nen-mua-dong.jpg', 'phone',1),
('Mùa thu 10', '10-hinh-nen-mua-thu-cho-dien-thoai-31-16-32-37.jpg', 'phone',1),
('Mùa thu 6', '6-hinh-nen-mua-thu-cho-dien-thoai-31-16-31-48.jpg', 'phone',1),
('Mùa thu 4', '4-hinh-nen-mua-thu-cho-dien-thoai-31-16-31-17.jpg', 'phone',1),
('Mùa thu 3', '3-hinh-nen-mua-thu-cho-dien-thoai-31-16-31-04.jpg', 'phone',1),
('Mùa thu 2', '2-hinh-nen-mua-thu-cho-dien-thoai-31-16-30-51.jpg', 'phone',1),
('Mùa thu 1', '1-hinh-nen-mua-thu-cho-dien-thoai-31-16-30-39.jpg', 'phone',1),
('Thành phố đêm 14', '14-hinh-nen-dien-thoai-thanh-pho-ve-dem-inkythuatso-01-13-35-24.jpg', 'phone',1),
('Thành phố đêm 13', '13-hinh-nen-dien-thoai-thanh-pho-ve-dem-inkythuatso-01-13-34-32.jpg', 'phone',1),
('Thành phố đêm 8', '8-hinh-nen-dien-thoai-thanh-pho-ve-dem-inkythuatso-01-13-33-16.jpg', 'phone',1),
('Thành phố đêm 3', '3-hinh-nen-dien-thoai-thanh-pho-ve-dem-inkythuatso-01-13-32-02.jpg', 'phone',1),
('Thành phố đêm 1', '1-hinh-nen-dien-thoai-thanh-pho-ve-dem-inkythuatso-01-13-31-09.jpg', 'phone',1),
('Giọt nước hoa 5', 'hinh-nen-dien-thoai-giot-nuoc-tren-hoa-la-5-31-13-15-19.jpg', 'phone',1),
('Giọt nước hoa 6', 'hinh-nen-dien-thoai-giot-nuoc-tren-hoa-la-6-31-13-15-37.jpg', 'phone',1),
('Giọt nước 3D 3', 'hinh-nen-giot-nuoc-3d-cho-dien-thoai-3-31-13-12-08.jpg', 'phone',1),
('Giọt nước 3D 2', 'hinh-nen-giot-nuoc-3d-cho-dien-thoai-2-31-13-11-50.jpg', 'phone',1),
('Giọt nước 3D 1', 'hinh-nen-giot-nuoc-3d-cho-dien-thoai-1-31-13-11-33.jpg', 'phone',1),
('Giọt nước HD 4', 'hinh-nen-giot-nuoc-dep-full-hd-cho-dien-thoai-4-31-13-10-27.jpg', 'phone',1),
('Giọt nước HD 3', 'hinh-nen-giot-nuoc-dep-full-hd-cho-dien-thoai-3-31-13-10-08.jpg', 'phone',1),
('Giọt nước HD 2', 'hinh-nen-giot-nuoc-dep-full-hd-cho-dien-thoai-2-31-13-09-46.jpg', 'phone',1),
('Giọt nước HD 1', 'hinh-nen-giot-nuoc-dep-full-hd-cho-dien-thoai-1-31-13-09-25.jpg', 'phone',1),
('Trái đất 3D 4', 'hinh-nen-trai-dat-3d-cho-dien-thoai-4-30-14-09-20.jpg', 'phone',1),
('Trái đất 3D 2', 'hinh-nen-trai-dat-3d-cho-dien-thoai-2-30-14-08-30.jpg', 'phone',1),
('Trái đất cute 3', 'hinh-nen-dep-trai-dat-cute-cho-dien-thoai-3-30-14-06-19.jpg', 'phone',1),
('Trái đất cute 1', 'hinh-nen-dep-trai-dat-cute-cho-dien-thoai-1-30-14-05-34.jpg', 'phone',1),
('Trái đất nền đen 5', 'anh-nen-dien-thoai-hinh-trai-dat-nen-den-5-30-14-04-43.jpg', 'phone',1),
('Trái đất nền đen 4', 'anh-nen-dien-thoai-hinh-trai-dat-nen-den-4-30-14-04-22.jpg', 'phone',1),
('Trái đất nền đen 3', 'anh-nen-dien-thoai-hinh-trai-dat-nen-den-3-30-14-03-58.jpg', 'phone',1);



