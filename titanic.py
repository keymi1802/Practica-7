import pandas as pd       #Importas la libreria pandas le asignamos el nombre de pd

dataframe = "Titanic.csv"         #crea una variable llamada dataframe que contenga el dataset del titanic.csv 
titanic_df = pd.read_csv(dataframe)   #Crea una variable llamada titanic_df que contiene los datos del dataframe, con ella manipularemos los datos

print("Dimensiones:\n", titanic_df.shape)         #Utiliza .shape pra obtener las dimenciones 
print("\nNúmero de datos:\n", titanic_df.size)    #Utiliza .size para tener el total del número de datos
print("\nNombres de sus columnas:\n", titanic_df.columns)         #Utiliza .colums para obtener los nombres de todas las columnas 
print("\nNombres de sus filas:\n", titanic_df.index)              #Utiliza .index para obtener los nombres de todas las filas
print("\nTipos de datos de las columnas:\n", titanic_df.dtypes)   #Utiliza .dtypes para obtener el tipo de datos que tienen las columnas 
print("\nLas 10 primeras filas:\n", titanic_df.head(10))          #Con .head() se pueden observar la cantidad de las primeras filas que desees, solo colocar el número entre el parentesis
print("\nLas 10 ultimas filas:\n", titanic_df.tail(10))           #Con .tali() se pueden observar la cantidad de las últimas filas que desees, solo colocar el número entre el parentesis

pasajero_148 = titanic_df.loc[147]                  #Busca al pasajero con ID 148 (el indice comieza en 0)
print("\nDatos del pasajero 148:\n", pasajero_148)  

pares = titanic_df.iloc[::2]                #Selecciona las filas con número par 
print("\nFilas pares de dataframe:\n",pares)

primera_clase = titanic_df[titanic_df['Pclass'] == 1]['Name'].sort_values()   #Filtra a las personas de primera clase y ordena sus nombres alfabéticamente
print("\nPersonas de primera clase en orden alfabetico:\n", primera_clase)

sobrevivieron = titanic_df['Survived'].value_counts(normalize=True) * 100     #Calcula el porcentaje de personas que sobrevivieron y las que no 

print("\nPorcentaje de personas que sobrevivieron:\n", sobrevivieron[1]) 
print("Porcentaje de personas que fallecieron:\n", sobrevivieron[0]) 

porcentaje_clase = titanic_df.groupby('Pclass')['Survived'].mean() * 100      #Calcula el porcentaje de las personas qeu sobrevivieron en cada clase 
print("\nPorcentaje de personas que sobrevivieron en cada clase:\n", porcentaje_clase)

edad_conocida = titanic_df.dropna(subset=['Age'])             #Filtra a los pasajeros que tienen edad conocida y elimina a los que tienen edad desconocida
print("\nPasajeros sin edad desconocida:\n ", edad_conocida)

edad_media = titanic_df[titanic_df['Sex'] == 'female'].groupby('Pclass')['Age'].mean()      #Calcula la edad media de las mujeres qeu viajaban en cada clase 
print("\nEdad media de las mujeres que viejaban en cada clase: \n", edad_media)

titanic_df['Menor de Edad'] = titanic_df['Age'].apply(lambda edad: edad < 18)           #Crear columna que indique si son mayores de edad con elementos booleanos 
print("\nColumna booleana para ver si el pasajero era menor de edad o no: \n",titanic_df)

sobrevivientes_edad_clase = titanic_df.groupby(['Pclass', titanic_df['Age'] < 18])['Survived'].mean() * 100         #Calcula el porcentaje de mayores de edad y menores de edad que sobrevivieron el cada clase 
print("\nPorcentaje de menores y mayores de edad que sobrevivieron en cada clase:\n", sobrevivientes_edad_clase)