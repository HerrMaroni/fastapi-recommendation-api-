
def compatible_colors(palette, main_color):
    # color_palette = ['Monochromatic','Complementary','Analogous','Split-Complementary','Triadic','Tetradic']
    list_of_cols = ['yellow', 'yellow-orange', 'orange', 'red-orange', 'red', 'red-violet', 'violet', 'blue-violet',
                    'blue', 'blue-green', 'green', 'yellow-green']

    if main_color in list_of_cols:
        i = list_of_cols.index(main_color) + 1
        if palette == 'Monochromatic':
            return main_color
        elif palette == 'Complementary':
            return [main_color, list_of_cols[(i + 6) % 12]]
        elif palette == 'Analogous':
            return [list_of_cols((i + 11) % 12), main_color, list_of_cols((i + 1) % 12)]
        elif palette == 'Split-Complementary':
            return [list_of_cols[(i + 7) % 12], main_color, list_of_cols[(i + 5) % 12]]
        elif palette == 'Triadic':
            return [list_of_cols[(i + 8) % 12], main_color, list_of_cols[(i + 4) % 12]]
        elif palette == 'Tetradic':
            return [main_color, list_of_cols[(i + 3) % 12], list_of_cols[(i + 6) % 12], list_of_cols[(i + 9) % 12]]
    else:
        return ['black', 'blue', 'white', 'beige']


def get_base_color(color):
    ind = 0
    x = []
    color = str(color).lower()
    list_of_cols = ['stone', 'khaki', 'black', 'white', 'blue', 'grey', 'brown', 'red', 'orange', 'yellow', 'green',
                    'purple', 'pink', 'silver', 'gold', 'navy']

    for el in list_of_cols:
        if el in str(color).lower():
            ind += 1
            x.append(el)

    if ind == 2:
        if all(b in x for b in ['yellow', 'orange']):
            return 'yellow-orange'
        elif all(b in x for b in ['red', 'orange']):
            return 'red-orange'
        elif all(b in x for b in ['red', 'violet']):
            return 'red-violet'
        elif all(b in x for b in ['blue', 'violet']):
            return 'blue-violet'
        elif all(b in x for b in ['blue', 'green']):
            return 'blue-green'
        elif all(b in x for b in ['yellow', 'green']):
            return 'yellow-green'
    if ind == 1:
        if color == 'navy':
            return 'blue'
        else:
            return x[0]
    else:
        return 'Multicolor'



