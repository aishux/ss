red_balls = 12
green_balls = 13
blue_balls = 14

data = {
    'Game 1': ['4 blue, 5 red', '6 green, 7 red, 8 blue'],
    'Game 2': ['2 blue, 5 red', '6 green, 0 red, 8 blue', '8 green, 7 blue, 2 red'],
    'Game 3': ['1 blue, 2 blue', '6 green, 7 green, 8 red']
}

keys_satisfying_criteria = []

for key, sets in data.items():
    red_total = 0
    green_total = 0
    blue_total = 0

    for game_set in sets:
        elements = game_set.split(', ')
        for element in elements:
            quantity, color = element.split(' ')
            if color == 'red':
                red_total += int(quantity)
            elif color == 'green':
                green_total += int(quantity)
            elif color == 'blue':
                blue_total += int(quantity)

    if red_total < red_balls and green_total < green_balls and blue_total < blue_balls:
        keys_satisfying_criteria.append(key)

print("Keys satisfying the criteria:", keys_satisfying_criteria)
