input_data = [
    "Game 1: 3 blue, 4 red; 2 blue 3 green; 5 red, 7 blue, 8 green",
    "Game 2: 2 blue, 4 red; 1 blue 2 green"
]

game_data = {}

for game in input_data:
    game_info = game.split(': ')
    game_name = game_info[0]
    colors_data = game_info[1].split('; ')

    game_data[game_name] = {}
    for colors in colors_data:
        color_list = colors.split(', ')
        for color in color_list:
            quantity, color_name = color.split(' ')
            if color_name not in game_data[game_name]:
                game_data[game_name][color_name] = int(quantity)
            else:
                game_data[game_name][color_name] += int(quantity)

print(game_data)
