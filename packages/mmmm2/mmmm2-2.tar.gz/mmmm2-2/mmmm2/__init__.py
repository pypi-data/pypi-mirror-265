def poleznost():
    s = '''x1, x2 = symbols('x1, x2')
u = ln(x1 + 4) + 3*ln(x2);
print(u)

# Предельная полезность по 1 благу:
Mu1 = u.diff(x1); Mu1 #Положительна, так как x1 > -4
# Предельная полезность по 2 благу:
Mu2 = u.diff(x2); Mu2 #Положительна, так как x2 > 0

# Эластичность функции полезности относительно первого блага:
Au1 = u / x1; Au1
# Эластичность функции полезности относительно второго блага:
Au2 = u / x2; Au2
    '''
    return pc.copy(s)

def kobb_duglas_bez_y0_c0():
    s = '''K, L = symbols('K, L')
alpha, beta = 0.2, 0.8
w, r = 3, 5
c0 = 1732
Y = K**alpha * L**beta;
print(Y)
C_mv = K*r + L*w
print(C_mv)
# Функция Лагранжа
lmd = symbols('lambda')
L_mv =Y + lmd*(c0 - C_mv)
print(L_mv)
Lr = simplify(nsolve([L_mv.diff(K), L_mv.diff(L), L_mv.diff(lmd)], [K, L, lmd],[1, 1, 1], dict = True)[0])
print(Lr)
print(f'Капитал: {Lr[K]}, Труд: {Lr[L]}')
    '''
    return pc.copy(s)

def lagranzh_roy():
    s = '''x1, x2, l = symbols('x1, x2, lambda')
p1 = 6
p2 = 7
I = 194

#Ф-я полезности
u = x1**(0.3) * x2**(0.6)
print(u)
#Ф-я Лагранжа
L = u + l*(I - p1*x1 - p2*x2)
print(L)
# Ф-я спроса Маршалла-Вальраса
MV = nsolve((L.diff(x1), L.diff(x2), L.diff(l)), (x1,x2,l), (11, 8, 1), dict = True)[0]
print(MV)
#Уровни потребления благ
print(f'x1: {MV[x1]}, x2: {MV[x2]}')
# Косвенная функция полезности
U = u.subs(MV)
print(U)
delta = 0.01
U_new = U - MV[l]*delta*x1_new
print(U_new)
alpha = 0.3
x1_new = (U_new/U)**(1/alpha)*MV[x1]
print(x1_new, MV[x1])
print(f'Разница в спросе \nx1: {MV[x1]-x1_new}')
    '''
    return pc.copy(s)

def polezn_lagranzh():
    s = '''alpha, beta, a, b, p1, p2, u0 = 0.4, 0.1, 7, 5, 4, 6, 2.5
x1, x2, Lambda = symbols('x1, x2, Lambda')
u = x1**alpha * (x2-a)**beta
c = x1*p1 + x2*p2
print(u, c)
L = c + Lambda*(u0 - u);
print(L)
A = nsolve([L.diff(x1), L.diff(x2), L.diff(Lambda)], [x1, x2, Lambda], [10, 14, 12], dict=True)[0]
print(A)

# Оптимальный уровень первого блага
X1 = A[x1]; X1
# Оптимальный уровень второго блага
X2 = A[x2]; X2
# Целевая функция потребителя
U = u.subs(A);
print(U)
    '''
    return pc.copy(s)

def hiks():
    s = '''p1, p2, u0, alpha, beta, a1, a2 = sp.symbols('p1 p2 u0 alpha beta a1 a2')
x1_star = (u0 / (p1 / p2 * beta/alpha)**beta)**(1 / (alpha + beta))+ a1
x2_star = (u0 * (p1 / p2 * beta/alpha)**alpha)**(1 / (alpha + beta))+ a2
# Определяем косвенную функцию расходов потребителя
E = p1 * x1_star + p2 * x2_star

# Вычисляем матрицу Слуцкого
S = sp.Matrix([[sp.diff(x1_star, p1), sp.diff(x1_star, p2)],
               [sp.diff(x2_star, p1), sp.diff(x2_star, p2)]])

#Матрица Слуцкого показывает, как изменяется спрос на благо в ответ на изменение его цены при постоянном уровне дохода. Она определяется как разность между эффектом дохода и эффектом замещения.
#Важно отметить, что блага в модели Хикса относятся к классу нормальных благ. Это подтверждается отрицательными элементами на главной диагонали матрицы Слуцкого, что означает,
#что с увеличением цены на благо у потребителя уменьшается его спрос при постоянном уровне дохода.
    '''
    return pc.copy(s)


def kobb_duglac_c0():
    s = '''K, L, alpha, beta, A = symbols('K, L, alpha, beta, A', positive=True)
Y = A * K**alpha * L**beta
print(Y)

# Свойство 1
Y.subs(K, 0) == 0, Y.subs(L, 0) == 0
# Свойство 2
Y.diff(K) > 0, Y.diff(L) > 0
# Свойство 3
display(Y.diff(K, 2) < 0) # должно быть тру
Y.diff(L, 2) < 0 # должно быть тру
# Свойство 4
m = symbols('m')
simplify(Y.subs([(K, m*K), (L, m*L)]) / Y)
alpha, beta, w, r, C0 = 0.54, 0.46, 8, 3, 2150
l = symbols('lambda', positive=True)
C = r*K + w*L;
print(C)
Y = K**alpha * L**beta
print(Y)
Lgr = Y + l*(C0 - C);
print(Lgr)
S_lr = nsolve([Lgr.diff(K), Lgr.diff(L), Lgr.diff(l)], [K, L, l], [1, 1, 1], dict=True)[0];
print(S_lr)
K_lr = S_lr[K];
print(K_lr)
L_lr = S_lr[L];
print(L_lr)
Y_max = Y.subs([(K, K_lr), (L, L_lr)]);
print(Y_max)
# alpha, beta - это эластичность выпуска капитала и рабочей силы соответственно
    '''
    return pc.copy(s)

