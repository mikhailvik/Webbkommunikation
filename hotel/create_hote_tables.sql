
CREATE TABLE "public"."hotel_rooms" ( 
  "id" SERIAL,
  "room_number" INTEGER NOT NULL,
  "type" VARCHAR(250) NULL,
  "price" NUMERIC NOT NULL,
  "created_at" TIMESTAMP NOT NULL DEFAULT now() ,
  CONSTRAINT "PK_hotel_rooms" PRIMARY KEY ("id")
);

CREATE TABLE "public"."hotel_guests" ( 
  "id" SERIAL,
  "firstname" VARCHAR(250) NULL,
  "lastname" VARCHAR(250) NULL,
  "address" VARCHAR(250) NULL,
  CONSTRAINT "PK_hotel_guests" PRIMARY KEY ("id")
);


CREATE TABLE "public"."hotel_bookings" ( 
  "id" SERIAL,
  "guest_id" INTEGER NOT NULL,
  "room_id" INTEGER NOT NULL,
  "datefrom" DATE NOT NULL DEFAULT now() ,
  "dateto" DATE NOT NULL DEFAULT now() ,
  "addinfo" VARCHAR(250) NULL,
  "created_at" TIMESTAMP NOT NULL DEFAULT now() ,
  CONSTRAINT "PK_hotel_bookings" PRIMARY KEY ("id"),
  CONSTRAINT "room fk" FOREIGN KEY ("room_id") REFERENCES "public"."hotel_rooms" ("id"),
  CONSTRAINT "guest fk" FOREIGN KEY ("guest_id") REFERENCES "public"."hotel_guests" ("id")
);