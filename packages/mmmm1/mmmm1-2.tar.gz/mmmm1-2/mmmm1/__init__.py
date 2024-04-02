import pyperclip as pc
    
def imports():
    s = '''from sympy import *
from sympy.plotting import *
    '''
    return pc.copy(s)
    
def poleznost():
    s = '''x1, x2 = symbols('x1 x2')
u_pl = ln(x1 + 1) + 3*ln(x2)
plot3d(u_pl, (x1, 12, 22), (x2, 14,24), title="Функция полезности")
#a) Подставляем случайное число x1 в функцию
u_pl_x1 = u_pl.subs(x1, 10)
print(u_pl_x1)
plot(u_pl_x1, (x2, 1, 22))

Выполняется свойство: Если $x_2^2 > x_2^1$, то $U(x_2^2, x_1) > U(x_2^1, x_1)$
print(u_pl.diff(x1))
С учётом, что $x_1$ > -1 и $x_2$ > 0, то производная всегда больше 0. Свойство функции полезности выполняется.
Подставляем случайное число 𝑥2 в функцию
u_pl_x2 = u_pl.subs(x2, 15)
print(u_pl_x2)

Выполняется свойство: Если $x_1^2 > x_1^1$, то $U(x_1^2, x_2) > U(x_1^1, x_2)$
u_pl.diff(x2)
С учётом, что $x_1$ > -1 и $x_2$ > 0, то производная всегда больше 0. Свойство функции полезности выполняется.

# б) Частная производная по x1:
dU_dx1 = u_pl.diff(x1)
dU_dx2 = u_pl.diff(x2)
print(dU_dx1)
#Частная производная по  𝑥2
print(dU_dx2)
#Предельная норма замещения первого блага вторым
MRS1 = dU_dx1 / dU_dx2
print(MRS1)
#Предельная норма замещения второго блага первым
MRS2 = dU_dx2 / dU_dx1
print(MRS2)
#Значимость функции полезности по  𝑥1
print(dU_dx1 * x1 / u_pl)
#Значимость функции полезности по  𝑥2
print(dU_dx2 * x2 / u_pl)
#Функция эластичности показывает, на сколько процентов изменится функция U при увеличении на процент $X_i$
    '''
    return pc.copy(s)
    
def kobb_duglas_bez_y0_c0():
    s = '''K, L, alpha, beta, r, w, Y0, lamda = symbols("K, L, alpha, beta, r, w, Y0, lamda", positive = True)
Y = K**alpha * L**beta
print(Y)
C = r*K + w*L
print(C)
Lgr = C + lamda*(Y0 - Y)
print(Lgr)
S_lr = solve([Lgr.diff(K), Lgr.diff(L), Lgr.diff(lamda)], [K, L, lamda], dict=True)[0]
print(S_lr)
K_lr = simplify(separatevars(S_lr[K]))
print(K_lr)
L_lr = simplify(separatevars(S_lr[L]))
print(L_lr)
lamda_lr = simplify(separatevars(S_lr[lamda]))
print(lamda_lr)
C_min = simplify(separatevars(C.subs([(K, K_lr), (L, L_lr), (lamda, lamda_lr)])))
print(C_min)
K_lr.subs([(alpha, 0.2), (beta, 0.8), (w, 3), (r, 5), (Y0, 1732)]) # требуется
L_lr.subs([(alpha, 0.2), (beta, 0.8), (w, 3), (r, 5), (Y0, 1732)]) # требуется
lamda_lr.subs([(alpha, 0.2), (beta, 0.8), (w, 3), (r, 5), (Y0, 1732)]) # не факт?
C_min.subs([(alpha, 0.2), (beta, 0.8), (w, 3), (r, 5), (Y0, 1732)]) # не факт?
    '''
    return pc.copy(s)

def lagranzh_roy():
    s = '''x1,x2, p1, p2, alpha, beta, I, lamda  = symbols("x1, x2, p1, p2, alpha, beta, I, lamda")
c = p1*x1 + p2*x2
u = (x1-9)**alpha * (x2-7)**beta
L = u + lamda * (I - c)
print(c)
print(u)
L = L.subs([(alpha, 0.3), (beta, 0.6), (p1, 6), (p2, 7), (I, 194)])
print(L)
A = nsolve([L.diff(x1), L.diff(x2), L.diff(lamda)], [x1,x2,lamda], [1,1,1], dict=True)[0]
print(A)
x1_best = re(A[x1])
x2_best = re(A[x2])
lamda_best = re(A[lamda])
print(x1_best)
print(x2_best)
print(lamda_best)
u = u.subs([(x1,x1_best), (x2, x2_best), (alpha, 0.3), (beta, 0.6)])
print(u)
u_new = u - lamda_best * x1_best * 0.01
print(u_new) # Тождество Роя
#Пусть цена на первое благо возвосла на 0.01
x1,x2, p1, p2, alpha, beta, I, lamda  = symbols("x1, x2, p1, p2, alpha, beta, I, lamda", positive=True)
c = p1*x1 + p2*x2
u = (x1-9.01)**alpha * (x2-7)**beta
L = u + lamda * (I - c)
L = L.subs([(alpha, 0.3), (beta, 0.6), (p1, 6), (p2, 7), (I, 194)])
A = nsolve([L.diff(x1), L.diff(x2), L.diff(lamda)], [x1,x2,lamda], [1,1,1], dict=True)[0]
x1_best = re(A[x1])
x2_best = re(A[x2])
lamda_best = re(A[lamda])
print(x1_best)
print(x2_best)
print(lamda_best)
u = u.subs([(x1,x1_best), (x2, x2_best), (alpha, 0.3), (beta, 0.6)])
print(u)
    '''
    return pc.copy(s)
    
