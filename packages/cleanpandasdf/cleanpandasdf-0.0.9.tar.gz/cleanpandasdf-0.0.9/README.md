# CleanPandasDF

**CleanPandasDF** is a powerful Python package designed specifically for data scientists, analysts, and anyone working with data in pandas dataframes. It focuses on automating the data cleaning process, making it more efficient and error-free. From standardizing column names to optimizing memory usage, **CleanPandasDF** ensures your dataframes are clean, concise, and ready for analysis.

## Features

- **Automatic Column Renaming**: Transform column names into a consistent format, making them easier to work with in your analysis.
- **Remove Single Cardinality Columns**: Automatically identify and remove columns with only one unique value, reducing unnecessary data bulk.
- **Null Value Management**: Effortlessly remove rows or columns with high percentages of null values, and apply sophisticated imputation strategies for missing data.
- **Memory Optimization**: Reduce the memory footprint of your dataframes, enabling faster processing and analysis without compromising data integrity.
- **Data Quality Insights**: Generate reports highlighting potential issues within your data, including outliers, inconsistent data types, and more.
- **Outlier Detection & Handling**: Identify and manage outliers in your data, with options for removal, correction, or flagging for further investigation.

## Installation

Install **CleanPandasDF** directly from PyPI:

```bash
pip install cleanpandasdf
```

## Quick Start

Getting started with **CleanPandasDF** is easy. Here's how to clean your dataframe in just a few lines of code:

```python
import pandas as pd
import cleanpandasdf as cpd

# Load your dataframe
df = pd.read_csv('your_data.csv')

# Clean your dataframe with CleanPandasDF
cleaned_df = cpd.clean(df)

# Your dataframe is now clean and ready for analysis!
```


### Advanced Usage

**CleanPandasDF** offers a range of features for more detailed data cleaning and analysis needs. Here are some examples of advanced usage:

### Custom Column Renaming
You can apply custom rules for renaming columns according to your preferences.


```python
cleaned_df = cpd.clean(df, rename_strategy='custom', custom_rules={'oldName': 'newName'})
```

## License

**CleanPandasDF** is made available under the MIT License. This license allows you to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the software, subject to the conditions outlined in the LICENSE file.


## Contact

If you have any questions, feedback, or want to get involved with **CleanPandasDF**, don't hesitate to reach out.

Email: [sijopkd@gmail.com]

GitHub: [https://github.com/sijopkd]
