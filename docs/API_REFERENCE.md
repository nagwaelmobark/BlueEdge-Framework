# API Reference - BlueEdge Framework

## Overview
The BlueEdge Framework provides comprehensive data cleaning capabilities for mobile edge computing environments. This API reference covers all core functions, methods, and classes used in the framework.

## Table of Contents
- [Core Data Cleaning Functions](#core-data-cleaning-functions)
- [Mobile Edge Processing](#mobile-edge-processing)
- [Firebase Integration](#firebase-integration)
- [Performance Monitoring](#performance-monitoring)
- [Utility Functions](#utility-functions)

---

## Core Data Cleaning Functions

### `levenshtein_distance(string1, string2, substitution_cost=0.5)`

Calculates the Levenshtein edit distance between two strings with customizable substitution cost.

**Parameters:**
- `string1` (str): First string for comparison
- `string2` (str): Second string for comparison  
- `substitution_cost` (float, default=0.5): Cost of character substitution

**Returns:**
- `float`: Normalized Levenshtein distance (0.0 to 1.0)

**Example:**
```python
from blueedge.core import levenshtein_distance

# Basic usage
distance = levenshtein_distance("Mohammed", "Mohammad")
print(f"Distance: {distance}")  # Output: Distance: 0.125

# With custom substitution cost
distance = levenshtein_distance("Sara", "Sarah", substitution_cost=0.3)
print(f"Distance: {distance}")  # Output: Distance: 0.15
```

---

### `normalize_name(full_name, remove_honorifics=True)`

Normalizes names by removing honorifics, converting to lowercase, and cleaning special characters.

**Parameters:**
- `full_name` (str): Complete name string to normalize
- `remove_honorifics` (bool, default=True): Whether to remove honorific prefixes

**Returns:**
- `dict`: Dictionary containing normalized name components
  - `first_name` (str): Normalized first name
  - `middle_name` (str): Normalized middle name  
  - `last_name` (str): Normalized last name
  - `full_normalized` (str): Complete normalized name

**Example:**
```python
from blueedge.core import normalize_name

# Basic normalization
result = normalize_name("Dr. Ahmed Hassan Omar")
print(result)
# Output: {
#   'first_name': 'ahmed',
#   'middle_name': 'hassan', 
#   'last_name': 'omar',
#   'full_normalized': 'ahmed hassan omar'
# }

# Without removing honorifics
result = normalize_name("Prof. Mohammed Ali", remove_honorifics=False)
print(result)
# Output: {
#   'first_name': 'prof.',
#   'middle_name': 'mohammed',
#   'last_name': 'ali', 
#   'full_normalized': 'prof. mohammed ali'
# }
```

---

### `detect_duplicates(record, database, threshold=0.25)`

Detects duplicate records using fuzzy string matching with configurable similarity threshold.

**Parameters:**
- `record` (dict): Record to check for duplicates
  - Required keys: `first_name`, `middle_name`, `last_name`, `id_number`
- `database` (list): List of existing records to compare against
- `threshold` (float, default=0.25): Similarity threshold (0.0 to 1.0)

**Returns:**
- `dict`: Duplicate detection results
  - `is_duplicate` (bool): Whether duplicate was found
  - `duplicate_id` (str): ID of matching record (if found)
  - `similarity_score` (float): Highest similarity score
  - `matched_fields` (list): Fields that matched

**Example:**
```python
from blueedge.core import detect_duplicates

# Sample record
new_record = {
    'first_name': 'Mohammed',
    'middle_name': 'Ahmed', 
    'last_name': 'Hassan',
    'id_number': '12345'
}

# Sample database
existing_db = [
    {
        'id': '001',
        'first_name': 'Mohammad',
        'middle_name': 'Ahmad',
        'last_name': 'Hasan',
        'id_number': '12346'
    }
]

# Check for duplicates
result = detect_duplicates(new_record, existing_db)
print(result)
# Output: {
#   'is_duplicate': True,
#   'duplicate_id': '001',
#   'similarity_score': 0.89,
#   'matched_fields': ['first_name', 'middle_name', 'last_name']
# }
```

---

## Mobile Edge Processing

### `EdgeProcessor` Class

Main class for handling mobile edge data processing operations.

#### `__init__(memory_limit=5000, processing_timeout=1.0)`

Initialize EdgeProcessor with resource constraints.

**Parameters:**
- `memory_limit` (int, default=5000): Memory limit in bytes
- `processing_timeout` (float, default=1.0): Processing timeout in seconds

#### `process_batch(records, batch_size=1000)`

Process multiple records in batches to maintain performance.

**Parameters:**
- `records` (list): List of records to process
- `batch_size` (int, default=1000): Number of records per batch

**Returns:**
- `dict`: Processing results
  - `processed_count` (int): Number of successfully processed records
  - `error_count` (int): Number of records with errors
  - `processing_time` (float): Total processing time
  - `memory_used` (int): Peak memory usage in bytes

**Example:**
```python
from blueedge.edge import EdgeProcessor

# Initialize processor
processor = EdgeProcessor(memory_limit=5000, processing_timeout=1.0)

# Sample records
records = [
    {'first_name': 'Ahmed', 'middle_name': 'Hassan', 'last_name': 'Omar'},
    {'first_name': 'Sara', 'middle_name': 'Mohammed', 'last_name': 'Ali'},
    # ... more records
]

# Process batch
result = processor.process_batch(records, batch_size=500)
print(result)
# Output: {
#   'processed_count': 2,
#   'error_count': 0, 
#   'processing_time': 0.85,
#   'memory_used': 4200
# }
```

---

## Firebase Integration

### `FirebaseConnector` Class

Handles real-time database operations with Firebase.

#### `__init__(config_path=None, credentials=None)`

Initialize Firebase connection.

**Parameters:**
- `config_path` (str, optional): Path to Firebase config file
- `credentials` (dict, optional): Firebase credentials dictionary

#### `upload_cleaned_data(data, collection_name='cleaned_records')`

Upload cleaned data to Firebase real-time database.

**Parameters:**
- `data` (dict or list): Cleaned data to upload
- `collection_name` (str, default='cleaned_records'): Target collection name

**Returns:**
- `dict`: Upload status
  - `success` (bool): Whether upload succeeded
  - `record_id` (str): Generated record ID
  - `timestamp` (str): Upload timestamp

**Example:**
```python
from blueedge.firebase import FirebaseConnector

# Initialize connector
firebase = FirebaseConnector(config_path='firebase_config.json')

# Upload cleaned data
cleaned_record = {
    'first_name': 'ahmed',
    'middle_name': 'hassan',
    'last_name': 'omar',
    'email': 'ahmed.hassan@example.com',
    'cleaned_at': '2024-01-15T10:30:00Z'
}

result = firebase.upload_cleaned_data(cleaned_record)
print(result)
# Output: {
#   'success': True,
#   'record_id': 'rec_1234567890',
#   'timestamp': '2024-01-15T10:30:15Z'
# }
```

---

## Performance Monitoring

### `PerformanceMonitor` Class

Monitors and tracks system performance metrics.

#### `start_monitoring()`

Begin performance monitoring session.

#### `get_metrics()`

Retrieve current performance metrics.

**Returns:**
- `dict`: Performance metrics
  - `cpu_usage` (float): CPU usage percentage
  - `memory_usage` (int): Memory usage in bytes
  - `processing_speed` (float): Records processed per second
  - `accuracy_rate` (float): Current accuracy percentage

**Example:**
```python
from blueedge.monitor import PerformanceMonitor

# Initialize monitor
monitor = PerformanceMonitor()
monitor.start_monitoring()

# Process some data...
# ...

# Get metrics
metrics = monitor.get_metrics()
print(metrics)
# Output: {
#   'cpu_usage': 15.2,
#   'memory_usage': 4800,
#   'processing_speed': 1150.5,
#   'accuracy_rate': 87.3
# }
```

---

## Utility Functions

### `validate_input(data, schema)`

Validates input data against predefined schema.

**Parameters:**
- `data` (dict): Data to validate
- `schema` (dict): Validation schema

**Returns:**
- `dict`: Validation results
  - `is_valid` (bool): Whether data is valid
  - `errors` (list): List of validation errors

### `generate_report(processing_results, output_format='json')`

Generates processing report in specified format.

**Parameters:**
- `processing_results` (dict): Results from processing operations
- `output_format` (str, default='json'): Output format ('json', 'csv', 'excel')

**Returns:**
- `str`: Generated report content

---

## Error Handling

### Exception Classes

#### `BlueEdgeError`
Base exception class for BlueEdge framework.

#### `ProcessingTimeoutError`
Raised when processing exceeds timeout limit.

#### `MemoryLimitExceededError`
Raised when memory usage exceeds limit.

#### `FirebaseConnectionError`
Raised when Firebase connection fails.

**Example:**
```python
from blueedge.exceptions import ProcessingTimeoutError, MemoryLimitExceededError

try:
    processor = EdgeProcessor()
    result = processor.process_batch(large_dataset)
except ProcessingTimeoutError as e:
    print(f"Processing timeout: {e}")
except MemoryLimitExceededError as e:
    print(f"Memory limit exceeded: {e}")
```

---

## Configuration

### Environment Variables

- `BLUEEDGE_MEMORY_LIMIT`: Default memory limit (default: 5000)
- `BLUEEDGE_TIMEOUT`: Default processing timeout (default: 1.0)
- `FIREBASE_CONFIG_PATH`: Path to Firebase configuration
- `BLUEEDGE_LOG_LEVEL`: Logging level (DEBUG, INFO, WARNING, ERROR)

### Configuration File Example

```json
{
    "processing": {
        "memory_limit": 5000,
        "timeout": 1.0,
        "batch_size": 1000
    },
    "similarity": {
        "threshold": 0.25,
        "substitution_cost": 0.5
    },
    "firebase": {
        "database_url": "your-database-url",
        "storage_bucket": "your-storage-bucket"
    }
}
```

---

## Installation and Setup

### Dependencies

```bash
# Core dependencies
pip install nltk pandas numpy

# Mobile app dependencies  
pip install kivy kivymd

# Firebase integration
pip install firebase-admin

# Additional utilities
pip install python-dotenv requests
```

### Quick Start

```python
# 1. Import the framework
from blueedge import BlueEdge

# 2. Initialize the processor
processor = BlueEdge(
    memory_limit=5000,
    threshold=0.25
)

# 3. Process your data
data = [
    {'first_name': 'Mohammed', 'last_name': 'Ahmed'},
    {'first_name': 'Mohammad', 'last_name': 'Ahmad'}
]

results = processor.clean_data(data)
print(results)
```

---

## Advanced Usage

### Custom Similarity Functions

```python
from blueedge.core import register_similarity_function

def custom_phonetic_similarity(str1, str2):
    """Custom phonetic similarity function"""
    # Your custom logic here
    return similarity_score

# Register your custom function
register_similarity_function('phonetic', custom_phonetic_similarity)

# Use in processing
processor = BlueEdge(similarity_function='phonetic')
```

### Batch Processing with Progress Tracking

```python
from blueedge.edge import EdgeProcessor
from blueedge.monitor import ProgressTracker

processor = EdgeProcessor()
tracker = ProgressTracker()

def process_with_progress(data_batches):
    tracker.start(total_batches=len(data_batches))
    
    results = []
    for i, batch in enumerate(data_batches):
        result = processor.process_batch(batch)
        results.append(result)
        
        tracker.update(i + 1)
        print(f"Progress: {tracker.get_percentage():.1f}%")
    
    tracker.finish()
    return results
```

---

## Version Information

- **Framework Version**: 1.0.0
- **API Version**: v1
- **Last Updated**: January 2025
- **Python Requirements**: >= 3.7
- **Dependencies**: NLTK, KIVY, Firebase SDK, Pandas

---

## Support and Resources

### Documentation Links
- **User Guide**: [USER_GUIDE.md](USER_GUIDE.md)
- **Architecture**: [ARCHITECTURE.md](ARCHITECTURE.md)
- **Performance Analysis**: [PERFORMANCE.md](PERFORMANCE.md)
- **Installation Guide**: [INSTALLATION.md](INSTALLATION.md)

### Community and Support
- **GitHub Repository**: [BlueEdge-Framework](https://github.com/username/BlueEdge-Framework)
- **Issues and Bug Reports**: [GitHub Issues](https://github.com/username/BlueEdge-Framework/issues)
- **Discussions**: [GitHub Discussions](https://github.com/username/BlueEdge-Framework/discussions)
- **Research Paper**: [BlueEdge Research Paper](link-to-paper)

### Contributing
- **Contributing Guide**: [CONTRIBUTING.md](CONTRIBUTING.md)
- **Code of Conduct**: [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md)
- **Development Setup**: See [docs/development.md](docs/development.md)

---

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Citation

If you use BlueEdge in your research, please cite:

```bibtex
@article{blueedge2024,
    title={BlueEdge: A Mobile Edge Computing Framework for Intelligent Data Cleaning},
    author={[Authors]},
    journal={[Journal]},
    year={2024},
    volume={[Volume]},
    pages={[Pages]}
}
``` 
