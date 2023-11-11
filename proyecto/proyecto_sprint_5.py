import pandas as pd
import numpy as np
import matplotlib.pyplot as plt 
from matplotlib.pyplot import show
import seaborn as sns

df = pd.read_csv('/datasets/games.csv')
print(df.head())
print()
print(df.info())

#! 1 Prepara los datos

df.columns = df.columns.str.lower() # Reemplaza los nombres de las columnas (ponlos en minúsculas).

df['year_of_release'] = pd.to_numeric(df['year_of_release'], errors='coerce').astype('Int64') # Convierte la fecha de lanzamiento a formato datetime.
df['critic_score'] = pd.to_numeric(df['critic_score'], errors='coerce').astype('Int64') # Convierte la calificación de los críticos a un tipo de datos Int64.
df['user_score'] = pd.to_numeric(df['user_score'], errors='coerce') # Convierte la calificación de los usuarios a un tipo de datos float64.

# 'year_of_release ---> Se convirtió a int64 ya que los años son numeros enteros.
# 'critic_score' ---> Se convirtió a int64 ya que los datos estan basados en 100 y no tienen decimales.
# 'user_score' –––> Se convirtió a float64 ya que son numeros y estaban como objeto.

# Valores ausentes

df['rating'] = df['rating'].fillna('RP')
df['user_score'] = df['user_score'].replace('tbd', np.nan).astype(float)

df.info()

# Rellenamos los valores ausentes de la columna rating, a RP que significa que el rating esta pendiente, ademas modificamos los tbd (To be determined) a NaN
# Posiblemente la falta de valores en estas celdas se deba a que no se registro la informacion de esos juegos o que no se tenia la informacion de esos juegos.

#! Calculo de ventas totales

# Para calcular las ventas totales sumamos las ventas de NA, EU, JP y otras ventas.

df['total_sales'] = df['na_sales'] + df['eu_sales'] + df['jp_sales'] + df['other_sales']

#! Paso 3. Analiza los datos

# Para analizar los datos de cada periodo se graficaran los datos de cada año.

plt.figure(1)
plt.figure(figsize=(15, 8))
df['year_of_release'].hist(bins=50)
plt.title('Distribución de juegos lanzados por año')
plt.xlabel('Año de lanzamiento')
plt.ylabel('Número de juegos')

# Los datos de cada periodo son significativos ya que podemos ver ciertas tendencias, a pesar de que los datos acaban en el 2016.
# Podemos observar que el lanzamiento de los juegos fueron fue en ascenso conforme el paso de los años, se puede ver una tendencia 
# Claramente hacia el alza, siendo del 2005 al 2010 el pico más grande en cuestión de lanzamientos,  de ahi en adelante se ve una clara 
# Tendencia a la baja en los lanzamientos pero esto se puede deber a que dejamos de tener informacion despues del 2016

#! Vamos a analizar las ventas totales por plataforma

#Agrupamos por plataforma, sumamos las ventas totales, ordenamos de mayor a menor y tomamos los 10 primeros valores.
df_sales_platform = df.groupby('platform')['total_sales'].sum().sort_values(ascending=False).head(10) 

#Graficamos los datos
plt.figure(2)
df_sales_platform.plot(kind='bar', figsize=(15, 5), title='Ventas totales por plataforma', xlabel='Plataforma', ylabel='Ventas totales')

#Creamos una tabla pivote con los datos de las ventas totales por año y plataforma
df_sales_platform_year_pivot = df.pivot_table(index='year_of_release', columns='platform', values='total_sales', aggfunc='sum')

#Creamos una lista con las plataformas que mas venden
top_platforms = df_sales_platform.index.tolist()

#Filtramos la tabla pivote con las plataformas que mas venden
top_platforms_sales = df_sales_platform_year_pivot[top_platforms]

plt.figure(3)
top_platforms_sales.plot(figsize=(16, 8), title='Ventas totales por año y plataforma')
plt.xlabel('Año de Lanzamiento')
plt.ylabel('Ventas Totales')
plt.legend(title='Plataforma')


