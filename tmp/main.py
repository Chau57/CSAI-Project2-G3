from hashi_solver_PySAT import HashiSolver


def read_input(filename):
    """Đọc file input và trả về ma trận grid"""
    grid = []
    with open(filename, 'r') as f:
        for line in f:
            line = line.strip()
            if line:
                row = [int(x) for x in line.replace(',', '').split()]
                grid.append(row)
    return grid


def write_output(filename, result):
    """Ghi kết quả ra file output theo format yêu cầu"""
    with open(filename, 'w') as f:
        for row in result:
            # Tạo format với dấu ngoặc kép và dấu phẩy
            formatted_row = '["' + '", "'.join(row) + '"]'
            f.write(formatted_row + '\n')


def main():
    # Đọc input
    input_file = 'input-00.txt'
    output_file = 'output-00.txt'
    
    print(f"Đọc file {input_file}...")
    grid = read_input(input_file)
    
    print(f"Grid size: {len(grid)}x{len(grid[0])}")
    print("Đang giải bài toán Hashiwokakero...")
    
    # Khởi tạo solver và giải
    solver = HashiSolver(grid)
    result = solver.solve()
    
    if result is None:
        print("Không tìm thấy lời giải!")
    else:
        print("Tìm thấy lời giải!")
        
        # Ghi kết quả ra file
        write_output(output_file, result)
        print(f"Đã ghi kết quả vào file {output_file}")
        
        # In kết quả ra màn hình
        print("\nKết quả:")
        for row in result:
            print(' '.join(row))


if __name__ == "__main__":
    main()
