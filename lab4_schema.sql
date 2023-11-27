CREATE TABLE `rooms`(
    `id` TEXT NOT NULL,
    `campus` TEXT NOT NULL,
    `floor` INT NOT NULL,
    `sign` TEXT NOT NULL
);
ALTER TABLE
    `rooms` ADD PRIMARY KEY `rooms_id_primary`(`id`);
CREATE TABLE `mentors`(
    `name` TEXT NOT NULL,
    `squad` INT NOT NULL,
    `room_id` TEXT NOT NULL
);
ALTER TABLE
    `mentors` ADD PRIMARY KEY `mentors_name_primary`(`name`);
ALTER TABLE
    `mentors` ADD UNIQUE `mentors_squad_unique`(`squad`);
CREATE TABLE `children`(
    `name` TEXT NOT NULL,
    `squad` INT NOT NULL,
    `age` INT NOT NULL,
    `lesson_1` TEXT NOT NULL,
    `lesson_2` TEXT NOT NULL,
    `room_id` TEXT NOT NULL
);
ALTER TABLE
    `children` ADD PRIMARY KEY `children_name_primary`(`name`);
CREATE TABLE `teachers`(
    `name` TEXT NOT NULL,
    `lesson` TEXT NOT NULL,
    `room_id` TEXT NOT NULL
);
ALTER TABLE
    `teachers` ADD PRIMARY KEY `teachers_name_primary`(`name`);
ALTER TABLE
    `teachers` ADD UNIQUE `teachers_lesson_unique`(`lesson`);
ALTER TABLE
    `teachers` ADD UNIQUE `teachers_room_id_unique`(`room_id`);
ALTER TABLE
    `children` ADD CONSTRAINT `children_squad_foreign` FOREIGN KEY(`squad`) REFERENCES `mentors`(`squad`);
ALTER TABLE
    `children` ADD CONSTRAINT `children_room_id_foreign` FOREIGN KEY(`room_id`) REFERENCES `rooms`(`id`);
ALTER TABLE
    `teachers` ADD CONSTRAINT `teachers_room_id_foreign` FOREIGN KEY(`room_id`) REFERENCES `rooms`(`id`);
ALTER TABLE
    `children` ADD CONSTRAINT `children_lesson_1_foreign` FOREIGN KEY(`lesson_1`) REFERENCES `teachers`(`lesson`);
ALTER TABLE
    `mentors` ADD CONSTRAINT `mentors_room_id_foreign` FOREIGN KEY(`room_id`) REFERENCES `rooms`(`id`);
ALTER TABLE
    `children` ADD CONSTRAINT `children_lesson_2_foreign` FOREIGN KEY(`lesson_2`) REFERENCES `teachers`(`lesson`);