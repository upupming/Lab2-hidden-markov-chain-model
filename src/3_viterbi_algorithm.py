import numpy

def get_nums_by_probability(start, end, probabilities, size):
    return numpy.random.choice(end + 1 - start, size, probabilities) + start

calculation_process = ''

def get_T_by_A(A):
    global calculation_process
    calculation_process = ''

    p = 0.6
    # 第一行表示从起始状态进入第一天
    # 第二行表示从前一天晴天进入后一天
    # 第三行表示从前一天雨天进入后一天
    P = numpy.array([[0.6, 0.4], [0.6, 0.4], [0.3, 0.7]])
    emission_probability = [[0.6, 0.3, 0.1], [0.1, 0.4, 0.5]]

    # A[0], A[1], ... 分别表示第 0、1、... 天的活动
    # 多加一位 T[0] = 0 表示起始状态
    # T[1], T[2], ... 分别表示第 1、2、... 天的预测天气
    # 计算过程中 T[i] = 1, 2 分别表示晴天和雨天
    T = numpy.zeros(A.size + 1, dtype=int)
    # 1. eg. A = [1, 3] = [walk, clean]
    # 5. eg1. after ending, get T[1] = 1
    for n in range(A.size):
        p_1 = 1.0
        # 2.1. eg1. when n=0, don't go into loop
        # 6.1. eg2. when n=1, p_1 *= P[0][0] = 0.6
        for i in range(n):
            p_1 *= P[T[i]][T[i+1]-1]
        # 3.1. eg1. p_1 *= P[0][0] = 0.6 从起始进入晴天
        # 7.1. eg2. when n=1, p_1 = p * P[1][0] = 0.6 * 0.6 = 0.36
        p_1 *= P[T[n]][0]
        # 4.1. eg1. p_1 *= emission_probability[0][0] = 0.6 * 0.6 = 0.36
        # 8.1. eg2. p_1 = 0.36 * emission_probability[0][2] = 0.24 * 0.1
        p_1 *= emission_probability[0][A[n]-1]

        p_2 = 1.0
        # 2.2. eg1. when n=0, don't go into loop
        # 6.1 eg2. when n=1, p_1 *= P[0][0] = 0.6
        for i in range(n):
            p_2 *= P[T[i]][T[i+1]-1]
        # 3.2. eg1. p_1 *= P[0][1] = 0.4 从起始进入雨天
        # 6.1. eg2. when n=1, p_2 *= P[1][1] = 0.6 * 0.4 = 0.24
        p_2 *= P[T[n]][1]
        # 4.2. eg1. p_2 *= emission_probability[1][0] = 0.4 * 0.1 = 0.04
        # 7.1. eg2. p_2 = 0.24 * emission_probability[1][2] = 0.24 * 0.5
        p_2 *= emission_probability[1][A[n]-1]

        if p_1 >= p_2:
            T[n+1] = 1
        else:
            T[n+1] = 2

        calculation_process += 'n = ' + str(n) + ', p_1 = '+ str(p_1) + ', p_2 = ' + str(p_2) + ', T[n] = ' + str(T[n+1]) + '\n'

    return T
    

def find_most_likely_weather_sequence(N):
    global calculation_process

    # Read from file
    with open(f'../results/2_activity-{N}.txt', 'r') as activity_file:
        activity = activity_file.readlines()
    # And recover activity
    A = numpy.fromstring(activity[1][12:-2], sep=' ',dtype=int)
    T = get_T_by_A(A)

    # Save to file
    with open(f'../results/3_most-likely-weather-{N}.txt', 'w+') as generate_results:
        generate_results.write(f'N = {N}\n')
        generate_results.write(calculation_process)
        generate_results.write(f'T = {T[1:]}\n')

def find_most_likely_weather_sequence(N=None, A=None, filename=None):
    global calculation_process

    # Using data from file
    if(N != None):
        # Read from file
        with open(f'../results/2_activity-{N}.txt', 'r') as activity_file:
            activity = activity_file.readlines()
        # And recover activity
        A = numpy.fromstring(activity[1][12:-2], sep=' ',dtype=int)
    
    # Using passed data
    elif(type(A) is numpy.ndarray and filename != None):
        T = get_T_by_A(A)
        
        # Save to file
        with open(f'../results/{filename}.txt', 'w+') as generate_results:
            generate_results.write(f'N = {A.size}\n')
            generate_results.write(calculation_process)
            generate_results.write(f'T = {T[1:]}\n')

    else:
        print('Please provide correct parameters!')
        return
    

find_most_likely_weather_sequence(A=numpy.array([1, 3, 2]), filename='3_example')
find_most_likely_weather_sequence(A=numpy.array([1, 2, 3]), filename='3_problem1')
find_most_likely_weather_sequence(A=numpy.array([2, 1, 3, 2, 3, 2, 2, 3, 3, 1, 2, 1, 1, 1, 2, 3, 3, 3, 3, 2]), filename='3_problem2')
find_most_likely_weather_sequence(N=20)