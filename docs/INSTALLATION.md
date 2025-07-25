# 🔧 BlueEdge Framework - Installation Guide

Complete step-by-step installation guide for the BlueEdge mobile edge data cleaning framework.

## 📋 Table of Contents

- [System Requirements](#-system-requirements)
- [Quick Installation](#-quick-installation)
- [Detailed Installation](#-detailed-installation)
- [Firebase Setup](#-firebase-setup)
- [Verification](#-verification)
- [Troubleshooting](#-troubleshooting)
- [Advanced Configuration](#-advanced-configuration)

## 🖥️ System Requirements

### Minimum Requirements

| Component | Requirement |
|-----------|-------------|
| **Operating System** | Windows 10+, macOS 10.14+, Ubuntu 18.04+ |
| **Python Version** | Python 3.8 or higher |
| **RAM** | 2GB available memory |
| **Storage** | 500MB free disk space |
| **Network** | Internet connection (optional for cloud features) |

### Recommended Requirements

| Component | Recommendation |
|-----------|----------------|
| **Operating System** | Windows 11, macOS 12+, Ubuntu 20.04+ |
| **Python Version** | Python 3.9+ |
| **RAM** | 4GB+ available memory |
| **Storage** | 1GB+ free disk space |
| **Network** | Broadband internet connection |

### Mobile Device Requirements

| Component | Requirement |
|-----------|-------------|
| **Platform** | Android 8.0+, iOS 12+ |
| **RAM** | 3GB+ available memory |
| **Storage** | 100MB free space |
| **Processor** | ARM64 or equivalent |

## ⚡ Quick Installation

### 1. Download and Extract

```bash
# Download the latest release
git clone https://github.com/your-username/blueedge-framework.git

# Navigate to project directory
cd blueedge-framework
```

### 2. Install Dependencies

```bash
# Install required packages
pip install -r requirements.txt
```

### 3. Run Application

```bash
# Start the enhanced mobile application
python blueedge_mobile_app.py
```

### 4. Verify Installation

```bash
# Test core functionality
python src/duplicate_detector.py
```

**Expected Output:**
```
✅ BlueEdge detector imported successfully
✅ Detector test passed - similarity: 0.94
🎉 BlueEdge Core ready!
```

## 🔨 Detailed Installation

### Step 1: Environment Setup

#### Windows

```powershell
# Check Python version
python --version

# Create virtual environment (recommended)
python -m venv blueedge-env

# Activate virtual environment
blueedge-env\Scripts\activate

# Upgrade pip
python -m pip install --upgrade pip
```

#### macOS/Linux

```bash
# Check Python version
python3 --version

# Create virtual environment (recommended)
python3 -m venv blueedge-env

# Activate virtual environment
source blueedge-env/bin/activate

# Upgrade pip
python -m pip install --upgrade pip
```

### Step 2: Download BlueEdge Framework

#### Option A: Git Clone (Recommended)

```bash
# Clone repository
git clone https://github.com/your-username/blueedge-framework.git

# Navigate to directory
cd blueedge-framework

# Check available branches
git branch -a
```

#### Option B: Download ZIP

1. Visit: https://github.com/your-username/blueedge-framework
2. Click "Code" → "Download ZIP"
3. Extract to desired location
4. Open terminal in extracted folder

### Step 3: Install Dependencies

#### Core Dependencies

```bash
# Install all required packages
pip install -r requirements.txt
```

#### Development Dependencies (Optional)

```bash
# Install development tools
pip install -r requirements-dev.txt
```

#### Manual Installation (if requirements.txt fails)

```bash
# Core framework
pip install kivy==2.3.1
pip install nltk==3.8.1
pip install python-Levenshtein==0.20.9

# Performance monitoring
pip install psutil==5.9.5

# Firebase integration
pip install requests==2.31.0
pip install firebase-admin==6.2.0

# Data processing
pip install pandas==2.0.3
pip install numpy==1.24.3

# Mobile development
pip install buildozer==1.5.0
pip install plyer==2.1.0
```

### Step 4: Download NLTK Data

```python
# Run this Python script once
import nltk
nltk.download('punkt')
nltk.download('stopwords')
print("✅ NLTK data downloaded successfully")
```

### Step 5: Project Structure Verification

After installation, your directory should look like:

```
📁 blueedge-framework/
├── 📄 README.md
├── 📄 requirements.txt
├── 📄 blueedge_mobile_app.py
├── 📄 performance_monitor.py
├── 📄 smart_cache.py
├── 📄 firebase_config.py
├── 📁 src/
│   ├── 📄 duplicate_detector.py
│   ├── 📄 similarity.py
│   └── 📄 data_anonymizer.py
├── 📁 data/
├── 📁 docs/
├── 📁 tests/
└── 📁 examples/
```

## 🔥 Firebase Setup

### 1. Create Firebase Project

1. **Visit Firebase Console**: https://console.firebase.google.com/
2. **Click**: "Create a project"
3. **Project Name**: `blueedge-framework`
4. **Enable**: Google Analytics (recommended)
5. **Click**: "Create project"

### 2. Setup Realtime Database

1. **Navigate**: Build → Realtime Database
2. **Click**: "Create Database"
3. **Select**: "Start in test mode"
4. **Choose**: Database location (us-central1 recommended)

### 3. Get Configuration Keys

#### Database URL:
- Copy the URL from Realtime Database dashboard
- Format: `https://blueedge-framework-xxxxx-default-rtdb.firebaseio.com/`

#### API Key:
1. **Go to**: Project Settings (⚙️ icon)
2. **Scroll to**: "Your apps" section
3. **Click**: Web app icon (`</>`)
4. **App name**: `BlueEdge-Web`
5. **Copy**: `apiKey` from configuration object

### 4. Configure BlueEdge

**Edit `firebase_config.py`:**

```python
def __init__(self):
    self.project_id = "your-project-id"  # Replace with your project ID
    self.database_url = "https://your-project-id-default-rtdb.firebaseio.com"  # Your database URL
    self.api_key = "your-api-key-here"  # Your API key
```

### 5. Test Firebase Connection

```bash
# Test Firebase connectivity
python firebase_config.py
```

**Expected Output:**
```
🔥 Firebase Config initialized for BlueEdge
🔗 Testing Firebase connection...
✅ Firebase connection successful!
✅ Firebase service ready for BlueEdge!
```

## ✅ Verification

### 1. Test Core Components

```bash
# Test duplicate detector
python src/duplicate_detector.py

# Test performance monitor
python performance_monitor.py

# Test smart cache
python smart_cache.py

# Test Firebase integration
python firebase_config.py
```

### 2. Run Full Application

```bash
# Start enhanced mobile application
python blueedge_mobile_app.py
```

**Expected Console Output:**
```
✅ KIVY imports successful
✅ BlueEdge detector imported successfully
✅ Firebase integration imported successfully
✅ Performance Monitor imported successfully
✅ Smart Cache imported successfully
🚀 Starting BlueEdge Enhanced Mobile Application...
✅ Performance monitoring enabled!
✅ Smart caching enabled!
✅ Firebase connected successfully!
🎉 BlueEdge Enhanced Mobile ready!
```

### 3. Test Application Features

1. **Mobile Interface**: Application window should open
2. **Smart Compare**: Enter two names and click "🚀 Smart Compare"
3. **Performance Dashboard**: Verify metrics are updating
4. **Quick Test**: Use "⚡ Quick Test" for sample data
5. **Cloud Sync**: Test "☁️ Sync" button (if Firebase configured)

## 🐛 Troubleshooting

### Common Issues

#### 1. Python Version Error

**Error**: `python: command not found`

**Solution**:
```bash
# Windows: Use 'py' instead of 'python'
py --version

# macOS/Linux: Use 'python3'
python3 --version
```

#### 2. Module Not Found Errors

**Error**: `ModuleNotFoundError: No module named 'kivy'`

**Solution**:
```bash
# Ensure virtual environment is activated
pip install --upgrade pip
pip install -r requirements.txt

# Or install manually:
pip install kivy[base]
```

#### 3. NLTK Data Missing

**Error**: `LookupError: Resource punkt not found`

**Solution**:
```python
import nltk
nltk.download('all')
```

#### 4. Firebase Connection Issues

**Error**: `Firebase connection failed: 404`

**Solutions**:
- Verify project ID and database URL
- Check internet connection
- Ensure database rules allow read/write
- Confirm API key is correct

#### 5. Kivy Import Errors

**Error**: `ImportError: DLL load failed while importing _window_sdl2`

**Solution**:
```bash
# Windows specific fix
pip uninstall kivy
pip install kivy[base]==2.3.1

# Alternative: Use conda
conda install kivy -c conda-forge
```

#### 6. Permission Errors

**Error**: `PermissionError: [Errno 13] Permission denied`

**Solution**:
```bash
# Use virtual environment
python -m venv blueedge-env
source blueedge-env/bin/activate  # Linux/Mac
# OR
blueedge-env\Scripts\activate     # Windows

pip install -r requirements.txt
```

### Performance Issues

#### Slow Application Startup

**Symptoms**: Application takes >10 seconds to start

**Solutions**:
1. **Disable unnecessary features**:
   ```python
   # In blueedge_mobile_app.py
   FIREBASE_AVAILABLE = False  # Disable Firebase temporarily
   ```

2. **Reduce cache size**:
   ```python
   # In smart_cache.py
   cache = SmartCache(max_size=20, max_memory_kb=10)
   ```

#### High Memory Usage

**Symptoms**: Application uses >200MB RAM

**Solutions**:
1. **Enable auto-cleanup**:
   ```python
   # Cleanup every 5 comparisons instead of 10
   if self.total_comparisons % 5 == 0:
       self._auto_cleanup()
   ```

2. **Reduce history size**:
   ```python
   # Keep fewer history items
   if len(self.results_history) > 5:
       self.results_history = self.results_history[:5]
   ```

### Network Issues

#### Offline Mode

If internet is not available:
- Application will work in offline mode
- Firebase features will be disabled
- Local caching and processing continue normally

#### Firewall Issues

If corporate firewall blocks Firebase:
```python
# Disable Firebase in firebase_config.py
FIREBASE_AVAILABLE = False
```

## 🔧 Advanced Configuration

### Environment Variables

Create `.env` file for configuration:

```bash
# .env file
FIREBASE_PROJECT_ID=your-project-id
FIREBASE_DATABASE_URL=https://your-project-default-rtdb.firebaseio.com
FIREBASE_API_KEY=your-api-key
BLUEEDGE_VERSION=1.0.0
DEBUG_MODE=False
CACHE_SIZE=50
CACHE_MEMORY_KB=25
PERFORMANCE_HISTORY=100
```

### Custom Configuration

**Edit configuration in each module:**

#### Performance Monitor
```python
# performance_monitor.py
self.thresholds = {
    'target_processing_ms': 800,    # Faster target
    'max_processing_ms': 1200,     # Stricter limit
    'estimated_memory_kb': 4000,   # Lower memory limit
    'min_cache_hit_rate': 0.8      # Higher cache requirement
}
```

#### Smart Cache
```python
# smart_cache.py
cache = SmartCache(
    max_size=100,        # More cache items
    max_memory_kb=50,    # More memory
    expire_hours=24      # Longer expiration
)
```

### Development Setup

```bash
# Install development dependencies
pip install pytest black flake8 mypy

# Setup pre-commit hooks (optional)
pip install pre-commit
pre-commit install

# Run tests
python -m pytest tests/

# Code formatting
black .

# Type checking
mypy blueedge_mobile_app.py
```

## 📱 Mobile Deployment

### Android APK Build

```bash
# Install buildozer
pip install buildozer

# Initialize buildozer
buildozer init

# Build APK
buildozer android debug

# Install on device
buildozer android deploy
```

### iOS Build (macOS only)

```bash
# Install kivy-ios
pip install kivy-ios

# Create iOS project
toolchain build python3 kivy

# Create Xcode project
toolchain create BlueEdge .
```

## 🆘 Support

### Getting Help

1. **Documentation**: Check all documentation in `docs/` folder
2. **Issues**: Create GitHub issue with details
3. **Discussions**: Join project discussions
4. **Examples**: Check `examples/` folder for sample code

### Bug Reports

Include this information:
- Operating system and version
- Python version
- Complete error message
- Steps to reproduce
- Expected vs actual behavior

### Feature Requests

Use GitHub issues with:
- Clear description of desired feature
- Use case explanation
- Potential implementation approach

---

🎉 **Installation Complete!** Your BlueEdge Framework is ready for mobile edge data cleaning.

**Next Steps**: [User Guide](USER_GUIDE.md) | [API Reference](API_REFERENCE.md) | [Performance Analysis](PERFORMANCE.md) 
