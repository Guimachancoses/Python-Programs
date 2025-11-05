from datetime import timedelta
from datetime import datetime, timedelta
import pyodbc


def insert_macros_data(connection, data, batch_size=1000):
    cursor = connection.cursor()
    total_inserted = 0  # Contador para total de registros inseridos

    try:
        # Processa os dados em lotes de batch_size
        for i in range(0, len(data), batch_size):
            batch_data = data[i:i + batch_size]

            # Cria a query SQL com parâmetros
            merge_query = """
            MERGE INTO MACROS AS target
            USING (VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)) AS source
            (vehicleid, plate, driverid, driver, Company, deviceid, DeviceType, eventtypeid, EventType, eventid, eventtimestamp, gpsspeed, canspeed, odometer, rpm, ignition, latitude, longitude, altitude, url)
            ON target.eventid = source.eventid
            WHEN NOT MATCHED BY TARGET THEN
                INSERT (vehicleid, plate, driverid, driver, Company, deviceid, DeviceType, eventtypeid, EventType, eventid, eventtimestamp, gpsspeed, canspeed, odometer, rpm, ignition, latitude, longitude, altitude, url)
                VALUES (source.vehicleid, source.plate, source.driverid, source.driver, source.Company, source.deviceid, source.DeviceType, source.eventtypeid, source.EventType, source.eventid, source.eventtimestamp, source.gpsspeed, source.canspeed, source.odometer, source.rpm, source.ignition, source.latitude, source.longitude, source.altitude, source.url);
            """

            # Para cada lote, executa o merge com os dados parametrizados
            for row in batch_data:
                cursor.execute(merge_query, (
                    row["vehicleid"], row["plate"], row["driverid"], row["driver"], row["Company"],
                    row["deviceid"], row["Device type"], row["eventtypeid"], row["Event type"],
                    row["eventid"], row["eventtimestamp"], row["gpsspeed"],
                    row["canspeed"], row["odometer"], row["rpm"], row["ignition"], row["latitude"],
                    row["longitude"], row["altitude"], row["url"]
                ))

            # Atualiza o contador de registros inseridos
            total_inserted += len(batch_data)

        # Commit após os lotes
        connection.commit()  # Confirma as inserções
        print(f"Dados inseridos com sucesso! \nTotal de registros inseridos: {total_inserted} \n")

    except pyodbc.Error as e:
        connection.rollback()  # Reverte em caso de erro
        print(f"Erro ao inserir dados: {e}")

    finally:
        cursor.close()

    return total_inserted


def adjust_dates(last_event_timestamp):
    dateToaj = ""
    dateFromaj = ""
    # Ajusta o dateFrom com base nas condições de hora e minuto
    if last_event_timestamp.hour == 23 and last_event_timestamp.minute >= 0:
        # Se for após 23:0, define para 00:00 do próximo dia
        dateFromaj = (last_event_timestamp + timedelta(days=1)
                      ).replace(hour=0, minute=0, second=0)
    elif last_event_timestamp.hour == 17 and last_event_timestamp.minute >= 0:
        # Se for após 17:0, define para 18:00 do mesmo dia
        dateFromaj = last_event_timestamp.replace(hour=18, minute=0, second=0)
    elif last_event_timestamp.hour == 11 and last_event_timestamp.minute >= 0:
        # Se for após 11:0, define para 12:00 do mesmo dia
        dateFromaj = last_event_timestamp.replace(hour=12, minute=0, second=0)
    elif last_event_timestamp.hour == 5 and last_event_timestamp.minute >= 0:
        # Se for após 05:0, define para 06:00 do mesmo dia
        dateFromaj = last_event_timestamp.replace(hour=6, minute=0, second=0)
    else:
        # Caso contrário, apenas soma 1 segundo ao last_event_timestamp
        dateFromaj = last_event_timestamp + timedelta(seconds=1)

    # Definir dateTo com base nas condições de hora do dateFrom
    hour = dateFromaj.hour
    minute = dateFromaj.minute

    if (hour == 0 and minute >= 0) or (hour < 11 and minute <= 40):
        dateToaj = (last_event_timestamp + timedelta(days=1)).replace(hour=11, minute=59, second=0)
    elif (hour == 11 and minute >= 0) or (hour < 23 and minute <= 59):
        dateToaj = (last_event_timestamp + timedelta(days=1)).replace(hour=23, minute=59, second=0)
        
    elif (hour == 23 and minute >= 0):
         dateToaj = dateFromaj.replace(hour=11, minute=59, second=0)
    # elif (hour == 18 and minute >= 0) or (hour < 23 and minute <= 40):
    #     dateToaj = dateFromaj.replace(hour=23, minute=59, second=0)

    # Formata as datas para string no formato desejado
    dateFrom_str = dateFromaj.strftime("%Y-%m-%d+%H:%M:%S")
    dateTo_str = dateToaj.strftime("%Y-%m-%d+%H:%M:%S")

    # Exibe as datas formatadas
    print(f"dateFrom: {dateFrom_str}")
    print(f"dateTo: {dateTo_str}\n")
    print("------------------------------------------------------")

    return dateFrom_str, dateTo_str


