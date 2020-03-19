import pickle

from optimization.pyomo_test.max_flow.discrete_max_flow import solve, print_result


def test_flow1():
    return pickle.load(open('./test_data/flow1.pickle', 'rb'))


if __name__ == '__main__':
    res = test_flow1()
    print(res['priorities'])
    # res['priorities'][(-542, -539)] = 2

    status, res = solve(**res)
    print(status); print_result(res)
