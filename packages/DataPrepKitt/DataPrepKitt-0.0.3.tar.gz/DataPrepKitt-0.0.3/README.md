# DataPrepKitt

DataPrepKitt is a Python package for data preprocessing tasks, including reading data from different file formats, summarizing datasets, handling missing values, and encoding categorical data.

## Installation

You can install DataPrepKitt using pip:

```python
pip install DataPrepKitt
```

## Example Usage:

```python
import pandas as pd
from DataPrepKitt.DataPrepKitt import DataPrepKit


# Initialize DataPrepKit object with file path
dataprep = DataPrepKit('path_to_your_dataset')

# Generate data summary
summary = dataprep.data_summary()
print(summary)
print('_______________________________')

# Handle missing values (e.g., remove rows with missing values)
handle_missing = dataprep.handle_missing_values(strategy='remove')
print(handle_missing)
print('_______________________________')

# Encode categorical data (automatically detect categorical columns)
encoded_data = dataprep.encode_categorical_data()
print(encoded_data)
print('_______________________________')

```
