# Disk Capacity Analyzer

A Python-based tool to analyze and visualize disk usage across different storage devices. Choose between multiple AI-powered analysis engines to get detailed insights into your disk space consumption.

## 🌟 Features

- **Multiple Analysis Engines**: Choose from different AI-powered analyzers (Grok AI, Gemini AI, Windsurf AI)
- **Cross-Platform**: Works on Windows, macOS, and Linux
- **Detailed Reporting**: Get comprehensive disk usage reports
- **CSV Export**: Save analysis results for further processing
- **User-Friendly**: Simple command-line interface

## 📦 Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/RogueChocoholic/diskCapacityList.git
   cd diskCapacityList
   ```

2. Create and activate a virtual environment (recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: .\\venv\\Scripts\\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## 🚀 Usage

Run the main script and follow the interactive prompts:

```bash
python main.py
```

### Command Line Arguments

You can also run the analysis directly with command line arguments:

```bash
# Using Windsurf AI (default)
python -m modules.windsurf.main C

# Using Gemini AI
python -m modules.gemini.main D

# Using Grok AI
python -m modules.grok.main E
```

### Output

The tool will:
1. Scan the specified drive
2. Display the top 10 largest folders
3. Save a detailed CSV report with complete folder sizes

## 📊 Supported AI Engines

1. **Windsurf AI**
   - Advanced disk space analysis
   - Detailed folder size breakdown
   - Optimized for large drives

2. **Gemini AI**
   - Smart file categorization
   - Visual representation of disk usage
   - Quick scan mode available

3. **Grok AI**
   - Fast analysis
   - Minimal resource usage
   - Ideal for quick checks

## 📝 Output Format

The CSV report includes the following columns:
- `folder_path`: Full path to the folder
- `size_bytes`: Size in bytes
- `size_mb`: Size in megabytes
- `size_gb`: Size in gigabytes

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Built with Python 3.x
- Inspired by the need for better disk space management tools
- Thanks to all contributors who have helped improve this project

## 📧 Contact

For questions or feedback, please open an issue on GitHub.
