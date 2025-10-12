# Contributing to Shane Medical Content Empire

Thank you for your interest in contributing to the Shane Medical Content Empire! This document provides guidelines for contributing to the project.

## Code of Conduct

We are committed to providing a welcoming and inclusive environment. All contributors must:

- Be respectful and professional
- Accept constructive criticism gracefully
- Focus on what is best for the project and community
- Show empathy towards others

## How to Contribute

### Reporting Issues

Before creating an issue:
1. Check if the issue already exists
2. Use the issue template if available
3. Provide detailed information:
   - Clear description of the problem
   - Steps to reproduce
   - Expected vs actual behavior
   - Screenshots if applicable
   - System information

### Suggesting Enhancements

Enhancement suggestions are welcome! Please:
1. Check if the enhancement has been suggested
2. Describe the enhancement clearly
3. Explain the use case and benefits
4. Consider implementation complexity

### Content Contributions

#### Medical Content
- Must be reviewed by qualified medical professionals
- Follow the provided templates
- Include proper citations and references
- Ensure HIPAA compliance (no PHI)
- Use de-identified case examples

#### Code Contributions
1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Make your changes
4. Run validation scripts:
   ```bash
   python scripts/validation/validate_content_schema.py
   python scripts/validation/check_medical_terminology.py
   ```
5. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
6. Push to the branch (`git push origin feature/AmazingFeature`)
7. Open a Pull Request

### Pull Request Process

1. **Before Submitting:**
   - Update documentation for any new features
   - Add tests if applicable
   - Run all validation scripts
   - Ensure compliance checks pass
   - Update the README if needed

2. **PR Description Should Include:**
   - Purpose of the changes
   - How to test the changes
   - Screenshots (for UI changes)
   - Related issues (if any)
   - Checklist of completed items

3. **Review Process:**
   - At least one maintainer must review
   - All automated checks must pass
   - Address review feedback
   - Maintainer will merge when approved

## Development Setup

### Prerequisites
- Unreal Engine 5.3+
- Python 3.11+
- Git with Git LFS
- 16GB+ RAM

### Installation
```bash
# Clone repository
git clone https://github.com/TheMedpreneur/Shane-Medical-Content-Empire.git
cd Shane-Medical-Content-Empire

# Install Python dependencies
pip install -r requirements-validation.txt

# Setup UE5 project
# (Follow UE5 setup instructions in README)
```

### Development Workflow

1. **Create a branch:**
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Make changes and test:**
   ```bash
   # Make your changes
   
   # Run validation
   python scripts/validation/validate_content_schema.py
   python scripts/compliance/hipaa_audit.py
   ```

3. **Commit changes:**
   ```bash
   git add .
   git commit -m "Description of changes"
   ```

4. **Push and create PR:**
   ```bash
   git push origin feature/your-feature-name
   # Then create PR on GitHub
   ```

## Style Guidelines

### Python Code
- Follow PEP 8 style guide
- Use meaningful variable names
- Add docstrings to functions
- Maximum line length: 100 characters
- Use type hints where appropriate

### Medical Content
- Use proper medical terminology
- Follow AMA style for citations
- Include learning objectives
- Ensure accessibility compliance
- Use clear, concise language

### UE5 Blueprints
- Use descriptive names
- Comment complex logic
- Follow UE5 best practices
- Organize assets in folders
- Use consistent naming conventions

## Medical Content Guidelines

### Accuracy Requirements
- All medical information must be current
- Cite authoritative sources
- Have content reviewed by SME
- Update regularly
- Include date of last review

### HIPAA Compliance
- Never include real patient data
- De-identify all case examples
- No specific dates (use ranges)
- No geographic identifiers beyond state/region
- No medical record numbers

### Educational Standards
- Align with learning objectives
- Use Bloom's taxonomy for objectives
- Include assessment criteria
- Support multiple learning styles
- Ensure accessibility (WCAG 2.1)

### Citation Standards
- Use AMA citation style
- Include DOI when available
- Cite primary sources
- Update references regularly
- Verify all citations

## Testing

### Validation Tests
```bash
# Run all validation scripts
python scripts/validation/validate_content_schema.py
python scripts/validation/check_medical_terminology.py
python scripts/validation/validate_educational_standards.py
python scripts/validation/check_citations.py
python scripts/validation/check_accessibility.py
```

### Compliance Tests
```bash
# Run compliance audits
python scripts/compliance/hipaa_audit.py
python scripts/compliance/fda_cfr11_audit.py
python scripts/compliance/gdpr_audit.py
```

## Documentation

### Code Documentation
- Comment complex algorithms
- Document public APIs
- Update README for new features
- Include usage examples

### Content Documentation
- Provide context in metadata
- Document assumptions
- Include teaching notes
- List required resources

## Recognition

Contributors will be recognized in:
- CONTRIBUTORS.md file
- Release notes
- Project documentation

Thank you for contributing to advancing medical education!

## Questions?

Contact us at:
- **Email:** contribute@medicalcontentempire.com
- **Discussions:** GitHub Discussions
- **Issues:** GitHub Issues

## License

By contributing, you agree that your contributions will be licensed under the project's license.
