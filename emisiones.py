import pandas as pd

em2016=pd.read_csv('emisiones-2016.csv',delimiter=',')      #Importamos los archivos de las emisiones 
em2017=pd.read_csv('emisiones-2017.csv',delimiter=',')
em2018=pd.read_csv('emisiones-2018.csv',delimiter=',')
em2019=pd.read_csv('emisiones-2019.csv',delimiter=',')

emisiones_df = pd.concat([em2016, em2017,em2018,em2019], ignore_index=True)     #Juntar las cuatro emisiones en un dataframe llamado emisiones_df
print("DataFrame con los datos de los cuatro archivos:\n", emisiones_df)

filtro_columnas = emisiones_df.loc[:, ['ESTACION', 'MAGNITUD', 'ANO', 'MES','D01', 'D02', 'D03', 'D04', 'D05', 'D06', 'D07',                  #Utilizamos la función .loc y especificamos 
                                          'D08', 'D09', 'D10', 'D11', 'D12', 'D13', 'D14','D15', 'D16', 'D17', 'D18', 'D19', 'D20', 'D21',    #las columnas que queremos
                                          'D22', 'D23', 'D24', 'D25', 'D26', 'D27', 'D28','D29', 'D30', 'D31']]
print("Columnas filtradas del dataframe:\n", filtro_columnas)

reestructura = pd.melt(emisiones_df, id_vars=['PROVINCIA', 'MUNICIPIO', 'ESTACION', 'MAGNITUD', 'PUNTO_MUESTREO', 'ANO', 'MES'], #Reestructura el dataframe especificando las columnas qeu no tendran cambios
                       var_name='DIA',        #Nueva columna que contiene los nombres de las columnas que se desahacen 
                       value_name='VALOR')     #Nombre de la nueva columna que contiene los nombres de las columnas deshechas 
print("\nDataFrame reestructurado:\n",reestructura)

import datetime
def fecha(row):     #Función que crea fechas 
    try:
        return datetime.datetime(row['ANO'], row['MES'], int(row['DIA'][1:]))   #unimos año, mes y dia, si la D
    except ValueError:
        return None
reestructura['FECHA'] = reestructura.apply(fecha, axis=1)     #Incluimos la funcion fecha para cada fila 

print("\nDataFrame con nueva columna 'fecha':\n", reestructura)

import numpy as np
reestructura = reestructura[~np.isnan(reestructura['FECHA'])]       #Eliminar fechas no validas 
reestructura = reestructura.sort_values(by=['ESTACION', 'FECHA'])   #Ordenar por contaminantes y fechas 
print("\nDataFrame ordenado por estaciones contaminantes y fecha:\n", reestructura)

estaciones_disponibles = reestructura['ESTACION'].unique()        #Valores unicos en la columna estacion
print("\nEstaciones disponibles:\n", estaciones_disponibles)

contaminantes_disponibles = reestructura['MAGNITUD'].unique()       #Valores unicos en la columna magnitud 
print("\nContaminantes disponibles:\n", contaminantes_disponibles)

#Filtra el dataframe emisiones_df por estación, contaminante y rango de fechas
def emisiones_fecha(dataframe, estacion, contaminante, fecha_inicio, fecha_fin):
    filtro = (dataframe['ESTACION'] == estacion) & \
             (dataframe['MAGNITUD'] == contaminante) & \
             (dataframe['FECHA'] >= fecha_inicio) & \
             (dataframe['FECHA'] <= fecha_fin)
    emisiones = dataframe.loc[filtro]
  
    return emisiones['VALOR']                         #Devuelve la columna valor que contiene las emisiones 

#Llama a la función con sus argumentos 
emisiones_serie = emisiones_fecha(dataframe=reestructura,
                                   estacion=estacion,
                                   contaminante=contaminante,
                                   fecha_inicio=fecha_inicio,
                                   fecha_fin=fecha_fin)
print(emisiones_serie)

reestructura['VALOR'] = pd.to_numeric(reestructura['VALOR'], errors='coerce')     #Convierte la columna VALOR en dato numerico y convierte valores no numericos en nulos
resumen = reestructura.groupby('MAGNITUD')['VALOR'].describe()                    #Agrupa los datospor contaminante 
print("\nResumen descriptivo para cada contaminante:\n", resumen )

def resumen_emisiones(dataframe, estacion, contaminante):

    filtro = (dataframe['ESTACION'] == estacion) & (dataframe['MAGNITUD'] == contaminante)    #Filtrar dataframe solo con las columnas necesarias 
    emisiones_filtradas = dataframe.loc[filtro, 'VALOR']
    
    resumen = emisiones_filtradas.describe()       #Calcula el resumen descriptivo 
    
    return resumen        #Devuelve el resumen 

estacion = 1      #Ejemplo de uso 
contaminante = 7
resumen_emisiones = resumen_emisiones(reestructura, estacion, contaminante)         #Llamar a la función 
print("Devuelva un resumen descriptivo de las emisiones del contaminante")
print(resumen_emisiones)

def emisiones_medias_m(datos, contaminante, año):
    filtro = (datos['MAGNITUD'] == contaminante) & (datos['ANO'] == año)      #Filtrar datos por contaminante y año
    datos_filtrados = datos[filtro]
    emisiones_medias = datos_filtrados.groupby('MES')['VALOR'].mean()     #Calcular emisiones media mensuales 
    return emisiones_medias                   #Devolver emisiones 

contaminante = 1                            #Ejemplo 
año = 2017
emisiones_medias = emisiones_medias_m(reestructura, contaminante, año)
print(emisiones_medias)


def medias_mensuales_estacion(datos, estacion):
    datos_estacion = datos[datos['ESTACION'] == estacion]         #Filtrar datos de estacion 
    medias_mensuales = datos_estacion.groupby(['MES', 'MAGNITUD'])['VALOR'].mean().reset_index()      #Calcular las medias de las emisiones de cada contaminante
    medias_mensuales_p = medias_mensuales.pivot(index='MES', columns='MAGNITUD', values='VALOR')      #Pivotar los datos para tener los contaminantes como columnas y los meses como índice
    return medias_mensuales_p         #Devolver resultados 

estacion = 8                 #Ejemplo de uso 
medias_mensuales = medias_mensuales_estacion(reestructura, estacion)
print(medias_mensuales)