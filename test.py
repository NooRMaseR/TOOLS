
# from sql import online_mysql

# DB = online_mysql(password="noormaser", database="test_db")
# DB.create_table_if_not("ppl2", {"name": "VARCHAR(50)", "age": "INTEGER(10)"})
# DB.insert_into_db("ppl2", {"name": "Ahmed", "age": 22})
# print(DB._sql_command)
# create an update command from sql to update name with your own query
# y = DB.find_into_db(
#     "ppl2",
#     where= {
#         "name": "Noor"
#     },
#     like= True
# )

# DB.custom_execute("UPDATE ppl2 SET name='noor' WHERE name='Noor'")
# print(DB.custom_execute("SELECT name, age FROM ppl2 WHERE name='Noor'"))
# print(DB.custom_execute("SELECT * FROM ppl2"))

# print(DB.find_cols_into_db("ppl2",("name", "age"),{"name":"Noor"}))
# print(DB._sql_command)

# print(DB.Get_db_data("ppl2"))
# DB.Update_db_data(
#     "ppl2",
#     set_command={"name": "noor", "age": 19},
#     where={"name": "nooR", "age": 20},
#     like=True,
# )

# DB.Delete_from_db(
#     "ppl2",
#     where= {
#         "name": "ahmed"
#     },
#     like=True
# )
# print(DB.Get_db_data("ppl2"))



# from sql import local_sqlite3


# db = local_sqlite3("test.db")
# db.create_table_if_not(
#     "ppl",
#     content= {
#         "name": "TEXT NOT NULL",
#         "age": "INTEGER NOT NULL"
#     }
# )
# db.insert_into_db(
#     "ppl", 
#     content= {
#         "name": "noor",
#         "age": 19
#     }
# )

# db.Update_db_data(
#     "ppl",
#     set_command= {
#         "name": "Ahmed"
#     },
#     where= {
#         "name": "ahmed",
#         "age": 15
#     }
# )

# print(db.Get_db_data("ppl"))
