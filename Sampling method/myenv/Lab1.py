#!/usr/bin/env python3
from cProfile import label
import pandas as pd
import math
import numpy as np
import matplotlib.pyplot as plt
table = pd.read_csv('Bitcoin.csv')
totalSumColumn = 'High'  
totalSumsArray = table[totalSumColumn].values
# Із вибраних даних,обсягом не менше 1000, будь-яким чином обрати 100.
totalSumsArray=totalSumsArray[:100]
#Ранжувати вибірку (розташувати данні в порядку зростання).
totalSumsArray.sort()
#Знайти розмах вибірки.
m=8#m
interval_size = (totalSumsArray[99] - totalSumsArray[0]) / (m-1) #Ширина інтервалу k
x_start=totalSumsArray[0]-(interval_size/2) #х початкове
# Create a list of intervals
intervals = []
intervals_rangevalue=[]
accumulated_count=0
for i in range(m):
    interval_start = round(x_start + i * interval_size, 0)
    interval_end = round(x_start + (i + 1) * interval_size, 0)
    interval_middle = round((interval_start + interval_end) / 2, 1)
    interval_count = ((totalSumsArray > interval_start) & (totalSumsArray <= interval_end)).sum() #+ (totalSumsArray == interval_end).sum()+(totalSumsArray == interval_start).sum()
    interval_range = f"{interval_start}-{interval_end}"
    frequency=interval_count/100
    accumulated_count +=interval_count
    accumulated_frequency=accumulated_count/100
    intervals_rangevalue.append((interval_start,interval_end,interval_count))
    intervals.append((i + 1, interval_range, interval_middle, interval_count,frequency,accumulated_count,accumulated_frequency))
    
# Create a DataFrame from the list of intervals
df = pd.DataFrame(intervals, columns=['і', 'Діапазон', 'Cередина Хі', 'Частота Ni', 'Частість Wi', 'Накопичена частота','Накопичена частість'])
# Display the DataFrame and 
print('k=' + str(interval_size))
print('X початкове=' + str(x_start))
print(df)

### Полігон
xi_middle = [r[2] for r in intervals]  # x-coordinates of the vertices
wi = [r[4] for r in intervals]   # y-coordinates of the vertices
# Create a figure and axis
fig, ax = plt.subplots()
# Plot the polygon
ax.plot(xi_middle, wi, alpha=1)  # 'b' for blue color, alpha for transparency
ax.scatter(xi_middle, wi, color='black')
# Set x-axis and y-axis labels
plt.xticks(xi_middle)
plt.yticks(wi) 
ax.set_xlabel('Xі')
ax.set_ylabel('W')
ax.set_title('Полігон частот')
plt.show()

### Гістограма
range_start = [r[0] for r in intervals_rangevalue]
range_end = [r[1] for r in intervals_rangevalue]
value = [r[2] for r in intervals_rangevalue]
middle = [r[2] for r in intervals]
width = [r[1] - r[0] for r in intervals_rangevalue]

# Find the index of the tallest bar
max_index = np.argmax(value)

# Create the histogram
plt.bar(range_start, value, width=width, align='edge', edgecolor='black')

# Draw the lines connecting the left top end of the tallest bar with its left neighboring bar
plt.plot([range_start[max_index], range_start[max_index+1]], [value[max_index], value[max_index+1]], color='black', linestyle='-')
line1StartPoint = [range_start[max_index], range_start[max_index+1]]
line1EndPoint = [value[max_index], value[max_index+1]]
# Draw the lines connecting the right top end of the tallest bar with its right neighboring bar
plt.plot([range_end[max_index], range_end[max_index-1]], [value[max_index], value[max_index-1]], color='black', linestyle='-')
#Обрахування координати точки перетину
line1_start_point = np.array([range_start[max_index], value[max_index]])
line1_end_point = np.array([range_start[max_index+1], value[max_index+1]])

line2_start_point = np.array([range_end[max_index], value[max_index]])
line2_end_point = np.array([range_end[max_index-1], value[max_index-1]])

