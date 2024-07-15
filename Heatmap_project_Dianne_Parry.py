""" Program to generate heatmaps displaying information regarding registered
    dogs in Hamilton, NZ.
    For COSC480 project.
    Author: Dianne Parry
    Date: 02/06/2023
"""

import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
from matplotlib.widgets import RadioButtons

# Please update file path here
FILE_PATH = r"Dog - Hamilton.csv"



def dog_data():
    """Opens the data file and returns as lines"""
    f = open(FILE_PATH)
    data = f.read()
    lines = data.splitlines()
    return lines


def alive_dogs(lines):
    """ Takes the lines of data and returns a dictionary containing dog_id
        as the key, and suburb, desexed, classification, and microchip
        as its values for dogs that are alive.
        :param lines:
        :return: dictionary of alive dogs and their attributes.
    """
    alive_dogs_dict = {}
    for line in lines:
        bits = line.split(',')
        dog_id, suburb, desexed, classification, alive, alive_2, microchip = \
            bits[1], bits[2], bits[18], bits[27], bits[15], bits[16], bits[36]
        if alive == "" and alive_2 == "":
            alive_dogs_dict[dog_id] = suburb, desexed, classification, microchip
    return alive_dogs_dict


def dogs_per_suburb(dogs):
    """ Takes dictionary of alive dogs and returns new dictionary of suburb as
        key and number of dogs in that suburb as the value.
        :param dogs: dictionary of alive dogs and their attributes.
        :return: dictionary of suburb and count as key/value pair
    """
    dogs_dict = {}
    for suburb, desexed, classification, microchip in dogs.values():
        if suburb not in dogs_dict:
            dogs_dict[suburb] = 1
        else:
            dogs_dict[suburb] += 1
    all_dogs_dict = dict(sorted(dogs_dict.items()))
    return all_dogs_dict


def suburb_array(dogs):
    """ Takes dictionary of alive dogs, creates a sorted list of suburbs, and
        returns array in shape (8, 6) to be used for heatmap annotations.
        :param dogs: dictionary of alive dogs and their attributes.
        :return: array of suburb names in shape (8, 6).
    """
    suburb_list = []
    for suburb, desexed, classification, microchip in dogs.values():
        if suburb not in suburb_list:
            suburb_list.append(suburb)
    sorted_suburb_list = sorted(suburb_list)
    sl_array = np.array(sorted_suburb_list)
    suburb_list_array = sl_array.reshape(8, 6)
    return suburb_list_array


def classified_suburbs(dogs):
    """ Takes dictionary of alive dogs and returns new dictionary of suburb as
        key and number of classified dogs in that suburb as the value.
        :param dogs: dictionary of alive dogs and their attributes.
        :return: dictionary of suburb and count as key/value pair.
    """
    classified_suburbs_dict = {}
    for suburb, desexed, classification, microchip in dogs.values():
        if suburb not in classified_suburbs_dict:
            classified_suburbs_dict[suburb] = 0
        if classification != "Not Applicable":
            classified_suburbs_dict[suburb] += 1
    classified_dict = dict(sorted(classified_suburbs_dict.items()))
    return classified_dict


def no_microchip_suburbs(dogs):
    """ Takes dictionary of alive dogs and returns new dictionary of suburb as
        key and number of dogs not microchipped in that suburb as the value.
        :param dogs: dictionary of alive dogs and their attributes.
        :return: dictionary of suburb and count as key/value pair.
    """
    no_microchip_suburbs_dict = {}
    for suburb, desexed, classification, microchip in dogs.values():
        if suburb not in no_microchip_suburbs_dict:
            no_microchip_suburbs_dict[suburb] = 0
        if microchip != "Y":
            no_microchip_suburbs_dict[suburb] += 1
    no_microchipped_dict = dict(sorted(no_microchip_suburbs_dict.items()))
    return no_microchipped_dict


def entire_suburbs(dogs):
    """ Takes dictionary of alive dogs and returns new dictionary of suburb as
        key and number of dogs not desexed in that suburb as the value.
        :param dogs: dictionary of alive dogs and their attributes.
        :return: dictionary of suburb and count as key/value pair.
    """
    entire_suburbs_dict = {}
    for suburb, desexed, classification, microchip in dogs.values():
        if suburb not in entire_suburbs_dict:
            entire_suburbs_dict[suburb] = 0
        if desexed == "N":
            entire_suburbs_dict[suburb] += 1
    entire_dict = dict(sorted(entire_suburbs_dict.items()))
    return entire_dict


def shaped_array(dictionary):
    """ Takes dictionary of key/value pairs and returns numpy array in shape
        (8, 6) to be used for heatmap of same shape.
        :param dictionary: suburb/count pairs.
        :return: numpy array in shape (8, 6)
    """
    dog_array = np.fromiter(dictionary.values(), dtype=int)
    shaped_dog_array = dog_array.reshape(8, 6)
    return shaped_dog_array