# La PS1 es un claro ejemplo de una plataforma que llego a tener ventas considerables y despues de 10 años dejo de tener ventas, 
# el caso de la PS2 es similar con alrededor de 10 - 11 años, Donde dejo de tener ventas. 
# La XBOX 360 con un periodo de 2005 a 2016 tendria aproximadamente 10 años, lo que nos da una tendencia 
# en que las plataformas antiguas desaparecen cada 10 años, con referente a cuanto tarda en aparecer una plataforma nueva hablando de la PS 
# en promediom tardan 5 años en aparecer estas mismas.

#! Filtrado de datos desde el año 2014

# Para poder generar un modelo de predicción de ventas para el 2017, se tomaran los datos desde el año 2014

# Filtramos los datos desde el año 2014
df_sales_platform_year_2014 = df.query('year_of_release >= 2014')

#! Vamos a analizar las ventas totales por año y plataforma

# Vamos a ver cuales son las plataformas lideres en ventas, cuales crecen y cuales se reducen.
# Ademas elegiremos las plataformas potencialmente mas rentables.

# Creamos una tabla pivote con los datos de las ventas totales por año y plataforma.
df_sales_platform_year_2014_pivot = df_sales_platform_year_2014.pivot_table(index='year_of_release', columns='platform', values='total_sales', aggfunc='sum')

#Agrupamos por plataforma, sumamos las ventas totales, ordenamos de mayor a menor y tomamos los 10 primeros valores.
df_sales_plataform_year_2014_top = df_sales_platform_year_2014.groupby('platform')['total_sales'].sum().sort_values(ascending=False).head(10)
print(df_sales_plataform_year_2014_top.head(10))

# Las plataformas que son lideres en ventas son PS4, XOne, 3DS, WPS3, X360, WiiU, PC, PSV, Wii, PSP.

plt.figure(4)
df_sales_platform_year_2014_pivot.plot(figsize=(15, 8), title='Ventas totales por año y plataforma')
plt.xlabel('Año de Lanzamiento')
plt.ylabel('Ventas Totales')
plt.legend(title='Plataforma')

# PS4, XOne y 3DS son líderes en ventas.
# PS4 parece tener un crecimiento y despues una caida pero puede deberse a la falta de datos del 2016. PSP, Wii, y X360 están en declive.
# PS4 y XOne parecen ser una apuesta potencialmente rentable para el futuro, dado su crecimiento.

#! Vamos a ver como se comportan las ventas de las plataformas lideres en ventas

# Ahora vamos a crear un diagrama de caja para las ventas globales de todos los juegos, desglosados por plataforma. 
# Y describiremos si las diferencias en las ventas son significativas, ademas vamos a ver que sucede con las ventas promedio en varias plataformas


df_top_platforms = df.query('platform in @top_platforms')

plt.figure(5)
plt.figure(figsize=(15, 8))
sns.boxplot(data=df, x='platform', y='total_sales', showfliers=True)
plt.title('Ventas totales por plataforma')
plt.xlabel('Plataforma')
plt.ylabel('Ventas totales')

plt.figure(6)
plt.figure(figsize=(16, 8))
sns.boxplot(data=df, x='platform', y='total_sales', showfliers=False)
plt.title('Ventas totales por plataforma')
plt.xlabel('Plataforma')
plt.ylabel('Ventas totales')

# Las diferencias en las ventas son significativas, ya que existen juegos que casi no venden y otros que son un exito total.
# Las ventas promedio en varias plataformas son significativas, ya que existe una tendencia en que las ventas promedio de las plataformas mas vendidas son mayores a las de las plataformas que no son tan vendidas.
# que otras plataformas tienen en promedio 0.4.
# Si dejamos los valores atipicos al ver las cajas del boxplot se ven muy pequeñas y no se puede apreciar bien la informacion, por eso se crear dos graficas. 

#! Vamos a ver como se comportan las ventas de las plataformas lideres en ventas

# Vamos a ver cómo las reseñas de usuarios y profesionales afectan las ventas de una plataforma popular. 


df_ps2 = df.query('platform == "PS2"')

plt.figure(7)
df_ps2.plot(x='user_score', y='total_sales', kind='scatter', figsize=(15, 8))
plt.xlabel('Calificacion del usuario')
plt.ylabel('Ventas Totales')
plt.title('Ventas relacionadas por calificacion de usuario')

