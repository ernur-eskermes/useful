-- upgrade --
CREATE TABLE IF NOT EXISTS "verification" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "link" UUID NOT NULL,
    "user_id" INT NOT NULL REFERENCES "user" ("id") ON DELETE CASCADE
);
COMMENT ON TABLE "verification" IS 'Модель для подтверждения регистраций пользователя';
-- downgrade --
DROP TABLE IF EXISTS "verification";
