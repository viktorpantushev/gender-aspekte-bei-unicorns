# 🦄 Gender Aspects in Unicorn Startups

## 📊 A Data-Driven Analysis of Founder Gender Representation in Global Unicorn Companies

### 🎯 Overview

Unicorn startups are privately held companies valued at more than one billion US dollars. These companies play a crucial role in innovation, entrepreneurship, and economic growth worldwide.

This project investigates gender representation among unicorn startup founders. Using publicly available data, we analyze how founder gender is distributed across countries, industries, sectors, and company valuations. The project combines web scraping, data cleaning, gender classification, and interactive data visualization to identify potential gender disparities within the global startup ecosystem.

---

## ❓ Research Question

**To what extent are women represented among founders of unicorn startups, and how does gender distribution vary across countries, industries, sectors, and startup valuations?**

---

## 🔬 Methodology

The analysis follows a multi-stage workflow:

1. 🌐 Data collection from public sources
2. 🧹 Data cleaning and preprocessing
3. 👥 Founder gender classification
4. 📈 Statistical analysis
5. 📊 Interactive visualization
6. 🖥️ Dashboard generation

### Workflow

```text
Wikipedia
    ↓
Data Scraping
    ↓
Data Cleaning
    ↓
Gender Classification
    ↓
Country Analysis
Industry Analysis
Valuation Analysis
    ↓
Interactive Visualizations
    ↓
HTML Dashboard
```

---

## 🌐 Data Collection

The project collects unicorn startup data from publicly available Wikipedia tables.

The script `scrape_wiki.py` uses:

* Requests
* BeautifulSoup
* Pandas

to extract structured information about unicorn companies and their founders. The extracted data is converted into CSV files for further processing and analysis.

---

## 🧹 Data Cleaning and Preparation

The notebook `scrape_and_clean.ipynb` performs the preprocessing of the collected data.

This includes:

* Cleaning founder names
* Standardizing column names
* Handling missing values
* Preparing datasets for gender classification
* Transforming and organizing relevant variables

The cleaned datasets form the basis for all subsequent analyses and visualizations.

---

## 👥 Gender Classification

Founder gender is determined using a multi-step classification approach.

### Step 1 – Name-Based Prediction

The project first uses the `gender_guesser` library to predict gender from first names.

### Step 2 – Indian Name Support

To improve classification accuracy for international founders, the project additionally uses the `guess_indian_gender` model.

### Step 3 – Public Biography Verification

For ambiguous cases, additional information is retrieved from:

* Wikidata
* Wikipedia
* Google Search snippets

The final classifications are normalized into three categories:

* Male
* Female
* Unknown

To reduce the risk of misclassification, uncertain cases are assigned to the category **Unknown**.

---

## 📈 Analyses Performed

The project investigates several dimensions of gender representation among unicorn founders.

### 🌍 Country Analysis

* Distribution of founders by gender across countries
* Comparison of male and female founder representation

### 🏭 Industry Analysis

* Gender distribution across unicorn industries
* Comparison of founder representation within industries

### 📂 Sector Analysis

* Gender distribution among major unicorn sectors
* Relative importance of different industries

### 💰 Valuation Analysis

* Gender representation across unicorn exit valuations
* Comparison between company valuation categories

---

## 📋 Dataset Summary

After the gender classification process, the analyzed dataset contained:

| Gender  | Count |
| ------- | ----- |
| Male    | 305   |
| Female  | 23    |
| Unknown | 88    |

The results indicate a substantial gender imbalance among unicorn founders, with male founders representing the majority of identified individuals.

---

## 📊 Visualizations

The project generates multiple interactive visualizations, including:

* 🌍 Gender distribution by country
* 🏭 Gender distribution by industry
* 📂 Gender distribution by sector
* 👥 Founder counts by gender
* 💰 Unicorn valuation analysis
* 📈 Sector comparison charts

All visualizations are exported as interactive HTML files.

---

## 🖥️ Interactive Dashboard

The script `build_webpage.py` automatically combines all generated visualizations into a single responsive HTML dashboard.

The dashboard provides:

* Interactive charts
* Zoom and navigation tools
* Hover information
* Export functionality

This enables users to explore the results in an intuitive and user-friendly way.

---

## 📁 Project Structure

```text
gender-aspekte-bei-unicorns/
│
├── graph_generation/
├── old/
├── src/
│   ├── scrape_wiki.py
│   ├── get_gender_data.py
│   ├── ai_graph_countries_gender.py
│   ├── ai_graph_exit_values_gender.py
│   ├── ai_graph_sectors_gender.py
│   ├── ai_plot_countries_gender_counts.py
│   ├── ai_plot_industry_unicorns.py
│   └── build_webpage.py
│
├── scrape_and_clean.ipynb
└── README.md
```

---

## 🛠️ Technologies Used

* Python
* Pandas
* Requests
* BeautifulSoup
* Jupyter Notebook
* gender_guesser
* guess_indian_gender
* HTML
* Data Visualization Libraries

---

## 🚀 How to Run the Project

1. Clone the repository.
2. Install the required Python packages.
3. Run `scrape_wiki.py` to collect the unicorn data.
4. Execute `scrape_and_clean.ipynb` to clean and prepare the dataset.
5. Run the visualization scripts in the `src` directory.
6. Execute `build_webpage.py` to generate the final interactive dashboard.

---

## 📦 Output

The project produces:

* Cleaned CSV datasets
* Gender classification results
* Interactive HTML visualizations
* A complete dashboard (`index.html`)

---

## ⚠️ Limitations

The gender classification process relies on names and publicly available information. Consequently, some founders cannot be classified with sufficient confidence and remain categorized as **Unknown**.

Furthermore, gender cannot always be accurately inferred from names alone. Therefore, the results should be interpreted as estimates rather than definitive classifications.

---

## 🎓 Academic Context

This project was developed as part of a university group project at **Technische Hochschule Nürnberg**.

The objective was to investigate gender representation among founders of unicorn startups through the application of web scraping, data preprocessing, gender classification, statistical analysis, and interactive data visualization techniques.
