# 🤝 Contributing to Truth Scanner Pro

Thank you for your interest in contributing to Truth Scanner Pro! This document provides guidelines for contributing to the project.

---

## 📋 Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [Development Process](#development-process)
- [Pull Request Process](#pull-request-process)
- [Coding Standards](#coding-standards)
- [Testing Guidelines](#testing-guidelines)
- [Documentation](#documentation)

---

## Code of Conduct

### Our Pledge
We are committed to providing a welcoming and inspiring community for all. Please be respectful and constructive in your interactions.

### Expected Behavior
- Use welcoming and inclusive language
- Be respectful of differing viewpoints
- Gracefully accept constructive criticism
- Focus on what is best for the community
- Show empathy towards other community members

---

## Getting Started

### 1. Fork the Repository
```bash
# Click the "Fork" button on GitHub
# Clone your fork
git clone https://github.com/YOUR_USERNAME/Truth_Scanner.git
cd Truth_Scanner
```

### 2. Set Up Development Environment
```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Install development dependencies
pip install pytest black flake8 mypy
```

### 3. Create a Branch
```bash
git checkout -b feature/your-feature-name
# or
git checkout -b fix/your-bug-fix
```

---

## Development Process

### Branch Naming
- Features: `feature/feature-name`
- Bug fixes: `fix/bug-description`
- Documentation: `docs/what-changed`
- Refactoring: `refactor/what-changed`

### Commit Messages
Write clear, descriptive commit messages:

```bash
# Good
git commit -m "Add confidence threshold configuration option"
git commit -m "Fix rate limiting bug in API endpoint"
git commit -m "Update README with Docker instructions"

# Bad
git commit -m "Update"
git commit -m "Fix bug"
git commit -m "Changes"
```

#### Commit Message Format
```
<type>: <subject>

<body (optional)>

<footer (optional)>
```

**Types:**
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes (formatting)
- `refactor`: Code refactoring
- `test`: Adding or updating tests
- `chore`: Maintenance tasks

**Example:**
```
feat: Add multi-language support for text analysis

- Implement language detection
- Add translation layer for UI
- Update documentation

Closes #123
```

---

## Pull Request Process

### Before Submitting

1. **Update Documentation**
   - Update README if needed
   - Add docstrings to new functions
   - Update API documentation

2. **Run Tests**
   ```bash
   python -m pytest tests/
   ```

3. **Check Code Style**
   ```bash
   black backend/ frontend/
   flake8 backend/
   ```

4. **Update CHANGELOG** (if applicable)

### Submitting PR

1. **Push to Your Fork**
   ```bash
   git push origin feature/your-feature-name
   ```

2. **Create Pull Request**
   - Go to the original repository
   - Click "New Pull Request"
   - Select your branch
   - Fill in the PR template

3. **PR Title Format**
   ```
   [Type] Brief description of changes
   ```
   Examples:
   - `[Feature] Add export to PDF functionality`
   - `[Fix] Resolve database connection timeout`
   - `[Docs] Update API examples`

4. **PR Description Template**
   ```markdown
   ## Description
   Brief description of changes

   ## Type of Change
   - [ ] Bug fix
   - [ ] New feature
   - [ ] Breaking change
   - [ ] Documentation update

   ## Testing
   - [ ] All tests pass
   - [ ] Added new tests
   - [ ] Manual testing completed

   ## Checklist
   - [ ] Code follows style guidelines
   - [ ] Self-review completed
   - [ ] Documentation updated
   - [ ] No new warnings

   ## Related Issues
   Closes #issue_number
   ```

---

## Coding Standards

### Python Code Style

Follow [PEP 8](https://www.python.org/dev/peps/pep-0008/) guidelines.

#### Use Black for Formatting
```bash
black backend/ --line-length 88
```

#### Use Type Hints
```python
def analyze_text(text: str) -> Dict[str, Any]:
    """
    Analyze text for confidence indicators.
    
    Args:
        text: The text to analyze
        
    Returns:
        Dictionary containing analysis results
    """
    pass
```

#### Docstring Format
Use Google-style docstrings:

```python
def function_name(param1: str, param2: int) -> bool:
    """
    Brief description of function.
    
    Detailed description if needed.
    
    Args:
        param1: Description of param1
        param2: Description of param2
        
    Returns:
        Description of return value
        
    Raises:
        ValueError: When param1 is empty
        
    Example:
        >>> function_name("test", 42)
        True
    """
    pass
```

### Frontend Code Style

#### JavaScript
- Use ES6+ syntax
- Use `const` and `let` (not `var`)
- Use arrow functions
- Add comments for complex logic

```javascript
// Good
const analyzeText = async (text) => {
    const response = await fetch('/api/analyze', {
        method: 'POST',
        body: JSON.stringify({ text })
    });
    return response.json();
};

// Bad
var analyzeText = function(text) {
    // Old-style function
};
```

#### CSS
- Use meaningful class names
- Follow BEM naming convention
- Keep selectors simple
- Add comments for sections

---

## Testing Guidelines

### Writing Tests

1. **Test File Naming**
   - `test_*.py` for test files
   - Match the module being tested

2. **Test Function Naming**
   ```python
   def test_feature_behavior():
       """Test that feature behaves correctly"""
       pass
   ```

3. **Test Structure**
   ```python
   def test_something():
       # Arrange
       scanner = TruthScanner()
       text = "Test text"
       
       # Act
       result = scanner.analyze(text)
       
       # Assert
       assert result['score'] > 0
   ```

4. **Coverage**
   - Aim for >80% code coverage
   - Test edge cases
   - Test error conditions

### Running Tests

```bash
# Run all tests
python -m pytest tests/

# Run specific test file
python -m pytest tests/test_scanner.py

# Run with coverage
python -m pytest --cov=backend tests/

# Run with verbose output
python -m pytest -v tests/
```

---

## Documentation

### Code Documentation

1. **Module Docstrings**
   ```python
   """
   Module Name - Brief Description
   
   Detailed description of module purpose.
   """
   ```

2. **Class Docstrings**
   ```python
   class TruthScanner:
       """
       Main scanner class for text analysis.
       
       This class provides methods for analyzing text
       and detecting confidence indicators.
       """
   ```

3. **Function Docstrings**
   - Always include for public functions
   - Include Args, Returns, Raises
   - Add examples for complex functions

### Documentation Files

- Update README.md for major changes
- Update API_EXAMPLES.md for API changes
- Update SETUP.md for installation changes
- Add to docs/ for detailed guides

---

## Development Tips

### Setting Up IDE

#### VS Code
Recommended extensions:
- Python
- Pylance
- Black Formatter
- GitLens

#### PyCharm
- Configure Black as external tool
- Enable PEP 8 inspection
- Set up pytest as test runner

### Debugging

```python
# Use debugger
import pdb; pdb.set_trace()

# Or use logging
import logging
logging.debug("Debug message")
```

### Common Issues

1. **Import Errors**
   - Ensure virtual environment is activated
   - Check PYTHONPATH

2. **Test Failures**
   - Run individual test first
   - Check test database state
   - Review logs

---

## Review Process

### What We Look For

- ✅ Code quality and readability
- ✅ Test coverage
- ✅ Documentation updates
- ✅ Performance considerations
- ✅ Security implications
- ✅ Backward compatibility

### Response Time

- Initial review: Within 2-3 days
- Follow-up reviews: Within 1-2 days
- Merge: After approval from maintainer

---

## Recognition

Contributors will be:
- Listed in CONTRIBUTORS.md
- Mentioned in release notes
- Thanked in documentation

---

## Questions?

- Open an issue for questions
- Join our discussions
- Contact maintainers

---

**Thank you for contributing to Truth Scanner Pro! 🙏**
