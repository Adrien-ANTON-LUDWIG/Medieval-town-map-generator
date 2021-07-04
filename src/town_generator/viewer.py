"""This module displays a city JSON file."""
import geopandas as gpd
import matplotlib.pylab as plt
from matplotlib.colors import ListedColormap


def display(filename):
    """
    Displays a city object.

    Args:
        filename (string): location of a JSON file representing a city.
    """
    colors_dic = {
        1: [167 / 255, 199 / 255, 99 / 255, 1],
        2: [254 / 255, 227 / 255, 71 / 255, 1],
        3: [0.25, 0.6, 0.25, 1],
        4: [0.25, 0.75, 0.9, 1],
        8: [0.8, 0.9, 0.55, 1],
        10: [0.7, 0.45, 0.25, 1],
        11: [0.5, 0.5, 0.63, 1],
        12: [0.85, 0.5, 0.85, 1],
        15: [0.75, 0.45, 0.15, 1],
        20: [0.6, 0.6, 1, 1],
        21: [0.3, 0.3, 0.8, 1],
        31: [0.4, 0.4, 0.4, 1],
        32: [0.6, 0.6, 0.6, 1],
        33: [0.2, 0.2, 0.2, 1],
        34: [133 / 255, 94 / 255, 66 / 255, 1],
        50: [0.95, 0.95, 0.95],
        52: [254 / 255, 235 / 255, 219 / 255],
        90: [1, 0, 0, 1]
    }
    colors = [[1, 0, 0, 1] for _ in range(max(colors_dic.keys()) + 1)]
    for i in colors_dic:
        colors[i] = colors_dic[i]
    color_map = ListedColormap(colors, name='Archi')

    shapes = gpd.read_file(filename)
    _, ax = plt.subplots(figsize=(20, 16))
    shapes.plot(
        column='category',
        cmap=color_map,
        k=len(colors) + 1,
        vmin=0,
        vmax=len(colors),
        # edgecolor='black',
        aspect='equal',
        ax=ax)
    shapes = shapes[(shapes.category > 9)]  # & (shapes.category < 50)]
    shapes.geometry.boundary.plot(color=None,
                                  edgecolor='black',
                                  linewidth=0.5,
                                  aspect='equal',
                                  ax=ax)
    # plt.grid()
    plt.show()
