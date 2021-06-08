import random
import time
import datetime

# import demjson
# from paho.mqtt import client as mqtt_client

import mysql.connector
import random

# ---------------connect to mysql database--------------------------------------------------------------------------------------------
mydb = mysql.connector.connect(
    user="django",
    password="Djangodb@1234",
    host="localhost",
    port=3306,
    database="Django",
    auth_plugin="mysql_native_password",
)

mycursor = mydb.cursor()
sqlformula = "INSERT INTO register_values_em6400 (tot_active_energy, i_a, i_b, i_c, i_avg, v_ab, v_bc, v_ca, v_ll_avg, v_an, v_bn, v_cn, v_ln_avg, active_pow_a, active_pow_b, active_pow_c, active_power_tot, pf_a, pf_b, pf_c, pf_tot, frequency, thd_i_a, thd_i_b, thd_i_c, thd_v_an, thd_v_bn, thd_v_cn, timestamp) VALUE (%s, %s,%s, %s, %s,%s, %s, %s,%s, %s, %s,%s, %s, %s,%s, %s, %s,%s, %s, %s,%s, %s, %s,%s, %s, %s,%s, %s, %s)"

while 1:
    tot_active_energy = random.randint(200000, 300000)
    i_a = round(random.uniform(350, 420), 3)
    i_b = round(random.uniform(350, 420), 3)
    i_c = round(random.uniform(350, 420), 3)
    i_avg = (i_a + i_b + i_c) / 3.0
    v_ab = round(random.uniform(418, 420), 3)
    v_bc = round(random.uniform(418, 420), 3)
    v_ca = round(random.uniform(418, 420), 3)
    v_ll_avg = (v_ab + v_bc + v_ca) / 3.0
    v_an = round(random.uniform(241, 243), 3)
    v_bn = round(random.uniform(241, 243), 3)
    v_cn = round(random.uniform(241, 243), 3)
    v_ln_avg = (v_an + v_bn + v_cn) / 3.0
    active_pow_a = round(random.uniform(50000, 95000), 1)
    active_pow_b = round(random.uniform(50000, 95000), 1)
    active_pow_c = round(random.uniform(50000, 95000), 1)
    active_power_tot = round(active_pow_a + active_pow_b + active_pow_c, 0)
    pf_a = round(random.uniform(0.6, 1), 6)
    pf_b = round(random.uniform(0.6, 1), 6)
    pf_c = round(random.uniform(0.6, 1), 6)
    pf_tot = (pf_a + pf_b + pf_c) / 3.0
    frequency = round(random.uniform(49, 51), 4)
    thd_i_a = 0
    thd_i_b = 0
    thd_i_c = 0
    thd_v_an = 0
    thd_v_bn = 0
    thd_v_cn = 0
    timestamp = datetime.datetime.now() + datetime.timedelta(hours=6.5)
    data = (
        tot_active_energy,
        i_a,
        i_b,
        i_c,
        i_avg,
        v_ab,
        v_bc,
        v_ca,
        v_ll_avg,
        v_an,
        v_bn,
        v_cn,
        v_ln_avg,
        active_pow_a,
        active_pow_b,
        active_pow_c,
        active_power_tot,
        pf_a,
        pf_b,
        pf_c,
        pf_tot,
        frequency,
        thd_i_a,
        thd_i_b,
        thd_i_c,
        thd_v_an,
        thd_v_bn,
        thd_v_cn,
        timestamp,
    )
    try:
        mycursor.execute(sqlformula, data)
        mydb.commit()
        print(str(timestamp) + " : appended")
    except Exception as e:
        print(e)
    time.sleep(5)
