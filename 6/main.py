from functools import reduce


test_time = [7, 15, 30]
test_distance = [9, 40, 200]

time = [44, 82,69,81]
distance = [202, 1076, 1138, 1458]

def find_min_distance(time: int, distance: int) -> int:
    wins = 0
    for i in range(time):
        time_remaining = time - i
        if i * time_remaining > distance:
            wins += 1
    return wins



s = reduce(lambda x,y: x * y, [find_min_distance(time, distance) for time, distance in zip(time, distance)], 1)
print(s)

test_time_2 = 71530
test_distance_2 = 940200

time_2 = 44826981
distance_2 = 202107611381458

print(find_min_distance(time_2, distance_2))