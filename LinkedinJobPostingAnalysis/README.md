# LinkedIn Job Posting Analysis

A comprehensive data science project analyzing LinkedIn job postings to uncover insights about job market trends, skill networks, and engagement patterns.

## Dataset Source

This analysis uses the **LinkedIn Job Postings (2023 - 2024)** dataset from Kaggle:

**Citation:**
> Arsh Koneru. (2024). LinkedIn Job Postings (2023 - 2024) [Data set]. Kaggle. https://doi.org/10.34740/KAGGLE/DSV/9200871

**Note:** The dataset files are not included in this repository due to size constraints. Please download the dataset from the Kaggle link above and place the files in the `archive/` directory to run the analysis.

## Project Overview

This project analyzes a large dataset of LinkedIn job postings to understand:
- Job market trends and patterns
- Skill co-occurrence networks and communities
- Job engagement metrics (views and applications)
- Salary distributions and compensation trends
- Sentiment analysis of job descriptions
- Industry and skill associations

## Dataset Structure

The project uses a structured dataset with the following components:

### Main Data Files
- **postings.csv** - Primary job postings data (123,849 records)
- **_sample_jobs.csv** - Sample subset for prototyping

### Supporting Data
- **Jobs Directory**
  - `job_skills.csv` - Job-skill mappings
  - `job_industries.csv` - Job-industry mappings  
  - `benefits.csv` - Job benefits data
  - `salaries.csv` - Salary information

- **Companies Directory**
  - `companies.csv` - Company information
  - `company_industries.csv` - Company-industry mappings
  - `company_specialities.csv` - Company specializations
  - `employee_counts.csv` - Company size data

- **Mappings Directory**
  - `industries.csv` - Industry name mappings
  - `skills.csv` - Skill name mappings

## Key Features

### 1. Data Processing & Validation
- Comprehensive schema validation and type coercion
- Missing data analysis and handling
- Data quality assessment with coverage metrics

### 2. Network Analysis
- **Bipartite Job-Skill Networks**: Connections between jobs and required skills
- **Skill Co-occurrence Networks**: How skills cluster together in job requirements
- **Community Detection**: Identifying skill communities using Louvain algorithm
- **Centrality Measures**: Degree, betweenness, and eigenvector centrality for skills

### 3. Engagement Analysis
- Job view and application metrics
- Skill-level engagement analysis
- Apply rate calculations and trends
- Performance metrics by skill type

### 4. Sentiment Analysis
- VADER sentiment analysis on job descriptions
- Correlation between sentiment and engagement
- Regression modeling of application rates

### 5. Association Mining
- Point-wise Mutual Information (PMI) for skill associations
- Jaccard similarity for skill co-occurrence
- Lift calculations for skill relationships

## Installation & Setup

### Prerequisites
- Python 3.7 or higher
- Jupyter Notebook

### Step 1: Clone the Repository
```bash
git clone https://github.com/yourusername/LinkedinJobPostingAnalysis.git
cd LinkedinJobPostingAnalysis
```

### Step 2: Install Dependencies
```bash
pip install pandas numpy networkx matplotlib nltk statsmodels
```

### Step 3: Download Required NLTK Data
```python
import nltk
nltk.download('vader_lexicon')
```

