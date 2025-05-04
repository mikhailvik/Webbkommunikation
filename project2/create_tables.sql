--my sql database
CREATE TABLE todo_users (
     id INT AUTO_INCREMENT PRIMARY KEY,
     username VARCHAR(50) NOT NULL,
     api_key VARCHAR(50) NOT NULL
 );
 
 CREATE TABLE todo_categori (
     id INT AUTO_INCREMENT PRIMARY KEY,
     category_name VARCHAR(50) NOT NULL
 );
 
 
 CREATE TABLE todo_notes (
     id INT AUTO_INCREMENT PRIMARY KEY,
     user_id INT,
     category_id INT,
     title VARCHAR(50),
     done TIMESTAMP NULL DEFAULT NULL,
     created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
     updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
     FOREIGN KEY (user_id) REFERENCES todo_users(id),
     FOREIGN KEY (category_id) REFERENCES todo_categori(id)
 );

-- PostgreSQL
 CREATE TABLE todo_users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(50) NOT NULL,
    api_key VARCHAR(50) NOT NULL
);

CREATE TABLE todo_categori (
    id SERIAL PRIMARY KEY,
    category_name VARCHAR(50) NOT NULL
);

CREATE TABLE todo_notes (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES todo_users(id),
    category_id INTEGER REFERENCES todo_categori(id),
    title VARCHAR(50),
    done TIMESTAMP NULL DEFAULT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);