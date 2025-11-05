from datetime import datetime, timedelta
from Controller.count import contar_registros
from tqdm import tqdm
import pyodbc
import csv
import os


def insert_telemetry_data(connection, data, csv_file_path=r'\\AGENDA\arq\temp_dataTel.csv', batch_size=1000):
    cursor = connection.cursor()
    total_inserted = 0  # Contador para total de registros inseridos
    temp_table = "#TempTelemetry"  # Tabela temporária no SQL Server

    # Conta o total de registros no array
    tdRegistros = len(data)  # Número total de registros

    print(f"Total registros encontrados na API... {tdRegistros}")
    print("------------------------------------------------------\n")

    try:
        # Desabilita autocommit para aumentar a performance
        connection.autocommit = False

        # Cria a tabela temporária
        create_temp_table_query = f"""
        CREATE TABLE {temp_table} (
            vehicleid NVARCHAR(50),
            plate NVARCHAR(50),
            driverid NVARCHAR(50),
            driver NVARCHAR(255),
            company NVARCHAR(255),
            deviceid NVARCHAR(50),
            device_type NVARCHAR(50),
            eventtypeid NVARCHAR(50),
            event_type NVARCHAR(255),
            eventvalue NVARCHAR(255),
            eventid NVARCHAR(50),
            eventtimestamp NVARCHAR(50),
            gpsspeed NVARCHAR(50),
            canspeed NVARCHAR(50),
            odometer NVARCHAR(50),
            rpm NVARCHAR(50),
            ignition NVARCHAR(50),
            latitude NVARCHAR(50),
            longitude NVARCHAR(50),
            altitude NVARCHAR(50),
            heading NVARCHAR(50),
            url NVARCHAR(255)
        );
        """
        cursor.execute(create_temp_table_query)

        # Salva os dados em um arquivo CSV temporário
        with open(csv_file_path, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file, delimiter='|',
                                quotechar="'", quoting=csv.QUOTE_MINIMAL)
            writer.writerow([
                "vehicleid", "plate", "driverid", "driver", "company", "deviceid", "device_type", "eventtypeid",
                "event_type", "eventvalue", "eventid", "eventtimestamp", "gpsspeed", "canspeed", "odometer",
                "rpm", "ignition", "latitude", "longitude", "altitude", "heading", "url"
            ])

            for row in data:
                writer.writerow([
                    sanitize_value(row["vehicleid"]), sanitize_value(
                        row["plate"]), sanitize_value(row["driverid"]),
                    sanitize_value(row["driver"]), sanitize_value(
                        row["Company"]), sanitize_value(row["deviceid"]),
                    sanitize_value(row["Device type"]), sanitize_value(
                        row["eventtypeid"]), sanitize_value(row["Event type"]),
                    sanitize_value(row["eventvalue"]), sanitize_value(
                        row["eventid"]), sanitize_value(row["eventtimestamp"]),
                    sanitize_value(row["gpsspeed"]), sanitize_value(
                        row["canspeed"]), sanitize_value(row["odometer"]),
                    sanitize_value(row["rpm"]), sanitize_value(
                        row["ignition"]), sanitize_value(row["latitude"]),
                    sanitize_value(row["longitude"]), sanitize_value(
                        row["altitude"]), sanitize_value(row["heading"]),
                    sanitize_value(row["url"])
                ])

        # Inicializa a barra de progresso
        with tqdm(total=tdRegistros, desc="Inserindo dados", unit="registros") as pbar:
            # BULK INSERT na tabela temporária
            bulk_insert_query = f"""
            BULK INSERT {temp_table}
            FROM '{csv_file_path}'
            WITH (
                FIELDTERMINATOR = '|',                      -- Delimitador de campo (CSV)
                ROWTERMINATOR = '\n',                       -- Delimitador de linha
                FIRSTROW = 2,                               -- Ignora a primeira linha (cabeçalho)
                CODEPAGE = '65001',                         -- UTF-8 encoding
                TABLOCK                                    -- Melhora a performance bloqueando a tabela
            );
            """
            cursor.execute(bulk_insert_query)
            connection.commit()

            # Atualiza o contador de registros inseridos
            total_inserted = tdRegistros
            pbar.update(tdRegistros)

        # Usa MERGE para evitar duplicidade na tabela final
        merge_query = f"""
        MERGE INTO telemetria AS target
        USING {temp_table} AS source
        ON target.eventid = source.eventid
        WHEN NOT MATCHED BY TARGET THEN
            INSERT (vehicleid, plate, driverid, driver, company, deviceid, device_type, eventtypeid, event_type,
                    eventvalue, eventid, eventtimestamp, gpsspeed, canspeed, odometer, rpm, ignition, latitude,
                    longitude, altitude, heading, url)
            VALUES (source.vehicleid, source.plate, source.driverid, source.driver, source.company, source.deviceid,
                    source.device_type, source.eventtypeid, source.event_type, source.eventvalue, source.eventid,
                    source.eventtimestamp, source.gpsspeed, source.canspeed, source.odometer, source.rpm, source.ignition,
                    source.latitude, source.longitude, source.altitude, source.heading, source.url);
        """
        cursor.execute(merge_query)
        connection.commit()

        print(f"Dados inseridos com sucesso! \nTotal de registros inseridos: {
              total_inserted}")
        print("------------------------------------------------------\n")

    except pyodbc.Error as e:
        connection.rollback()  # Reverte em caso de erro
        print(f"Erro ao inserir dados: {e}")

    finally:
        cursor.close()
        connection.autocommit = True  # Reabilita autocommit

        # Remove o arquivo CSV temporário
        if os.path.exists(csv_file_path):
            os.remove(csv_file_path)

    return total_inserted


