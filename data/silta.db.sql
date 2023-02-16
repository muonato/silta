BEGIN TRANSACTION;
CREATE TABLE IF NOT EXISTS "classes" (
	"class_id"	INTEGER,
	"class"	TEXT,
	"category"	INTEGER,
	PRIMARY KEY("class_id" AUTOINCREMENT),
	FOREIGN KEY("category") REFERENCES "classes"("class_id")
);
CREATE TABLE IF NOT EXISTS "operators" (
	"operator_id"	INTEGER,
	"operator"	TEXT,
	"login"	TEXT,
	PRIMARY KEY("operator_id" AUTOINCREMENT)
);
CREATE TABLE IF NOT EXISTS "products" (
	"product_id"	INTEGER,
	"product"	TEXT,
	"host"	INTEGER,
	"link"	INTEGER,
	"type"	INTEGER,
	"location"	INTEGER,
	FOREIGN KEY("host") REFERENCES "projects"("project_id"),
	PRIMARY KEY("product_id" AUTOINCREMENT),
	FOREIGN KEY("link") REFERENCES "products"("product_id"),
	FOREIGN KEY("location") REFERENCES "classes"("class_id"),
	FOREIGN KEY("type") REFERENCES "classes"("class_id")
);
CREATE TABLE IF NOT EXISTS "tasks" (
	"task_id"	INTEGER,
	"task"	TEXT,
	"object"	INTEGER,
	"owner"	INTEGER,
	"notes"	TEXT,
	"timestamp"	INTEGER DEFAULT current_timestamp,
	"active"	INTEGER,
	FOREIGN KEY("owner") REFERENCES "operators"("operator_id"),
	FOREIGN KEY("object") REFERENCES "products"("product_id"),
	PRIMARY KEY("task_id" AUTOINCREMENT),
	FOREIGN KEY("active") REFERENCES "classes"("class_id")
);
CREATE TABLE IF NOT EXISTS "projects" (
	"project_id"	INTEGER,
	"project"	TEXT,
	"subject"	INTEGER,
	"author"	INTEGER,
	"status"	INTEGER,
	FOREIGN KEY("status") REFERENCES "classes"("class_id"),
	FOREIGN KEY("author") REFERENCES "operators"("operator_id"),
	FOREIGN KEY("subject") REFERENCES "classes"("class_id"),
	PRIMARY KEY("project_id" AUTOINCREMENT)
);
INSERT INTO "classes" ("class_id","class","category") VALUES (1,'-',NULL);
INSERT INTO "classes" ("class_id","class","category") VALUES (2,'_status',NULL);
INSERT INTO "classes" ("class_id","class","category") VALUES (3,'_product',NULL);
INSERT INTO "classes" ("class_id","class","category") VALUES (4,'_location',NULL);
INSERT INTO "classes" ("class_id","class","category") VALUES (5,'_project',NULL);
INSERT INTO "classes" ("class_id","class","category") VALUES (6,'_process',NULL);
INSERT INTO "classes" ("class_id","class","category") VALUES (7,'_task',NULL);
INSERT INTO "operators" ("operator_id","operator","login") VALUES (1,'Administrator','cm9vdDpzaWx0YQ==');
COMMIT;
