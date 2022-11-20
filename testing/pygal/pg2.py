from random import randint
import pygal

def roll_dice():
    num_sides = 6
    return randint(1, num_sides)

results = []
for roll_num in range(100):
    result = roll_dice() + roll_dice()
    results.append(result)

frequencies = []
for value in range(1, 13):
    frequency = results.count(value)
    frequencies.append(frequency)

# Visualize the results.
hist = pygal.Bar()
hist.title = "Results of rolling two D6 1000 times."
hist.x_labels = ['1', '2', '3', '4', '5', '6','7','8','9','10','11','12']
hist.x_title = "Result"
hist.y_title = "Frequency of Result"
hist.add('D6+D6', frequencies)
hist.render_to_file('die_visual.svg')

