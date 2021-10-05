from car_param_libs import road_params, tyres, engines, gear_ratio, Leiderman
from prettytable import PrettyTable
import math

car_weight = 78.7  # вес машины, кН
car_height = 3.3  # высота машины, м
cargo_weight = 37  # вес груза, кН
road_type = road_params.rolling_resistance.get('Асфальтовая')  # тип дороги
road_condition = road_params.adhesion.get('Асфальтовая сухая')  # состояние дороги
leading_rise = 0.03  # руководящий подъем 00/0
car_width = 2.5  # ширина машины, м
gear_box_type = gear_ratio.gear_ratio_dict.get('ZF9s1310')  # тип КПП
loaded_car_min_speed = 90  # минимальная скорость груженой машины, км/ч
loaded_car_max_speed = 110  # максимальная скорость груженой машины, км/ч
empty_car_speed = 120  # скорость порожней машины, км/ч
cabin_height = 2.8  # высота кабины, м
cabin_width = 2.5  # ширина кабины, м
car_engine = engines.engines_dict.get('ЯМЗ 240м2')  # двигатель
car_axles_amount = 2  # количество осей автомобиля
tyres_type = tyres.tyres_dict.get('260-508P')  # Обозначение шин
cg_car_height = 0.7  # высота центра тяжести ТС, м Hg
first_axle_to_cg_length = 1.8  # расстояние от центра тяжести до передней оси, м А
cg_to_last_axle_or_rocker_length = 2.2  # расстояние от центра тяжести до задней оси или балансира, м В
last_axle_to_cargo_Cg_length = 0.3  # расстояние от задней оси до центра тяжести груза, м br
cargo_cg_height = 1.2  # высота центра тяжести груза, м hr
hpp_to_last_axle_length = 1.1  # расстояние от точки приложения крюковой силы тяги
                                # до задней оси. м bкр (hpp - hook pull point)
hpp_height = 0.8  # высота приложения крюковой силы тяги, м hкр
last_axles_spacing = 0  # расстояние между задними осями, м С
gauge_width = 1.4  # ширина колеи, м B
wheels_on_axle_1 = 2  # количество колес на первой оси, шт.
wheels_on_axle_2 = 2  # количество колес на второй оси, шт.
# wheels_on_axle_3 = 2  # количество колес на третьей оси, шт.
Leider = Leiderman.Leiderman_dict.get('Дизельный')  # тип двигателя
n0 = 750  # начальная скорость построения скоростной характеристики
ntr = 0.8
lp2 = 1

F = car_height * car_width  # площадь сечения машины
nsh = car_axles_amount * 2  # nш
Me = 9550 * car_engine.get('Ne') / car_engine.get('ne')


def table_tuple_maker(fld_name_lst, t_title, *args):
    table = PrettyTable()
    table.field_names = fld_name_lst
    for arg in args:
        table.add_row([i for i in arg])
    file = open('results.txt', 'a', encoding='utf-8')
    file.write('\n\n')
    file.write('{}\n'.format(t_title))
    file.write(table.get_string())
    file.close()


def speed_charac_values(n, nmax, Nemax, A_L, B_L, A0_L, B0_L, gen_L, C0_L: float) -> tuple:
    """Функция рассчитывает необходимые значения для построения скоростной характеристики
        двигателя и возвращает их в виде кортежа значений"""
    Ne = Nemax * (A_L * (n / nmax) + B_L * (n / nmax) ** 2 - (n / nmax) ** 3)
    Me = 9550 * (Ne / n)
    gen = gen_L * (A0_L - B0_L * (n / nmax) + C0_L * (n / nmax) ** 2)
    Gt = Ne * gen / 1000

    return n, round(Ne, 1), round(Me, 1), round(gen, 1), round(Gt, 1)


