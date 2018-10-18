import numpy

def get_nums_by_probability(start, end, probabilities, size):
    return numpy.random.choice(end + 1 - start, size, probabilities) + start

def generate_weather(p, q, N):
    W = numpy.empty(N, dtype=int)
    W[0] = get_nums_by_probability(1, 2, [p, q], 1)
    for n in range(1, N):
        W[n] = get_nums_by_probability(1, 2, [p if W[n - 1]==1 else q, (1 - p) if W[n - 1]==1 else (1 - q)], 1)
    # Save to file
    with open(f'../results/1_weather-{N}.txt', 'w+') as generate_results:
        generate_results.write(f'N = {N}\n')
        generate_results.write(f'W = {W}\n')

generate_weather(0.6, 0.3, 20)