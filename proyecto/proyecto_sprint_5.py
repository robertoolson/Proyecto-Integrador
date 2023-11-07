import pandas as pd
import numpy as np
import matplotlib.pyplot as plt 
from matplotlib.pyplot import show
import seaborn as sns

df = pd.read_csv('dataset/games.csv')
print(df.head())

#! Paso 2. Prepara los datosclear
#TODO Reemplaza los nombres de las columnas (ponlos en minúsculas).

df.columns = df.columns.str.lower()

#TODO Convierte los datos en los tipos necesarios.

df['year_of_release'] = pd.to_numeric(df['year_of_release'], errors='coerce').astype('Int64')
df['critic_score'] = pd.to_numeric(df['critic_score'], errors='coerce').astype('Int64')
df['user_score'] = pd.to_numeric(df['user_score'], errors='coerce')

#TODO Describe las columnas en las que los tipos de datos han sido cambiados y explica por qué.

# year_of_release Se convirtió a int64 ya que los años son numeros enteros.
# critic_score Se convirtió a int64 ya que los datos estan basados en 100 y no tienen decimales.
# user_score Se convirtió a float64 ya que son numeros y estaban como objeto.

#TODO Si es necesario, elige la manera de tratar los valores ausentes:

# No se llenaron los valores ausentes

#TODO Explica por qué rellenaste los valores ausentes como lo hiciste o por qué decidiste dejarlos en blanco.

# Completar los valores ausentes por el momento no sera necesario ya que los datos son bastante sensibles y no se puede rellenar con un valor que no sea el correcto.

#TODO ¿Por qué crees que los valores están ausentes? Brinda explicaciones posibles.

# Los valores estan ausentes ya que no se tienen datos de esos juegos.
# Los valres estan ausentes ya que no se registro la informacion de esos juegos.

#TODO Presta atención a la abreviatura TBD: significa "to be determined" (a determinar). Especifica cómo piensas manejar estos casos.

# Los valores TBD se dejaron como NaN ya que no se puede rellenar con un valor que no sea el correcto.

#TODO Calcula las ventas totales (la suma de las ventas en todas las regiones) para cada juego y coloca estos valores en una columna separada.

df['total_sales'] = df['na_sales'] + df['eu_sales'] + df['jp_sales'] + df['other_sales']

#! Paso 3. Analiza los datos
#TODO Mira cuántos juegos fueron lanzados en diferentes años. ¿Son significativos los datos de cada período?


plt.figure(1)
df['year_of_release'].hist(bins=50)
plt.title('Distribución de juegos lanzados por año')
plt.xlabel('Año de lanzamiento')
plt.ylabel('Número de juegos')


# Los datos de cada periodo no son significativos ya que no se tiene la misma cantidad de datos por año. 

#TODO Observa cómo varían las ventas de una plataforma a otra. Elige las plataformas con las mayores ventas totales y construye una distribución basada en los datos de cada año. 
#TODO Busca las plataformas que solían ser populares pero que ahora no tienen ventas. ¿Cuánto tardan generalmente las nuevas plataformas en aparecer y las antiguas en desaparecer?

df_sales_platform = df.groupby('platform')['total_sales'].sum().sort_values(ascending=False).head(10) #Agrupamos por plataforma, sumamos las ventas totales, ordenamos de mayor a menor y tomamos los 10 primeros valores. 

plt.figure(2)
df_sales_platform.plot(kind='bar', figsize=(15, 5), title='Ventas totales por plataforma', xlabel='Plataforma', ylabel='Ventas totales') #Graficamos los datos


df_sales_platform_year_pivot = df.pivot_table(index='year_of_release', columns='platform', values='total_sales', aggfunc='sum') #Creamos una tabla pivote con los datos de las ventas totales por año y plataforma
top_platforms = df_sales_platform.index.tolist() #Creamos una lista con las plataformas que mas venden
top_platforms_sales = df_sales_platform_year_pivot[top_platforms] #Filtramos la tabla pivote con las plataformas que mas venden

