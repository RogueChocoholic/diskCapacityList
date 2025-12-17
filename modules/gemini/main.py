import os
import csv
from typing import List, Tuple

def get_folder_size(start_path: str) -> int:
    """
    Recursively calculates the total size of a folder in bytes.

    Args:
        start_path: The path to the folder.

    Returns:
        The total size of the folder and its contents in bytes.
    """
    total_size = 0
    try:
        # os.walk is an efficient way to traverse a directory tree
        for dirpath, dirnames, filenames in os.walk(start_path):
            for f in filenames:
                fp = os.path.join(dirpath, f)
                # Check if it is a symbolic link and skip to avoid infinite loops or errors
                if not os.path.islink(fp):
                    # Add file size to total size
                    total_size += os.path.getsize(fp)
    except Exception as e:
        # Print a message for errors (like permission denied) and continue
        print(f"Error accessing path {start_path}: {e}")
        return 0 # Return 0 if the path couldn't be fully accessed
        
    return total_size

def bytes_to_human_readable(size_bytes: int) -> str:
    """
    Converts a size in bytes to a human-readable format (e.g., KB, MB, GB).
    """
    # Define units
    if size_bytes == 0:
        return "0 B"
    
    units = ['B', 'KB', 'MB', 'GB', 'TB', 'PB']
    i = 0
    size = size_bytes
    while size >= 1024 and i < len(units) - 1:
        size /= 1024.0
        i += 1
    
    return f"{size:.2f} {units[i]}"

def analyze_disk_usage(drive_letter: str, output_csv_filename: str = 'GeminI_folder_sizes.csv'):
    """
    Scans the specified drive, calculates folder sizes, sorts them, 
    and writes the results to a CSV file.
    
    Args:
        drive_letter: The letter of the local disk (e.g., 'C').
        output_csv_filename: The name of the CSV file to create.
    """
    # Construct the base path for the drive
    if os.name == 'nt':  # For Windows
        base_path = f"{drive_letter.upper()}:\\"
    elif os.name == 'posix': # For Linux/macOS, assuming the letter is a mounted directory name
        base_path = f"/{drive_letter}" 
    else:
        print("Unsupported operating system.")
        return

    print(f"🚀 Starting scan of {base_path}...")
    
    # Get all immediate subdirectories
    try:
        top_level_items = [os.path.join(base_path, name) for name in os.listdir(base_path)]
        subdirectories = [item for item in top_level_items if os.path.isdir(item)]
    except FileNotFoundError:
        print(f"❌ Error: Drive letter '{drive_letter}' or path '{base_path}' not found.")
        return
    except PermissionError:
        print(f"❌ Error: Permission denied for accessing '{base_path}'.")
        return
    except Exception as e:
        print(f"❌ An unexpected error occurred: {e}")
        return

    folder_data: List[Tuple[str, int]] = []
    
    # Process each subdirectory
    for i, folder_path in enumerate(subdirectories):
        print(f"  ({i+1}/{len(subdirectories)}) Calculating size for: {folder_path}...")
        size_bytes = get_folder_size(folder_path)
        folder_data.append((folder_path, size_bytes))

    # Sort the list from highest size to lowest
    # The key is the size (index 1 in the tuple), and reverse=True for descending order
    folder_data.sort(key=lambda item: item[1], reverse=True)

    # Write the results to a CSV file
    with open(output_csv_filename, 'w', newline='', encoding='utf-8') as csvfile:
        csv_writer = csv.writer(csvfile)
        
        # Write the header row
        csv_writer.writerow(['Folder Path', 'Size (Bytes)', 'Size (Human Readable)'])
        
        # Write the data rows
        for folder_path, size_bytes in folder_data:
            human_readable_size = bytes_to_human_readable(size_bytes)
            csv_writer.writerow([folder_path, size_bytes, human_readable_size])

    print("\n✅ Scan complete!")
    print(f"Results have been saved to **{output_csv_filename}**.")
    
# --- Main Execution Block ---
if __name__ == "__main__":
    # 1. Get the drive letter from the user
    drive = input("Enter the local disk letter (e.g., C, D, or for Linux/macOS, a path like home): ").strip()
    
    # 2. Call the main function
    # Note: If the user enters 'C', the base path will be 'C:\' on Windows.
    # On Linux/macOS, if the user enters 'home', the base path will be '/home'.
    analyze_disk_usage(drive)