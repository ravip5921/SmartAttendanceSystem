import mysql.connector


def createdb():
    host = 'localhost'
    user = 'root'
    password = ''
    port = 3306
    dbname = 'sas'

    len_cid = 15
    len_cname = 20
    len_scode = 10
    len_subname = 50
    len_did = 10
    len_dname = 100
    len_tid = 10
    len_tname = 50
    len_sid = 15
    len_sname = 50
    len_username = 30
    len_password = 55

    db_query = "CREATE DATABASE {}".format(dbname)
    query_selectdb = "USE {}".format(dbname)

    table_admin_query = '''CREATE TABLE admin(username VARCHAR({0}) NOT NULL,
                                              password VARCHAR({1}) NOT NULL
                                              )ENGINE = InnoDB;'''.format(len_username, len_password)

    table_department_query = '''CREATE TABLE department(dID VARCHAR({0}),
                                                        name VARCHAR({1}) NOT NULL,
                                                        PRIMARY KEY(dID)
                                                        )ENGINE = InnoDB;'''.format(len_did, len_dname)

    table_classroom_query = '''CREATE TABLE class(cID VARCHAR({0}),
                                                        name varchar({1}) NOT NULL, 
                                                        dID VARCHAR({2}),
                                                        `sem` TINYINT UNSIGNED,
                                                        PRIMARY KEY(cID),
                                                        FOREIGN KEY (dID) REFERENCES department(dID)
                                                        )ENGINE = InnoDB;'''.format(len_cid, len_cname, len_did)

    table_subject_query = '''CREATE TABLE subject(scode VARCHAR({0}),
                                                    name VARCHAR({1}) NOT NULL,
                                                    PRIMARY KEY(scode)
                                                    )ENGINE = InnoDB;'''.format(len_scode, len_subname)

    table_teacher_query = '''CREATE TABLE teacher(tID VARCHAR({0}),
                                                    name VARCHAR({1}) NOT NULL,
                                                    dID VARCHAR({2}),
                                                    PRIMARY KEY(tID),
                                                    FOREIGN KEY (dID) REFERENCES department(dID)
                                                    )ENGINE = InnoDB;'''.format(len_tid, len_tname, len_did)

    table_teaches_query = '''CREATE TABLE teaches(tID VARCHAR({0}),
                                                    scode VARCHAR({1}),
                                                    cID VARCHAR({2}),
                                                    `sem` TINYINT UNSIGNED,
                                                    PRIMARY KEY(tID, scode, cID, sem),
                                                    FOREIGN KEY (tID) REFERENCES teacher(tID),
                                                    FOREIGN KEY (scode) REFERENCES subject(scode),
                                                    FOREIGN KEY (cID) REFERENCES class(cID)
                                                    )ENGINE = InnoDB;'''.format(len_tid, len_scode, len_cid)

    table_student_query = '''CREATE TABLE student(sID VARCHAR({0}),
                                                    name VARCHAR({1}) NOT NULL,
                                                    cID VARCHAR({2}),
                                                    dID VARCHAR({3}),
                                                    PRIMARY KEY(sID),
                                                    FOREIGN KEY (cID) REFERENCES class(cID),
                                                    FOREIGN KEY (dID) REFERENCES department(dID)
                                                    )ENGINE = InnoDB;'''.format(len_sid, len_sname, len_cid, len_did)

    table_facedata_query = '''CREATE TABLE facedata(sID VARCHAR({0}),
                                                    `index` TINYINT UNSIGNED NOT NULL,
                                                    `embedding` FLOAT NOT NULL,
                                                    PRIMARY KEY(sID,`index`),
                                                    FOREIGN KEY (sID) REFERENCES student(sID)
                                                    )ENGINE = InnoDB;'''.format(len_sid)

    table_attendance_query = '''CREATE TABLE attendance(`aID` INTEGER UNSIGNED AUTO_INCREMENT,
                                                        time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                                                        tID VARCHAR({}),
                                                        scode VARCHAR({}),
                                                        cID VARCHAR({}),
                                                        PRIMARY KEY(aID),
                                                        UNIQUE (time, cID),
                                                        FOREIGN KEY (tID) REFERENCES teacher(tID),
                                                        FOREIGN KEY (scode) REFERENCES subject(scode),
                                                        FOREIGN KEY (cID) REFERENCES class(cID)
                                                        )ENGINE = InnoDB;'''.format(len_tid, len_scode, len_cid)

    table_record_query = '''CREATE TABLE record(`aID` INTEGER UNSIGNED,
                                                sID VARCHAR({0}),
                                                presence BOOLEAN DEFAULT False,
                                                PRIMARY KEY(aID, sID),
                                                FOREIGN KEY (aID) REFERENCES attendance(aID),
                                                FOREIGN KEY (sID) REFERENCES student(sID)
                                                )ENGINE = InnoDB;'''.format(len_sid)

    table_queries = [table_admin_query,
                     table_department_query,
                     table_classroom_query,
                     table_subject_query,
                     table_teacher_query,
                     table_teaches_query,
                     table_student_query,
                     table_facedata_query,
                     table_attendance_query,
                     table_record_query]

    try:
        mysqlconn = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            port=port)
        mysqlexecuter = mysqlconn.cursor()
        try:
            print('Executing... ', db_query)
            mysqlexecuter.execute(db_query)
        except mysql.connector.Error as e:
            print(e)
        try:
            print('Executing... ', query_selectdb)
            mysqlexecuter.execute(query_selectdb)
            for query in table_queries:
                try:
                    print('Executing... ', query)
                    mysqlexecuter.execute(query)
                except mysql.connector.Error as e:
                    print(e)
        except mysql.connector.Error as e:
            print(e)
    except mysql.connector.Error as e:
        print(e)


if __name__ == '__main__':
    createdb()
