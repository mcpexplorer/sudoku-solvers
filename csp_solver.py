from ortools.sat.python import cp_model

def solve_sudoku(grid):
    model = cp_model.CpModel()
    cells = {}

    # 创建变量
    for i in range(9):
        for j in range(9):
            if grid[i][j] == 0:  # 0 表示空格
                cells[i, j] = model.NewIntVar(1, 9, f'cell_{i}_{j}')
            else:
                cells[i, j] = model.NewIntVar(grid[i][j], grid[i][j], f'fixed_cell_{i}_{j}')

    # 添加数独约束
    for i in range(9):
        model.AddAllDifferent([cells[i, j] for j in range(9)])  # 行
        model.AddAllDifferent([cells[j, i] for j in range(9)])  # 列

    for i in range(3):
        for j in range(3):
            model.AddAllDifferent([cells[i * 3 + x, j * 3 + y] for x in range(3) for y in range(3)])  # 3x3 方块

    # 创建求解器
    solver = cp_model.CpSolver()
    status = solver.Solve(model)

    # 输出结果
    if status == cp_model.OPTIMAL or status == cp_model.FEASIBLE:
        return [[solver.Value(cells[i, j]) for j in range(9)] for i in range(9)]
    else:
        return None

# 示例数独棋盘
sudoku_grid = [
    [8, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 3, 6, 0, 0, 0, 0, 0],
    [0, 7, 0, 0, 9, 0, 2, 0, 0],
    [0, 5, 0, 0, 0, 7, 0, 0, 0],
    [0, 0, 0, 0, 4, 5, 7, 0, 0],
    [0, 0, 0, 1, 0, 0, 0, 3, 0],
    [0, 0, 1, 0, 0, 0, 0, 6, 8],
    [0, 0, 8, 5, 0, 0, 0, 1, 0],
    [0, 9, 0, 0, 0, 0, 4, 0, 0]
]

solved_grid = solve_sudoku(sudoku_grid)
if solved_grid:
    for row in solved_grid:
        print(row)
else:
    print('没有找到解')