plt.figure(8)
df_ps2.plot(x = 'critic_score', y = 'total_sales', kind='scatter', figsize=(15, 8))
plt.title('Ventas relacionadas por calificacion de la critica')
plt.xlabel('Calificacion de la critica')
plt.ylabel('Ventas Totales')

#! Calculo de correlacion entre las ventas y las calificaciones de los usuarios y de la critica

# Filtrar el dataframe para incluir solo filas donde ambos 'critic_score' y 'user_score' no son nulos
df_ps2_clean = df_ps2.dropna(subset=['critic_score', 'user_score'])

df_ps2_clean.loc[:, 'critic_score'] = df_ps2_clean['critic_score'].astype(float)
df_ps2_clean.loc[:, 'user_score'] = df_ps2_clean['user_score'].astype(float)

df_ps2_clean = df_ps2_clean.reset_index(drop=True)

critic_corr = df_ps2_clean['critic_score'].corr(df_ps2_clean['total_sales'])
user_corr = df_ps2_clean['user_score'].corr(df_ps2_clean['total_sales'])
print(f"Critic Score Correlation: {critic_corr}")
print(f"User Score Correlation: {user_corr}")

# La calificacion de los usuarios afecta en baja medida a las ventas ya que existe una correlacion entre las ventas y la calificacion de los usuarios.
# La calificacion de la critica si es significativa ya que existe una correlacion entre las ventas y la calificacion de la critica.

#! Vamos a ver como se comportan las ventas de los juegos que se lanzaron en mas de una plataforma

#Agrupamos por nombre de juego y contamos la cantidad de plataformas en las que se lanzo el juego.
platform_count_per_game = df.groupby('name')['platform'].nunique()

#Filtramos los juegos que se lanzaron en mas de una plataforma.
games_in_multiple_platforms = platform_count_per_game[platform_count_per_game >= 2].index

#Agrupamos por nombre de juego y sumamos las ventas totales de los juegos que se lanzaron en mas de una plataforma.
df_top_games_sales_in_multiple_platforms = df.groupby('name')['total_sales'].sum()

#Filtramos los datos con los juegos que se lanzaron en mas de una plataforma
df_top_games_multiplatform = df_top_games_sales_in_multiple_platforms[df_top_games_sales_in_multiple_platforms.index.isin(games_in_multiple_platforms)]

#Ordenamos de mayor a menor y tomamos los 10 primeros valores.
df_top_10_multiplatform_games = df_top_games_multiplatform.sort_values(ascending=False).head(10)

#Creamos una lista con los juegos que se lanzaron en mas de una plataforma.
df_top_multiplatform_games = df_top_10_multiplatform_games.index.tolist()

# Filtramos los datos con los juegos que se lanzaron en mas de una plataforma.
df_top_games_details = df[df['name'].isin(df_top_multiplatform_games)]

#Creamos una tabla pivote con los datos de las ventas totales por juego y plataforma.
df_top_games_pivot_table = df_top_games_details.pivot_table(index='name', columns='platform', values='total_sales', aggfunc='sum', fill_value=0)

#Reordenamos la tabla pivote con los juegos que se lanzaron en mas de una plataforma.
df_top_games_pivot_table = df_top_games_pivot_table.reindex(df_top_multiplatform_games)


colors = ['red', 'green', 'blue', 'orange', 'purple', 'cyan', 'magenta', 'yellow', 'grey', 'teal', 'lightblue', 'brown']
plt.figure(9)
plt.figure(figsize=(14, 8)) 
df_top_games_pivot_table.plot(kind='bar', figsize=(14, 8), width=0.8, color=colors) #Graficamos los datos
plt.title('Comparación de Ventas por Plataforma de los Juegos Más Vendidos')
plt.ylabel('Ventas Totales (en millones)')
plt.xlabel('Juego')
plt.legend(title='Plataforma', bbox_to_anchor=(1.05, 1), loc='upper left')
plt.xticks(rotation=45)
plt.tight_layout()

# Los juegos que se lanzaron en mas de una plataforma son GTA V, Call of Duty: Black Ops 3, Call of Duty: Black Ops, Wii Sports, Call of Duty: Modern Warfare 3, 
# Call of Duty: Black Ops II, Wii Play, New Super Mario Bros., Call of Duty: Ghosts, Call of Duty: Modern Warfare 2.