def plot_heatmaps(annotations, count_1, count_2, count_3, count_4):
    """ Takes five arrays, one to be used for annotations and the remaining four
        to be used as quantities for heatmaps, and produces four Seaborn heatmaps
        that can be toggled between using radio buttons. Radio buttons also offer
        the option to close the window with 'exit'.
    :param annotations: Array in shape (10, 5) of suburbs.
    :param count_1: Array in shape (10, 5) of all alive dogs per suburb. This
    array is used to display the initial heatmap.
    :param count_2: Array in shape (10, 5) of classified dogs per suburb.
    :param count_3: Array in shape (10, 5) of dogs not microchipped per suburb.
    :param count_4: Array in shape (10, 5) of dogs not desexed per suburb.
    :return: Four heatmaps which can be toggled between using radio buttons.
    """
    fig, (ax, cbar_ax) = plt.subplots(ncols=2, figsize=(8, 6),
                                      gridspec_kw={'width_ratios': [10, 1]})

    sns.heatmap(count_1, linewidth=1, linecolor='black', cmap="YlGnBu",
                annot=annotations, annot_kws={'fontsize': 10}, fmt='',
                yticklabels=False, xticklabels=False,
                ax=ax, cbar_ax=cbar_ax)
    ax.set_title("All Registered Dogs", horizontalalignment='center',
                 verticalalignment='bottom', fontsize=18)

    rax = fig.add_axes([0.01, 0.4, 0.10, 0.4], facecolor='lightgoldenrodyellow')
    radio = RadioButtons(rax, ('All registered \ndogs', 'Classified dogs',
                               'Dogs not \nmicrochipped', 'Dogs not \ndesexed',
                               'Exit and show \nall'),
                         label_props={'fontsize': [10]})

    def choose_map(label):
        """ Drives the RadioButton feature, allowing to switch between each. """
        if label == 'All registered \ndogs':
            sns.heatmap(count_1, linewidth=1, linecolor='black', cmap="YlGnBu",
                        annot=annotations, annot_kws={'fontsize': 10},
                        fmt='', yticklabels=False, xticklabels=False,
                        ax=ax, cbar_ax=cbar_ax)
            ax.set_title("All Registered Dogs", horizontalalignment='center',
                         verticalalignment='bottom', fontsize=18)
            plt.show()
        if label == 'Classified dogs':
            sns.heatmap(count_2, linewidth=1, linecolor='black', cmap="YlGnBu",
                        annot=annotations, annot_kws={'fontsize': 10}, fmt='',
                        yticklabels=False, xticklabels=False,
                        ax=ax, cbar_ax=cbar_ax)
            ax.set_title("Classified Dogs", horizontalalignment='center',
                         verticalalignment='bottom', fontsize=18)
            plt.show()
        if label == 'Dogs not \nmicrochipped':
            sns.heatmap(count_3, linewidth=1, linecolor='black', cmap="YlGnBu",
                        annot=annotations, annot_kws={'fontsize': 10}, fmt='',
                        yticklabels=False, xticklabels=False,
                        ax=ax, cbar_ax=cbar_ax)
            ax.set_title("Dogs Not Microchipped", horizontalalignment='center',
                         verticalalignment='bottom', fontsize=18)
            plt.show()
        if label == 'Dogs not \ndesexed':
            sns.heatmap(count_4, linewidth=1, linecolor='black', cmap="YlGnBu",
                        annot=annotations, annot_kws={'fontsize': 10}, fmt='',
                        yticklabels=False, xticklabels=False,
                        ax=ax, cbar_ax=cbar_ax)
            ax.set_title("Dogs Not Desexed", horizontalalignment='center',
                         verticalalignment='bottom', fontsize=18)
            plt.show()
        if label == 'Exit and show \nall':
            plt.close()

    radio.on_clicked(choose_map)
    plt.show()


