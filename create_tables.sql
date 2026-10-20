DROP DATABASE IF EXISTS campus_flea_market;
CREATE DATABASE campus_flea_market
    DEFAULT CHARACTER SET utf8mb4
    DEFAULT COLLATE utf8mb4_unicode_ci;

USE campus_flea_market;

-- 用户表
CREATE TABLE users (
    user_id INT PRIMARY KEY AUTO_INCREMENT,
    username VARCHAR(50) NOT NULL UNIQUE,
    email VARCHAR(100) UNIQUE,
    phone VARCHAR(20),
    password VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 商品表
CREATE TABLE products (
    product_id INT PRIMARY KEY AUTO_INCREMENT,
    seller_id INT NOT NULL,
    title VARCHAR(200) NOT NULL,
    description TEXT,
    price DECIMAL(10,2),
    category VARCHAR(50),
    status TINYINT DEFAULT 1,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 订单表
CREATE TABLE orders (
    order_id INT PRIMARY KEY AUTO_INCREMENT,
    buyer_id INT NOT NULL,
    product_id INT NOT NULL,
    seller_id INT NOT NULL,
    quantity INT DEFAULT 1,
    total_price DECIMAL(10,2),
    status TINYINT DEFAULT 1,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- 评价表
CREATE TABLE reviews (
    review_id INT PRIMARY KEY AUTO_INCREMENT,
    order_id INT NOT NULL,
    user_id INT NOT NULL,
    product_id INT NOT NULL,
    rating TINYINT NOT NULL,
    content TEXT,
    status TINYINT DEFAULT 1,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

INSERT INTO users (username, email, phone, password) VALUES
('huang_test_1001', 't1001@school.edu', '13800131001', '123456'),
('huang_test_1003', 't1003@school.edu', '13800131003', '123456'),
('huang_test_1005', 't1005@school.edu', '13800131005', '123456'),
('huang_test_1015', 't1015@school.edu', '13800131015', '123456');


INSERT INTO products (product_id, seller_id, title, description, price, category) VALUES
(101, 4, 'PROBE_1009_阈值', '下单用商品', 99.00, '其他'),
(102, 4, '测试商品', '锚点商品', 40.00, '其他');