def speed_charac_table(n0):
    """Функция передает значения скоростей в speed_charac_values(*args)
        полученные кортежи добавляет в список speed_list для их дальнейшего
        построчного использования. Формирует таблицу значений.
        Возвращает таблицу и список speed_list"""
    speed_list = []  # инициализируем список
    sc = PrettyTable()  # объявляем о создании таблицы
    sc.field_names = ['№', 'n, об/мин', 'Ne, кВт',
                      'Me, Н*м', 'gен, г/(кВт*ч)', 'Gt, кг/ч']
    n = n0  # начальное значение примем таким, каким оно будет передано из исходных данных
    for i in range(6):  # формируем шесть строк таблицы
        if i == 5:
            n = car_engine.get('ne')
        #  вызываем функцию
        string = speed_charac_values(
            n,
            nmax=car_engine.get('ne'),
            Nemax=car_engine.get('Ne'),
            A_L=Leider.get('A'),
            B_L=Leider.get('B'),
            A0_L=Leider.get('A0'),
            B0_L=Leider.get('B0'),
            gen_L=Leider.get('gен'),
            C0_L=Leider.get('C0')
        )

        speed_list.append(string)
        sc.add_row([i + 1, string[0], string[1], string[2], string[3], string[4]])
        n = (car_engine.get('ne') - n0) / 5 + n  # увеличиваем значение скорости

    return sc, speed_list


speed_characteristic = open('results.txt', 'w', encoding='utf-8')
speed_characteristic.write('Скоростная характеристика двигателя\n')
speed_characteristic.write(speed_charac_table(n0)[0].get_string())
speed_characteristic.close()
a_speed_list = speed_charac_table(n0)[1]
Me_list = [a_speed_list[i][2] for i in range(len(a_speed_list))]  # Список зн Me из скор. хар-ки
max_en_Me = max(Me_list)  # Максимальное Me
for i in a_speed_list:
    if max_en_Me in i:
        max_Me_en_speed = i[0]  # Соответствующее Me max значение n
only_speed_list = [a_speed_list[j][0] for j in range(len(a_speed_list))]




def conditions_values(f1, ip, va: float, load=0.0) -> tuple:
    """Рассчитывает значения Pk и Ne при выполнении условия,
        наложенного на скорость. Возвращает кортеж значений."""
    if va > 25:
        addition = (0.0006 * F * va ** 2) / 13
    else:
        addition = 0
    Pk_cond = (car_weight + load) * (f1 + ip) + addition
    Ne_cond = Pk_cond * va / (3.6 * ntr)

    return round(Pk_cond, 2), round(Ne_cond, 1)


for i_cond in range(3):  # формируем три условия
    if i_cond == 0:
        hard_val = conditions_values(road_type, leading_rise,
                                     loaded_car_min_speed, load=cargo_weight)
        hard_set = ('тяжелые', road_type, leading_rise,
                    loaded_car_min_speed, hard_val[0], hard_val[1])
    if i_cond == 1:
        mid_val = conditions_values(road_type - 0.002, leading_rise * 0.2,
                                    loaded_car_max_speed, load=cargo_weight)
        mid_set = ('средние', round(road_type - 0.002, 3), round(leading_rise * 0.2, 3),
                   loaded_car_max_speed, mid_val[0], mid_val[1])
    if i_cond == 2:
        # при движении в легких условиях, машина не перевозит груз
        light_val = conditions_values(road_type - 0.005, 0, empty_car_speed)  # отсутствие им.арг.
        light_set = ('легкие', round(road_type - 0.005, 3), 0,
                     empty_car_speed, light_val[0], light_val[1])

# Выделяем максимальные значения Pk и N из таблицы условий
max_speed = max(hard_set[3], mid_set[3], light_set[3])
max_Pk_cond = max(hard_set[4], mid_set[4], light_set[4])
max_Ne_cond = max(hard_set[5], mid_set[5], light_set[5])

# Запись результата в файл
conds = PrettyTable()
conds.field_names = ['Условия движения', 'f1', 'ip, 00/0', 'Va, км/ч', 'Pk', 'Ne']
conds.add_row([i for i in hard_set])
conds.add_row([i for i in mid_set])
conds.add_row([i for i in light_set])
conditions = open('results.txt', 'a', encoding='utf-8')
conditions.write('\n\n')
conditions.write('Параметры движения\n')
conditions.write(conds.get_string())
conditions.write('\nМаксимальные значения: Va = {}, Pk = {}, Ne = {}\n'.format(
                                max_speed, max_Pk_cond, max_Ne_cond))
conditions.close()


