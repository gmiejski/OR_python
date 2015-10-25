import codecs
from time import sleep
from matplotlib.pylab import *
import collections


# if len(sys.argv) < 2:
#     print("Need file with history as argument!")
# exit(1)
# filename = "../"+sys.argv[1]
#
filename="../history.txt"

print(matplotlib.matplotlib_fname())
data = collections.defaultdict(lambda: [])
curr_index = None

def to_number(x):
    if x == 'OK':
        return 0
    elif x.startswith("I"):
        return (int(x[1:]))*5+200
    else:
        return int(x[1:])*5 + 100


for line in codecs.open(filename, "r", "utf-8"):
    l = line.rstrip()
    if len(l) == 0:
        continue
    if l.startswith("#"):
        curr_index = int(l[1:])
        print("Loading data: " + str(curr_index))
    elif l.startswith("["):
        a = l.replace("'", "").replace("[", "").replace("]", "").replace(" ", "").split(",")
        cells = list(map(lambda x: to_number(x), a))
        data[curr_index].append(cells)

print("")

showed = 0

im = matshow(data[showed], cmap=cm.jet)
figure = im.figure


def button(event):
    global showed
    if event.key == 'left':
        if showed > 0:
            showed -= 1
            im.set_data(data[showed])
            figure.canvas.draw()
    elif event.key == 'right':
        if showed < curr_index:
            showed += 1
            im.set_data(data[showed])
            figure.canvas.draw()


figure.canvas.mpl_connect('key_press_event', button)

show()

sleep(10)