### Step 4: Download Dataset
1. Go to the [Kaggle dataset page](https://doi.org/10.34740/KAGGLE/DSV/9200871)
2. Download the dataset files
3. Extract and place all files in the `archive/` directory structure as shown above

## Usage

Run the main analysis notebook:

```bash
jupyter notebook analysis.ipynb
```

### Key Analysis Steps

1. **Data Loading & Validation**
   ```python
   # Load main dataset
   jobs = pd.read_csv("archive/postings.csv")
   
   # Validate schema and data quality
   missing_cols = expected_cols - set(jobs.columns)
   ```

2. **Feature Engineering**
   ```python
   # Create skill and industry lists per job
   skills_per_job = job_skills.groupby("job_id")["skill_name"].agg(lambda x: sorted(set(x.dropna())))
   
   # Calculate engagement metrics
   jobs2["apply_rate"] = jobs2["applies"] / jobs2["views"]
   ```

3. **Network Analysis**
   ```python
   # Build skill co-occurrence network
   S = nx.bipartite.weighted_projected_graph(B_js, skills_nodes)
   
   # Detect communities
   comms = nx.community.louvain_communities(S, weight="weight", seed=42)
   ```

4. **Sentiment Analysis**
   ```python
   # Apply VADER sentiment analysis
   sia = SentimentIntensityAnalyzer()
   jobs2["sentiment"] = jobs2["description"].apply(lambda x: sia.polarity_scores(x)["compound"])
   ```

## Key Findings

### Top Skills by Frequency
The most in-demand skills across job postings include:
- Information Technology
- Marketing  
- Customer Service
- Sales
- Project Management

### Skill Network Insights
- Skills form distinct communities (e.g., technical, business, creative)
- Strong associations between complementary skills
- Bridge skills that connect different domains

### Engagement Patterns
- Jobs with higher sentiment scores show different engagement patterns
- Certain skills correlate with higher application rates
- Salary and job views are significant predictors of applications

## Visualizations

The project generates several key visualizations:

1. **Skill Co-occurrence Network** - Shows how skills cluster together
2. **Bipartite Job-Skill Graph** - Relationships between jobs and skills
3. **Community Detection Plot** - Skill communities with engagement metrics
4. **Engagement Analysis Charts** - Apply rates by skill and sentiment

## Statistical Models

### Regression Analysis
- **OLS Regression**: `apply_rate ~ sentiment + normalized_salary + log_views`
- **Logistic Regression**: `any_apply ~ sentiment + normalized_salary + log_views`

### Network Metrics
- **Association Measures**: PMI, Jaccard similarity, Lift
- **Centrality Measures**: Degree, betweenness, eigenvector centrality
- **Community Detection**: Louvain algorithm with modularity optimization

## Data Quality Metrics

- **98.58%** of jobs have at least one skill link
- **98.84%** of jobs have at least one industry link
- Comprehensive coverage across salary, location, and company data

## Dependencies

```
pandas>=1.3.0
numpy>=1.21.0
networkx>=2.6.0
matplotlib>=3.4.0
nltk>=3.6.0
statsmodels>=0.12.0
```

## Project Structure

```
LinkedinJobPostingAnalysis/
├── analysis.ipynb          # Main analysis notebook
├── README.md              # Project documentation
├── .gitignore            # Git ignore file
└── archive/              # Dataset directory (not tracked)
    ├── postings.csv
    ├── _sample_jobs.csv
    ├── companies/
    │   ├── companies.csv
    │   ├── company_industries.csv
    │   ├── company_specialities.csv
    │   └── employee_counts.csv
    ├── jobs/
    │   ├── benefits.csv
    │   ├── job_industries.csv
    │   ├── job_skills.csv
    │   └── salaries.csv
    └── mappings/
        ├── industries.csv
        └── skills.csv
```

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/new-analysis`)
3. Commit your changes (`git commit -am 'Add new analysis'`)
4. Push to the branch (`git push origin feature/new-analysis`)
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Citation

If you use this analysis in your research, please cite both this repository and the original dataset:

```bibtex
@misc{linkedin_job_analysis,
  title={LinkedIn Job Posting Analysis: Network Analysis and Engagement Patterns},
  author={Your Name},
  year={2025},
  url={https://github.com/yourusername/LinkedinJobPostingAnalysis}
}

@misc{koneru2024linkedin,
  title={LinkedIn Job Postings (2023 - 2024)},
  author={Arsh Koneru},
  year={2024},
  publisher={Kaggle},
  url={https://doi.org/10.34740/KAGGLE/DSV/9200871}
}
```

## Contact

For questions or collaboration opportunities, please reach out through GitHub issues or email.
