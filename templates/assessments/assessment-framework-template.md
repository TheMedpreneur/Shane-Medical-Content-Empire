# Assessment Framework Template

## Assessment Overview
- **Assessment Name**: [Assessment Title]
- **Assessment Code**: [ASMT-XXX]
- **Module/Course**: [Parent Module or Course]
- **Assessment Type**: [Formative / Summative / Diagnostic]
- **Purpose**: [Knowledge Check / Skill Validation / Certification]
- **Version**: 1.0
- **Date Created**: [YYYY-MM-DD]

---

## Assessment Goals

### Primary Objectives
1. [Measure understanding of core concepts]
2. [Evaluate application of knowledge]
3. [Assess critical thinking and decision-making]

### Learning Outcomes Assessed
- **LO1**: [Specific learning outcome from module]
- **LO2**: [Specific learning outcome from module]
- **LO3**: [Specific learning outcome from module]
- **LO4**: [Specific learning outcome from module]

### Bloom's Taxonomy Levels
| Cognitive Level | Percentage | Question Count |
|----------------|------------|----------------|
| Remember | 15% | [X questions] |
| Understand | 25% | [X questions] |
| Apply | 30% | [X questions] |
| Analyze | 20% | [X questions] |
| Evaluate | 10% | [X questions] |

---

## Assessment Specifications

### Format Details
```json
{
  "TotalQuestions": 25,
  "QuestionTypes": {
    "MultipleChoice": 15,
    "TrueFalse": 5,
    "Matching": 0,
    "ShortAnswer": 3,
    "CaseBasedScenario": 2
  },
  "TimeLimit": 45,
  "TimeLimitEnforced": true,
  "AttemptsAllowed": 3,
  "PassingScore": 80,
  "QuestionPoolSize": 75,
  "RandomizeQuestions": true,
  "RandomizeAnswers": true
}
```

### Scoring Rubric
```json
{
  "TotalPoints": 100,
  "PointDistribution": {
    "MultipleChoice": 2,
    "TrueFalse": 2,
    "ShortAnswer": 5,
    "CaseScenario": 10
  },
  "PartialCredit": {
    "MultipleSelect": true,
    "ShortAnswer": false
  },
  "NegativeMarking": false
}
```

---

## Question Bank Structure

### Section 1: Foundational Knowledge (Remember/Understand)

#### Question 1.1 - Multiple Choice
**Question**: [Question text about basic medical or AI concept]

**Options**:
- A) [Correct answer]
- B) [Distractor - common misconception]
- C) [Distractor - plausible but incorrect]
- D) [Distractor - opposite of correct]

**Correct Answer**: A
**Points**: 2
**Learning Outcome**: LO1
**Cognitive Level**: Remember
**Explanation**: [Why the answer is correct and why others are not]
**Reference**: [Module section or reading]

---

#### Question 1.2 - True/False
**Question**: [Statement about medical concept or procedure]

**Options**:
- True
- False

**Correct Answer**: True
**Points**: 2
**Learning Outcome**: LO2
**Cognitive Level**: Understand
**Explanation**: [Detailed explanation]
**Reference**: [Module section]

---

### Section 2: Application (Apply)

#### Question 2.1 - Multiple Choice with Clinical Context
**Question**: A 45-year-old patient presents with [symptoms]. An AI diagnostic system suggests [diagnosis] with 85% confidence. What is the most appropriate next step?

**Options**:
- A) [Action 1]
- B) [Action 2 - Correct]
- C) [Action 3]
- D) [Action 4]

**Correct Answer**: B
**Points**: 2
**Learning Outcome**: LO3
**Cognitive Level**: Apply
**Explanation**: [Clinical reasoning for the correct choice]
**Reference**: [Module section, clinical guidelines]

---

#### Question 2.2 - Interactive Simulation
**Question**: Using the 3D anatomical model, identify and label the following structures affected by the pathology.

**Format**: Interactive UE5 component
**Blueprint**: `BP_Assessment_AnatomyLabeling`
**Required Actions**:
1. Identify structure 1
2. Identify structure 2
3. Identify structure 3