def auxiliary_calculations_1():
    """Производит промежуточные расчеты для таблицы промежуточных
    расчетов 1 и возвращает кортеж значений"""
    Zk = (cargo_weight + car_weight) / nsh
    Rc = tyres_type.get('sr') / 1000
    Rd = Rc * tyres_type.get('delta')
    pic_type = tyres_type.get('pic_type')
    Kd = (max_Pk_cond * Rd) / (Me * ntr) * 10 ** 3
    Kc = ((car_weight + cargo_weight) * road_condition * Rd) / (Me * ntr) * 10 ** 3

    return car_engine.get('ne'), Zk, Rc, road_condition, round(Rd, 3), \
           pic_type, round(Kd, 2), round(Kc, 5)


ac_1_tpl = auxiliary_calculations_1()
table_tuple_maker(['nн', 'Zk, кН', 'Rc, м', 'Коэфф. деформ.',
                   'Rд, м', 'Тип рисунка', 'Kд', 'Kc'], 'Промежуточные вычисления 1', ac_1_tpl)


def auxiliary_calculations_2():
    """Производит промежуточные расчеты для таблицы промежуточных
    расчетов 2 и возвращает кортеж значений"""
    K1 = (ac_1_tpl[6] + ac_1_tpl[7]) / 2
    Kvys = 0.377 * ((ac_1_tpl[4] * ac_1_tpl[0]) / max_speed)
    m = (math.log10(K1 / Kvys) / math.log10(ac_1_tpl[0] / max_Me_en_speed)) + 1
    l0 = Kvys / (sorted(gear_box_type.values())[0] * lp2)
    q = sorted(gear_box_type.values())[-1] / sorted(gear_box_type.values())[-2]

    return round(K1, 3), round(Kvys, 2), round(m, 2), \
        lp2, round(l0, 2), round(q, 2)


ac_2_tpl = auxiliary_calculations_2()
table_tuple_maker(['K1', 'K выс', 'm', 'lp2', 'l0', 'q'],
                  'Промежуточные вычисления 2', ac_2_tpl)


def auxiliary_calculations_3():
    """Производит промежуточные расчеты для таблицы промежуточных
    расчетов 3 и возвращает кортеж значений"""
    lp1 = (ac_2_tpl[3] * (ac_2_tpl[5] + 1)) / 2
    F_ac3 = cabin_width * cabin_height
    g = 10

    return lp1, F_ac3, g, max_en_Me, max_Me_en_speed


ac_3_tpl = auxiliary_calculations_3()
table_tuple_maker(['lp1', 'F, м^2', 'g, м/с^2', 'Me макс, Н/м', 'nм, об/мин'],
                  'Промежуточные вычисления 3', ac_3_tpl)


def transmission_ratios(lp, l0):
    """Возвращает список передаточных чисел трансмиссии"""
    tr_list = [round(gr_num * lp * l0, 1)
               for gr_num in gear_box_type.values()]

    return tr_list


table_tuple_maker([str(i + 1) for i in range(len(gear_box_type))],
                  'Передаточные числа КПП', gear_box_type.values())

Rkpp_reg_1 = transmission_ratios(ac_2_tpl[3], ac_2_tpl[4])
table_tuple_maker([str(i + 1) for i in range(len(gear_box_type))],
                  'Передаточные числа трансмиссии для режима РКПП 1', Rkpp_reg_1)
Rkpp_reg_2 = transmission_ratios(ac_3_tpl[0], ac_2_tpl[4])
table_tuple_maker([str(i + 1) for i in range(len(gear_box_type))],
                  'Передаточные числа трансмиссии для режима РКПП 2', Rkpp_reg_2)

#---------------------Формирование таблиц Vai, Pki, Pai--------------------------------#


def va_trans_char(seq, i_val):
    lst = []
    for i_rat in seq:
        lst.append(round(0.377 * ((ac_1_tpl[4] * i_val) / i_rat), 1))
    return lst


def pk_trans_char(seq, i_val):
    lst = []
    for i_rat in seq:
        lst.append(round(((i_val * i_rat * ntr) / ac_1_tpl[4] * 10 ** -3), 1))
    return lst


def pa_trans_char(Va, Pk):
    general_list = []
    for i_row in range(len(Va)):
        lst = []
        for val in range(len(Va[i_row])):
            if Va[i_row][val] > 25:
                lst.append(round(Pk[i_row][val] - ((0.006 * F * Va[i_row][val]) / 13), 1))
            else:
                lst.append(Pk[i_row][val])
        general_list.append(lst)
    return general_list


Va1_i = []
Va2_i = []
for i_speed in only_speed_list:
    Va1_i.append(va_trans_char(Rkpp_reg_1, i_speed))
    Va2_i.append(va_trans_char(Rkpp_reg_2, i_speed))

