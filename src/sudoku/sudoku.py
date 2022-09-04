import numpy as np
import matplotlib.pyplot as plt

class Sudoku():


    def __init__(self, filename):
        # problem & solution
        self.sudoku_problem = self.read(filename)
        self.sudoku = np.copy(self.sudoku_problem)
        # quadrants
        self.quadrants = np.zeros((9,9)).astype(int)
        self.set_quadrants()
        # options
        self.sudoku_options = np.zeros((9,9,9)).astype(int)
        self.initialize_options()

    def read(self, filename):
        sudoku = np.genfromtxt(filename, delimiter=',').astype(int)
        assert sudoku.shape == (9,9), \
            'Error: File contains sudoku with shape {},'.format(sudoku.shape) \
            +' only (9, 9) allowed!'
        return sudoku

    def set_quadrants(self):
        for i0 in range(3):
            for j0 in range(3):
                for i in range(3):
                    for j in range(3):
                        self.quadrants[3*i0+i, 3*j0+j] = 3*i0+j0

    def initialize_options(self):
        for i in range(9):
            for j in range(9):
                if self.sudoku[i,j] == 0:
                    self.sudoku_options[i,j,:] = np.array(list(range(1,10)))
       
    def show(self, plot_options=False): 
        fig, ax = plt.subplots(1,1, figsize=(10,10))
        ax.axis('off')
        ax.axis('equal')
        # grid
        for x in [-0.5, 2.5, 5.5, 8.5]:
            ax.plot([x, x], [-0.5, 8.5], '-k', lw=4)
        for x in [0.5, 1.5, 3.5, 4.5, 6.5, 7.5]:
            ax.plot([x, x], [-0.5, 8.5], '-k', lw=2)
        for y in [-0.5, 2.5, 5.5, 8.5]:
            ax.plot([-0.5, 8.5], [y, y], '-k', lw=4)
        for y in [0.5, 1.5, 3.5, 4.5, 6.5, 7.5]:
            ax.plot([-0.5, 8.5], [y, y], '-k', lw=2)
        ax.fill([-0.5, 2.5, 2.5, -0.5], [2.5, 2.5, 5.5, 5.5],
                color='lightgray')
        ax.fill([5.5, 8.5, 8.5, 5.5], [2.5, 2.5, 5.5, 5.5],
                 color='lightgray')
        ax.fill([2.5, 5.5, 5.5, 2.5], [-0.5, -0.5, 2.5, 2.5],
                 color='lightgray')
        ax.fill([2.5, 5.5, 5.5, 2.5], [5.5, 5.5, 8.5, 8.5],
                 color='lightgray')
        # solution & options
        options_offset = np.array([[-1,1], [0,1], [1,1],
                                   [-1,0], [0,0], [1,0],
                                   [-1,-1], [0,-1], [1,-1]])        
        for i in range(9):
            for j in range(9):
                if self.sudoku[i,j] != 0:
                    if self.sudoku[i,j] == self.sudoku_problem[i,j]:
                        color='k'
                    else:
                        color='orange'
                    ax.text(j,8-i, self.sudoku[i,j],
                            ha='center', va='center',
                            color=color, fontsize=30)
                elif plot_options is True:
                    for k in range(9):
                        if self.sudoku_options[i,j,k] != 0:
                            ax.text(j+0.25*options_offset[k,0],
                                    8-i+0.25*options_offset[k,1],
                                    self.sudoku_options[i,j,k],
                                    ha='center', va='center',
                                    color='r', fontsize=12)    
        plt.show()
        
    def reduce_options(self):
        for i in range(9):
            row_set = set(self.sudoku[i,:])-{0}
            for j in range(9):
                column_set = set(self.sudoku[:,j])-{0}
                quadrant_set = set(self.sudoku[
                    self.quadrants==self.quadrants[i,j]])-{0}
                if self.sudoku[i,j]==0:
                    for k in row_set.union(column_set).union(quadrant_set):
                        self.sudoku_options[i,j,k-1] = 0
        # reduce options in other quadrants
    
    def fill_fields(self):
        field_filled = False
        # only one remaining option in field
        for i in range(9):
            for j in range(9):
                options = set(self.sudoku_options[i,j,:])-{0}
                if len(options) == 1 and field_filled == False:
                    self.sudoku[i,j] = list(options)[0]
                    self.sudoku_options[i,j,:] = 0
                    field_filled = True
        # only one remaining option per row/column/quadrant
        for i in range(9):
            for j in range(9):
                if sum(self.sudoku_options[i,:,j] == j+1) == 1 \
                    and field_filled == False:
                    self.sudoku[i,self.sudoku_options[i,:,j] == j+1] = j+1
                    self.sudoku_options[i,
                        self.sudoku_options[i,:,j] == j+1,:] = 0
                    field_filled = True
                    print('setting {} in row {}'.format(j+1, i))
                if sum(self.sudoku_options[:,i,j] == j+1) == 1 \
                    and field_filled == False:
                    self.sudoku[self.sudoku_options[:,i,j] == j+1,i] = j+1
                    self.sudoku_options[
                        self.sudoku_options[:,i,j] == j+1,i,:] = 0
                    field_filled = True
                    print('setting {} in column {}'.format(j+1, i))
                    break
                if sum(self.sudoku_options[self.quadrants==i,j] == j+1) == 1 \
                    and field_filled == False:
                    ii_quadrant = np.where(self.quadrants==i)
                    ii_single = np.where(self.sudoku_options[self.quadrants==i,j] == j+1)
                    self.sudoku[ii_quadrant[0][ii_single[0]],
                                ii_quadrant[1][ii_single[0]]] = j+1
                    self.sudoku_options[ii_quadrant[0][ii_single[0]],
                                        ii_quadrant[1][ii_single[0]],:] = 0
                    field_filled = True
                    print('setting {} in quadrant {}'.format(j+1, i))
                    break
        
    
    def solve(self, show_intermediate=False):
        iter = 0
        max_iter = 81 - sum(sum(self.sudoku_problem == 0))
        while (0 in set(self.sudoku.flatten())) and (iter < max_iter):
            self.reduce_options()
            if show_intermediate is True:
                sudoku.show(plot_options=True)
            self.fill_fields()
            if show_intermediate is True:
                sudoku.show(plot_options=True)
            iter = iter + 1
        if 0 in set(self.sudoku.flatten()):
            print('Given sudoku could not be solved.')

    def check(self):
        correct = True
        for i in range(9):
            row_set = set(self.sudoku[i,:])-{0}
            if row_set != set(range(1,10)):
                correct = False
                print('Error in row {}!'.format(i))
            column_set = set(self.sudoku[:,i])-{0}
            if column_set != set(range(1,10)):
                correct = False
                print('Error in column {}!'.format(i))
            quadrant_set = set(self.sudoku[
                self.quadrants==i])-{0}
            if quadrant_set != set(range(1,10)):
                correct = False
                print('Error in quadrant {}!'.format(i))
        if correct is True:
            print('Solution is correct!')
        return correct


if __name__=='__main__':
    sudoku = Sudoku('../../data/sudoku_hard_2.txt')
    sudoku.solve(show_intermediate=True)
    sudoku.show()
    sudoku.check()