# Y podemos ver que las ventas de los juegos que se lanzaron en mas de una plataforma son significativas, ya que existe una tendencia en que las ventas de los 
# juegos que se lanzaron en mas de una plataforma son mayores a las de los juegos que no se lanzaron en mas de una plataforma.


#! Echaremos un vistazo a la distribución general de los juegos por género. ¿Qué se puede decir de los géneros más rentables? ¿Puedes generalizar acerca de los géneros con ventas altas y bajas?

#Agrupamos por genero y sumamos las ventas totales.
df_genre = df.groupby('genre')['total_sales'].sum().sort_values(ascending=False)

plt.figure(10)
df_genre.plot(kind='bar', figsize=(14, 8)) #Graficamos los datos
plt.title('Ventas totales por genero')
plt.xlabel('Genero')
plt.ylabel('Ventas totales')

# Los generos mas rentables son Action, Sports, Shooter, Role-Playing, Platform, Misc, Racing, Fighting, Simulation, Adventure, Strategy, Puzzle.
# Podemos generalizar que los generos con ventas altas son los que apuntan a un publico mas joven y los generos con ventas bajas son los que apuntan a un publico mas adulto.

#! Crearemos un perfil de usuario para cada región


df_na_sales = df.groupby('platform')['na_sales'].sum().sort_values(ascending=False).head(5) #Agrupamos por plataforma y sumamos las ventas totales en NA, ordenamos de mayor a menor y tomamos los 5 primeros valores.
df_eu_sales = df.groupby('platform')['eu_sales'].sum().sort_values(ascending=False).head(5) #Agrupamos por plataforma y sumamos las ventas totales en EU, ordenamos de mayor a menor y tomamos los 5 primeros valores.
df_jp_sales = df.groupby('platform')['jp_sales'].sum().sort_values(ascending=False).head(5) #Agrupamos por plataforma y sumamos las ventas totales en JP, ordenamos de mayor a menor y tomamos los 5 primeros valores.

plt.figure(11)
df_na_sales.plot(kind='bar', figsize=(14, 8)) #Graficamos los datos
plt.title('Ventas totales por plataforma en NA')
plt.xlabel('Plataforma')
plt.ylabel('Ventas totales')


# Las 5 plataformas principales en NA son X360, PS2, Wii, PS3, DS.

plt.figure(12)
df_eu_sales.plot(kind='bar', figsize=(14, 8)) #Graficamos los datos
plt.title('Ventas totales por plataforma en EU')
plt.xlabel('Plataforma')
plt.ylabel('Ventas totales')


# Las 5 plataformas principales en EU son PS2, PS3, X360, Wii, PS.

plt.figure(13)
df_jp_sales.plot(kind='bar', figsize=(14, 8)) #Graficamos los datos
plt.title('Ventas totales por plataforma en JP')
plt.xlabel('Plataforma')
plt.ylabel('Ventas totales')

# Las 5 plataformas principales en JP son DS, PS, PS2, SNES, 3DS.


# Las variaciones en sus cuotas de mercado de una region a otra son que en NA y EU las plataformas mas vendidas son PS2, PS3, X360, Wii y en JP las plataformas mas vendidas son DS, PS, PS2, SNES, 3DS.

#! Vamos a ver como se comportan las ventas de los juegos por genero en cada region

df_na_genre = df.groupby('genre')['na_sales'].sum().sort_values(ascending=False).head(5) #Agrupamos por genero y sumamos las ventas totales en NA, ordenamos de mayor a menor y tomamos los 5 primeros valores.
df_eu_genre = df.groupby('genre')['eu_sales'].sum().sort_values(ascending=False).head(5) #Agrupamos por genero y sumamos las ventas totales en EU, ordenamos de mayor a menor y tomamos los 5 primeros valores.
df_jp_genre = df.groupby('genre')['jp_sales'].sum().sort_values(ascending=False).head(5) #Agrupamos por genero y sumamos las ventas totales en JP, ordenamos de mayor a menor y tomamos los 5 primeros valores.

