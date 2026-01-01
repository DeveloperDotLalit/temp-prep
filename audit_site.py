import os

ROOT_DIR = r"d:\Gravity\TempFolder\Android\temp-prep"

def get_front_matter_info(file_path):
    info = {"title": None, "parent": None, "grand_parent": None, "nav_order": None, "path": file_path}
    try:
        if not os.path.exists(file_path): return info
        with open(file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        in_fm = False
        fm_count = 0
        for line in lines:
            if line.strip() == '---':
                fm_count += 1
                if fm_count == 1: in_fm = True
                if fm_count == 2: break
                continue
            
            if in_fm:
                parts = line.split(':', 1)
                if len(parts) == 2:
                    key = parts[0].strip()
                    val = parts[1].strip()
                    if (val.startswith('"') and val.endswith('"')) or (val.startswith("'") and val.endswith("'")):
                        val = val[1:-1]
                    
                    if key == "title": info["title"] = val
                    if key == "parent": info["parent"] = val
                    if key == "grand_parent": info["grand_parent"] = val
                    if key == "nav_order": 
                        try:
                            info["nav_order"] = float(val) # allow decimals
                        except:
                            info["nav_order"] = val
    except Exception:
        pass
    return info

def main():
    print("Starting Site Audit...")
    
    # 1. Map all Titles to Files
    # Title -> [List of Files defining this title]
    # Ideally 1:1, but duplicates cause issues.
    title_map = {}
    
    # Rel Path -> Info
    all_files = {}

    for root, dirs, files in os.walk(ROOT_DIR):
        if "_site" in root or ".git" in root: continue
        
        for f in files:
            if f.lower().endswith(".md"):
                full_path = os.path.join(root, f)
                rel_path = os.path.relpath(full_path, ROOT_DIR)
                
                info = get_front_matter_info(full_path)
                info["rel_path"] = rel_path
                
                all_files[rel_path] = info
                
                if info["title"]:
                    if info["title"] not in title_map:
                        title_map[info["title"]] = []
                    title_map[info["title"]].append(rel_path)

    print(f"Scanned {len(all_files)} Markdown files.")
    
    issues = []
    
    # 2. Check logic
    for path, info in all_files.items():
        # Check 1: Duplicate Titles (Only critical if they are Parents)
        if info["title"] and len(title_map[info["title"]]) > 1:
            # It's okay to have duplicate titles if they are leaf nodes, BUT 
            # if they are used as a Parent, it's ambiguous.
            # We can't easily know if they are used as parent without checking everyone else.
            # But we can check if they are Phase files (likely parents).
            if "index.md" in path and path != "index.md":
                 issues.append(f"[WARNING] Duplicate Title '{info['title']}' found in: {title_map[info['title']]}")

        # Check 2: Parent Existence
        parent = info["parent"]
        if parent:
            if parent not in title_map:
                issues.append(f"[ERROR] Orphan: '{path}' refers to non-existent parent '{parent}'")
            else:
                # Check 3: Grand Parent Consistency
                pass # Logic is complex, assume Parent is correct for now.
                
                # Verify Parent isn't a duplicate (Ambiguous parent)
                if len(title_map[parent]) > 1:
                     issues.append(f"[ERROR] Ambiguous Parent: '{path}' refers to '{parent}' which is defined in multiple files: {title_map[parent]}")

        # Check 4: Nav Order Format
        if info["nav_order"] and not isinstance(info["nav_order"], (int, float)):
             issues.append(f"[WARNING] Invalid Nav Order in '{path}': {info['nav_order']}")

    # 3. Check Root Nav Orders (Modules)
    # Filter files that have NO parent (Roots) but are not the home page
    roots = []
    for path, info in all_files.items():
        if not info["parent"] and info["title"] != "Home" and "index.md" in path:
             roots.append((info["nav_order"], info["title"], path))
             
    roots.sort(key=lambda x: (x[0] if isinstance(x[0], (int, float)) else 999))
    
    print("\nRoot Module Order:")
    for order, title, path in roots:
        print(f"{order}: {title} ({path})")
        
    if not issues:
        print("\n[OK] No Critical Architecture Issues Found.")
    else:
        print("\n[FAIL] Issues Found:")
        for i in issues:
            print(i)

if __name__ == "__main__":
    main()