def get_current_time_brasilia_minus_2_hours():

    import pytz
    # Define o fuso horário de Brasília
    brasilia_tz = pytz.timezone('America/Sao_Paulo')

    # Obtém a hora atual em UTC e converte para o fuso horário de Brasília
    now_brasilia = datetime.now(brasilia_tz)

    # Subtrai 2 horas
    time_minus_2_hours = now_brasilia - timedelta(hours=2)

    # Retorna o resultado formatado
    return time_minus_2_hours.strftime("%Y-%m-%d %H:%M:%S")


def get_current_time_brasilia():

    import pytz
    # Define o fuso horário de Brasília
    brasilia_tz = pytz.timezone('America/Sao_Paulo')

    # Obtém a hora atual em UTC e converte para o fuso horário de Brasília
    now_brasilia = datetime.now(brasilia_tz)

    # Retorna o resultado formatado
    return now_brasilia.strftime("%Y-%m-%d+%H:%M:%S")


# Exemplo de uso da função insert_telemetry_data
def MainMacros():
    query = "SELECT MAX(eventtimestamp) AS LastEventTimestamp FROM MACROS;"
    json_data = [1]
    dateTo_str = "2021-05-01+00:00:00"

    from Modules.connectSQL import connect_to_database
    from Modules.getLastDate import get_last_event_timestamp

    # Buscar hora atual
    horaAtual2_str = get_current_time_brasilia_minus_2_hours()

    # Remove o sinal "+" para que o formato seja reconhecido corretamente
    dateToc = datetime.strptime(dateTo_str, "%Y-%m-%d+%H:%M:%S")
    horaAtual2 = datetime.strptime(horaAtual2_str, "%Y-%m-%d %H:%M:%S")

    tdInsert = 0

    while json_data and (dateToc <= horaAtual2):
        # Supondo que você já tenha uma conexão estabelecida
        connection = connect_to_database()

        # Obtém a última data do evento
        last_event_timestamp = get_last_event_timestamp(query, connection)

        if connection:
            # Exemplo de como chamar fetchEventReport para obter os dados
            from Modules.getDataLoad import fetchEventReport
            datefrom, dateTo = adjust_dates(last_event_timestamp)

            dateToc = datetime.strptime(dateTo, "%Y-%m-%d+%H:%M:%S")

            if dateToc >= horaAtual2:
                dateTo = get_current_time_brasilia()

            url = f"https://api3-ng.tracknow.com/reports/eventreport.php?userlanguageid=3&timezone=America%2FSao_Paulo&datefrom={datefrom}&dateto={dateTo}&plate=&canspeedoperator1=geq&canspeed1=&canspeedoperator2=leq&canspeed2=&gpsspeedoperator1=geq&gpsspeed1=&gpsspeedoperator2=leq&gpsspeed2=&rpmoperator1=geq&rpm1=&rpmoperator2=leq&rpm2=&vehiclebrandid=&deviceid=&devicefunctionid=&devicetypeid=&devicebrandid=&showmacros=set&companyid%5B%5D=361&countryid=&regionid=&uploadprotocol=&eventid=&showgpsspeed=set&showcanspeed=set&showignition=set&showodometer=set&showlatitude=set&showlongitude=set&showaltitude=set&showrpm=set&showevent=set&showeventtime=set&showeventtypeid=set&gbcompany=set&gbdeviceid=set&gbdevicetype=set&gbvehicleid=set&gbdriver=set&gbeventtype=set"

        # Exemplo de como chamar fetchEventReport para obter os dados
            json_data = fetchEventReport(url)

            if json_data and "rows" in json_data:
                totalInsert = insert_macros_data(
                    connection, json_data["rows"])

                tdInsert += totalInsert

                if totalInsert == 0:
                    # Fecha a conexão com o banco de dados
                    connection.close()
                    exit

        # Fecha a conexão com o banco de dados
            connection.close()

    return tdInsert