**Correct Answers**: [List of correct structure names]
**Points**: 5
**Learning Outcome**: LO4
**Cognitive Level**: Apply
**Auto-Grading**: Yes (via blueprint logic)

---

### Section 3: Analysis & Evaluation (Analyze/Evaluate)

#### Question 3.1 - Case-Based Scenario
**Scenario**: 
```
Patient Information:
- Age: [X]
- Gender: [X]
- Chief Complaint: [X]
- Medical History: [X]
- Current Medications: [X]

Diagnostic Data:
- Lab Results: [X]
- Imaging: [X]
- AI Analysis Output: [X]
```

**Questions**:
1. **Part A** (5 points): Analyze the AI system's output. What factors likely contributed to its diagnostic recommendation?
   - **Grading Criteria**:
     - Identifies key diagnostic features (2 points)
     - Explains AI reasoning (2 points)
     - Demonstrates understanding of algorithm (1 point)

2. **Part B** (5 points): Evaluate the reliability of this AI recommendation. What additional information would you need?
   - **Grading Criteria**:
     - Critical evaluation of AI output (2 points)
     - Identifies limitations (2 points)
     - Suggests appropriate follow-up (1 point)

**Total Points**: 10
**Learning Outcomes**: LO5, LO6
**Cognitive Level**: Analyze, Evaluate
**Grading Type**: Rubric-based (manual or semi-automated)

---

#### Question 3.2 - Multiple Select
**Question**: Which of the following factors should be considered when evaluating an AI diagnostic tool for clinical deployment? (Select all that apply)

**Options**:
- [ ] A) Sensitivity and specificity
- [ ] B) Training data diversity
- [ ] C) Computational cost
- [ ] D) User interface design
- [ ] E) Integration with existing systems
- [ ] F) Regulatory compliance

**Correct Answers**: A, B, E, F
**Partial Credit**: Yes (0.5 points per correct selection/omission)
**Total Points**: 2
**Learning Outcome**: LO7
**Cognitive Level**: Evaluate
**Explanation**: [Why each option is correct or incorrect]

---

### Section 4: Short Answer Questions

#### Question 4.1 - Short Answer
**Question**: Explain in 2-3 sentences how convolutional neural networks are used in medical image analysis and why they are particularly effective for this application.

**Model Answer**:
[Expected comprehensive answer demonstrating understanding of CNNs, their architecture, feature extraction capabilities, and specific advantages in medical imaging contexts]

**Grading Rubric**:
- **5 points**: Comprehensive answer covering all key aspects
- **4 points**: Good answer covering most aspects with minor gaps
- **3 points**: Adequate answer covering basic concepts
- **2 points**: Partial answer with significant gaps
- **1 point**: Minimal understanding demonstrated
- **0 points**: Incorrect or no answer

**Keywords Expected**: [CNN, feature extraction, spatial hierarchy, medical imaging, pattern recognition]
**Learning Outcome**: LO8
**Cognitive Level**: Understand/Apply

---

## Assessment Delivery

### Platform Requirements
```json
{
  "DeliveryPlatform": "Custom LMS / Moodle / Canvas",
  "TechnicalRequirements": {
    "Browser": "Chrome 90+, Firefox 88+, Safari 14+",
    "JavaScript": "Required",
    "Cookies": "Required",
    "PopupBlocker": "Disabled",
    "InternetSpeed": "Minimum 5 Mbps"
  },
  "AccessibilityFeatures": {
    "ScreenReaderCompatible": true,
    "KeyboardNavigation": true,
    "TextToSpeech": true,
    "AdjustableTextSize": true,
    "HighContrastMode": true,
    "ExtendedTime": "Available for accommodations"
  }
}
```

### Proctoring Requirements
```json
{
  "ProctoringType": "None / AI-Proctored / Human-Proctored",
  "Requirements": {
    "WebcamRequired": false,
    "MicrophoneRequired": false,
    "ScreenRecording": false,
    "BrowserLockdown": false,
    "IdentityVerification": false
  },
  "SecurityMeasures": {
    "QuestionRandomization": true,
    "AnswerRandomization": true,
    "TimeLimit": true,
    "SingleSession": true,
    "PreventCopyPaste": true
  }
}
```

