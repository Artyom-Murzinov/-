#Эвольвента зуба конической шестеренки!!!

from math import cos, sin, tan, pi, radians, atan, degrees, sqrt, acos, asin
import ezdxf
from ezdxf.math import ConstructionArc


def tooth_involute():
    z1 = 65
    z2 = 18
    m = 20
    angle = 20
    u = z1/z2 #Передаточное число
    Hae = 0.21 #Для конических шестеренок коэффициент высоты головки зуба
    Hael = (1+Hae) * m #Высота головки зуба
    Hfel = Hael + 0.2 * m #Высота ножки зуба
    p = m*pi #Шаг зубьев
    s = 0.5*p #Толщина зуба
    e = 0.5*p #Ширина впадин
    dividing_diameter = z2*m #Делительный диаметр
    Ugol_dd = degrees(atan(z2/z1)) #Угол делительный
    Mr = (dividing_diameter/2)/sin(radians(Ugol_dd)) #Межосевое растояние
    
    diameter_vertices = dividing_diameter + 2 * Hael * cos(radians(Ugol_dd)) #Внешний диаметр вершин
    diameter_depressions = dividing_diameter - 2 * Hfel * cos(radians(Ugol_dd)) #Диаметр впадин
    main_diameter = dividing_diameter * cos(radians(angle)) #Основная окружность
    point = (diameter_vertices - ((diameter_vertices - main_diameter)/3))/2 #Поиск точки 1/3 растояния окружности вершин и основной окружности
    katet = sqrt(point**2 - (main_diameter/2)**2) #Длина касательной из точки и основной окружности
    radius = (katet/4)*3 #Радиус эвольвенты
    #Расчет левой строны эвльвенты
    angles = degrees(asin((main_diameter/2)/(point))) #Расчет угла 
    point_X = point - radius*cos(radians(angles)) #Центр дуги эвольвенты X
    point_Y = radius*sin(radians(angles)) #Центр дуги эвольвенты Y
    angle1 = degrees(atan((point_Y / point_X))) # Угол расположения центра эвольвенты
    angle2 = degrees(acos(((diameter_vertices/2)**2 + (sqrt(point_X**2+point_Y**2))**2 - (radius)**2)/ (2*(diameter_vertices/2)*(sqrt(point_X**2+point_Y**2)))))
    point1_startX = (diameter_vertices/2)* cos(radians(angle1-angle2))  #Точки начала дуги X
    point1_startY = (diameter_vertices/2)* sin(radians(angle1-angle2))  #Точки начала дуги Y
    angle3 = degrees(acos(((diameter_depressions/2)**2 + (sqrt(point_X**2+point_Y**2))**2 - (radius)**2)/ (2*(diameter_depressions/2)*(sqrt(point_X**2+point_Y**2)))))
    point1_endX = (diameter_depressions/2)* cos(radians(angle1 - angle3))  #Точки конец дуги X
    point1_endY = (diameter_depressions/2)* sin(radians(angle1 - angle3))  #Точки конец дуги Y
    #Расчет правой стороны эвольвенты
    angle4 = degrees(acos(((dividing_diameter/2)**2 + (sqrt(point_X**2+point_Y**2))**2 - (radius)**2)/ (2*(dividing_diameter/2)*(sqrt(point_X**2+point_Y**2))))) #Точка пересечения эвольвенты и делительного диаметра
    angle5 = (360/z2)/4 
    angle6 = angle1 - (angle5+angle4)*2
    point_startX = (diameter_depressions/2)* cos(radians(angle6 + angle3))  #Точки начала дуги X
    point_startY = (diameter_depressions/2)* sin(radians(angle6 + angle3))  #Точки начала дуги Y
    point_endX = (diameter_vertices/2)* cos(radians(angle6 + angle2))  #Точки конец дуги X
    point_endY = (diameter_vertices/2)* sin(radians(angle6 + angle2))  #Точки конец дуги Y


    print(f'Диаметр вершин =      {diameter_vertices}мм')
    print(f'Делительный диаметр = {dividing_diameter}мм')
    print(f'Диаметр впадин =      {diameter_depressions}мм')
    print(f'Основная окружность = {main_diameter}mm')
    print(f'Межосевое расстояние = {Mr}')
    print(f'Толщина зуба = {s/cos(radians(Ugol_dd))}')

    

    doc = ezdxf.new('R2018')
    msp = doc.modelspace()
    
    # Построение радиусов в эвольвенту
    arc_rigt = ConstructionArc.from_2p_radius(start_point =(round(point1_startX, 4), round(point1_startY, 4)) , end_point =(round(point1_endX, 4), round(point1_endY, 4)), radius = round(radius, 4) , ccw = False, center_is_left = True)
    arc_ligt = ConstructionArc.from_2p_radius(start_point =(round(point_startX, 4), round(point_startY, 4)) , end_point =(round(point_endX, 4), round(point_endY, 4)), radius = round(radius, 4) , ccw = False, center_is_left = True)
    arc_depressions = ConstructionArc.from_2p_radius(start_point =(round(point1_endX, 4), round(point1_endY, 4)) , end_point =(round(point_startX, 4), round(point_startY, 4)), radius = round(diameter_depressions/2, 4) , ccw = False, center_is_left = True)
    # Запись в DXF файл
    arc_rigt.add_to_layout(msp)
    arc_depressions.add_to_layout(msp)
    arc_ligt.add_to_layout(msp)
    
    # Сохранение DXF файла
    doc.saveas("involute_tooth.dxf")

if __name__ == "__main__":
    tooth_involute()