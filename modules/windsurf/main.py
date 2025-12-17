import os
import csv
from datetime import datetime
from pathlib import Path

def get_folder_size(folder_path):
    """Calculate the total size of a folder and its subfolders in bytes."""
    total_size = 0
    for dirpath, dirnames, filenames in os.walk(folder_path):
        for filename in filenames:
            try:
                file_path = os.path.join(dirpath, filename)
                # Skip if it is a symbolic link
                if not os.path.islink(file_path):
                    total_size += os.path.getsize(file_path)
            except (PermissionError, FileNotFoundError):
                # Skip files that can't be accessed
                continue
    return total_size

def get_disk_folders_sorted(drive_letter):
    """
    Get all folders in the root of a drive and return them sorted by size.
    
    Args:
        drive_letter (str): Single letter representing the drive (e.g., 'C', 'D')
        
    Returns:
        list: List of tuples containing (folder_path, size_in_bytes)
    """
    drive_path = f"{drive_letter.upper()}:\\"
    if not os.path.exists(drive_path):
        print(f"Drive {drive_letter.upper()}: does not exist.")
        return []
    
    print(f"Scanning folders in {drive_path}...")
    folders = []
    
    try:
        # Get all items in the root directory
        with os.scandir(drive_path) as entries:
            for entry in entries:
                if entry.is_dir(follow_symlinks=False):
                    try:
                        folder_path = entry.path
                        print(f"Analyzing {folder_path}...")
                        size = get_folder_size(folder_path)
                        folders.append((folder_path, size))
                    except (PermissionError, FileNotFoundError):
                        # Skip folders that can't be accessed
                        continue
    except PermissionError:
        print(f"Permission denied when accessing drive {drive_path}")
        return []
    
    # Sort folders by size in descending order
    folders.sort(key=lambda x: x[1], reverse=True)
    return folders

def save_to_csv(folders, output_file=None):
    """
    Save folder sizes to a CSV file.
    
    Args:
        folders (list): List of tuples (folder_path, size_in_bytes)
        output_file (str, optional): Path to output CSV file. If not provided, generates a filename.
        
    Returns:
        str: Path to the generated CSV file
    """
    if not output_file:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_file = f"disk_usage_{timestamp}.csv"
    
    # Convert sizes to MB and GB for better readability
    data = []
    for folder_path, size in folders:
        size_mb = size / (1024 * 1024)  # Convert to MB
        size_gb = size_mb / 1024  # Convert to GB
        data.append({
            'folder_path': folder_path,
            'size_bytes': size,
            'size_mb': size_mb,
            'size_gb': size_gb
        })
    
    try:
        with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
            fieldnames = ['folder_path', 'size_bytes', 'size_mb', 'size_gb']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            
            writer.writeheader()
            for row in data:
                writer.writerow(row)
        
        print(f"Results saved to: {os.path.abspath(output_file)}")
        return os.path.abspath(output_file)
    except Exception as e:
        print(f"Error saving to CSV: {e}")
        return None

def analyze_disk_usage(drive_letter, output_file=None):
    """
    Main function to analyze disk usage and save to CSV.
    
    Args:
        drive_letter (str): Single letter representing the drive (e.g., 'C', 'D')
        output_file (str, optional): Path to output CSV file. If not provided, generates a filename.
    """
    print(f"Starting disk usage analysis for drive {drive_letter.upper()}:")
    print("This may take a while for large drives...")
    print("-" * 50)
    
    # Get sorted folders
    folders = get_disk_folders_sorted(drive_letter)
    
    if not folders:
        print("No folders found or an error occurred.")
        return
    
    # Print summary
    print("\nTop 10 largest folders:")
    print("-" * 80)
    print(f"{'Folder Path':<60} {'Size (GB)':>10} {'Size (MB)':>15}")
    print("-" * 80)
    
    for i, (folder, size) in enumerate(folders[:10], 1):
        size_mb = size / (1024 * 1024)
        size_gb = size_mb / 1024
        print(f"{i}. {folder[:57] + '...' if len(folder) > 60 else folder:<60} {size_gb:>10.2f} {size_mb:>15.2f}")
    
    # Save to CSV
    print("\nSaving results to CSV...")
    csv_path = save_to_csv(folders, output_file)
    
    if csv_path:
        print(f"\nAnalysis complete! Results saved to: {csv_path}")
    else:
        print("\nError: Could not save results to CSV.")

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description='Analyze disk usage and save to CSV')
    parser.add_argument('drive', help='Drive letter to analyze (e.g., C, D)')
    parser.add_argument('-o', '--output', help='Output CSV file path (optional)')
    
    args = parser.parse_args()
    
    analyze_disk_usage(args.drive, args.output)