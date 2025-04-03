CREATE TABLE "public"."hotel_bookings" ( 
  "id" SERIAL,
  "guest_id" INTEGER NOT NULL,
  "room_id" INTEGER NOT NULL,
  "datefrom" DATE NOT NULL DEFAULT now() ,
  "dateto" DATE NOT NULL DEFAULT now() ,
  "addinfo" VARCHAR(250) NULL,
  CONSTRAINT "PK_hotel_bookings" PRIMARY KEY ("id")
);

CREATE TABLE "public"."hotel_guests" ( 
  "id" SERIAL,
  "firstname" VARCHAR(250) NULL,
  "lastname" VARCHAR(250) NULL,
  "address" VARCHAR(250) NULL,
  CONSTRAINT "PK_hotel_guests" PRIMARY KEY ("id")
);

CREATE TABLE "public"."hotel_guests" ( 
  "id" SERIAL,
  "firstname" VARCHAR(250) NULL,
  "lastname" VARCHAR(250) NULL,
  "address" VARCHAR(250) NULL,
  CONSTRAINT "PK_hotel_guests" PRIMARY KEY ("id")
);