def polezn_lagranzh():
    s = '''x1,x2, p1, p2, alpha, beta, lamda, u0  = symbols("x1, x2, p1, p2, alpha, beta, lamda, u0", positive=True)
c = 6*x1 + 4*x2
u = x1**0.4 * (x2-7)**0.6
L = c + lamda * (5.3 - u)
print(L)
Sol = solve([L.diff(x1), L.diff(x2), L.diff(lamda)],[x1,x2,lamda], dict=True)[0]
print(Sol)
x1_best = Sol[x1]
x2_best = Sol[x2]
lamda_best = Sol[lamda]
print(x1_best)
print(x2_best)
print(lamda_best)
C_min = c.subs([(x1, x1_best), (x2, x2_best)])
print(C_min)
x1_new = x1_best
print(x1_new)
x2_new = x2_best
print(x2_new)
lamda_new = lamda_best
print(lamda_new)
    '''
    return pc.copy(s)
    
def hiks():    
    s = '''p1, p2, u0, alpha, beta, a1, a2 = sp.symbols('p1 p2 u0 alpha beta a1 a2')
x1_star = (u0 / (p1 / p2 * beta/alpha)**beta)**(1 / (alpha + beta))+ a1
x2_star = (u0 * (p1 / p2 * beta/alpha)**alpha)**(1 / (alpha + beta))+ a2
# Определяем косвенную функцию расходов потребителя
E = p1 * x1_star + p2 * x2_star
# Вычисляем матрицу Слуцкого
S = sp.Matrix([[sp.diff(x1_star, p1), sp.diff(x1_star, p2)], [sp.diff(x2_star, p1), sp.diff(x2_star, p2)]])
#Матрица Слуцкого показывает, как изменяется спрос на благо в ответ на изменение его цены при постоянном уровне дохода. Она определяется как разность между эффектом дохода и эффектом замещения.
#Важно отметить, что блага в модели Хикса относятся к классу нормальных благ. Это подтверждается отрицательными элементами на главной диагонали матрицы Слуцкого, что означает,что с увеличением цены на благо у потребителя уменьшается его спрос при постоянном уровне дохода.
    '''    
    return pc.copy(s)


def kobb_duglas_y0():
    s = '''r, w, Y0, lamda = symbols("r, w, Y0, lamda", positive = True)
C = r*K + w*L
Y = K**alpha * L**beta
print(C)
Lgr = C + lamda*(Y0 - Y)
print(Lgr)
S_lr = solve([Lgr.diff(K), Lgr.diff(L), Lgr.diff(lamda)], [K, L, lamda], dict=True)[0]
print(S_lr)
K_lr = simplify(separatevars(S_lr[K]))
print(K_lr)
L_lr = simplify(separatevars(S_lr[L]))
print(L_lr)
lamda_lr = simplify(separatevars(S_lr[lamda]))
print(lamda_lr)
C_min = simplify(separatevars(C.subs([(K, K_lr), (L, L_lr), (lamda, lamda_lr)])))
print(C_min)
K_lr.subs([(alpha, 0.4), (beta, 0.6), (w, 4), (r, 10), (Y0, 120)])
L_lr.subs([(alpha, 0.4), (beta, 0.6), (w, 4), (r, 10), (Y0, 120)])
lamda_lr.subs([(alpha, 0.4), (beta, 0.6), (w, 4), (r, 10), (Y0, 120)])
C_min.subs([(alpha, 0.4), (beta, 0.6), (w, 4), (r, 10), (Y0, 120)])
    '''
    return pc.copy(s)
   
def kobb_duglas_c0():
    s = '''r, w, Y0, lamda = symbols("r, w, Y0, lamda", positive = True)
K, L, alpha, beta, A = symbols("K, L, alpha, beta, A", positive = True)
C = r*K + w*L
Y = K**alpha * L**beta
Lgr = C + lamda*(Y0 - Y)
S_lr = solve([Lgr.diff(K), Lgr.diff(L), Lgr.diff(lamda)], [K, L, lamda], dict=True)[0]
K_lr = simplify(separatevars(S_lr[K]))
L_lr = simplify(separatevars(S_lr[L]))
lamda_lr = simplify(separatevars(S_lr[lamda]))
C_min = simplify(separatevars(C.subs([(K, K_lr), (L, L_lr), (lamda, lamda_lr)])))
print(K_lr.subs([(alpha, 0.54), (beta, 0.46), (w, 8), (r, 3), (Y0, 2150)]))
print(L_lr.subs([(alpha, 0.54), (beta, 0.46), (w, 8), (r, 3), (Y0, 2150)]))
print(lamda_lr.subs([(alpha, 0.54), (beta, 0.46), (w, 8), (r, 3), (Y0, 2150)]))
print(C_min.subs([(alpha, 0.54), (beta, 0.46), (w, 8), (r, 3), (Y0, 2150)]))
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
    s = '''a1, a2, p1, p2, I, x1, x2 = symbols('a1 a2 p1 p2 I x1 x2')
x1_star = 1 / p1 * a1 / (a1 + a2)
x2_star = 1 / p2 * a2 / (a1 + a2)
u = a1 * x1 ** a1 * x2 ** a2
u_star = u.subs({x1: x1_star, x2: x2_star})
V = u_star.simplify()
dV_dp2 = diff(V, p2)
x2_star_I = x2_star.subs({p1: I/x1})
dx2_star_dI = diff(x2_star_I, I).simplify()
λ_star = solve(a1 * p1 * x1 ** (a1 - 1) * x2 ** a2 - p1, x1)[0]
print(V, dV_dp2, dx2_star_dI, λ_star)
#Косвенная функция полезности имеет вид:
print(V)
#Тождество Роя
print(dV_dp2)
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
