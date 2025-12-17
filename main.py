from modules.gemini.main import analyze_disk_usage as gemini_main
from modules.grok.main import list_subfolder_sizes as grok_main
from modules.windsurf.main import analyze_disk_usage as windsurf_main

if __name__ == "__main__":
    main = int(input("Program built with which AI do you prefer: \n 1. Grok AI\n 2. Gemini AI\n 3. Windsurf AI\n ----------------------------------------\n"))
    print("----------------------------------------")
    drive = input("Enter the local disk letter (e.g., C, D, or for Linux/macOS, a path like home): ").strip()
   
    if main == 1:
        grok_main(drive)
    elif main == 2:
        gemini_main(drive)
    elif main == 3:
        windsurf_main(drive)
    else:
        print(f"The option you chose ({main}) is not available in the list of available modules")

