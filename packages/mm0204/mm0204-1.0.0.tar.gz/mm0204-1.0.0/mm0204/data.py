data = {
    'task_0' : '''
Важные характеристики полезности:

- Предельная полезность - $\Mu_x = u_x'$ (сколько приносит доп. единица блага пользы)
- Предельная норма замещения - $MRS_{12} = \frac{\Mu_1}{\Mu_2}$ (сколько приносит другое благо пользы при уменьшении первого на единицу)
- Средняя полезность - $Au_1 = \frac u {x_1}$ (сколько благо в среднем приносит пользы)
- Эластичность - $Eu_1 = \frac{\Mu_1}{Au_1}$ (на сколько % изменится одно благо при изменении другого на 1%)


Два типа моделей:

- Маршала (максимизация полезности при заданном доходе)
- Хикса (минимизация затрат при заданной полезности)


Для решения с помощью Лагранжа используется следующая схема:

Пусть $X$ - некоторая функция для максимизации (минимизации), $Y$ - некоторое условие, $y_0$ - значение, ограничивающее условие, тогда: 

$L = X + \lambda (y_0 - Y)$

Решить систему:

$\begin{cases}
L_{x_1}' = 0 \\
L_{x_2}' = 0 \\
L_\lambda' = 0
\end{cases}$


Смысл множителя Лагранжа: предельная полезность по доходу потребителя или по полезности

Можно его найти, имея косвенную функцию полезности:

$\lambda^* = U_I'$


Тождество Роя: $u_{p_i}' = -x_i^*\lambda^*$

Если $d$ - величина, на которое изменилось благо $x_i$, то

$u_{new} = u_{old} - \lambda^* x_i^* d$


Лемма Шепарда:

Если $\Delta p_i$ - изменение цены $p_i$, то

$С_{new} = С_{old} + x_i^* \Delta p_i$


Косвенная функция полезности по Маршалу:

$u(x_1^*, x_2^*)$


Косвенная функция расходов потребителя по Хиксу:

$C^* = p_1 x_1^* + p_2 x_2^*$


Матрица Слуцкого:

$\begin{bmatrix}
C''_{p_1, p_1} & C''_{p_1, p_2} \\
C''_{p_2, p_1} & C''_{p_2, p_2}
\end{bmatrix}$


Матрица показывает, что:

- так как функция расходов выпукла вверх, то диагональные элементы матрицы отрицательны
- показывает, что блага в модели Хикса - обыкновенные и не являются продуктами Гиффена (то есть спрос падает при росте цены, а у Гиффена спрос растёт при росте цены)


Экономические блага в модели Хикса - обыкновенные и не являются продуктами Гиффена


# Производственная функция

Свойства функции Кобба-Дугласа:

- Если $K = 0$ или $L = 0$, то и вся функция $= 0$
- При увеличении $K$ или $L$, ПФ также увеличивается (взять прозводные, они $> 0$, а значит функция возрастающая)
- Чем больше $K, L$, тем меньше возрастает ПФ (взять вторые производные, < 0, по ней функция вогнутая)
- Если компоненты увеличить в $m$ раз, то выпуск увеличится в $m^{\alpha + \beta}$ раз


Характеристики ПФ:

- Средние продукты факторов производства - $APK = \frac{y}{K}$, $APL = \frac{y}{L}$
- Предельные продукты факторов производства - $MPK = y_K'$, $MPL = y_L'$
- Предельная норма замещения - $MRS_{KL} = \frac{MPK}{MPL}$
- Эластичность ПФ по факторам - $E_K = \frac{MPK}{APK}$


Виды сроков:
- Краткосрочный ($K$ фиксированный)
- Долгосрочный ($K$ может меняться)
    ''',
    'task_1' : '''
x1, x2 = sp.symbols('x1 x2', positive = True)
u = sp.ln(x1 + 4) + 3*sp.ln(x2)


Mu1 = u.diff(x1)
Mu1_2 = Mu1.diff(x1)


Mu2 = u.diff(x2)
Mu2_2 = Mu2.diff(x2)


# Таким образом:
# Функция полезности непрерывна, так как логарифмическая функция непрерывна на своей области определения
# Вторые производные всегда отрицательны, а следовательно, предельные полезности убывают по мере увеличения каждого блага, 
# то есть нет смысла неограниченно увеличивать количество благ


# Предельные полезности благ:
Mu1, Mu2
#интерпретация: при увеличении количества блага, уменьшается предельная полезность, а значит оптимальное количество блага ограничено


# эластичность первого
Au1 = u/x1
Eu1 = Mu1/Au1


# эластичность второго
Au2 = u/x2
Eu2 = Mu2/Au2
Eu2


# Интерпретация: эластичность показывает, на сколько процентов изменится общая полезность при изменении количества блага на 1%. 
# Для x1 это x1/(x1+4) делённое на логарифм от общей полезности, а для x2 3 елить на логарифм общей полезности
''',
    'task_2' : '''
L, K, lam = sp.symbols('L K lambda', real=True, positive=True)

alpha = 0.2
beta = 0.8
w = 3
r = 5
C0 = 1732

Y = K ** alpha * L ** beta

u = K**alpha * L**beta


# ограничение бюджета
constraint = C0 - (w*L + r*K)
# функция Лагранжа для максимизации
Lagrangian = u + lam * constraint

system = [
    Lagrangian.diff(L),
    Lagrangian.diff(K),
    Lagrangian.diff(lam)
]


# solution = sp.solve(system, [L, K, lam], dict=True) # не хочет считать
solution = sp.nsolve(system, [L, K, lam], [1, 1, 1], dict=True)


Y.subs([(L, solution[0][L]), (K, solution[0][K])])


# через оптимайз
def cobb_douglas(x):
    K, L = x
    return -(K**alpha * L**beta)  #минус !!

cons = ({'type': 'eq', 'fun': lambda x: C0  - (w*x[1] + r*x[0])})
x0 = np.array([1, 1])

res = minimize(cobb_douglas, x0, constraints=cons)

optimal_K, optimal_L = res.x
optimal_Y = -(res.fun)

optimal_K, optimal_L, optimal_Y
''',
    'task_3' : '''
alpha = 0.3
beta = 0.6
a1 = 9
a2 = 7
p1 = 6
p2 = 7
I = 194

x1, x2, lam = sp.symbols('x1 x2 lambda', real=True, positive=True)
u = x1**alpha * x2**beta

L = u + lam * (I - (p1*x1 + p2*x2))


res = sp.solve((L.diff(x1), L.diff(x2), L.diff(lam)), (x1, x2, lam), dict=True)
lambda_best = sp.re(res[0][lam])
x1_best = sp.re(res[0][x1])
x2_best = sp.re(res[0][x2])
lambda_best, x1_best, x2_best


u_best = u.subs([(x1, x1_best), (x2, x2_best), (lam, lambda_best)])
u_best


# множитель Лагранджа можно интерпретировать как предельную полезность по доходу потребителя

delta_x1 = 0.01
u_best_new = u_best - lambda_best * x1_best * delta_x1
print(f'Оптимум полезности изменился на {u_best_new - u_best}')
''',
    'task_4' : '''
x1, x2, lam = sp.symbols('x1 x2 lambda', real=True, positive=True)
p = (4, 6)
u0 = 2.5

u = (x1 - 7)**0.4 * (x2 - 5)**0.1
constraint = u0 - u

L = p[0] * x1 + p[1] * x2 + lam * constraint

res = sp.nsolve((L.diff(x1), L.diff(x2), L.diff(lam)), (x1, x2, lam), (10, 10, 1), dict=True)
x1_best = res[0][x1]
x2_best = res[0][x2]
assert x1_best > 7
assert x2_best > 5
x1_best, x2_best

p[0] * x1_best + p[1] * x2_best

# множитель Лагранджа можно интерпретировать как предельную полезность по доходу потребителя
''',
    'task_5' : '''
u0, p1, p2, alpha, beta, a1, a2 = sp.symbols('u0 p1 p2 alpha beta a1 a2')

x1_star =  (u0 /(p1/p2 * beta/alpha)**beta)**(1/(alpha + beta)) + a1
x2_star = (u0 * (p1/p2 * beta/alpha)**alpha)**(1/(alpha + beta)) + a2


c = x1_star * p1 + x2_star * p2


# Блага в модели Хикса имеют обратную зависимость между спросом и ценой, то есть являются обыкновенными (обратное - товары Гиффена)
c_dp1p1 = sp.diff(sp.diff(c, p1), p1).simplify()
c_dp1p2 = sp.diff(sp.diff(c, p1), p2).simplify()
c_dp2p1 = sp.diff(sp.diff(c, p2), p1).simplify()
c_dp2p2 = sp.diff(sp.diff(c, p2), p2).simplify()

slutsky_matrix = sp.Matrix([[c_dp1p1, c_dp1p2],
                         [c_dp2p1, c_dp2p2]])

# Диагональные элементы матрицы Слуцкого имеют отрицательные знаки, а следовательно, функция расходов выпукла вверх (вторая производная отрицательна)
# Так как наблюдается свойство выше, то стоимость и спрос товаров имеют обратную зависимость, а следовательно, товары являются обыкновенными и не являются товарами Гиффена
''',
    'task_6' : '''
w = 4
r = 6
Y0 = 420

L, K, alpha, beta, lam= sp.symbols('L K alpha beta lambda', positive=True, real=True)

Y = L**alpha * K**beta


Lagr = w*L + r*K + lam * (Y0 - Y)
res = sp.solve([Lagr.diff(L), Lagr.diff(K), Lagr.diff(lam)], [L, K, lam], dict=True)
res[0][K]
# Экономический смысл показателей степени производственной функции это эластичность труда для $\alpha$, а $\beta$ это эластичность капитала

MPK = sp.simplify(Y.diff(K))
MPK

MPL = sp.simplify(Y.diff(L))
MPL

# сколько единиц капитала необходимо, чтобы заменить одну единицу труда

# MPL измеряется относительно изменения единицы труда, 
# а  MPK относительно изменения единицы капитала
# таким образом, их частное это изменение относительно друг друга
MRS_LK = (MPL/MPK).simplify()
MRS_LK
''',
    'task_7' : '''
L, K, lam = sp.symbols('L K lambda', real=True, positive=True)

alpha = 0.54
beta = 0.46
w = 8
r = 3
C0 = 2150

Y = K**alpha * L**beta


# свойство 1
# При K = 0 или L = 0, производственная функцию равна нулю
Y.subs([(K, 0)]), Y.subs([(L, 0)])


# свойство 2
# При увеличении K и L функция возрастает
display(Y.diff(K))
Y.diff(L) # производные всегда положительны, так как L и K положительны => возрастает


# свойство 3
# чем больше K и L, тем меньше прирост ПФ
display(Y.diff(K, 2)) # вторые производные всегда отрицательны
Y.diff(L, 2) # значит функцию вогнута и уменьшает наклон касательных


# свойство 4
# если компоненты увеличить в m раз, то выпусr увеличится в m**(alpha + beta) раз
#пусть m = 5
Y.subs([(K, 5*K), (L, 5*L)]) # увеличилась в 5 ** (0.54 + 0.46) = 5**1 = 5 раз


# Экономический смысл показателей степени производственной функции это эластичность труда для $\alpha$, а $\beta$ это эластичность капитала
A_K = Y/K
A_L = Y/L

M_K = Y.diff(K)
M_L = Y.diff(L)

E_K = (M_K/A_K).simplify()
E_K

E_L = (M_L/A_L).simplify()
E_L
''',
    'task_8' : '''
p1, p2, x1, x2, alpha, beta, a, lam = sp.symbols('p1, p2, x1, x2, alpha, beta, a, lambda', 
                                                 positive=True, real=True)
alpha = 0.6
beta = 0.3
a = 6
p1 = 3
p2 = 4.2
u0 = 5.3

c = p1*x1 + p2*x2
u = x1**alpha * (x2 - a)**beta
Lagr = c + lam * (u0 - u)

sp.nsolve([Lagr.diff(x1), Lagr.diff(x2), Lagr.diff(lam)], [x1, x2, lam], (10, 10, 1), dict=True) #обычный солв откинулся

# Нет аналитического решения (sympy не считает с помощью. solve..) => не получится показать свойство с lambda
# если б считал, ты просто берём производные с условия и показываем свойство для C
''',
    'task_9' : '''
p = 10
K = 75
p_k = 4
p_l = 2

L = sp.Symbol('L')


y = K ** 0.6 * L ** 0.4
revenue = p * y - p_k * K - p_l * L
rev = revenue.diff(L).simplify()


p_l = sp.Symbol('p_l')
revenue = p * y - p_k * K - p_l * L
rev = revenue.diff(L).simplify()
L_best = sp.solve(rev, L, dict=True)[0][L]
y_plot = y.subs([(L, L_best)])


y_plot.diff(p_l) #производная всегда отрицательна - убывает


y_func = sp.lambdify(p_l, y_plot)
xx = np.arange(1, 100)

plt.plot(xx, y_func(xx))
plt.xlabel('Цена труда')
plt.ylabel('Объём предложения')


# значения свойств в задании 7
# 1 свойство
K = sp.Symbol('K')
y = K ** 0.6 * L ** 0.4
y.subs([(K, 0)]), y.subs([(L, 0)]) #выполняется


# 2 свойство
display(y.diff(K).simplify())
y.diff(L).simplify() #первые производные всегда положительны, 2 свойство выполняется, функция неубывает


# 3 свойство
display(y.diff(K, 2).simplify())
display(y.diff(L, 2).simplify()) #вторые производные всегда отрицательны, 3 свойство выполняется, функция выгнута вниз


# 4 свойство
m = sp.symbols('m')
sp.simplify(y.subs([(L, m * L), (K, m * K)])) # свойство выполняется, увеличивается в m**(0.6 + 0.5) раза

# Экономический смысл показателей степени производственной функции это эластичность труда для $\alpha$ (0.4 в данной задаче), а $\beta$ это эластичность капитала (0.6)
''',
    'task_10' : '''
a0, a1, a2, I, p1, p2 = sp.symbols('a0, a1, a2, I, p1, p2')

x1 = I / p1 * a1 / (a1 + a2)
x2 = I / p2 * a2 / (a1 + a2)

u = (a0 * x1 ** a1 * x2 ** a2).simplify()


# Множитель Лагранжа показывает предельную полезность по доходу, а значит его можно найти следующим образом:
lambd = u.diff(I).simplify()
lambd


# Проверка тождества Роя: $u_{p_2}' = -x_2^*\lambda^*$
u.diff(p2) + x2 * lambd
''',
    'task_11' : '''
price = 16
K = 56
r = 6
L = sp.symbols('L')
w = 3

y = K ** 0.5 * L ** 0.5
c = r*K + w*L
revenue = price * y - c

L_best = sp.solve(revenue.diff(L))[0]

L_best


y.subs([(L, L_best)])
''',
    'task_12' : '''
a0, a1, a2, x1, x2 = sp.symbols('a0, a1, a2, x1, x2', positive=True)

y = a0 * x1 ** a1 * (a2 * x1 + x2 ** (1 - a1))


# значения свойств в задании 7
# 1 свойство
y.subs([(x1, 0)])   
y.subs([(x2, 0)]).simplify() # первое свойство не выполняется


# 2 свойство
y.diff(x1).simplify()
y.diff(x2).simplify() # второе свойство выполняется при a1 < 1


# 3 свойство
y.diff(x1, 2).simplify()
y.diff(x2, 2).simplify() # если a1 < 1, то функция вогнутая, свойство выполняется для y''_x2


# 4 свойство
m = sp.symbols('m')
sp.simplify(y.subs([(x1, m * x1), (x2, m * x2)]) / y) # свойство не выполняется


# средние
AP1 = (y / x1).simplify()
(y / x2).simplify()
display(AP1)
AP2


# предельные
MP1 = y.diff(x1).simplify()
MP2 = y.diff(x2).simplify()
display(MP1)
MP2


# эластичности
E1 = MP1 / AP1
E2 = MP2 / AP2
display(E1)
E2


vars = {a0: 2.6, a1: 0.5, a2: 0.8}

AP1.subs(vars)

AP2.subs(vars)

MP1.subs(vars).simplify().expand()

MP2.subs(vars)

E1.subs(vars).simplify()

E2.subs(vars).simplify()
'''
}

import pyperclip

def task(number):
    ''' number от 0 до 12'''

    pyperclip.copy(fr"{data[f'task_{number}']}")