import time,random,sys
from PyQt4.QtCore import *
from PyQt4.QtGui import *

def gen_random_array(len_x, len_y):
    array = list()
    for y in range(len_y):
        array.append(list())
        for x in range(len_x):
            array[y].append(random.choice((0,1)))
    return array
       
def game_of_life(array):
    generations = 500
    for g in range(generations):
        print_array(array)
        array = next_generation(array)
        time.sleep(1)
        
def next_generation(array):
    new_array = list()
    for y in range(len(array)):
        new_array.append(list())
        for x in range(len(array[y])):
            neighbours = calculate_neighbours(array, x, y)
            if array[y][x] == 0:
                if neighbours == 3:
                    new_array[y].append(1)
                else:
                    new_array[y].append(0)
            else:
                if neighbours < 2 or neighbours > 3:
                    new_array[y].append(0)
                else:
                    new_array[y].append(1)
    return new_array

def print_array(array):
    for line in array:
        print '-' * (len(line)*2+1)
        line_str = '|' + '|'.join(map(str, line)) + '|'
        print line_str.replace('1', 'x').replace('0', 'o')
    print '-' * (len(line)*2+1)
    
    
def calculate_neighbours(array, x, y):
    num = 0
    # not left border
    if x > 0:
        # left cell
        if array[y][x-1] == 1:
            num += 1
        if y > 0 and array[y-1][x-1] == 1:
            num += 1
        if y < len(array)-1 and array[y+1][x-1] == 1:
            num +=1
    # not right border
    if x < len(array[y])-1:
        # right cell
        if array[y][x+1] == 1:
            num += 1
        if y > 0 and array[y-1][x+1] == 1:
            num += 1
        if y < len(array)-1 and array[y+1][x+1] == 1:
            num += 1
    # upper cell
    if y > 0 and array[y-1][x] == 1:
        num +=1
    # bottom cell
    if y < len(array)-1 and array[y+1][x] == 1:
        num +=1
        
    return num

class MainWindow(QWidget):
    def __init__(self, array):
        QWidget.__init__(self)
        self.alive = 'X'
        self.dead = '.'
        self.array = array
        self.len_y = len(array)
        self.len_x = len(array[0])
        self.counter = 0
        self.generations = 5
        layout = QVBoxLayout()
        self.setLayout(layout)
        grid_widget = QWidget()
        self.grid = QGridLayout()
        grid_widget.setLayout(self.grid)
        layout.addWidget(grid_widget)
        self.reset_button = QPushButton(QIcon.fromTheme('edit-clear'), 'Reset')
        self.start_button = QPushButton(QIcon.fromTheme('go-next'), 'Next')
        self.generation_label = QLabel(str(self.counter))
        layout.addWidget(self.generation_label)
        layout.addWidget(self.reset_button)
        layout.addWidget(self.start_button)
        self.connect(self.reset_button, SIGNAL('clicked()'), self.reset)
        self.connect(self.start_button, SIGNAL('clicked()'), self.game_of_life)
        self.widget_array = list()
        for y in range(self.len_y):
            self.widget_array.append(list())
            for x in range(self.len_x):
                val = self.alive if self.array[y][x] == 1 else self.dead
                label = QLabel(val)
                self.widget_array[y].append(label)
                self.grid.addWidget(label,x,y)
    
    def game_of_life(self):
        #self.widget_array[0][0].setText('foo')
        #for g in range(self.generations):
            self.array = next_generation(self.array)
            self.update()
            #time.sleep(1)
                
    def reset(self):
        self.array = gen_random_array(self.len_x, self.len_y)
        self.counter = 0
        self.update()
        
    def update(self):
        self.counter += 1
        self.generation_label.setText(str(self.counter))
        for y, line in enumerate(self.array):
            for x, val in enumerate(line):
                #print 'setting', x, y, 'to', val
                val = self.alive if val == 1 else self.dead
                self.widget_array[y][x].setText(str(val))
                
if __name__ == '__main__':
    app = QApplication(sys.argv)
    x = 32
    y = 32
    array = gen_random_array(x,y)
    window = MainWindow(array)
    
    window.show()
    #window.game_of_life(500)
    sys.exit(app.exec_())
    