def show_all_heatmaps(suburbs, count_1, count_2, count_3, count_4):
    """ Takes five arrays, one to be used for annotations and the remaining four
        to be used as quantities for heatmaps, and produces four matplotlib
        heatmaps that show in one window. This view allows annotations of both
        suburbs and count.
    :param suburbs: Array in shape (8, 6) of suburbs.
    :param count_1: Array in shape (8, 6) of all alive dogs per suburb.
    :param count_2: Array in shape (8, 6) of classified dogs per suburb.
    :param count_3: Array in shape (8, 6) of dogs not microchipped per suburb.
    :param count_4: Array in shape (8, 6) of dogs not desexed per suburb.
    :return: Four heatmaps shown in one window.
    """
    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, layout="constrained",
                                                 figsize=(13, 6))

    heatmap_1 = ax1.imshow(count_1, cmap="YlGnBu", aspect=0.3, alpha=0.7)
    fig.colorbar(heatmap_1)
    ax1.set_xticks([])
    ax1.set_yticks([])
    ax1.set_title("All Registered Dogs")
    for i in range(suburbs.shape[0]):
        for j in range(suburbs.shape[1]):
            ax1.text(j, i, suburbs[i, j], ha="center", va="bottom", size=8)
    for i in range(count_1.shape[0]):
        for j in range(count_1.shape[1]):
            ax1.text(j, i, count_1[i, j], ha="center", va="top", size=8)
    ax1.set_yticks(np.arange(-0.5, 8, 1))
    ax1.set_xticks(np.arange(0.5, 5, 1))
    ax1.set_xticklabels("")
    ax1.set_yticklabels("")
    ax1.tick_params(axis='both', colors='white')
    ax1.grid(True, which='major', color='black', linestyle='-')

    heatmap_2 = ax2.imshow(count_2, cmap="YlGnBu", aspect=0.3, alpha=0.7)
    fig.colorbar(heatmap_2)
    ax2.set_xticks([])
    ax2.set_yticks([])
    ax2.set_title("Classified Dogs")
    for i in range(suburbs.shape[0]):
        for j in range(suburbs.shape[1]):
            ax2.text(j, i, suburbs[i, j], ha="center", va="bottom", size=8)
    for i in range(count_2.shape[0]):
        for j in range(count_2.shape[1]):
            ax2.text(j, i, count_2[i, j], ha="center", va="top", size=8)
    ax2.set_yticks(np.arange(-0.5, 8, 1))
    ax2.set_xticks(np.arange(0.5, 5, 1))
    ax2.set_xticklabels("")
    ax2.set_yticklabels("")
    ax2.tick_params(axis='both', colors='white')
    ax2.grid(True, which='major', color='black', linestyle='-')

    heatmap_3 = ax3.imshow(count_3, cmap="YlGnBu", aspect=0.3, alpha=0.7)
    fig.colorbar(heatmap_3)
    ax3.set_xticks([])
    ax3.set_yticks([])
    ax3.set_title("Dogs Not Microchipped")
    for i in range(suburbs.shape[0]):
        for j in range(suburbs.shape[1]):
            ax3.text(j, i, suburbs[i, j], ha="center", va="bottom", size=8)
    for i in range(count_3.shape[0]):
        for j in range(count_3.shape[1]):
            ax3.text(j, i, count_3[i, j], ha="center", va="top", size=8)
    ax3.set_yticks(np.arange(-0.5, 8, 1))
    ax3.set_xticks(np.arange(0.5, 5, 1))
    ax3.set_xticklabels("")
    ax3.set_yticklabels("")
    ax3.tick_params(axis='both', colors='white')
    ax3.grid(True, which='major', color='black', linestyle='-')

    heatmap_4 = ax4.imshow(count_4, cmap="YlGnBu", aspect=0.3, alpha=0.7)
    fig.colorbar(heatmap_4)
    ax4.set_title("Dogs Not Desexed")
    for i in range(suburbs.shape[0]):
        for j in range(suburbs.shape[1]):
            ax4.text(j, i, suburbs[i, j], ha="center", va="bottom", size=8)
    for i in range(count_1.shape[0]):
        for j in range(count_4.shape[1]):
            ax4.text(j, i, count_4[i, j], ha="center", va="top", size=8)
    ax4.set_yticks(np.arange(-0.5, 8, 1))
    ax4.set_xticks(np.arange(0.5, 5, 1))
    ax4.set_xticklabels("")
    ax4.set_yticklabels("")
    ax4.tick_params(axis='both', colors='white')
    ax4.grid(True, which='major', color='black', linestyle='-')
    plt.show()


def main():
    """ Read a file of data regarding registered dogs in Hamilton, convert the
        data into multiple dictionaries and arrays depending on the condition
        being assessed, create and display four heatmaps, one at a time, which
        can be toggled between using radio buttons. On exit, new window opens
        showing all four heatmaps at the same time.
    """
    lines = dog_data()
    dogs = alive_dogs(lines)
    suburbs = suburb_array(dogs)
    all_dogs_dict = dogs_per_suburb(dogs)
    classified_dict = classified_suburbs(dogs)
    not_microchipped_dict = no_microchip_suburbs(dogs)
    entire_dict = entire_suburbs(dogs)
    all_dogs = shaped_array(all_dogs_dict)
    classifieds = shaped_array(classified_dict)
    entires = shaped_array(entire_dict)
    no_microchips = shaped_array(not_microchipped_dict)
    plot_heatmaps(suburbs, all_dogs, classifieds, no_microchips, entires)
    show_all_heatmaps(suburbs, all_dogs, classifieds, no_microchips, entires)


main()
