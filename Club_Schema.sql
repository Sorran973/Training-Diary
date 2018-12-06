CREATE SCHEMA ClubSchema;

SELECT * FROM ClubSchema.Client;

DELETE FROM ClubSchema.Set;
DELETE FROM ClubSchema.Exercise;
DELETE FROM ClubSchema.Workout;
DELETE FROM ClubSchema.Client;
DELETE FROM ClubSchema.Trainer;

DROP VIEW ClubSchema.WorkoutView;

DROP TABLE ClubSchema.Set;
DROP TABLE ClubSchema.Exercise;
DROP TABLE ClubSchema.Workout;
DROP TABLE ClubSchema.Client;
DROP TABLE ClubSchema.Trainer;

DROP SEQUENCE ClubSchema.trainer_id;
DROP SEQUENCE ClubSchema.client_id;
DROP SEQUENCE ClubSchema.workout_id;
DROP SEQUENCE ClubSchema.exercise_id;
DROP SEQUENCE ClubSchema.set_id;


SELECT * FROM ClubSchema.Workout;
DROP TABLE ClubSchema.ExerciseDB;
DROP SEQUENCE ClubSchema.exercise_db_id;

---------------  Тренер  -----------------------------------------------------------------------------------------------

CREATE SEQUENCE IF NOT EXISTS ClubSchema.trainer_id
  AS INT
  MINVALUE 1
  NO MAXVALUE
  NO CYCLE;

CREATE TABLE IF NOT EXISTS ClubSchema.Trainer
(
  trainerID INT PRIMARY KEY NOT NULL DEFAULT nextval('ClubSchema.trainer_id'),
  firstName VARCHAR(25) NOT NULL,
  lastName VARCHAR(25) NOT NULL,
  middleName VARCHAR(25)
);

INSERT INTO ClubSchema.Trainer (firstName, lastName) VALUES ('Iskandar', 'Rajabov');

UPDATE ClubSchema.Trainer SET lastName = 'Раджабов' WHERE trainerID = 1;

SELECT * FROM ClubSchema.Trainer;


CREATE TRIGGER trig_Update_Tainer AFTER UPDATE
ON postgres.ClubSchema.Trainer
FOR EACH ROW
EXECUTE PROCEDURE postgres.ClubSchema.change_trainer_for_client();

CREATE OR REPLACE FUNCTION postgres.ClubSchema.change_trainer_for_client() RETURNS TRIGGER AS $$
BEGIN
  IF NEW.isFired != OLD.isFired
  THEN
      UPDATE ClubSchema.Client SET trainerID =
      RAISE EXCEPTION 'trying to update non-updateble field';
  END IF;
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

SELECT DISTINCT ON (trainerID) clientID FROM ClubSchema.Client;



CREATE TRIGGER trig_Update_Tainer AFTER INSERT
ON postgres.ClubSchema.Client
FOR EACH ROW
EXECUTE PROCEDURE postgres.ClubSchema.change_num_client_of_trainer();
---------------  Клиент  -----------------------------------------------------------------------------------------------


CREATE SEQUENCE IF NOT EXISTS ClubSchema.client_id
  AS INT
  MINVALUE 1
  NO MAXVALUE
  NO CYCLE;

CREATE TABLE IF NOT EXISTS ClubSchema.Client
(
  clientID INT PRIMARY KEY NOT NULL DEFAULT nextval('ClubSchema.client_id'),
  firstName VARCHAR(25) NOT NULL,
  lastName VARCHAR(25) NOT NULL,
  middleName VARCHAR(25),
  trainerID INT NOT NULL,

--   UNIQUE (firstName, lastName, middleName),

  FOREIGN KEY (trainerID) REFERENCES ClubSchema.Trainer (trainerID)

);

INSERT INTO ClubSchema.Client (firstName, lastName) VALUES ('Антон', 'Булхак', 5);



UPDATE ClubSchema.Client SET trainerID = 2 WHERE clientID = 1;
SELECT * FROM ClubSchema.Client;

SELECT clientID, trainerID FROM ClubSchema.Client;

