# Student Performance Analyzer with GenAI

## Research Project Overview

An AI-powered system for analyzing student performance data using Google's Gemini AI. This tool provides comprehensive individual and comparative analyses suitable for educational research.

## Features

### Core Capabilities
- ✅ **Multi-format Support**: CSV, Excel (.xlsx, .xls), and TXT files
- ✅ **Individual Analysis**: Detailed performance review for each student
- ✅ **Comparative Analysis**: Class-wide insights and statistical patterns
- ✅ **Report Generation**: Professional formatted reports with timestamps
- ✅ **Activity Logging**: Track all analysis sessions
- ✅ **Error Handling**: Robust error management and retry logic

### Research-Ready Features
- Statistical summaries and insights
- Pattern identification and trend analysis
- Evidence-based recommendations
- Professional academic language
- Exportable reports for research documentation

## Project Structure

```
project/
├── main.py                      # Main application entry point
├── modules/
│   ├── data_extractor.py        # Data reading and validation
│   ├── gemini_analyzer.py       # AI analysis engine
│   └── report_generator.py      # Report creation and export
├── data/                        # Input data files (user-created)
├── outputs/
│   ├── reports/                 # Generated analysis reports
│   └── logs/                    # Activity logs
├── .env                         # API keys (create this)
├── requirements.txt             # Python dependencies
└── README.md                    # This file
```

## Installation

### 1. Clone or Download the Project

```bash
git clone <your-repository-url>
cd student-performance-analyzer
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Set Up API Key

Create a `.env` file in the project root:

```plaintext
GOOGLE_API_KEY=your_gemini_api_key_here
```

**How to get a Gemini API key:**
1. Visit [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Sign in with your Google account
3. Click "Create API Key"
4. Copy the key to your `.env` file

## Usage

### Basic Usage

1. **Place your data file** in the `data/` folder
   - Supported formats: `.csv`, `.xlsx`, `.xls`, `.txt`
   - Example: `grades.xlsx`, `student_data.csv`

2. **Run the application**
   ```bash
   python main.py
   ```

3. **Follow the prompts**
   - Enter your filename when prompted
   - Choose analysis type (individual, comparative, or both)
   - Optionally save the report

### Example Data Format

#### For CSV/Excel Files:
```csv
student_name,math_score,science_score,english_score,attendance
John Doe,85,78,92,95
Jane Smith,92,88,85,98
Bob Johnson,76,82,79,88
```

#### For Text Files:
Any plain text content (essays, reports, assignments, etc.)

## Analysis Types

### 1. Individual Student Analysis
- Performance summary for each student
- Identification of strengths
- Constructive improvement suggestions
- Overall assessment

### 2. Comparative Class Analysis
- Class-wide performance trends
- Statistical insights (mean, median, standard deviation)
- Performance distribution patterns
- Correlations between different metrics
- Research-oriented findings

### 3. Combined Analysis (Recommended)
- Both individual and comparative analyses
- Comprehensive research documentation

## Output Examples

### Console Output
```
=============================================
    Student Performance Analyzer with GenAI
    Version 2.0 - Research Edition
=============================================

✓ Created 'outputs' directory
✓ Data loaded successfully

⏳ Performing individual student analysis...
✓ Individual analysis complete

=============================================
           AI ANALYSIS RESULTS
=============================================