Pk1_i = []
Pk2_i = []
for i_Me in Me_list:
    Pk1_i.append(pk_trans_char(Rkpp_reg_1, i_Me))
    Pk2_i.append(pk_trans_char(Rkpp_reg_2, i_Me))


Pa1_i = pa_trans_char(Va1_i, Pk1_i)
Pa2_i = pa_trans_char(Va2_i, Pk2_i)


headr_1 = ['Va1 1', 'Va1 2', 'Va1 3', 'Va1 4',
           'Va1 5', 'Va1 6', 'Va1 7', 'Va1 8',
           'Va1 9', 'Va1 10', 'Va1 11', 'Va1 12',
           'Va1 13', 'Va1 14', 'Va1 15', 'Va1 16']
headr_2 = ['Va2 1', 'Va2 2', 'Va2 3', 'Va2 4',
           'Va2 5', 'Va2 6', 'Va2 7', 'Va2 8',
           'Va2 9', 'Va2 10', 'Va2 11', 'Va2 12',
           'Va2 13', 'Va2 14', 'Va2 15', 'Va2 16']
headr_3 = ['Pk1 1', 'Pk1 2', 'Pk1 3', 'Pk1 4',
           'Pk1 5', 'Pk1 6', 'Pk1 7', 'Pk1 8',
           'Pk1 9', 'Pk1 10', 'Pk1 11', 'Pk1 12',
           'Pk1 13', 'Pk1 14', 'Pk1 15', 'Pk1 16']
headr_4 = ['Pk1 1', 'Pk1 2', 'Pk1 3', 'Pk1 4',
           'Pk1 5', 'Pk1 6', 'Pk1 7', 'Pk1 8',
           'Pk1 9', 'Pk1 10', 'Pk1 11', 'Pk1 12',
           'Pk1 13', 'Pk1 14', 'Pk1 15', 'Pk1 16']
headr_5 = ['Pa1 1', 'Pa1 2', 'Pa1 3', 'Pa1 4',
           'Pa1 5', 'Pa1 6', 'Pa1 7', 'Pa1 8',
           'Pa1 9', 'Pa1 10', 'Pa1 11', 'Pa1 12',
           'Pa1 13', 'Pa1 14', 'Pa1 15', 'Pa1 16']
headr_6 = ['Pa1 1', 'Pa1 2', 'Pa1 3', 'Pa1 4',
           'Pa1 5', 'Pa1 6', 'Pa1 7', 'Pa1 8',
           'Pa1 9', 'Pa1 10', 'Pa1 11', 'Pa1 12',
           'Pa1 13', 'Pa1 14', 'Pa1 15', 'Pa1 16']

table_tuple_maker(headr_1[:len(Rkpp_reg_1)],
                  'Va1 для РКПП 1', Va1_i[0], Va1_i[1], Va1_i[2],
                  Va1_i[3], Va1_i[4], Va1_i[5])

table_tuple_maker(headr_2[:len(Rkpp_reg_2)],
                  'Va2 для РКПП 2', Va2_i[0], Va2_i[1], Va2_i[2],
                  Va2_i[3], Va2_i[4], Va2_i[5])

table_tuple_maker(headr_3[:len(Rkpp_reg_1)],
                  'Pk1 для РКПП 1', Pk1_i[0], Pk1_i[1], Pk1_i[2],
                  Pk1_i[3], Pk1_i[4], Pk1_i[5])

table_tuple_maker(headr_4[:len(Rkpp_reg_2)],
                  'Pk2 для РКПП 2', Pk2_i[0], Pk2_i[1], Pk2_i[2],
                  Pk2_i[3], Pk2_i[4], Pk2_i[5])

table_tuple_maker(headr_5[:len(Rkpp_reg_1)],
                  'Pa1 для РКПП 1', Pa1_i[0], Pa1_i[1], Pa1_i[2],
                  Pa1_i[3], Pa1_i[4], Pa1_i[5])

table_tuple_maker(headr_6[:len(Rkpp_reg_2)],
                  'Pa2 для РКПП 2', Pa2_i[0], Pa2_i[1], Pa2_i[2],
                  Pa2_i[3], Pa2_i[4], Pa2_i[5])

#---------------------------------------------end---------------------------------------------#