plt.figure(3)
top_platforms_sales.plot(figsize=(15, 8), title='Ventas totales por año y plataforma')
plt.xlabel('Año de Lanzamiento')
plt.ylabel('Ventas Totales')
plt.legend(title='Plataforma')


# La PS1 es un claro ejemplo de una plataforma que llego a tener ventas considerables y despues de 10 años dejo de tener ventas, el caso de la PS2 es similar con alrededor de 10 - 11 años
# Donde dejo de tener ventas, la XBOX 360 con un periodo de 2005 a 2016 tendria aproximadamente 10 años, lo que nos da una tendencia en que las plataformas antiguas desaparecen
# Cada 10 años, con referente a cuanto tarda en aparecer una plataforma nueva hablando de la PS en promediom tardan 5 años en aparecer estas mismas.

#TODO Determina para qué período debes tomar datos. Para hacerlo mira tus respuestas a las preguntas anteriores. Los datos deberían permitirte construir un modelo para 2017.

# Se tomaran los datos desde el año 2000 ya que no se tienen tantos datos de los años anteriores.

#TODO Trabaja solo con los datos que consideras relevantes. Ignora los datos de años anteriores.

df_sales_platform_year_2000 = df.query('year_of_release >= 2000') #Filtramos los datos desde el año 2000

#TODO ¿Qué plataformas son líderes en ventas? ¿Cuáles crecen y cuáles se reducen? Elige varias plataformas potencialmente rentables.

df_sales_platform_year_2000_pivot = df_sales_platform_year_2000.pivot_table(index='year_of_release', columns='platform', values='total_sales', aggfunc='sum') #Creamos una tabla pivote con los datos de las ventas totales por año y plataforma.

df_sales_plataform_year_2000_top = df_sales_platform_year_2000.groupby('platform')['total_sales'].sum().sort_values(ascending=False).head(10) #Agrupamos por plataforma, sumamos las ventas totales, ordenamos de mayor a menor y tomamos los 10 primeros valores.

# Las plataformas que son lideres en ventas son PS2, X360, PS3, Wii, DS, PS4, GBA, PSP, 3DS, XB.

plt.figure(4)
df_sales_platform_year_2000_pivot.plot(figsize=(15, 8), title='Ventas totales por año y plataforma')
plt.xlabel('Año de Lanzamiento')
plt.ylabel('Ventas Totales')
plt.legend(title='Plataforma')


# PS2, X360, PS3 y Wii son líderes en ventas en sus respectivos períodos.
# PS4 parece estar creciendo. PS2, X360, y PS3 han pasado su pico y están en declive. Wii tuvo un pico pero cayó rápidamente.
# PS4 parece ser una apuesta potencialmente rentable para el futuro, dado su crecimiento sostenido.

#TODO Crea un diagrama de caja para las ventas globales de todos los juegos, desglosados por plataforma. ¿Son significativas las diferencias en las ventas? ¿Qué sucede con las ventas promedio en varias plataformas? Describe tus hallazgos.

df_top_platforms = df.query('platform in @top_platforms')

plt.figure(5)
sns.boxplot(data=df, x='platform', y='total_sales', showfliers=True)
plt.title('Ventas totales por plataforma')
plt.xlabel('Plataforma')
plt.ylabel('Ventas totales')

plt.figure(6)
sns.boxplot(data=df, x='platform', y='total_sales', showfliers=False)
plt.title('Ventas totales por plataforma')
plt.xlabel('Plataforma')
plt.ylabel('Ventas totales')


# Las diferencias en las ventas son significativas, ya que existen juegos que casi no venden y otros que son un exito total.
# Las ventas promedio en varias plataformas son significativas, ya que existe una tendencia en que las ventas promedio de las plataformas mas vendidas son mayores a las de las plataformas que no son tan vendidas.
# que otras plataformas tienen en promedio 0.4.
# Si dejamos los valores atipicos al ver las cajas del boxplot se ven muy pequeñas y no se puede apreciar bien la informacion, por eso se crear dos graficas. 


#TODO Mira cómo las reseñas de usuarios y profesionales afectan las ventas de una plataforma popular (tu elección). Crea un gráfico de dispersión y calcula la correlación entre las reseñas y las ventas. Saca conclusiones.

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


