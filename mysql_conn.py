import mysql.connector as mysqlc

def insert_sensordata_db(data):
    cnx=mysqlc.connect(user='admin',password='admin',
               host='127.0.0.1',database='database_logistics')
    cursor = cnx.cursor()
    q_sensor_data=("INSERT INTO sensor_data "
                    "(SensorID,WorkplaceID,Color,R,G,B) "
                    "VALUES (%s,%s,%s,%s,%s,%s)"
                    )
    sensor_data=data
    cursor.execute(q_sensor_data,sensor_data)
    cnx.commit()
    cursor.close()
    cnx.close()
    print('data inserted into db')

def read_data_from_db(p_no):
    print('caf')

if __name__ == "__main__":
    insert_sensordata_db(["1",'WP100','cierna','1000','1000','1000'])