📊 INDIVIDUAL STUDENT ANALYSIS
------------------------------------------------------------
[AI-generated analysis appears here]
```

### Generated Report
Reports are saved in `outputs/reports/` with format:
```
report_[filename]_[timestamp].txt
```

Example: `report_grades_20241012_143052.txt`

## Research Applications

This tool is suitable for:

- **Educational Research**: Analyze student performance patterns
- **Intervention Planning**: Identify students needing support
- **Curriculum Development**: Understand learning outcomes
- **Statistical Analysis**: Generate data for research papers
- **Longitudinal Studies**: Track performance over time
- **Comparative Studies**: Compare different classes or cohorts

## Configuration

### Gemini Model Settings

In `gemini_analyzer.py`, you can adjust:

```python
generation_config={
    'temperature': 0.7,      # Creativity (0.0-1.0)
    'top_p': 0.95,          # Nucleus sampling
    'top_k': 40,            # Top-k sampling
    'max_output_tokens': 2048,  # Response length
}
```

### Data Limits

- **CSV/Excel**: Up to 100 rows displayed (all analyzed)
- **Text files**: Up to 8000 characters analyzed
- **API retries**: 3 attempts with 2-second delays

## Troubleshooting

### Common Issues

#### 1. "GOOGLE_API_KEY not found"
**Solution**: Create a `.env` file with your API key

#### 2. "openpyxl library not found"
**Solution**: 
```bash
pip install openpyxl
```

#### 3. "File not found"
**Solution**: 
- Check file is in `data/` folder
- Verify exact filename (case-sensitive)
- Check file extension

#### 4. "API request failed"
**Solution**:
- Verify API key is valid
- Check internet connection
- Ensure you have API quota remaining

#### 5. Unicode/Encoding errors
**Solution**: The tool automatically tries multiple encodings (utf-8, latin-1, iso-8859-1, cp1252)

## Best Practices for Research

### Data Preparation
1. **Clean your data**: Remove extra spaces, standardize column names
2. **Use clear headers**: E.g., `student_name`, `math_score`, `attendance`
3. **Include sufficient data**: At least 10-20 students for meaningful patterns
4. **Document metadata**: Keep track of data collection dates and methods

### Analysis Workflow
1. Start with comparative analysis for overview
2. Follow up with individual analysis for details
3. Save all reports for documentation
4. Review logs for analysis history
5. Export multiple analyses for comparison

### Report Usage
- Include in research documentation
- Attach to IRB submissions
- Share with stakeholders
- Archive for longitudinal studies

## Advanced Features

### Custom Prompts
Modify prompts in `gemini_analyzer.py` to:
- Focus on specific metrics
- Add custom evaluation criteria
- Adjust analysis depth
- Include domain-specific terminology

### Batch Processing
Process multiple files by modifying `main.py`:
```python
for file_name in os.listdir('data'):
    # Your processing code
```

### Data Validation
Add custom validation in `data_extractor.py`:
```python
def validate_student_data(df):
    # Your validation logic
```

## Privacy & Ethics

### Important Considerations
- **Anonymize data**: Remove identifying information before analysis
- **Secure storage**: Keep API keys and data files secure
- **Informed consent**: Ensure appropriate permissions for data use
- **Data retention**: Follow institutional policies on data storage
- **Bias awareness**: AI analysis may reflect training data biases

### Compliance
- FERPA compliance for US educational data
- GDPR compliance for EU student data
- Local data protection regulations
- Institutional review board (IRB) requirements

## Limitations

1. **AI Interpretation**: Gemini's analysis is based on patterns, not pedagogical expertise
2. **Context**: AI may miss cultural or institutional context
3. **Quantitative Focus**: Best with numerical data; qualitative analysis is limited
4. **API Dependency**: Requires internet connection and valid API key
5. **Token Limits**: Very large datasets may need truncation

## Future Enhancements

Potential improvements for future versions:
- [ ] Data visualization with charts and graphs
- [ ] Multi-file batch processing
- [ ] Custom report templates
- [ ] Integration with learning management systems
- [ ] Export to PDF, HTML, or Word formats
- [ ] Advanced statistical analysis
- [ ] Predictive modeling capabilities
- [ ] Web-based interface

## Contributing

For research collaborations or contributions:
1. Fork the repository
2. Create a feature branch
3. Test thoroughly
4. Submit pull request with documentation

## Citation

If using this tool in research, please cite:
```
[Your Name]. (2024). Student Performance Analyzer with GenAI. 
Version 2.0. [Repository URL]
```

## License

[Specify your license here - MIT, GPL, etc.]

## Support

For issues, questions, or collaboration:
- Check the documentation
- Review troubleshooting section
- Open an issue on GitHub
- Contact: [your-email@example.com]

## Acknowledgments

- Built with Google Gemini AI
- Powered by Python and pandas
- Designed for educational research

## Version History

### Version 2.0 (Research Edition)
- Enhanced error handling and logging
- Comparative analysis feature
- Report generation system
- Improved prompts for research quality
- Statistical summaries
- Activity logging

### Version 1.0 (Initial Release)
- Basic individual student analysis
- Multi-format file support
- Gemini AI integration

---

**Happy Researching! 🎓📊**