plt.figure(14)
df_na_genre.plot(kind='bar', figsize=(14, 8)) #Graficamos los datos
plt.title('Ventas totales por genero en NA')
plt.xlabel('Genero')
plt.ylabel('Ventas totales')

# Los 5 generos principales en NA son Action, Sports, Shooter, Platform, Misc.

plt.figure(15)
df_eu_genre.plot(kind='bar', figsize=(14, 8)) #Graficamos los datos
plt.title('Ventas totales por genero en EU')
plt.xlabel('Genero')
plt.ylabel('Ventas totales')

# Los 5 generos principales en EU son Action, Sports, Shooter, Racing, Misc.

plt.figure(16)
df_jp_genre.plot(kind='bar', figsize=(14, 8)) #Graficamos los datos
plt.title('Ventas totales por genero en JP')
plt.xlabel('Genero')
plt.ylabel('Ventas totales')

# Los 5 generos principales en JP son Role-Playing, Action, Sports, Platform, Misc.


# La diferencia esta en que NA y EU mantienen una simulutud en los generos mas vendidos, mientras que JP tiene una diferencia teniendo el genero como Role-Playing como el mas vendido.

#! Vamos a ver como se comportan las ventas de los juegos por clasificacion en cada region

df_na_rating = df.groupby('rating')['na_sales'].sum().sort_values(ascending=False) #Agrupamos por clasificacion y sumamos las ventas totales en NA, ordenamos de mayor a menor.
df_eu_rating = df.groupby('rating')['eu_sales'].sum().sort_values(ascending=False) #Agrupamos por clasificacion y sumamos las ventas totales en EU, ordenamos de mayor a menor.
df_jp_rating = df.groupby('rating')['jp_sales'].sum().sort_values(ascending=False) #Agrupamos por clasificacion y sumamos las ventas totales en JP, ordenamos de mayor a menor.

plt.figure(17)
df_na_rating.plot(kind='bar', figsize=(14, 8)) #Graficamos los datos
plt.title('Ventas totales por clasificacion en NA')
plt.xlabel('Clasificacion')
plt.ylabel('Ventas totales')

# Las clasificaciones que mas venden en NA son E, T, M, E10+, EC, AO.

plt.figure(18)
df_eu_rating.plot(kind='bar', figsize=(14, 8)) #Graficamos los datos
plt.title('Ventas totales por clasificacion en EU')
plt.xlabel('Clasificacion')
plt.ylabel('Ventas totales')

# Las clasificaciones que mas venden en EU son E, M, T, E10+, AO, RP.

plt.figure(19)
df_jp_rating.plot(kind='bar', figsize=(14, 8)) #Graficamos los datos
plt.title('Ventas totales por clasificacion en JP')
plt.xlabel('Clasificacion')
plt.ylabel('Ventas totales')

# Las clasificaciones que mas venden en JP son E, T, M, E10+, AO, RP.


# Tras analizar las ventas totales por clasificación se observa que las clasificaciones 'E' (Everyone) y 'M' (Mature) tienen un rendimiento de ventas particularmente fuerte en todas las regiones. 
# Sin embargo, hay variaciones notables; por ejemplo, en JP, los juegos clasificados como 'T' (Teen) venden relativamente más que en NA y EU. Esto puede reflejar diferencias culturales en las preferencias de juego o en la demografía de los jugadores. 
# Los juegos clasificados como 'AO' (Adults Only) y 'RP' (Rating Pending) tienen ventas significativamente menores, lo que podría estar relacionado con la disponibilidad limitada de estos títulos en el mercado. 
# Estos resultados sugieren que las clasificaciones de ESRB sí tienen un impacto en las ventas en regiones individuales.


#! Paso 5. Prueba las siguientes hipótesis:

#Las calificaciones promedio de los usuarios para las plataformas Xbox One y PC son las mismas.

df_xbox_one = df_sales_platform_year_2014.query('platform == "XOne"')
df_pc = df_sales_platform_year_2014.query('platform == "PC"')

df_xbox_one_clean = df_xbox_one['user_score'].dropna()
df_pc_clean = df_pc['user_score'].dropna()

print(df_xbox_one_clean.mean())
print(df_pc_clean.mean())

