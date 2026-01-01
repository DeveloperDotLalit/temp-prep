import os

ROOT_DIR = r"d:\Gravity\TempFolder\Android\temp-prep"

def update_front_matter(file_path, updates):
    """Updates specific keys in Front Matter."""
    try:
        if not os.path.exists(file_path): 
            print(f"Skipping {file_path} (Not found)")
            return

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
                key = line.split(':', 1)[0].strip()
                if key in updates:
                    new_lines.append(f"{key}: {updates[key]}\n")
                else:
                    new_lines.append(line)
            else:
                new_lines.append(line)
        
        with open(file_path, 'w', encoding='utf-8') as f:
            f.writelines(new_lines)
        print(f"Fixed: {file_path}")
            
    except Exception as e:
        print(f"Error updating {file_path}: {e}")

def main():
    # 1. Fix Orphans
    orphans = [
        (r"01 Unit_UI_Testing\CheatSheet.md", "Unit & UI Testing"),
        (r"01 Unit_UI_Testing\FinalCheatSheet.md", "Unit & UI Testing"),
        (r"01 Unit_UI_Testing\MiniBookBlock.md", "Unit & UI Testing"),
        (r"02 DI\CheatSheet.md", "Dependency Injection"),
        (r"03 Architecture_MVVM_MVI_Clean\CheatSheet.md", "Architecture (MVVM/MVI/Clean)"),
        (r"05 KotlinAdvance\CheatSheet.md", "Advanced Kotlin"),
    ]
    
    print("Fixing Orphans...")
    for rel_path, correct_parent in orphans:
        full_path = os.path.join(ROOT_DIR, rel_path)
        update_front_matter(full_path, {"parent": correct_parent})

    # 2. Fix Nav Order Collision
    # Module 14 should be 14. Module 15 should be 15.
    print("Fixing Nav Order...")
    mod14 = os.path.join(ROOT_DIR, r"14 Current Project working - Focus on tech used\index.md")
    update_front_matter(mod14, {"nav_order": 14})
    
    mod15 = os.path.join(ROOT_DIR, r"15 TheQuestionBank\index.md")
    update_front_matter(mod15, {"nav_order": 15})

    # 3. Fix Duplicate Titles in Question Bank
    # Rename "Coroutines" -> "Coroutines Q&A"
    print("Fixing Duplicates...")
    q_cor = os.path.join(ROOT_DIR, r"15 TheQuestionBank\03_Coroutines.md")
    update_front_matter(q_cor, {"title": "Coroutines Q&A"})
    
    q_flow = os.path.join(ROOT_DIR, r"15 TheQuestionBank\04_Flow.md")
    update_front_matter(q_flow, {"title": "Flow Q&A"})

if __name__ == "__main__":
    main()
