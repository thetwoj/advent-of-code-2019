def parse_image(img_width, img_height):
    layers = {}
    with open("input.txt") as f:
        line = f.readline().strip()
    layer_count = len(line) // (img_width * img_height)
    for l in range(layer_count):
        layer = []
        layers[l] = layer
        for x in range(img_width):
            column = []
            layer.append(column)
            for y in range(img_height):
                position = (l * img_width * img_height) + (y * img_width) + x
                column.append(int(line[position]))
    return layers


def fewest_zeroes(layers):
    zero_counts = {}
    for index, layer in layers.items():
        zero_count = 0
        for x in layer:
            for pixel in x:
                if pixel == 0:
                    zero_count += 1
        zero_counts[index] = zero_count
    return min(zero_counts, key=zero_counts.get)


def count_digits_in_layer(layer, digit):
    digit_count = 0
    for x in layer:
        for pixel in x:
            if pixel == digit:
                digit_count += 1
    return digit_count


def collapse_layers(layers):
    canvas = layers[0]
    for layer_index, layer in layers.items():
        for x, column in enumerate(layer):
            for y, pixel in enumerate(column):
                if pixel == 2:
                    continue
                if canvas[x][y] != 2:
                    if layer_index == 0:
                        current = canvas[x][y]
                        canvas[x][y] = "." if current == 0 else "#"
                    continue
                canvas[x][y] = "." if pixel == 0 else "#"

    return canvas


def print_layer(layer):
    width = len(layer)
    height = len(layer[0])
    for y in range(height):
        for x in range(width):
            if x == width - 1:
                print(layer[x][y])
            else:
                print(layer[x][y], end="")


if __name__ == "__main__":
    image = parse_image(25, 6)
    layer_number = fewest_zeroes(image)
    fewest_zeroes_layer = image[layer_number]
    ones = count_digits_in_layer(fewest_zeroes_layer, 1)
    twos = count_digits_in_layer(fewest_zeroes_layer, 2)
    print(f"part one: {ones * twos}")
    print()
    final_image = collapse_layers(image)
    print(f"part two:")
    print_layer(final_image)