def u0_i_vector_cen_P():
    s = '''x1, x2, alpha, beta, p1, p2, I, Lambda, u0, a = symbols('x1, x2, alpha, beta, p1, p2, I, lambda, u0, a', positive=True)
alpha, beta, a, p1, p2, u0 = 0.6, 0.3, 6, 3, 4.2, 5.3
u = x1**alpha * (x2-a)**beta
c = x1*p1 + x2*p2
print(u, c)
L = c + Lambda*(u0 - u)
print(L)
L.diff(x1)
print(L)
Sol = nsolve([L.diff(x1), L.diff(x2), L.diff(Lambda)], [x1, x2, Lambda],[7, 12, 10], dict=True)[0]; SolSol = nsolve([L.diff(x1), L.diff(x2), L.diff(Lambda)], [x1, x2, Lambda],[7, 12, 10], dict=True)[0]
print(Sol)
print(c.subs(Sol) == L.subs(Sol)) # Предельные расходы потребителя равны множетелю Лагранжа
    '''
    return pc.copy(s)

def marshal_lagransh():
    s = '''p1, p2, I, a0, a1, a2, l = sp.symbols('p1 p2 I a0 a1 a2 l')

# Определяем функцию полезности и функции спроса по Маршаллу
u = a0 * (I / p1 * a1 / (a1 + a2))**a1 * (I / p2 * a2 / (a1 + a2))**a2
x1_star = I / p1 * a1 / (a1 + a2)
x2_star = I / p2 * a2 / (a1 + a2)

# Находим множитель Лагранжа
L = u - l * (p1 * x1_star + p2 * x2_star - I)
Множитель Лагранжа связан с оптимизацией функции полезности при наличии ограничения бюджета. Он отражает предельную полезность дополнительной единицы расходов на потребление при заданных ценах и уровне дохода.
    '''
    return pc.copy(s)

def firma_na_konk_rinke():
    s = '''price = 16  # Цена продажи продукции
capital_price = 6  # Цена аренды капитала 
capital_quantity = 56  # Количество капитала
wage_rate = 3  # Ставка заработной платы 
production_function_coefficient = 0.5  # Коэффициенты производственной функции

# Задаем переменные
l = sp.Symbol('l')

# Затраты на капитал и труд
capital_costs = capital_price * capital_quantity
labor_costs = wage_rate * l

# Производственная функция
production_function = (capital_quantity ** 0.5) * (l ** 0.5)

# Прибыль
revenue = price * production_function
costs = capital_costs + labor_costs
profit = revenue - costs

# Находим оптимальное количество труда, максимизирующее прибыль
optimal_labor_quantity = sp.solve(sp.diff(profit, l), l)[0]

# Выпуск при оптимальном количестве труда
optimal_output = production_function.subs(l, optimal_labor_quantity)

# Вывод результатов
print("Оптимальное количество труда:", optimal_labor_quantity)
print("Выпуск фирмы при оптимальном количестве труда:", optimal_output)
    '''
    return pc.copy(s)

def voprosa_4():
    s = '''from sympy import *
L, K, alpha, beta, lamda = symbols('L, K, alpha, beta, lamda')
alpha, beta = 0.6, 0.4
K = 75
Y = K **alpha*L**beta
w = 2
r = 4
p = 10
Lagr = p*Y - w*L - r*K
L_max = solve(diff(Lagr, L))[0]
C = w*L_max + r*K
print(C)
Delta_w = symbols('Delta_w')
from sympy import *
L, K, alpha, beta, lamda = symbols('L, K, alpha, beta, lamda')
alpha, beta = 0.6, 0.4
K = 75
Y = K **alpha*L**beta
w = 2 + Delta_w
r = 4
p = 10
Lagr = p*Y - w*L - r*K
L_max = solve(diff(Lagr, L), L)[0]
display((Y.subs(L, L_max)))
    '''
    return pc.copy(s)


def kobb_duglas_y0():
    s = '''L, K, alpha, beta, lamda= symbols('L, K, alpha, beta, lamda')
alpha, beta = 0.7, 0.5  #опциональноY = K **alpha*L**beta
w = 4
r = 6C = w*L + r*K
Y0 = 420Lagrange = w*L + r*K + lamda*(Y0 - Y)
Sl = nsolve([diff(Lagrange, K), diff(Lagrange, L), diff(Lagrange, lamda)], [L, K, lamda], [1, 1, 1], dict = True)[0]print(Sl)
L, K, alpha, beta, lamda= symbols('L, K, alpha, beta, lamda')Y = K **alpha*L**beta
MPK = diff(Y, K)display(MPK)
MPL = diff(Y, L)display(MPL)
MRS = MPL/MPKdisplay(MRS)
#Показатель степени $α$ показывает, насколько сильно выпуск зависит от количества используемого капитала.#Чем больше значение $α$, тем больше влияние капитала на объём производства.
Показатель степени $β$ показывает, насколько сильно выпуск зависит от количества используемого труда.
#Чем больше значение $β$, тем больше влияние труда на объём производства.
    '''
    return pc.copy(s)
