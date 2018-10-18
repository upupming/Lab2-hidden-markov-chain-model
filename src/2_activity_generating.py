import numpy

def get_nums_by_probability(start, end, probabilities, size):
    return numpy.random.choice(end + 1 - start, size, probabilities) + start

def generate_activity(N):
    # Read from file
    with open(f'../results/1_weather-{N}.txt', 'r') as weather_file:
        weather = weather_file.readlines()
    # And recover W
    W = numpy.fromstring(weather[1][5:-2], sep=' ', dtype=int)
    
    emission_probability = {
        'Sunny' : [0.6, 0.3, 0.1],
        'Rainy' : [0.1, 0.4, 0.5]
    }
    activity = numpy.empty(N, dtype=int)
    for n in range(N):
        if(W[n] == 1):
            activity[n] = get_nums_by_probability(1, 3, emission_probability['Sunny'], 1)
        elif(W[n] == 2):
            activity[n] = get_nums_by_probability(1, 3, emission_probability['Rainy'], 1)

    # Save to file
    with open(f'../results/2_activity-{N}.txt', 'w+') as generate_results:
        generate_results.write(f'N = {N}\n')
        generate_results.write(f'activity = {activity}\n')

generate_activity(20)