line1_direction = line1_end_point - line1_start_point
line2_direction = line2_end_point - line2_start_point

t1 = np.cross(line2_start_point - line1_start_point, line2_direction) / np.cross(line1_direction, line2_direction)
t2 = np.cross(line1_start_point - line2_start_point, line1_direction) / np.cross(line2_direction, line1_direction)

intersection_point = line1_start_point + t1 * line1_direction

print("Точка перетину: ", intersection_point)

plt.plot(intersection_point[0], intersection_point[1], 'ko')

# Add a text label for the intersection point
plt.text(intersection_point[0], intersection_point[1], f'Мода: ({intersection_point[0]:.2f})', ha='left', va='top', fontsize=12)

plt.xticks(middle)
plt.yticks(value)
plt.xlabel('Інтервали')
plt.ylabel('Частота')
plt.title('Гістограма')
plt.show()

###Кумулята
wi_accumulated = [r[6] for r in intervals] 

median_valueX = np.median(xi_middle)
median_valueY = np.median(wi_accumulated)
xi_middle.append(median_valueX)
wi_accumulated.append(median_valueY)
xi_middle.sort()
wi_accumulated.sort()
plt.plot(xi_middle, wi_accumulated, 'bo-')  # 'bo-' specifies blue color, circle markers, and solid line

for i in range(len(xi_middle)):
    plt.plot([xi_middle[i], xi_middle[i]], [0, wi_accumulated[i]], color='black', linestyle='dotted')  
    plt.plot([0, xi_middle[i]], [wi_accumulated[i], wi_accumulated[i]], color='black', linestyle='dotted') 
    if xi_middle[i] == median_valueX or wi_accumulated[i] == median_valueY:
        plt.plot([xi_middle[i], xi_middle[i]], [0, wi_accumulated[i]], color='red', linestyle='-',label='Медіана')  
        plt.plot([0, xi_middle[i]], [wi_accumulated[i], wi_accumulated[i]], color='red', linestyle='-') 
        plt.text(xi_middle[i], 0, f'{xi_middle[i]:.2f}', color='red', ha='center', va='top', rotation=0, fontsize=8)
        plt.text(0, wi_accumulated[i], f'{wi_accumulated[i]:.2f}', color='red', ha='right', va='bottom', rotation=0, fontsize=8)
xi_middle.remove(median_valueX)
wi_accumulated.remove(median_valueY)
plt.xticks(xi_middle) 
plt.yticks(wi_accumulated) 
plt.xlabel('Xі')
plt.ylabel('Wнак')
#plt.xticks(fontsize=8)
#plt.yticks(fontsize=8)
plt.title('Кумулята')
plt.legend()
plt.show()

###Пункт 4.a середнє значення
suma=0
for i in range(m):
    suma+=intervals[i][2]*intervals[i][3]
x_avarage=suma/100
suma=0
print('Середнє значення:'+str(x_avarage))
###Пункт 4.В Дисперсію, середнє квадратичне відхилення і коефіцієнт варіації розподілу
for i in range(m):
    suma+=((intervals[i][2]-x_avarage)**2)*intervals[i][3]
dispersion=suma/100
print('Дисперсія:'+str(dispersion))
print('Середнє квадратичне відхилення:'+str(math.sqrt(dispersion)))
print('Коефіцієнт валідації(%):'+str((math.sqrt(dispersion)/x_avarage)*100))
###Пункт 4.Г Коефіцієнт асиметрії та ексцес розподілу
suma=0
for i in range(m):
    suma+=(math.pow(intervals[i][2]-x_avarage,3))*intervals[i][3]
coef_asimetr=suma/(100*math.pow(math.sqrt(dispersion),3))
print('Kоефіцієнт асиметрії:'+str(coef_asimetr))
suma=0
for i in range(m):
    suma+=(math.pow(intervals[i][2]-x_avarage,4))*intervals[i][3]
exces=(suma/(100*math.pow(math.sqrt(dispersion),4)))-3
print('Ексцес розподілу:'+str(exces))