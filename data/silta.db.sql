BEGIN TRANSACTION;
CREATE TABLE IF NOT EXISTS "tasks" (
	"task_id"	INTEGER NOT NULL UNIQUE,
	"task_host"	INTEGER,
	"task_done"	INTEGER DEFAULT 0,
	"task_name"	TEXT DEFAULT '(new)',
	PRIMARY KEY("task_id" AUTOINCREMENT),
	FOREIGN KEY("task_host") REFERENCES "tasks"("task_id")
);
CREATE TABLE IF NOT EXISTS "attrs" (
	"attr_id"	INTEGER NOT NULL UNIQUE,
	"attr_host"	INTEGER,
	"attr_type"	TEXT,
	"attr_name"	TEXT DEFAULT 'Unknown',
	"attr_data"	TEXT DEFAULT '(new)',
	FOREIGN KEY("attr_host") REFERENCES "tasks"("task_id"),
	PRIMARY KEY("attr_id" AUTOINCREMENT)
);
COMMIT;
