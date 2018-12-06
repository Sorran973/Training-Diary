from PyQt5 import QtCore

import psycopg2
import time




class Controller:
    def __init__(self):
        self.connection = psycopg2.connect(
            "dbname = 'postgres' user = 'postgres' host='localhost' port='5432' user = 'postgres' password = 'postgres'")
        self.connection.autocommit = True
        self.cursor = self.connection.cursor()

    def close_connection(self):
        self.cursor.close()
        self.connection.close()

####### Block of getters

    def getClientNames(self, id):
        self.cursor.execute('SELECT lastName, firstName, middleName, clientID FROM ClubSchema.Client WHERE trainerID = %s', [id])
        list = self.cursor.fetchall()
        resList = []
        for i in list:
            resList.append("{0} {1} {2} {3}".format(i[0], i[1], i[2], i[3]))
        return resList

    def getWorkoutsInInterval(self, clientID, fromDate, todate):
        self.cursor.execute('SELECT date, time FROM ClubSchema.Workout WHERE clientID = %s AND type = FALSE AND date BETWEEN %s AND %s', (clientID, fromDate, todate))
        list = self.cursor.fetchall()
        return list

    def getTrainerID(self, id):
        self.cursor.execute('SELECT trainerID FROM ClubSchema.Client WHERE clientID = %s', [id])
        return self.cursor.fetchone()[0]


    def getWOD(self, clientID):
        self.cursor.execute('SELECT time, name, weight, reps FROM ClubSchema.WorkoutView WHERE date = current_date AND type = FALSE AND clientID = %s', [clientID])
        list = self.cursor.fetchall()
        return list

    def getPlannedWorkout(self, date, clientID):
        self.cursor.execute('SELECT time, name, weight, reps FROM ClubSchema.WorkoutView WHERE date = %s  AND type = FALSE AND clientID = %s', (date, clientID))
        list = self.cursor.fetchall()
        return list

    def getPlannedWorkoutTrainer(self, date, time, clientID):
        self.cursor.execute('SELECT name, weight, reps FROM ClubSchema.WorkoutView WHERE date = %s AND time = %s  AND type = FALSE AND clientID = %s', (date, time, clientID))
        list = self.cursor.fetchall()
        return list

    def getDoneWorkout(self, date, clientID):
        self.cursor.execute('SELECT time, name, weight, reps FROM ClubSchema.WorkoutView WHERE date = %s  AND type = TRUE AND clientID = %s', (date, clientID))
        list = self.cursor.fetchall()
        return list

    def getDoneWorkoutTrainer(self, date, time, clientID):
        self.cursor.execute('SELECT name, weight, reps FROM ClubSchema.WorkoutView WHERE date = %s AND time = %s AND type = TRUE AND clientID = %s', (date, time, clientID))
        list = self.cursor.fetchall()
        return list

    def getExerciseNames(self):
        self.cursor.execute('SELECT name FROM postgres.ClubSchema.ExerciseDB ORDER BY exerciseInDBID')
        list = self.cursor.fetchall()
        return [i[0] for i in list]


####### Block of inserts

    def insertClient(self, list):
        self.cursor.execute('SELECT last_value FROM ClubSchema.trainer_id')
        trainerID = self.cursor.fetchone()
        list.append(trainerID[0])
        insert_command = "INSERT INTO ClubSchema.Client (firstName, lastName, middleName, trainerID) VALUES (%s, %s, %s, %s) RETURNING clientID"
        self.cursor.execute(insert_command, list)
        return self.cursor.fetchone()[0]

    def insertTrainer(self, list):
        insert_command = "INSERT INTO ClubSchema.Trainer (firstName, lastName, middleName) VALUES (%s, %s, %s) RETURNING trainerID"
        self.cursor.execute(insert_command, list)
        return self.cursor.fetchone()[0]


    def insertWorkoutClient(self, date, time, trainerID, clientID):
        insert_command = "INSERT INTO ClubSchema.Workout (date, time, type, trainerID, clientID) VALUES (current_date, %s, TRUE, %s, %s)"
        self.cursor.execute(insert_command, (time, clientID, trainerID))

    def insertWorkoutFromTrainer(self, date, time, trainerID, clientID):
        insert_command = "INSERT INTO ClubSchema.Workout (date, time, type, trainerID, clientID) VALUES (current_date, %s, FALSE, %s, %s)"
        self.cursor.execute(insert_command, (time, clientID, trainerID))

    def insertWorkoutClientWithoutTime(self, trainerID, clientID):
        insert_command = "INSERT INTO ClubSchema.Workout (date, time, type, trainerID, clientID) VALUES (current_date, current_time, TRUE, %s, %s)"
        self.cursor.execute(insert_command, (clientID, trainerID))

    def insertExercise(self, exerciseName):
        self.cursor.execute('SELECT exerciseInDBID FROM ClubSchema.ExerciseDB WHERE name=%s', [exerciseName])
        exerciseInDBID = self.cursor.fetchone()[0]
        self.cursor.execute('SELECT last_value FROM ClubSchema.workout_id')
        workoutID = self.cursor.fetchone()[0]
        insert_command = "INSERT INTO ClubSchema.Exercise (workoutID, exerciseInDBID) VALUES (%s, %s)"
        self.cursor.execute(insert_command, (workoutID, exerciseInDBID))

    def insertSet(self, weight, reps):
        self.cursor.execute('SELECT last_value FROM ClubSchema.exercise_id')
        exerciseID = self.cursor.fetchone()[0]
        insert_command = "INSERT INTO ClubSchema.Set (weight, reps, exerciseID) VALUES (%s, %s, %s)"
        self.cursor.execute(insert_command, (weight, reps, exerciseID))

    def select_record(self):
        self.cursor.execute("SELECT last_value FROM ClubSchema.workout_id")
        record = self.cursor.fetchall()
        for record in record:
            print(record)

