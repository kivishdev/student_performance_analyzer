import os
import sys
from datetime import datetime
from modules.data_extractor import read_data
from modules.gemini_analyzer import analyze_student_data, generate_comparative_analysis
from modules.report_generator import save_analysis_report

def display_banner():
    """Display application banner with version info."""
    print("\n" + "="*60)
    print("    Student Performance Analyzer with GenAI")
    print("    Version 2.0 - Research Edition")
    print("="*60)

def setup_directories():
    """Create necessary directories for the application."""
    directories = ['data', 'outputs', 'outputs/reports', 'outputs/logs']
    for directory in directories:
        if not os.path.exists(directory):
            os.makedirs(directory)
            print(f"✓ Created '{directory}' directory")

def get_user_input():
    """Get and validate user input for file selection."""
    print("\n" + "-"*60)
    print("INSTRUCTIONS")
    print("-"*60)
    print("1. Place your data file in the 'data' folder")
    print("2. Supported formats: .xlsx, .xls, .csv, .txt")
    print("3. Enter the filename below (e.g., 'grades.xlsx')")
    print("-"*60)
    
    while True:
        file_name = input("\n📁 Enter filename (or 'q' to quit): ").strip()
        
        if file_name.lower() == 'q':
            print("\n👋 Exiting application...")
            sys.exit(0)
        
        if not file_name:
            print("❌ Filename cannot be empty. Please try again.")
            continue
            
        file_path = os.path.join('data', file_name)
        
        if os.path.exists(file_path):
            return file_path, file_name
        else:
            print(f"❌ File not found: {file_name}")
            print("   Please check the filename and try again.")
            
            # Show available files in data folder
            if os.path.exists('data'):
                files = [f for f in os.listdir('data') if not f.startswith('.')]
                if files:
                    print("\n   Available files in 'data' folder:")
                    for f in files:
                        print(f"   - {f}")

def log_analysis(file_name, success=True, error_msg=None):
    """Log analysis attempts to a log file."""
    log_path = os.path.join('outputs', 'logs', 'analysis_log.txt')
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    status = "SUCCESS" if success else "FAILED"
    
    with open(log_path, 'a', encoding='utf-8') as log_file:
        log_entry = f"[{timestamp}] {status} - File: {file_name}"
        if error_msg:
            log_entry += f" - Error: {error_msg}"
        log_file.write(log_entry + "\n")

def display_analysis_options():
    """Display available analysis options."""
    print("\n" + "-"*60)
    print("ANALYSIS OPTIONS")
    print("-"*60)
    print("1. Standard Analysis (Individual student performance)")
    print("2. Comparative Analysis (Class-wide insights & statistics)")
    print("3. Both (Recommended for comprehensive research)")
    print("-"*60)
    
    while True:
        choice = input("\n📊 Select analysis type (1-3): ").strip()
        if choice in ['1', '2', '3']:
            return int(choice)
        print("❌ Invalid choice. Please enter 1, 2, or 3.")

def main():
    """Main application function."""
    try:
        # Display banner
        display_banner()
        
        # Setup directories
        setup_directories()
        
        # Get file input
        file_path, file_name = get_user_input()
        
        # Read data
        print(f"\n📖 Reading data from '{file_name}'...")
        student_data = read_data(file_path)
        
        if student_data is None:
            log_analysis(file_name, success=False, error_msg="Data reading failed")
            print("\n❌ Analysis stopped: Unable to read data")
            return
        
        print("✓ Data loaded successfully")
        
        # Get analysis type preference
        analysis_choice = display_analysis_options()
        
        # Perform analysis
        print("\n🤖 Analyzing data with AI...")
        print("   This may take a moment. Please wait...\n")
        
        results = {}
        
        # Standard analysis
        if analysis_choice in [1, 3]:
            print("⏳ Performing individual student analysis...")
            standard_analysis = analyze_student_data(student_data)
            results['standard'] = standard_analysis
            print("✓ Individual analysis complete")
        
        # Comparative analysis
        if analysis_choice in [2, 3]:
            print("⏳ Performing comparative class analysis...")
            comparative_analysis = generate_comparative_analysis(student_data)
            results['comparative'] = comparative_analysis
            print("✓ Comparative analysis complete")
        
        # Display results
        print("\n" + "="*60)
        print("           AI ANALYSIS RESULTS")
        print("="*60)
        
        if 'standard' in results:
            print("\n📊 INDIVIDUAL STUDENT ANALYSIS")
            print("-"*60)
            print(results['standard'])
        
        if 'comparative' in results:
            print("\n📈 COMPARATIVE CLASS ANALYSIS")
            print("-"*60)
            print(results['comparative'])
        
        print("\n" + "="*60)
        
        # Save report
        save_choice = input("\n💾 Save analysis report? (y/n): ").strip().lower()
        if save_choice == 'y':
            report_path = save_analysis_report(file_name, results)
            print(f"✓ Report saved: {report_path}")
            log_analysis(file_name, success=True)
        else:
            log_analysis(file_name, success=True)
        
        print("\n✨ Analysis complete! Thank you for using the system.\n")
        
    except KeyboardInterrupt:
        print("\n\n⚠️  Analysis interrupted by user.")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ An unexpected error occurred: {e}")
        log_analysis(file_name if 'file_name' in locals() else "Unknown", 
                    success=False, error_msg=str(e))
        sys.exit(1)

if __name__ == "__main__":
    main()