print(df_ps2['user_score'].corr(df_ps2['total_sales']))

# La calificacion de los usuarios afecta en baja medida a las ventas ya que existe una correlacion entre las ventas y la calificacion de los usuarios.

print(df_ps2['critic_score'].corr(df_ps2['total_sales']))

# La calificacion de la critica si es significativa ya que existe una correlacion entre las ventas y la calificacion de la critica.


#TODO Teniendo en cuenta tus conclusiones compara las ventas de los mismos juegos en otras plataformas.

platform_count_per_game = df.groupby('name')['platform'].nunique() #Agrupamos por nombre de juego y contamos la cantidad de plataformas en las que se lanzo el juego.
games_in_multiple_platforms = platform_count_per_game[platform_count_per_game >= 2].index #Filtramos los juegos que se lanzaron en mas de una plataforma.
df_top_games_sales_in_multiple_platforms = df.groupby('name')['total_sales'].sum() #Agrupamos por nombre de juego y sumamos las ventas totales de los juegos que se lanzaron en mas de una plataforma.
df_top_games_multiplatform = df_top_games_sales_in_multiple_platforms[df_top_games_sales_in_multiple_platforms.index.isin(games_in_multiple_platforms)] #Filtramos los datos con los juegos que se lanzaron en mas de una plataforma
df_top_10_multiplatform_games = df_top_games_multiplatform.sort_values(ascending=False).head(10) #Ordenamos de mayor a menor y tomamos los 10 primeros valores.
df_top_multiplatform_games = df_top_10_multiplatform_games.index.tolist() #Creamos una lista con los juegos que se lanzaron en mas de una plataforma.
df_top_games_details = df[df['name'].isin(df_top_multiplatform_games)] # Filtramos los datos con los juegos que se lanzaron en mas de una plataforma.
df_top_games_pivot_table = df_top_games_details.pivot_table(index='name', columns='platform', values='total_sales', aggfunc='sum', fill_value=0) #Creamos una tabla pivote con los datos de las ventas totales por juego y plataforma.
df_top_games_pivot_table = df_top_games_pivot_table.reindex(df_top_multiplatform_games) #Reordenamos la tabla pivote con los juegos que se lanzaron en mas de una plataforma.


colors = ['red', 'green', 'blue', 'orange', 'purple', 'cyan', 'magenta', 'yellow', 'grey', 'pink', 'black', 'brown']

plt.figure(9)
plt.figure(figsize=(14, 10)) 
df_top_games_pivot_table.plot(kind='bar', figsize=(14, 8), width=0.8, color=colors) #Graficamos los datos

plt.title('Comparación de Ventas por Plataforma de los Juegos Más Vendidos')
plt.ylabel('Ventas Totales (en millones)')
plt.xlabel('Juego')
plt.legend(title='Plataforma', bbox_to_anchor=(1.05, 1), loc='upper left')
plt.xticks(rotation=45)
plt.tight_layout()


#TODO Echa un vistazo a la distribución general de los juegos por género. ¿Qué se puede decir de los géneros más rentables? ¿Puedes generalizar acerca de los géneros con ventas altas y bajas?

df_genre = df.groupby('genre')['total_sales'].sum().sort_values(ascending=False) #Agrupamos por genero y sumamos las ventas totales.

plt.figure(10)
df_genre.plot(kind='bar', figsize=(14, 8)) #Graficamos los datos
plt.title('Ventas totales por genero')
plt.xlabel('Genero')
plt.ylabel('Ventas totales')


# Los generos mas rentables son Action, Sports, Shooter, Role-Playing, Platform, Misc, Racing, Fighting, Simulation, Adventure, Strategy, Puzzle.
# Podemos generalizar que los generos con ventas altas son los que apuntan a un publico mas joven y los generos con ventas bajas son los que apuntan a un publico mas adulto.

#! Paso 4. Crea un perfil de usuario para cada región


#TODO Para cada región (NA, UE, JP) determina:
#TODO Las cinco plataformas principales. Describe las variaciones en sus cuotas de mercado de una región a otra.
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

#TODO Los cinco géneros principales. Explica la diferencia.

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

