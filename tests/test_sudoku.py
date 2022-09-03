from sudoku.sudoku import Sudoku
import os

def test_solution_easy():
    path = os.path.join(os.path.dirname(os.path.realpath(__file__)),
                        'test_sudoku/sudoku_easy_1.txt') 
    sudoku_easy = Sudoku(path)
    sudoku_easy.solve()
    assert sudoku_easy.check() == True

def test_solution_hard():
    path = os.path.join(os.path.dirname(os.path.realpath(__file__)),
                        'test_sudoku/sudoku_hard_1.txt') 
    sudoku_hard = Sudoku(path)
    sudoku_hard.solve()
    assert sudoku_hard.check() == True

if __name__=='__main__':
    test_solution_easy()