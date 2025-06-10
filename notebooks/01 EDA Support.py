#%% Import data
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

df_sprt = pd.read_pickle("../data/processed/df_sprt.pkl")

status_chagelog = pd.read_pickle("../data/processed/status_changelog.pkl")

sns.set_style("whitegrid")

sns.set_palette(sns.color_palette("tab10"))

plt.rcParams.update({
    "font.family": "DejaVu Sans",
    "axes.facecolor": "white",
    "figure.facecolor": "white",
    "savefig.facecolor": "white",
    "grid.color": "gray",
    "grid.linestyle": "--"
})


#%% Created support tickets per Year by Work Category
sprt_year = df_sprt[['Created','Work category']].copy()
sprt_year['Year'] = sprt_year['Created'].dt.year
sprt_year_grouped = sprt_year.groupby(['Year', 'Work category']).size().unstack(fill_value=0)


ax = sprt_year_grouped.plot(
    kind='bar',
    stacked=True
)

plt.title("Created support tickets per Year by Work Category")
plt.xlabel("Year")
plt.ylabel("Number of Tickets")
plt.legend(title="Work Category", bbox_to_anchor=(1.05, 1), loc='upper left')
plt.tight_layout()
plt.show()

#%% CNSD Created tickets per Year-Month by Work Category

df_sprt['Year-Month'] = df_sprt['Created'].dt.to_period('M').astype(str)

# Agrupar por Year-Month y Work category
ticket_counts = df_sprt.groupby(['Year-Month', 'Work category']).size().unstack(fill_value=0)

# Plot de barras apiladas
ticket_counts.plot(kind='bar', stacked=True, figsize=(12, 6), colormap='crest')

plt.title('Created support tickets per Year-Month by Work Category')
plt.xlabel('Year-Month')
plt.ylabel('Number of Tickets')
plt.xticks(rotation=45)
plt.legend(title='Work Category')
#plt.tight_layout()
plt.show()

#%% 

df_sprt['Weekday'] = df_sprt['Created'].dt.day_name()

# Orden de los días de la semana
order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']

# Contar tickets por día
grouped = df_sprt.groupby(['Weekday', 'Work category']).size().unstack(fill_value=0)
grouped = grouped.reindex(order)

grouped.plot(kind='bar', stacked=True, figsize=(10, 6), colormap='crest')

plt.title("Support tickets created by Day of the Week and Work Category", fontsize=14)
plt.xlabel("Day of the Week")
plt.ylabel("Number of Tickets")
plt.xticks(rotation=45)
plt.legend(title="Work Category")
plt.tight_layout()
plt.show()

#%% Hora del día
df_sprt['Created Hour'] = df_sprt['Created'].dt.hour

# Agrupar por hora y Work category
grouped = df_sprt.groupby(['Created Hour', 'Work category']).size().unstack(fill_value=0)


hour_labels = [f"{h%12 or 12} {'AM' if h < 12 else 'PM'}" for h in grouped.index]

# Gráfico de barras apiladas
grouped.plot(kind='bar', stacked=True, colormap='crest')

plt.title("Created support tickets by Hour of the Day and Work Category")
plt.xlabel("Hour of the Day")
plt.ylabel("Number of Tickets")
plt.xticks(rotation=45)
plt.legend(title="Work Category")
plt.tight_layout()
plt.show()

















# Recuentos generales 
# Volumen de tickets por año, mes, semana, día de semana. Hora
# Distribución de tipos de issue (Issue Type, Priority, Resolution).
# ¿Cuántos tickets se resolvieron? (Criterio: Closed existe > 1 en el changelog)


#Tiempos
# Tiempo promedio desde created hasta closed
# Tieme in this status por status
#Reopened

# ¿Quienes trabajan más?
# Distribución por assignee, reporter

# Ciclo de vida del ticket (visualizaciones chidas)

#storytelling
#visualizaciones
#Objetivo: Mostrar los resultados con impacto visual.
#Histogramas de tiempos de resolución.
#Gráficas de Gantt para flujos de tickets.
#Heatmap de estados vs. tiempo.
#Barras por ticket status a lo largo del tiempo.
#usar IA para analizar el summary y tal ves description


#Soporte vs Desarrollo 
#Cuál tiene mejor tiempo de respuesta?
#¿Cuál tiene más interacciones?


#peguntas
#¿Qué tipos de tickets se demoran más?
#¿Qué tan rápido damos la primera respuesta?
#¿Quiénes están asignando/resolviendo más?
#¿Qué tipo de ticket tiende a quedar mucho tiempo sin atención?
#¿Qué clientes (si están anonimizados) tienen más tickets o generan más esfuerzo?
# %%
