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
CREATE TABLE "public"."todo_users" ( 
  "id" SERIAL,
  "username" VARCHAR(250) NOT NULL,
  "api_key" VARCHAR(250) NOT NULL,
  CONSTRAINT "PK_todo_users" PRIMARY KEY ("id")
);

CREATE TABLE "public"."todo_category" ( 
  "id" SERIAL,
  "category_name" VARCHAR(250) NOT NULL,
  CONSTRAINT "PK_todo_category" PRIMARY KEY ("id")
);

CREATE TABLE "public"."todo_notes" ( 
  "id" SERIAL,
  "user_id" INTEGER NOT NULL,
  "category_id" INTEGER NOT NULL,
  "title" VARCHAR(250) NOT NULL,
  "done" TIMESTAMP NULL,
  "created_at" TIMESTAMP NOT NULL DEFAULT now() ,
  "updated_at" TIMESTAMP NOT NULL DEFAULT now() ,
  CONSTRAINT "PK_todo_notes" PRIMARY KEY ("id"),
  CONSTRAINT "user_fk" FOREIGN KEY ("user_id") REFERENCES "public"."todo_users" ("id"),
  CONSTRAINT "category_fk" FOREIGN KEY ("category_id") REFERENCES "public"."todo_category" ("id")
);