-------------------  Список тренировок  --------------------------------------------------------------------------------

CREATE SEQUENCE IF NOT EXISTS ClubSchema.workout_id
  AS INT
  MINVALUE 1
  NO MAXVALUE
  NO CYCLE;

CREATE TABLE IF NOT EXISTS ClubSchema.Workout
(
  workoutID INT PRIMARY KEY       NOT NULL DEFAULT nextval('ClubSchema.workout_id'),
  date DATE NOT NULL DEFAULT current_date,
  time TIME NOT NULL DEFAULT current_time,
  isDone BOOLEAN NOT NULL,
  trainerID INT NOT NULL,
  clientID INT NOT NULL,

  FOREIGN KEY (trainerID) REFERENCES ClubSchema.Trainer (trainerID),
  FOREIGN KEY (clientId) REFERENCES ClubSchema.Client (clientID)
);

INSERT INTO ClubSchema.Workout (date, time, type, trainerID, clientID) VALUES ('2018.10.28', '08:00:00', TRUE , 1, 1);
INSERT INTO ClubSchema.Workout (date, time, type, trainerID, clientID) VALUES ('2018.10.28', '20:00:00', FALSE , 1, 1);


SELECT * FROM ClubSchema.Workout;

UPDATE ClubSchema.Workout SET date = '2018.10.29', time = '21:00:00' WHERE workoutID = 24

SELECT date, time, type FROM ClubSchema.Workout WHERE clientID = 99659;

DELETE FROM ClubSchema.Workout WHERE workoutID = 23

-----------------  Упражнение в тренировке  ----------------------------------------------------------------------------

CREATE SEQUENCE IF NOT EXISTS ClubSchema.exercise_id
  AS INT
  MINVALUE 1
  NO MAXVALUE
  NO CYCLE;

CREATE TABLE IF NOT EXISTS ClubSchema.Exercise
(
  exerciseID INT PRIMARY KEY NOT NULL DEFAULT nextval('ClubSchema.exercise_id'),
  workoutID INT NOT NULL,
  exerciseInDBID INT NOT NULL,

  FOREIGN KEY (workoutID) REFERENCES ClubSchema.Workout (workoutID),
  FOREIGN KEY (exerciseInDBID) REFERENCES ClubSchema.ExerciseDB (exerciseInDBID)
);

INSERT INTO ClubSchema.Exercise (workoutID, exerciseInDBID) VALUES (currval('ClubSchema.workout_id'), 5);
INSERT INTO ClubSchema.Exercise (workoutID, exerciseInDBID) VALUES (currval('ClubSchema.workout_id'), 6);

DELETE FROM ClubSchema.Exercise WHERE exerciseID = 23

SELECT * FROM ClubSchema.Exercise;

-----------------  Подход в упражнении  --------------------------------------------------------------------------------


CREATE SEQUENCE IF NOT EXISTS ClubSchema.set_id
  AS INT
  MINVALUE 1
  NO MAXVALUE
  NO CYCLE;

CREATE TABLE IF NOT EXISTS ClubSchema.Set
(
  setID INT PRIMARY KEY NOT NULL DEFAULT nextval('ClubSchema.set_id'),
  weight INT NOT NULL,
  reps INT NOT NULL,
  exerciseID INT NOT NULL,

  FOREIGN KEY (exerciseID) REFERENCES ClubSchema.Exercise (exerciseID)
);

INSERT INTO ClubSchema.Set (weight, reps, exerciseID) VALUES (100, 2, currval('ClubSchema.exercise_id'));
INSERT INTO ClubSchema.Set (weight, reps, exerciseID) VALUES (100, 2, currval('ClubSchema.exercise_id'));
INSERT INTO ClubSchema.Set (weight, reps, exerciseID) VALUES (100, 2, currval('ClubSchema.exercise_id'));
INSERT INTO ClubSchema.Set (weight, reps, exerciseID) VALUES (60, 5, currval('ClubSchema.exercise_id'));
INSERT INTO ClubSchema.Set (weight, reps, exerciseID) VALUES (60, 5, currval('ClubSchema.exercise_id'));
INSERT INTO ClubSchema.Set (weight, reps, exerciseID) VALUES (60, 5, currval('ClubSchema.exercise_id'));



