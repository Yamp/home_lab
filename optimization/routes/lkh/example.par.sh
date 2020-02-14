SPECIAL
PROBLEM_FILE = example.vrp
TOUR_FILE = example.res
#CANDIDATE_FILE = example.cand
#PI_FILE = example.pen
MTSP_OBJECTIVE = MINMAX
DEPOT = 1

#OPTIMUM = 1183

# TODO?
#ASCENT_CANDIDATES = 5000

# начальный период для ascent
#INITIAL_PERIOD = 10000
INITIAL_STEP_SIZE = 1

# TODO?
MAX_CANDIDATES = 6

RUNS = 5

# похоже, что это количество обязательных триалов
#BACKBONE_TRIALS = 1000

# сколько попыток улучшения делать
#MAX_TRIALS = 10000

#KICKS = 10

# максимальное количество ребер-кандидатов на каждом шаге поиска
#MAX_BREADTH = 1000

# BORUVKA | GREEDY |  MOORE |NEAREST-NEIGHBOR | QUICK-BORUVKA | SIERPINSKI | WALK
INITIAL_TOUR_ALGORITHM = WALK

#EXCESS = ??  excess * lbound(tour) = max alpha for candidate

# K для K-opt
#MOVE_TYPE = 5

# Делать ли BACKTRAKING K-opt первым в последовательности (TODO?)
#BACKTRACKING = NO

# CANDIDATE_FILE =
#CANDIDATE_SET_TYPE = ALPHA
#EXTRA_CANDIDATES = 0
#EXTRA_CANDIDATE_SET_TYPE = QUADRANT


# понятные
STOP_AT_OPTIMUM = YES
SUBGRADIENT = YES
SEED = 42
TRACE_LEVEL = 500