############# Block of updaters

    def changeTrainer(self, clientID, trainerID):
        self.cursor.execute('UPDATE ClubSchema.Client SET trainerID = %s WHERE clientID = %s', (trainerID, clientID))


############# Block of test

    def testInsertTrainer(self):
        list = ['Артём', 'Булхак', 'Николаевич']
        for i in range(5):
            self.cursor.execute("INSERT INTO ClubSchema.Trainer (firstName, lastName, middleName ) VALUES (%s, %s, %s)", list)



    def testInsertClient(self):
        list = ['Антон', 'Булхак', 'Николаевич', 1]
        n = 0
        for i in range(1):
            start_time = time.time()
            self.cursor.execute("INSERT INTO ClubSchema.Client (firstName, lastName, middleName, trainerID) VALUES (%s, %s, %s, %s)", list)
            print((time.time() - start_time) * 1000, "ms")
            n += 1
            if n % 2 == 0:
                list[3] += 1

    def testInsertWorkoutClient(self, dateList):
        clientID = 1
        for j in range(1):
            start_time = time.time()

            self.cursor.execute('SELECT trainerID FROM ClubSchema.Client WHERE clientID = %s', [clientID])
            trainerID = self.cursor.fetchone()[0]

            for i in range(1):
                date = dateList[i]
                realDate = QtCore.QDate.fromString(date, 'd.M.yyyy').toPyDate()

                insert_command = "INSERT INTO ClubSchema.Workout (date, time, isDone, trainerID, clientID) VALUES (%s, current_time, FALSE, %s, %s) RETURNING workoutID"
                self.cursor.execute(insert_command, (realDate, trainerID, clientID))

                workoutID = self.cursor.fetchone()[0]

                insert_command = "INSERT INTO ClubSchema.Exercise (workoutID, exerciseInDBID) VALUES (%s, %s) RETURNING exerciseID"
                self.cursor.execute(insert_command, (workoutID, 1))

                exerciseID = self.cursor.fetchone()[0]
                insert_command = "INSERT INTO ClubSchema.Set (weight, reps, exerciseID) VALUES (%s, %s, %s)"
                self.cursor.execute(insert_command, (100, 4, exerciseID))

            clientID += 1
            print(clientID)
            print((time.time() - start_time) * 1000, "ms")



    def first(self):
        start_time = time.time()
        self.cursor.execute('SELECT firstName, lastName, middleName, clientID FROM ClubSchema.Client WHERE trainerID = 3')
        print((time.time() - start_time) * 1000, "ms")
        print(self.cursor.fetchall())

    def second(self):
        start_time = time.time()
        self.cursor.execute(
            "SELECT date, time FROM ClubSchema.Workout WHERE clientID = 4 AND isDone = FALSE AND date BETWEEN '2018.01.01' AND '2018.12.01'")
        print((time.time() - start_time) * 1000, "ms")
        print(self.cursor.fetchall())

    def third(self):
        start_time = time.time()
        self.cursor.execute(
            "SELECT time, name, weight, reps FROM ClubSchema.WorkoutView WHERE date = '2018.01.01' AND isDone = FALSE AND clientID = 1")
        print((time.time() - start_time) * 1000, "ms")
        print(self.cursor.fetchall())

    def fourth(self):
        start_time = time.clock()
        self.cursor.execute(
            "INSERT INTO ClubSchema.Client (firstName, lastName, middleName, trainerID) VALUES ('Антон', 'Булхак', 'Николаевич', 1) ")
        print((time.clock() - start_time) * 1000, "ms")

    def fifth(self):
        start_time = time.clock()
        self.cursor.execute("INSERT INTO ClubSchema.Workout (date, time, isDone, trainerID, clientID) VALUES ('2018.11.01', current_time, TRUE, 1, %s) ", [1])
        print((time.clock() - start_time) * 1000, "ms")

