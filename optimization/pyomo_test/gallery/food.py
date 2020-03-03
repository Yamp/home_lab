from pyomo.environ import *
import numpy as np

# =============================== Модель и множества данных ==================================
model = AbstractModel()
model.food, model.nutr = Set(), Set()  # Множества данных для задачи

# =============================== ПАРАМЕТРЫ ЗАДАЧИ ===========================================
# параметры
model.min_nutr = Param(model.nutr, within=NonNegativeReals, default=0.0)
model.max_nutr = Param(model.nutr, within=NonNegativeReals, default=np.inf)

model.max_vol = Param(within=PositiveReals)  # максимальный объем еды
model.prices = Param(model.food, within=PositiveReals)  # цена каждой еды
model.vols = Param(model.food, within=PositiveReals)  # объем каждой еды

model.nutrs_in_food = Param(model.food, model.nutr, within=NonNegativeReals)

# переменные
model.f_nums = Var(model.food, within=NonNegativeIntegers)  # количество хавок

# =============================== ПЕРЕМЕННЫЕ И КОСТЫ ===========================================

# минимизируем общую цену
model.cost = Objective(rule=lambda m: sum(m.prices[i] * m.f_nums[i] for i in m.food))

# Ограничиваем общий объем еды
model.vol_constr = Constraint(
    rule=lambda m: sum(m.vols[i] * m.f_nums[i] for i in m.food) <= m.max_vol
)

# ограничение на итоговое количество нутриентов с параметром (j)
model.nutrient_limit = Constraint(
    model.nutr,
    rule=lambda m, j: inequality(
        lower=m.min_nutr[j],
        body=sum(m.nutrs_in_food[i, j] * m.f_nums[i] for i in m.food),  # верхняя граница
        upper=m.max_nutr[j],  # нижняя граница
        strict=False,
    ),
)

if __name__ == "__main__":
    data = {None: {
        'food': {None: [1, 2, 3, 4]},
        'nutr': {None: [1, 2, 3]},
        'min_nutr': {1: 3, 2: 3, 3: 3},
        'prices': {1: 1, 2: 2, 3: 3, 4: 4},
        'vols': {1: 3, 2: 6, 3: 1, 4: 7},
        'max_vol': {None: 10},

        'nutrs_in_food': {
            (1, 1): 1, (1, 2): 1, (1, 3): 1,
            (2, 1): 1, (2, 2): 1, (2, 3): 1,
            (3, 1): 1, (3, 2): 1, (3, 3): 1,
            (4, 1): 1, (4, 2): 1, (4, 3): 1,
        }
    }}

    instance = model.create_instance(data,,
    instance.valid_model_component()
    opt = SolverFactory('cbc')
    opt.solve_tsp(instance)


    instance.display()