#TODO Si las clasificaciones de ESRB afectan a las ventas en regiones individuales.

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
#TODO Las calificaciones promedio de los usuarios para las plataformas Xbox One y PC son las mismas.

df_xbox_one = df.query('platform == "XOne"')
df_pc = df.query('platform == "PC"')

df_xbox_one_clean = df_xbox_one['user_score'].dropna()
df_pc_clean = df_pc['user_score'].dropna()

print(df_xbox_one_clean.mean())
print(df_pc_clean.mean())

#TODO Cómo formulaste las hipótesis nula y alternativa.

# Para formular las hipotesis tomamos en cuenta que las calificaciones promedio de los usuarios para las plataformas Xbox One y PC son las mismas.
# Tomando como hipotesis nula que las calificaciones promedio de los usuarios para las plataformas Xbox One y PC son las mismas.

# H0: Las calificaciones promedio de los usuarios para las plataformas Xbox One y PC son las mismas.
# H1: Las calificaciones promedio de los usuarios para las plataformas Xbox One y PC son diferentes.


#TODO Establece tu mismo el valor de umbral alfa.
# Alfa = 0.05

from scipy import stats as st

alpha = 0.05

results = st.ttest_ind(df_xbox_one_clean, df_pc_clean, equal_var=False)

print('p-value:', results.pvalue)

if (results.pvalue < alpha):
    print('Rechazamos la hipotesis nula')
else:
    print('No rechazamos la hipotesis nula')

# El resultado del p-value es menor al valor de alfa, por lo que rechazamos la hipotesis nula y aceptamos la hipotesis alternativa. 
# Por lo que las calificaciones promedio de los usuarios para las plataformas Xbox One y PC son diferentes.


#TODO Las calificaciones promedio de los usuarios para los géneros de Acción y Deportes son diferentes.

df_action = df.query('genre == "Action"')
df_sports = df.query('genre == "Sports"')

df_action_clean = df_action['user_score'].dropna()
df_sports_clean = df_sports['user_score'].dropna()

print(df_action_clean.mean())
print(df_sports_clean.mean())

#TODO Cómo formulaste las hipótesis nula y alternativa.

# Para formulas las hipotesis tomamos en cuenta que las calificaciones promedio de los usuarios para los géneros de Acción y Deportes son diferentes.
# Tomando como hipotesis nula que las calificaciones promedio de los usuarios para los géneros de Acción y Deportes son las mismas.

# H0: Las calificaciones promedio de los usuarios para los géneros de Acción y Deportes son las mismas.
# H1: Las calificaciones promedio de los usuarios para los géneros de Acción y Deportes son diferentes.

#TODO Establece tu mismo el valor de umbral alfa.
# Alfa = 0.05

results = st.ttest_ind(df_action_clean, df_sports_clean, equal_var=False)

print('p-value:', results.pvalue)

if (results.pvalue < alpha):
    print('Rechazamos la hipotesis nula')
else:
    print('No rechazamos la hipotesis nula')

# El resultado del p-value es menor al valor de alfa, por lo que rechazamos la hipotesis nula y aceptamos la hipotesis alternativa.
# Por lo que las calificaciones promedio de los usuarios para los géneros de Acción y Deportes son diferentes.

#! Paso 6. Escribe una conclusión general

# Al realizar este proyecto se pudo observar que las ventas de los videojuegos dependen de varios factores como la plataforma, el genero, la clasificacion, etc.
# Tambien se pudo observar que las ventas de los videojuegos si pueden llegar a depender de la calificacion de los usuarios y de la critica, y sobre todo de la critica.
# Ademas podemos darnos cuenta que las ventas de una region a otra si varian por ejemplo en NA y EU las plataformas mas vendidas son PS2, PS3, X360, Wii y en JP las plataformas mas vendidas son DS, PS, PS2, SNES, 3DS.
# El proyecto nos ayudo a entender como se comportan las ventas de los videojuegos y que factores influyen en estas mismas.
# Ademas de darnos un panorama general para poder tomar decisiones acorde a las regiones, en las que se quiera lanzar un videojuego.
