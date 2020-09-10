import mysql.connector as mysqlc

user='admin'
password='admin'
host='127.0.0.1'
database='database_logistics'

def insert_sensordata_db(data):
    cnx=mysqlc.connect(user=user,password=password,
               host=host,database=database)
    cursor = cnx.cursor()
    q_sensor_data=("INSERT INTO sensor_data "
                    "(SensorID,WorkplaceID,Color) "
                    "VALUES (%s,%s,%s)"
                    )
    sensor_data=data
    cursor.execute(q_sensor_data,sensor_data)
    cnx.commit()
    cursor.close()
    cnx.close()
    print('data inserted into db')

def read_bom_from_db(p_no):
    read=["_Mat1","_Mat2","_Mat3","_OP_TIME"]
    read= [p_no+x for x in read]
    cnx=mysqlc.connect(user=user,password=password,
               host=host,database=database)
    cursor = cnx.cursor(buffered=True)
    q_products= ("SELECT {},{},{},{} FROM products ".format(read[0],
                                                            read[1],
                                                            read[2],
                                                            read[3]))
    cursor.execute(q_products)
    cursor_data=list(cursor.fetchall())
    cursor_data=[list(x) for x in cursor_data]
    print(cursor_data)
    cursor.close()
    cnx.close()
    return cursor_data

def read_buffer_status(p_no):
    read=["_Mat1","_Mat2","_Mat3"]
    read= [p_no+x for x in read]
    cnx=mysqlc.connect(user=user,password=password,
               host=host,database=database)
    cursor = cnx.cursor(buffered=True)
    q_buffer_status=("SELECT Buffer_status from bom_edit Where ID=%s OR ID=%s OR ID=%s")
    cursor.execute(q_buffer_status,read)
    buffer_status=list(cursor.fetchall())
    buffer_status=[list(x) for x in buffer_status]
    cursor.close()
    cnx.close()
    return buffer_status

if __name__ == "__main__":
    insert_sensordata_db(["1",'WP100','cierna','1000','1000','1000'])
    read_bom_from_db("WP2")
    read_buffer_status("WP2")