# Para formular las hipotesis tomamos en cuenta que las calificaciones promedio de los usuarios para las plataformas Xbox One y PC son las mismas.
# Tomando como hipotesis nula que las calificaciones promedio de los usuarios para las plataformas Xbox One y PC son las mismas.

# H0: Las calificaciones promedio de los usuarios para las plataformas Xbox One y PC son las mismas.
# H1: Las calificaciones promedio de los usuarios para las plataformas Xbox One y PC son diferentes.

# Alfa = 0.05

from scipy import stats as st

alpha = 0.05

results = st.ttest_ind(df_xbox_one_clean, df_pc_clean, equal_var=False)

print('p-value:', results.pvalue)

if (results.pvalue < alpha):
    print('Rechazamos la hipotesis nula')
else:
    print('No rechazamos la hipotesis nula')

# Los datos no proporcionan suficiente evidencia para rechazar la hipótesis nula, por lo que no podemos decir que las 
# calificaciones promedio de los usuarios difieran entre las plataformas Xbox One y PC.


#! Las calificaciones promedio de los usuarios para los géneros de Acción y Deportes son diferentes.

df_action = df_sales_platform_year_2014.query('genre == "Action"')
df_sports = df_sales_platform_year_2014.query('genre == "Sports"')

df_action_clean = df_action['user_score'].dropna()
df_sports_clean = df_sports['user_score'].dropna()

print(df_action_clean.mean())
print(df_sports_clean.mean())


# Para formulas las hipotesis tomamos en cuenta que las calificaciones promedio de los usuarios para los géneros de Acción y Deportes son diferentes.
# Tomando como hipotesis nula que las calificaciones promedio de los usuarios para los géneros de Acción y Deportes son las mismas.

# H0: Las calificaciones promedio de los usuarios para los géneros de Acción y Deportes son las mismas.<br>
# H1: Las calificaciones promedio de los usuarios para los géneros de Acción y Deportes son diferentes.

# Alfa = 0.05

results = st.ttest_ind(df_action_clean, df_sports_clean, equal_var=False)

print('p-value:', results.pvalue)

if (results.pvalue < alpha):
    print('Rechazamos la hipotesis nula')
else:
    print('No rechazamos la hipotesis nula')

# El resultado del p-value es menor al valor de alfa, por lo que rechazamos la hipotesis nula y aceptamos la hipotesis alternativa.
# Los usuarios tienden a calificar los juegos de género Acción de manera significativamente diferente a los juegos de género Deportes, 
# con los juegos de Acción recibiendo en promedio calificaciones más altas en este conjunto de datos.

#! Paso 6. Escribe una conclusión general

# Al hacer este proyecto, descubrimos que las ventas de videojuegos son una mezcla compleja de factores. Las plataformas, géneros y 
# calificaciones por edad juegan un papel crucial, pero son las reseñas tanto de críticos como de usuarios las que tienen un peso notable. 
# Las evaluaciones de los críticos tienen una correlación significativa con las ventas, con un coeficiente de 0.39, y aunque las opiniones 
# de los usuarios también son importantes, su impacto es más moderado.

# Observando las tendencias regionales, nos encontramos con preferencias distintas por continente. En Norteamérica y Europa, las consolas 
# como PS2, PS3, X360 y Wii dominan el mercado, mientras que en Japón, las preferencias se inclinan hacia las plataformas DS, PS, PS2, SNES y 3DS. 
# Esta información es vital para estrategias de mercado enfocadas regionalmente.

# En el aspecto estadístico, al comparar las calificaciones promedio de los usuarios entre Xbox One y PC, no encontramos diferencias significativas, 
# con un p-valor de 0.116. En cambio, al contrastar los géneros de Acción y Deportes, la diferencia es clara y significativa, con un p-valor de 1.18e-14, 
# lo que sugiere que las preferencias de género varían notablemente.<br>

# Para concluir, este análisis nos provee de una guía valiosa para la toma de decisiones estratégicas en la industria de los videojuegos. 
# Estos datos actúan como una brújula para aquellos que buscan posicionar su producto con éxito, y nos recuerdan la importancia de basar nuestras 
# estrategias en información sólida y no dejarlas al azar.
