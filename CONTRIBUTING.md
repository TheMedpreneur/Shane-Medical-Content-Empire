# Contributing to Shane-Medical-Content-Empire

Thank you for your interest in contributing to the AI-powered medical education content creation system! This guide will help you get started.

## Table of Contents

1. [Getting Started](#getting-started)
2. [Development Workflow](#development-workflow)
3. [Code Standards](#code-standards)
4. [Documentation](#documentation)
5. [Testing](#testing)
6. [Security and Compliance](#security-and-compliance)
7. [Submitting Changes](#submitting-changes)

## Getting Started

### Prerequisites

Before contributing, ensure you have:
- Completed all required security and compliance training
- Set up your development environment (see `Documentation/Setup-Guides/`)
- Read through the project README and documentation
- Familiarized yourself with HIPAA and FERPA requirements

### First-Time Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/TheMedpreneur/Shane-Medical-Content-Empire.git
   cd Shane-Medical-Content-Empire
   ```

2. **Install dependencies**
   - Unreal Engine 5.3+
   - Ludus AI plugin
   - Cursor AI extension
   - Medical Anatomy Pack (with valid license)

3. **Configure your environment**
   - Follow guides in `Documentation/Setup-Guides/`
   - Set up environment variables
   - Configure security settings

4. **Create a feature branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

## Development Workflow

### Branch Naming Convention

- `feature/` - New features (e.g., `feature/add-cardiology-module`)
- `bugfix/` - Bug fixes (e.g., `bugfix/fix-rendering-issue`)
- `hotfix/` - Critical production fixes
- `docs/` - Documentation updates
- `refactor/` - Code refactoring
- `test/` - Test additions or modifications

### Workflow Steps

1. **Create a branch** from `develop`
2. **Make your changes** following coding standards
3. **Test thoroughly** (see Testing section)
4. **Update documentation** if needed
5. **Commit your changes** with descriptive messages
6. **Push to GitHub** and create a Pull Request
7. **Address review feedback**
8. **Merge** once approved

## Code Standards

### General Principles

- Write clean, readable, maintainable code
- Follow SOLID principles
- Keep functions small and focused
- Use meaningful variable and function names
- Comment complex logic, not obvious code
- Avoid premature optimization

### Language-Specific Standards

#### Unreal Engine / C++
- Follow Unreal Engine coding standards
- Use `UPROPERTY()` and `UFUNCTION()` macros appropriately
- Prefix classes: `U` for UObject-derived, `A` for Actor-derived, `F` for structs
- Use BlueprintCallable where appropriate for designer access

#### Python
- Follow PEP 8 style guide
- Use type hints for function parameters and returns
- Write docstrings for all public functions and classes
- Use virtual environments for dependencies

#### Blueprints
- Use clear, descriptive node naming
- Organize nodes neatly with reroute nodes
- Add comments to explain complex logic
- Keep blueprints focused and modular

### File Organization

```
Core-Systems/
  UE5-Project/
    Content/
      Medical/        # Medical-specific assets
      UI/             # User interface
      Blueprints/     # Blueprint classes
  Ludus-AI-Blueprints/
    [Organized by feature]
  Cursor-AI-Code/
    [Organized by module]
```

## Documentation

### What to Document

- All public APIs and functions
- Setup and configuration procedures
- Architecture and design decisions
- Medical content sources and citations
- Security and compliance procedures

### Documentation Standards

- Use Markdown for all documentation
- Include code examples where helpful
- Keep documentation up-to-date with code changes
- Add screenshots and diagrams for clarity
- Reference medical standards and evidence

### Required Documentation for New Features

1. Feature description and rationale
2. Technical implementation details
3. Medical accuracy verification
4. Security and compliance considerations
5. User guide or tutorial
6. API documentation (if applicable)

## Testing

### Required Tests

- **Unit Tests**: Test individual components
- **Integration Tests**: Test component interactions
- **Medical Accuracy Tests**: Validate medical content
- **Security Tests**: Verify security controls
- **Performance Tests**: Ensure acceptable performance

### Medical Content Validation

All medical content must be:
1. Reviewed by qualified medical professionals
2. Verified against current medical standards
3. Cited with evidence-based sources
4. Compliant with educational standards (ACGME competencies)
5. Documented with review dates and reviewers

### Testing Checklist

Before submitting a PR:
- [ ] All tests pass
- [ ] New code has test coverage
- [ ] Medical content reviewed by SME
- [ ] Security implications considered
- [ ] Performance impact assessed
- [ ] Documentation updated
- [ ] No sensitive data in commits

## Security and Compliance

### Critical Requirements

- **NEVER** commit sensitive data (PHI, PII, credentials)
- Use environment variables for secrets
- Follow secure coding practices
- Implement proper authentication and authorization
- Encrypt sensitive data at rest and in transit

### HIPAA Compliance

- No real patient data in educational content
- De-identify all clinical cases
- Use fictional patient scenarios
- Obtain proper consent for any real cases
- Review `Security-Compliance/HIPAA-Guidelines.md`

### Security Review

Security review required for:
- Authentication/authorization changes
- Data storage or transmission changes
- Third-party integrations
- API modifications
- Access control changes

## Submitting Changes

### Pull Request Process

1. **Create PR** with descriptive title and description
2. **Complete PR template** (if provided)
3. **Link related issues** or tickets
4. **Request reviewers** (minimum 2 for medical content)
5. **Ensure CI passes** (all workflows green)
6. **Address feedback** promptly and professionally
7. **Squash commits** if requested
8. **Celebrate** when merged! 🎉

### PR Description Template

```markdown
## Description
[Brief description of changes]

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Breaking change
- [ ] Documentation update
- [ ] Medical content update

## Medical Review (if applicable)
- [ ] Reviewed by qualified medical professional
- [ ] Evidence-based sources cited
- [ ] Current medical standards verified

## Testing
- [ ] All tests pass
- [ ] New tests added
- [ ] Manual testing completed

## Security and Compliance
- [ ] No sensitive data included
- [ ] HIPAA compliance verified
- [ ] Security implications considered

## Documentation
- [ ] Documentation updated
- [ ] README updated (if needed)
- [ ] API docs updated (if applicable)

## Checklist
- [ ] Code follows project standards
- [ ] Self-review completed
- [ ] Comments added for complex logic
- [ ] No console warnings or errors
- [ ] Compatible with project requirements
```

### Commit Message Guidelines

Use clear, descriptive commit messages:

```
<type>(<scope>): <subject>

<body>

<footer>
```

**Types:**
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes (formatting)
- `refactor`: Code refactoring
- `test`: Test additions or changes
- `chore`: Build process or tooling changes

**Examples:**
```
feat(modules): Add cardiology anatomy module

Implement comprehensive cardiology module with 3D heart models,
interactive visualizations, and assessment questions.

Reviewed-by: Dr. Jane Smith, MD
Closes #123
```

## Code Review

### As a Reviewer

- Be respectful and constructive
- Focus on code quality and standards
- Verify medical accuracy
- Check security implications
- Suggest improvements, don't demand changes
- Approve when requirements are met

### As an Author

- Respond to feedback professionally
- Ask for clarification if needed
- Make requested changes promptly
- Explain design decisions when appropriate
- Thank reviewers for their time

## Getting Help

### Resources

- **Documentation**: `Documentation/` directory
- **Setup Guides**: `Documentation/Setup-Guides/`
- **Security**: `Security-Compliance/`
- **Issues**: GitHub Issues for bug reports and feature requests

### Communication Channels

- **GitHub Issues**: Technical discussions and bug reports
- **Pull Requests**: Code review and feedback
- **Team Meetings**: Weekly sync and planning
- **Slack/Discord**: [If applicable] Daily communication

## Recognition

We value all contributions! Contributors will be:
- Acknowledged in release notes
- Added to CONTRIBUTORS file
- Recognized in team meetings
- Eligible for contributor benefits

## Questions?

If you have questions not covered in this guide:
1. Check existing documentation
2. Search closed issues
3. Ask in team channels
4. Create a new issue with the `question` label

---

Thank you for contributing to medical education innovation! 🏥📚✨
