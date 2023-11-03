import pandas as pd
import numpy as np
import matplotlib.pyplot as plt 
import seaborn as sns

df = pd.read_csv('Proyecto Integrador/dataset/games.csv')
print(df.head())

#! Paso 2. Prepara los datos
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

df['year_of_release'].hist(bins=50)
plt.title('Distribución de juegos lanzados por año')
plt.xlabel('Año de lanzamiento')
plt.ylabel('Número de juegos')
plt.show()

# Los datos de cada periodo no son significativos ya que no se tiene la misma cantidad de datos por año. 

#TODO Observa cómo varían las ventas de una plataforma a otra. Elige las plataformas con las mayores ventas totales y construye una distribución basada en los datos de cada año. 
#TODO Busca las plataformas que solían ser populares pero que ahora no tienen ventas. ¿Cuánto tardan generalmente las nuevas plataformas en aparecer y las antiguas en desaparecer?

df_sales_plataform = df.groupby('platform')['total_sales'].sum().sort_values(ascending=False).head(10)
df_sales_plataform.plot(kind='bar', figsize=(15, 5), title='Ventas totales por plataforma', xlabel='Plataforma', ylabel='Ventas totales')
plt.show() 


df_sales_plataform_year = df.pivot_table(index='year_of_release', columns='platform', values='total_sales', aggfunc='sum')
top_platforms = df_sales_plataform.index.tolist() 
top_platforms_pivot = df_sales_plataform_year[top_platforms]

top_platforms_pivot.plot(figsize=(15, 8), title='Ventas totales por año y plataforma')
plt.xlabel('Año de Lanzamiento')
plt.ylabel('Ventas Totales')
plt.legend(title='Plataforma')
plt.show()

# La PS1 es un claro ejemplo de una plataforma que llego a tener ventas considerables y despues de 10 años dejo de tener ventas, el caso de la PS2 es similar con alrededor de 10 - 11 años
# Donde dejo de tener ventas, la XBOX 360 con un periodo de 2005 a 2016 tendria aproximadamente 10 años, lo que nos da una tendencia en que las plataformas antiguas desaparecen
# Cada 10 años, con referente a cuanto tarda en aparecer una plataforma nueva hablando de la PS en promediom tardan 5 años en aparecer estas mismas.

#TODO Determina para qué período debes tomar datos. Para hacerlo mira tus respuestas a las preguntas anteriores. Los datos deberían permitirte construir un modelo para 2017.

# Se tomaran los datos desde el año 2000 ya que es el año donde se tiene la mayor cantidad de datos y se puede hacer un analisis mas completo.

#TODO Trabaja solo con los datos que consideras relevantes. Ignora los datos de años anteriores.

df = df.query('year_of_release >= 2000')

#TODO ¿Qué plataformas son líderes en ventas? ¿Cuáles crecen y cuáles se reducen? Elige varias plataformas potencialmente rentables.

df_sales_plataform_top = df.groupby('platform')['total_sales'].sum().sort_values(ascending=False).head(10)
df_sales_plataform_top.plot(kind='bar', figsize=(15, 5), title='Ventas totales por plataforma', xlabel='Plataforma', ylabel='Ventas totales')
plt.show()

# Las plataformas que son lideres en ventas son la PS2, X360, PS3, Wii, DS, PS, GBA, PS4, PSP, PC.

df_sales_plataform_year_2000 = df.pivot_table(index='year_of_release', columns='platform', values='total_sales', aggfunc='sum')
top_platforms_pivot_2000 = df_sales_plataform_year_2000[top_platforms]

top_platforms_pivot_2000.plot(figsize=(15, 8), title='Ventas totales por año y plataforma')
plt.xlabel('Año de Lanzamiento')
plt.ylabel('Ventas Totales')
plt.legend(title='Plataforma')
plt.show()

# PS2, X360, PS3 y Wii son líderes en ventas en sus respectivos períodos.
# PS4 parece estar creciendo. PS2, X360, y PS3 han pasado su pico y están en declive. Wii tuvo un pico pero cayó rápidamente.
# PS4 parece ser una apuesta potencialmente rentable para el futuro, dado su crecimiento sostenido.

#TODO Crea un diagrama de caja para las ventas globales de todos los juegos, desglosados por plataforma. ¿Son significativas las diferencias en las ventas? ¿Qué sucede con las ventas promedio en varias plataformas? Describe tus hallazgos.

df_top_platforms = df[df['platform'].isin(top_platforms)]
df_sales_platform_year_2000 = df_top_platforms.pivot_table(index='year_of_release', columns='platform', values='total_sales', aggfunc='sum')
sns.boxplot(data=df_top_platforms, x='platform', y='total_sales')
plt.title('Ventas totales por plataforma')
plt.xlabel('Plataforma')
plt.ylabel('Ventas totales')
plt.show()

# Las diferencias en las ventas son significativas, ya que existen juegos que casi no venden y otros que son un exito total.
# Las ventas promedio en varias plataformas son significativas, podemos ver la venta promedio de la plataforma GB es alrededor de 0.8 millones de copias mientras 
# que otras plataformas tienen en promedio 0.4.
# Si dejamos los valores atipicos al ver las cajas del boxplot se ven muy pequeñas y no se puede apreciar bien la informacion, por eso se decidio quitarlas. 


#TODO Mira cómo las reseñas de usuarios y profesionales afectan las ventas de una plataforma popular (tu elección). Crea un gráfico de dispersión y calcula la correlación entre las reseñas y las ventas. Saca conclusiones.

df_ps2 = df.query('platform == "PS"')
df_ps2.plot(x='user_score', y='total_sales', kind='scatter', figsize=(15, 8))
plt.xlabel('Calificacion del usuario')
plt.ylabel('Ventas Totales')
plt.title('Ventas relacionadas por calificacion de usuario')
plt.show()

df_ps2.plot(x = 'critic_score', y = 'total_sales', kind='scatter', figsize=(15, 8))
plt.title('Ventas relacionadas por calificacion de la critica')
plt.xlabel('Calificacion de la critica')
plt.ylabel('Ventas Totales')
plt.show()

df_ps2.dropna(subset=['user_score', 'critic_score'], inplace=True)
print(df_ps2['user_score'].corr(df_ps2['total_sales']))
print(df_ps2['critic_score'].corr(df_ps2['total_sales']))




#TODO Teniendo en cuenta tus conclusiones compara las ventas de los mismos juegos en otras plataformas.
#TODO Echa un vistazo a la distribución general de los juegos por género. ¿Qué se puede decir de los géneros más rentables? ¿Puedes generalizar acerca de los géneros con ventas altas y bajas?