DELETE FROM ClubSchema.Set WHERE setID = 20
DELETE FROM ClubSchema.Set WHERE setID = 21
DELETE FROM ClubSchema.Set WHERE setID = 22
DELETE FROM ClubSchema.Set WHERE setID = 23
DELETE FROM ClubSchema.Set WHERE setID = 24
DELETE FROM ClubSchema.Set WHERE setID = 25


SELECT * FROM ClubSchema.Set;

---------------  View тренировки  --------------------------------------------------------------------------------------

DROP VIEW ClubSchema.WorkoutView;


CREATE VIEW ClubSchema.WorkoutView AS
  SELECT c.clientID, w.date, w.time, w.isDone, eInDB.name, s.weight, s.reps
    FROM ClubSchema.Workout w INNER JOIN ClubSchema.Exercise e ON w.workoutID = e.workoutID
  INNER JOIN ClubSchema.Set s ON e.exerciseID = s.exerciseID
  INNER JOIN ClubSchema.ExerciseDB eInDB ON e.exerciseInDBID = eInDB.exerciseInDBID
  INNER JOIN ClubSchema.Client c ON c.clientID = w.clientID ORDER BY s.setID;


SELECT * FROM ClubSchema.WorkoutView;


---------------  База упражнений  --------------------------------------------------------------------------------------

DROP TABLE ClubSchema.ExerciseDB;
DROP SEQUENCE ClubSchema.exercise_db_id;

CREATE SEQUENCE IF NOT EXISTS ClubSchema.exercise_db_id
  AS INT
  MINVALUE 1
  NO MAXVALUE
  NO CYCLE;

CREATE TABLE IF NOT EXISTS ClubSchema.ExerciseDB
(
  exerciseInDBID INT PRIMARY KEY       NOT NULL DEFAULT nextval('ClubSchema.exercise_db_id'),
  name       VARCHAR(50)                      NOT NULL UNIQUE ,
  muscleGroup VARCHAR(30) NOT NULL
);

INSERT INTO ClubSchema.ExerciseDB (name, muscleGroup) VALUES ('Жим лежа', 'Грудь');
INSERT INTO ClubSchema.ExerciseDB (name, muscleGroup) VALUES ('Жим лежа под углом', 'Грудь');
INSERT INTO ClubSchema.ExerciseDB (name, muscleGroup) VALUES ('Разводка с гантелями', 'Грудь');
INSERT INTO ClubSchema.ExerciseDB (name, muscleGroup) VALUES ('Отжимания', 'Грудь');

INSERT INTO ClubSchema.ExerciseDB (name, muscleGroup) VALUES ('Становая тяга', 'Спина');
INSERT INTO ClubSchema.ExerciseDB (name, muscleGroup) VALUES ('Подтягивания', 'Спина');
INSERT INTO ClubSchema.ExerciseDB (name, muscleGroup) VALUES ('Тяга штанги к поясу', 'Спина');
INSERT INTO ClubSchema.ExerciseDB (name, muscleGroup) VALUES ('Тяга в горизонтальном блоке', 'Спина');

INSERT INTO ClubSchema.ExerciseDB (name, muscleGroup) VALUES ('Приседания', 'Ноги');
INSERT INTO ClubSchema.ExerciseDB (name, muscleGroup) VALUES ('Выпады', 'Ноги');
INSERT INTO ClubSchema.ExerciseDB (name, muscleGroup) VALUES ('Разгибания ног в тренажере', 'Ноги');
INSERT INTO ClubSchema.ExerciseDB (name, muscleGroup) VALUES ('Разведение ног в тренажере', 'Ноги');


SELECT * FROM ClubSchema.ExerciseDB;



------------------------------------------------------------------------------------------------------------------------
select * from pg_tables where schemaname='clubschema';
select * from pg_views where schemaname='clubschema';
select * from pg_sequences where schemaname='clubschema';