### Accommodation Support
- **Extended Time**: +50% time for documented needs
- **Alternative Formats**: Audio version, large print
- **Assistive Technology**: Compatible with screen readers
- **Breaks**: Scheduled breaks available (pause timer)
- **Quiet Environment**: Option for supervised location

---

## Grading & Feedback

### Automated Grading
```json
{
  "AutoGradedQuestions": [
    "MultipleChoice",
    "TrueFalse",
    "Matching",
    "InteractiveLabeling"
  ],
  "ImmediateScoring": true,
  "PartialCreditLogic": "Defined in question metadata"
}
```

### Manual Grading
```json
{
  "ManualGradedQuestions": [
    "ShortAnswer",
    "Essay",
    "CaseAnalysis"
  ],
  "GradingDeadline": "48 hours from submission",
  "MultipleGraders": false,
  "BlindGrading": true,
  "RubricRequired": true
}
```

### Feedback Delivery
```json
{
  "FeedbackTiming": "Immediate / After attempt / After deadline",
  "FeedbackTypes": {
    "CorrectAnswers": true,
    "Explanations": true,
    "ReferenceMaterials": true,
    "PersonalizedComments": true
  },
  "ScoreDisplay": {
    "PercentageScore": true,
    "LetterGrade": false,
    "DetailedBreakdown": true,
    "ComparisonToAverage": false
  }
}
```

### Remediation Path
```json
{
  "RemediationTrigger": "Score < 80%",
  "RemediationOptions": [
    "Review incorrect questions",
    "Additional practice exercises",
    "Recommended module sections to review",
    "Optional tutoring session",
    "Alternative learning resources"
  ],
  "RetakePolicy": {
    "AllowRetake": true,
    "MaxAttempts": 3,
    "WaitTime": "24 hours between attempts",
    "BestScoreKept": true
  }
}
```

---

## Quality Assurance

### Item Analysis
```json
{
  "Metrics": {
    "DifficultyIndex": {
      "Calculation": "Percentage of students answering correctly",
      "Target": "0.3 - 0.9 (30% - 90%)",
      "ReviewTrigger": "< 0.2 or > 0.95"
    },
    "DiscriminationIndex": {
      "Calculation": "Point-biserial correlation",
      "Target": "> 0.3",
      "ReviewTrigger": "< 0.2"
    },
    "Reliability": {
      "Method": "Cronbach's Alpha",
      "Target": "> 0.7",
      "ReviewTrigger": "< 0.6"
    }
  },
  "AnalysisFrequency": "After every 50 attempts",
  "ActionThresholds": {
    "FlagForReview": "Metrics outside target range",
    "RemoveFromPool": "Consistently poor performance",
    "RewriteQuestion": "Systematic issues identified"
  }
}
```

### Peer Review Process
- **Initial Development**: Subject matter expert creates questions
- **Peer Review 1**: Another SME reviews for accuracy
- **Peer Review 2**: Instructional designer reviews for clarity
- **Pilot Testing**: Small group of learners attempt assessment
- **Statistical Analysis**: Item analysis after initial deployment
- **Revision**: Update based on data and feedback

---

## Validity & Reliability

### Content Validity
- [ ] Questions align with learning outcomes
- [ ] Coverage of all critical topics
- [ ] Appropriate difficulty distribution
- [ ] SME validation completed

### Construct Validity
- [ ] Questions measure intended constructs
- [ ] Different question types for different cognitive levels
- [ ] Progression from simple to complex

### Reliability
- **Internal Consistency**: Target Cronbach's α > 0.7
- **Test-Retest**: Correlation > 0.8 (if applicable)
- **Inter-Rater**: Agreement > 85% for manual grading

### Fairness & Bias Review
- [ ] Language is clear and unambiguous
- [ ] No cultural bias in questions
- [ ] No gender bias in examples
- [ ] Medical scenarios are diverse and representative
- [ ] Accessibility standards met

---

## Security & Integrity

