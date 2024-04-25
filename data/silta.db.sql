BEGIN TRANSACTION;
CREATE TABLE IF NOT EXISTS "tasks" (
	"task_id"	INTEGER NOT NULL UNIQUE,
	"task_host"	INTEGER,
	"task_done"	INTEGER DEFAULT 0,
	"task_name"	TEXT DEFAULT '(new)',
	FOREIGN KEY("task_host") REFERENCES "tasks"("task_id"),
	PRIMARY KEY("task_id" AUTOINCREMENT)
);
CREATE TABLE IF NOT EXISTS "attrs" (
	"attr_id"	INTEGER NOT NULL UNIQUE,
	"attr_host"	INTEGER,
	"attr_type"	TEXT,
	"attr_name"	TEXT DEFAULT '(new)',
	"attr_data"	TEXT DEFAULT '(new)',
	PRIMARY KEY("attr_id" AUTOINCREMENT),
	FOREIGN KEY("attr_host") REFERENCES "tasks"("task_id")
);
COMMIT;
