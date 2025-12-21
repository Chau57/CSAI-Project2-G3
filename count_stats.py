import os
import glob

# --- CẤU HÌNH ĐƯỜNG DẪN ---
# Bạn hãy sửa đường dẫn này trỏ tới thư mục chứa file .txt của bạn
INPUT_DIR = "data/inputs" 

def parse_grid(filepath):
    """Đọc file text và chuyển thành ma trận 2D (list of lists)"""
    grid = []
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if not line: continue
                # Tách bằng dấu phẩy, loại bỏ khoảng trắng thừa và chuyển sang int
                row = [int(x.strip()) for x in line.split(',')]
                grid.append(row)
    except Exception as e:
        print(f"Error reading {filepath}: {e}")
        return []
    return grid

def analyze_puzzle(grid):
    """
    Phân tích grid để đếm:
    1. Kích thước (Rows x Cols)
    2. Số lượng đảo (Islands)
    3. Số cạnh tiềm năng (Edges): Số cặp đảo có thể nối với nhau (thẳng hàng, không bị chặn)
    """
    if not grid: return 0, 0, 0, 0
    
    rows = len(grid)
    cols = len(grid[0])
    islands = 0
    potential_edges = 0
    
    for r in range(rows):
        for c in range(cols):
            # Nếu gặp một đảo
            if grid[r][c] != 0:
                islands += 1
                
                # --- THUẬT TOÁN ĐẾM CẠNH ---
                # Chỉ cần nhìn sang Phải và xuống Dưới để không đếm trùng
                
                # 1. Nhìn sang Phải (Horizontal)
                for k in range(c + 1, cols):
                    val = grid[r][k]
                    if val != 0: # Gặp đảo hàng xóm
                        potential_edges += 1
                        break # Dừng, vì không thể nối xuyên qua đảo này
                        
                # 2. Nhìn xuống Dưới (Vertical)
                for k in range(r + 1, rows):
                    val = grid[k][c]
                    if val != 0: # Gặp đảo hàng xóm
                        potential_edges += 1
                        break # Dừng
                        
    return rows, cols, islands, potential_edges

def main():
    # Tìm tất cả file .txt trong thư mục
    search_path = os.path.join(INPUT_DIR, "input-*.txt")
    files = sorted(glob.glob(search_path))
    
    if not files:
        print(f"Không tìm thấy file nào trong: {search_path}")
        print("Hãy kiểm tra lại biến INPUT_DIR trong code.")
        return

    print("\n" + "="*80)
    print(f"{'File Name':<15} | {'Size':<10} | {'Islands':<8} | {'Edges':<8} | {'Complexity (3^E)'}")
    print("-" * 80)
    
    # Dữ liệu để in ra dạng LaTeX (nếu cần copy vào báo cáo)
    latex_rows = []

    for filepath in files:
        grid = parse_grid(filepath)
        rows, cols, islands, edges = analyze_puzzle(grid)
        filename = os.path.basename(filepath).replace(".txt", "")
        
        # In ra màn hình console
        complexity = f"3^{edges}"
        print(f"{filename:<15} | {rows}x{cols:<5} | {islands:<8} | {edges:<8} | {complexity}")
        
        # Lưu định dạng LaTeX
        latex_row = f"{filename} & ${rows} \\times {cols}$ & {islands} & {edges} & Very Hard \\\\"
        latex_rows.append(latex_row)

    # --- In ra format bảng LaTeX để copy vào báo cáo ---
    print("\n" + "="*80)
    print("MÃ LATEX ĐỂ COPY VÀO BÁO CÁO:")
    print("="*80)
    print(r"\begin{table}[H]")
    print(r"\centering")
    print(r"\caption{Thống kê chi tiết bộ dữ liệu kiểm thử}")
    print(r"\label{tab:testcases}")
    print(r"\begin{tabular}{|c|c|c|c|l|}")
    print(r"\hline")
    print(r"\textbf{Input} & \textbf{Kích thước} & \textbf{Số đảo} & \textbf{Số cạnh ($|E|$)} & \textbf{Mục đích / Độ khó} \\ \hline")
    
    for row in latex_rows:
        print(row + " \\hline")
        
    print(r"\end{tabular}")
    print(r"\end{table}")

if __name__ == "__main__":
    main()