def sanitize_value(value):
    if value is None or value == '':
        return ''
    sanitized = str(value).replace('\n', '').replace(
        '\r', '').replace('\t', '').strip()
    return sanitized


def adjust_dates(last_event_timestamp):
    # Ajusta o dateFrom com base nas condições de hora e minuto
    if last_event_timestamp.hour == 23 and last_event_timestamp.minute >= 55:
        # Se for após 23:55, define para 00:00 do próximo dia
        dateFromaj = (last_event_timestamp + timedelta(days=1)
                      ).replace(hour=0, minute=0, second=0)
    elif last_event_timestamp.hour == 17 and last_event_timestamp.minute >= 55:
        # Se for após 17:55, define para 18:00 do mesmo dia
        dateFromaj = last_event_timestamp.replace(hour=18, minute=0, second=0)
    elif last_event_timestamp.hour == 11 and last_event_timestamp.minute >= 55:
        # Se for após 11:55, define para 12:00 do mesmo dia
        dateFromaj = last_event_timestamp.replace(hour=12, minute=0, second=0)
    elif last_event_timestamp.hour == 5 and last_event_timestamp.minute >= 55:
        # Se for após 05:55, define para 06:00 do mesmo dia
        dateFromaj = last_event_timestamp.replace(hour=6, minute=0, second=0)
    else:
        # Caso contrário, apenas soma 1 segundo ao last_event_timestamp
        dateFromaj = last_event_timestamp + timedelta(seconds=1)

    # Definir dateTo com base nas condições de hora do dateFrom
    hour = dateFromaj.hour
    minute = dateFromaj.minute

    if (hour == 0 and minute >= 0) or (hour < 6 and minute <= 59):
        dateToaj = dateFromaj.replace(hour=5, minute=59, second=0)
    elif (hour == 6 and minute >= 0) or (hour < 12 and minute <= 59):
        dateToaj = dateFromaj.replace(hour=11, minute=59, second=0)
    elif (hour == 12 and minute >= 0) or (hour < 18 and minute <= 59):
        dateToaj = dateFromaj.replace(hour=17, minute=59, second=0)
    elif (hour == 18 and minute >= 0) or (hour < 23 and minute <= 59):
        dateToaj = dateFromaj.replace(hour=23, minute=59, second=0)

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
def MainTelemetria():
    query = "SELECT MAX(eventtimestamp) AS LastEventTimestamp FROM telemetria;"
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

            url = f"https://api3-ng.tracknow.com/reports/eventreport.php?userlanguageid=3&timezone=America%2FSao_Paulo&datefrom={datefrom}&dateto={
                dateTo}&plate=&canspeedoperator1=geq&canspeed1=&canspeedoperator2=leq&canspeed2=&gpsspeedoperator1=geq&gpsspeed1=&gpsspeedoperator2=leq&gpsspeed2=&rpmoperator1=geq&rpm1=&rpmoperator2=leq&rpm2=&vehiclebrandid=&deviceid=&devicefunctionid=&devicetypeid=&devicebrandid=&showtelemetry=set&companyid%5B%5D=361&countryid=&regionid=&uploadprotocol=&eventid=&showgpsspeed=set&showcanspeed=set&showignition=set&showodometer=set&showlatitude=set&showlongitude=set&showaltitude=set&showheading=set&showrpm=set&showevent=set&showeventtime=set&showeventvalue=set&showeventtypeid=set&gbcompany=set&gbdeviceid=set&gbdevicetype=set&gbvehicleid=set&gbvehicle=set&gbdriver=set&gbeventtype=set"

        # Exemplo de como chamar fetchEventReport para obter os dados
            json_data = fetchEventReport(url)

            if json_data and "rows" in json_data:
                totalInsert = insert_telemetry_data(
                    connection, json_data["rows"])

                tdInsert += totalInsert

                if totalInsert == 0:
                    # Fecha a conexão com o banco de dados
                    connection.close()
                    exit

        # Fecha a conexão com o banco de dados
            connection.close()

    return tdInsert
