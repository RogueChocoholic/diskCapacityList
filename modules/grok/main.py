import os
import csv
import sys

def get_folder_size(path):
    """Calculate the total size of a folder (including all contents) in bytes."""
    total = 0
    try:
        for dirpath, dirnames, filenames in os.walk(path):
            for f in filenames:
                fp = os.path.join(dirpath, f)
                # Skip if it's a symbolic link (to avoid errors/loops)
                if not os.path.islink(fp):
                    try:
                        total += os.path.getsize(fp)
                    except (OSError, PermissionError):
                        pass  # Skip files we can't access
    except (OSError, PermissionError):
        pass  # Skip folders we can't access
    return total

def list_subfolder_sizes(drive_letter):
    # Normalize the drive path (e.g., "C:" -> "C:\")
    drive_path = drive_letter.upper()
    if not drive_path.endswith(':\\'):
        drive_path += ':\\'
    
    if not os.path.exists(drive_path):
        print(f"The drive {drive_path} does not exist.")
        return
    
    print(f"Scanning top-level folders on {drive_path} ... (this may take a while)")
    
    folders = []
    try:
        items = os.listdir(drive_path)
    except PermissionError:
        print("Permission denied: Unable to access the drive.")
        return
    
    for item in items:
        item_path = os.path.join(drive_path, item)
        if os.path.isdir(item_path):
            print(f"Calculating size for: {item}")
            size = get_folder_size(item_path)
            folders.append((item, size))
    
    # Sort by size descending
    folders.sort(key=lambda x: x[1], reverse=True)
    
    # Save to CSV
    csv_file = 'folder_sizes.csv'
    with open(csv_file, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['Folder Name', 'Size (bytes)', 'Size (MB)', 'Size (GB)'])
        for name, size_bytes in folders:
            size_mb = size_bytes / (1024 ** 2)
            size_gb = size_bytes / (1024 ** 3)
            writer.writerow([name, size_bytes, f'{size_mb:.2f}', f'{size_gb:.2f}'])
    
    print(f"\nDone! Results saved to '{csv_file}'")
    print("\nTop 10 largest folders:")
    for i, (name, size_bytes) in enumerate(folders[:10], 1):
        size_gb = size_bytes / (1024 ** 3)
        print(f"{i}. {name}: {size_gb:.2f} GB")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python folder_sizes.py <drive_letter>")
        print("Example: python folder_sizes.py C:")
    else:
        list_subfolder_sizes(sys.argv[1])