### Academic Integrity Measures
```json
{
  "PreventionStrategies": [
    "Question randomization from large pool",
    "Answer order randomization",
    "Time limits to prevent resource sharing",
    "Unique questions per attempt",
    "Proctoring (if required)",
    "Honor code acknowledgment"
  ],
  "DetectionMethods": [
    "Pattern analysis of answers",
    "Timing analysis",
    "Browser activity monitoring",
    "Plagiarism detection for text responses"
  ],
  "ConsequencesPolicy": "Defined in course syllabus"
}
```

### Data Protection
- **Student Data**: FERPA compliant
- **Assessment Content**: Proprietary, not to be shared
- **Encryption**: All data encrypted in transit and at rest
- **Access Control**: Role-based access to questions and results
- **Retention**: Scores retained per institutional policy

---

## Reporting & Analytics

### Individual Learner Report
```json
{
  "ReportIncludes": [
    "Overall score and percentage",
    "Score by section/topic",
    "Time taken",
    "Questions missed",
    "Correct answers and explanations",
    "Areas for improvement",
    "Recommended next steps"
  ],
  "Format": "PDF / Web view",
  "Availability": "Immediate after grading complete"
}
```

### Instructor Dashboard
```json
{
  "Metrics": [
    "Class average and distribution",
    "Pass/fail rate",
    "Time statistics",
    "Question performance (difficulty, discrimination)",
    "Learning outcome achievement",
    "Common misconceptions"
  ],
  "Visualizations": [
    "Score distribution histogram",
    "Question performance bar chart",
    "Learning outcome heatmap",
    "Attempt timeline"
  ],
  "ExportOptions": ["CSV", "Excel", "PDF"]
}
```

### Program-Level Analytics
```json
{
  "AggregateMetrics": [
    "Module completion rates",
    "Average scores over time",
    "Comparison across cohorts",
    "Correlation with other assessments",
    "Predictive success indicators"
  ],
  "ReportingFrequency": "Quarterly",
  "Stakeholders": ["Program directors", "Curriculum committee"]
}
```

---

## Continuous Improvement

### Review Cycle
1. **Post-Assessment Analysis** (Immediate)
   - Item statistics calculation
   - Identification of problematic questions
   - Student feedback collection

2. **Quarterly Review** (Every 3 months)
   - Comprehensive item analysis
   - Question bank updates
   - Rubric refinement

3. **Annual Review** (Yearly)
   - Validity and reliability studies
   - Alignment with updated guidelines
   - Curriculum mapping verification

### Update Log
| Version | Date | Changes | Approved By |
|---------|------|---------|-------------|
| 1.0 | [Date] | Initial assessment created | [Name] |
| 1.1 | [Date] | Updated 5 questions based on item analysis | [Name] |
| 1.2 | [Date] | Added 2 new case scenarios | [Name] |

---

## Compliance & Standards

### Educational Standards
- [ ] Complies with [Institution] assessment standards
- [ ] Aligned with [Professional Body] guidelines
- [ ] Meets accreditation requirements

### Medical Standards
- [ ] Medical content validated by licensed professionals
- [ ] References current clinical practice guidelines
- [ ] Includes appropriate disclaimers

### Technical Standards
- [ ] WCAG 2.1 Level AA accessible
- [ ] QTI 2.1 compliant (if LMS export required)
- [ ] SCORM/xAPI compatible

---

## Version Control & Documentation

### Change Management
- All changes tracked in version history
- Major changes require SME approval
- Students notified of significant updates
- Archived versions maintained

### Documentation
- Question bank spreadsheet maintained
- Rubrics documented and shared
- Analysis reports archived
- Feedback summary compiled

---

## Contact Information

### Assessment Coordinator
- **Name**: [Name]
- **Email**: [Email]
- **Phone**: [Phone]

### Subject Matter Expert
- **Name**: [Name, Credentials]
- **Email**: [Email]
- **Specialty**: [Medical Specialty]

### Technical Support
- **Email**: assessment-support@medical-content-empire.com
- **Hours**: [Support hours]

---

## Notes & Future Enhancements
[Additional notes about planned improvements, known issues, or special considerations]
