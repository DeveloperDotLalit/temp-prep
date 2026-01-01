import os

ROOT_DIR = r"d:\Gravity\TempFolder\Android\temp-prep"

def update_nav_order(file_path, order):
    try:
        if not os.path.exists(file_path): return
        with open(file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        new_lines = []
        in_fm = False
        fm_count = 0
        
        for line in lines:
            if line.strip() == '---':
                fm_count += 1
                if fm_count == 1: in_fm = True
                if fm_count == 2: in_fm = False
                new_lines.append(line)
                continue

            if in_fm:
                if line.strip().startswith("nav_order:"):
                    new_lines.append(f"nav_order: {order}\n")
                else:
                    new_lines.append(line)
            else:
                new_lines.append(line)
        
        with open(file_path, 'w', encoding='utf-8') as f:
            f.writelines(new_lines)
        print(f"Updated {os.path.basename(file_path)} -> {order}")
            
    except Exception as e:
        print(f"Error updating {file_path}: {e}")

def main():
    # 1. Home
    update_nav_order(os.path.join(ROOT_DIR, "index.md"), 1)
    
    # 2. Modules
    # Map prefix to offset
    # 01 -> 2
    for item in os.listdir(ROOT_DIR):
        if os.path.isdir(os.path.join(ROOT_DIR, item)):
            # Try to parse prefix
            prefix = item.split(' ')[0]
            if prefix.isdigit():
                num = int(prefix)
                new_order = num + 1
                
                index_path = os.path.join(ROOT_DIR, item, "index.md")
                update_nav_order(index_path, new_order)

if __name__ == "__main__":
    main()
