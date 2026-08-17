# IAPS - Intelligent Audit Planning and Risk Assessment System
## Project Requirements & Vision Document

**Project Name:** Intelligent Audit Planning and Risk Assessment System (IAPS)  
**Organization:** NCDC (Papua New Guinea)  
**Developer:** Jerry Lelumai (Year 4 CS Student, Divine Word University)  
**Duration:** 10 weeks (Agile/Scrum methodology)  
**Phase Focus:** Planning Phase of Auditing (Foundation for future Execution & Reporting phases)

---

## 1. PROJECT OVERVIEW

### Vision
Automate and enhance the audit planning process by providing auditors and supervisors with intelligent, AI-assisted decision support tools that enable faster risk assessment, better resource allocation, and data-driven audit planning.

### Core Purpose
- **Simplify** audit planning for internal auditors
- **Accelerate** risk assessment and materiality calculations
- **Integrate** financial data analytics with AI-powered insights
- **Ensure** compliance and audit trail documentation
- **Support** collaborative audit planning across teams

### Target Users
- Internal Auditors
- Audit Supervisors
- Finance/Data Managers
- Audit Management/Leadership

---

## 2. SYSTEM SCOPE & PHASES

### Current Implementation: Phase 1 - Planning
This system focuses exclusively on the **Planning Phase** of auditing:
- Engagement setup and management
- Financial data ingestion and analysis
- Risk identification and scoring
- Internal control assessment
- Materiality determination
- AI-assisted audit planning recommendations
- Dashboard and reporting

### Future Phases (Not in scope for this iteration)
- **Phase 2 - Execution:** Detailed testing procedures, evidence collection, issue tracking
- **Phase 3 - Reporting:** Audit findings compilation, opinion formation, report generation

---

## 3. FUNCTIONAL REQUIREMENTS

### 3.1 User Management & Authentication
- **2FA (Two-Factor Authentication)** support
- **Role-Based Access Control (RBAC)**
  - Admin role
  - Audit Supervisor role
  - Auditor role
  - Finance/Data Manager role
- Secure password hashing (bcrypt)
- JWT-based stateless authentication
- Session management and audit logging

### 3.2 Engagement Management
- Create and manage audit engagements
- Define engagement scope and objectives
- Track engagement timeline and milestones
- Link financial entities to engagements
- Engagement status tracking (Planning, In Progress, Completed)

### 3.3 Financial Data Management
- **Data Upload:** Support for financial statements and transaction data (CSV, Excel)
- **Data Validation:** Automated validation and error handling
- **Data Storage:** Structured database schema for financial data

### 3.4 Financial Analytics Engine
- **Financial Ratio Analysis:**
  - Liquidity ratios (Current, Quick, Working Capital)
  - Profitability ratios (ROA, ROE, Margins)
  - Efficiency ratios (Asset Turnover, Receivables Days)
  - Leverage ratios (Debt-to-Equity, Interest Coverage)
  
- **Trend Analysis:**
  - Year-over-year comparison
  - Period-over-period analysis
  - Trend visualization (line charts, graphs)
  
- **Variance Analysis:**
  - Budget vs. Actual comparison
  - Threshold-based alerts for significant variances
  - Variance trend identification

### 3.5 Materiality Calculation
- **Quantitative Materiality:**
  - Multiple calculation methods (revenue %, income %, equity %)
  - Benchmark-based calculations
  - Sliding scale determination
  
- **Qualitative Materiality:**
  - Consideration of sensitive accounts
  - Regulatory requirements
  - Known problem areas
  
- **Performance Materiality:** Calculated as % of quantitative materiality
- **Clearly Trivial Threshold:** Defined for posting decisions

### 3.6 Internal Control Assessment
- **Control Questionnaire:** Structured questionnaire for control evaluation
- **Risk of Material Misstatement (RMM):** 
  - Inherent Risk (IR) assessment
  - Control Risk (CR) assessment
  - Risk of Material Misstatement (ROMM) calculation: IR × CR
- **Control Effectiveness Scoring:** Rate controls as Effective/Partially Effective/Ineffective

### 3.7 Risk Assessment & Scoring System
- **Risk Identification:** Automated risk detection based on:
  - Financial metrics anomalies
  - Variance analysis results
  - Control assessment findings
  - Industry benchmarking
  
- **Risk Scoring Matrix:**
  - Likelihood × Impact = Risk Score
  - Risk categories: Critical, High, Medium, Low
  - Risk prioritization for audit focus
  
- **Risk Documentation:**
  - Risk description and justification
  - Risk owner assignment
  - Mitigation strategies

### 3.8 AI-Assisted Audit Planning
- **Claude 3.5 Sonnet Integration:**
  - Generates audit procedures based on identified risks
  - Suggests sample sizes for testing
  - Recommends key audit areas based on risk profile
  - Proposes resource allocation (auditor expertise required)
  
- **AI Output Storage:**
  - Recommendations stored in database
  - Audit supervisor review and approval workflow
  - Modification tracking
  
- **AI Reliability:** Risk engine operates independently (no AI dependency for core calculations)

### 3.9 Document Management
- Upload and store audit-related documents:
  - Financial statements
  - Internal control documentation
  - Risk assessment forms
  - Audit procedures
  - Working papers (foundation for Phase 2)
  
- Version control and audit trail
- Document classification and tagging

### 3.10 Interactive Dashboards
- **Engagement Overview Dashboard:**
  - Engagement status at a glance
  - Progress indicators
  - Key metrics and KPIs
  
- **Risk Assessment Dashboard:**
  - Risk heatmap visualization
  - Risk by category breakdown
  - Top risks requiring attention
  
- **Financial Analytics Dashboard:**
  - Key financial ratios
  - Trend analysis charts
  - Variance highlights
  - Benchmark comparisons
  
- **Planning Summary Dashboard:**
  - Materiality summary (quantitative + qualitative)
  - Internal control assessment results
  - Audit procedures overview
  - Resource requirements

### 3.11 Audit Trail & Compliance
- **Complete Audit Logging:**
  - User actions logged with timestamp
  - Data changes tracked (who, what, when, why)
  - AI interaction logging (prompts, responses)
  - Report generation logging
  
- **Compliance Documentation:**
  - Audit standard compliance checklist
  - Evidence collection tracking
  - Regulatory requirement mappings
  
- **Data Integrity:**
  - Database integrity constraints
  - Transaction atomicity for critical operations

### 3.12 Task Management & Sign-Off
- **Task Creation:** Automated task generation from audit procedures
- **Task Assignment:** Assign tasks to team members
- **Task Tracking:**
  - Status tracking (Not Started, In Progress, Completed, Blocked)
  - Due dates and priority levels
  - Progress indicators
  
- **Sign-Off Workflow:**
  - Evidence-based sign-off
  - Supervisor approval gates
  - Change approval process
  
- **Team Collaboration:**
  - Task comments and discussions
  - Activity feeds
  - Notification system

### 3.13 Reporting & Export
- **Audit Plan Reports:**
  - Summary of audit scope and approach
  - Identified risks and planned procedures
  - Materiality and sampling recommendations
  - Resource requirements
  
- **Export Formats:**
  - PDF reports
  - Excel workbooks
  - CSV data exports
  
- **Print Optimization:**
  - Print-friendly layouts
  - Summary and detailed views

---

## 4. NON-FUNCTIONAL REQUIREMENTS

### Performance
- Response time < 2 seconds for dashboard loads
- API response time < 500ms for 95th percentile
- Support concurrent users: 50+ simultaneous
- Database query optimization for large datasets

### Scalability
- Horizontal scaling for API services
- Database connection pooling
- Caching strategy for frequent queries (Redis)
- CDN for static assets (frontend)

### Security
- HTTPS/TLS for all communications
- SQL injection prevention (parameterized queries)
- CSRF token protection
- XSS protection
- Rate limiting on API endpoints
- Input validation and sanitization
- Secure headers (CSP, X-Frame-Options, etc.)

### Reliability
- 99.5% uptime target
- Database backup and recovery procedures
- Automated health checks
- Graceful error handling

### Usability
- Intuitive UI/UX design
- Responsive design (mobile, tablet, desktop)
- Accessibility compliance (WCAG 2.1 AA)
- Comprehensive user documentation
- Help tooltips and guidance

### Maintainability
- Clean, documented code
- Consistent coding standards
- Comprehensive logging
- Monitoring and alerting
- Automated testing (unit, integration, e2e)

---

## 5. TECHNOLOGY STACK

### Backend
- **Language:** Python 3.11+
- **Framework:** Django 4.2+ (with Django REST Framework)
- **Task Queue:** Celery (for async processing of AI requests)
- **Caching:** Redis
- **Database:** PostgreSQL 14+

### Frontend
- **Framework:** React 18+
- **Build Tool:** Vite
- **UI Library:** Bootstrap 5 or Material-UI
- **Charts/Visualization:** Chart.js or D3.js
- **State Management:** Redux or Context API
- **Package Manager:** npm/yarn

### AI Integration
- **AI Service:** Claude 3.5 Sonnet (via Anthropic API)
- **Request Queue:** Celery + Redis (for handling API rate limits)
- **Response Caching:** Local database storage

### Infrastructure & DevOps
- **Containerization:** Docker
- **Orchestration:** Docker Compose (dev), Kubernetes (production)
- **API Gateway:** Traefik (reverse proxy + load balancing)
- **Authentication:** Keycloak (centralized auth server)
- **CI/CD:** GitHub Actions
- **Container Registry:** GitHub Container Registry (GHCR)

### Database
- **Primary:** PostgreSQL 14+
- **Cache:** Redis
- **Backup:** PostgreSQL native backup (pg_dump)

### Development Environment
- **IDE:** VS Code (with DevContainers)
- **Version Control:** Git + GitHub
- **Package Management:** pip (Python), npm (Node.js)
- **Testing:** pytest (Python), Jest (JavaScript)
- **Linting:** pylint, Black (Python); ESLint (JavaScript)
- **Documentation:** Sphinx (Python), JSDoc (JavaScript)

---

## 6. DATA MODELS & ARCHITECTURE

### Core Entities

#### User
- ID, Email, Password Hash, Full Name
- Role (Admin, Supervisor, Auditor, Finance Manager)
- 2FA Status, Last Login, Created Date
- Active/Inactive Status

#### Engagement
- ID, Name, Client/Organization
- Engagement Period (From-To Dates)
- Scope and Objectives
- Assigned Auditors and Supervisor
- Status (Planning, In Progress, Completed)
- Financial Entities Included
- Materiality Settings
- Created Date, Last Updated

#### FinancialData
- ID, Engagement ID
- Upload Date, Data Period (Year/Quarter)
- Account Code, Account Name, Amount
- Validation Status
- Source (Manual Upload, System Integration, etc.)

#### FinancialRatio
- ID, Engagement ID, Calculation Date
- Ratio Type (Liquidity, Profitability, Efficiency, Leverage)
- Ratio Name, Value, Benchmark, Variance %
- Trend Analysis (Current vs. Prior Period)

#### Materiality
- ID, Engagement ID
- Quantitative Materiality (calculated %)
- Qualitative Materiality Assessment
- Performance Materiality (calculated %)
- Clearly Trivial Threshold
- Benchmark Used, Calculation Justification
- Approved By, Approval Date

#### InternalControl
- ID, Engagement ID, Control ID
- Control Description and Objective
- Inherent Risk, Control Risk, ROMM
- Effectiveness Rating
- Control Owner, Assessment Date
- Testing Approach and Sample Size

#### Risk
- ID, Engagement ID, Risk ID
- Risk Description and Category
- Inherent Risk Score, Control Risk Score, ROMM
- Likelihood × Impact = Risk Score
- Audit Procedures (linked)
- Risk Owner, Mitigation Strategy
- Status (Identified, Mitigated, Accepted)

#### AuditProcedure
- ID, Engagement ID, Risk ID
- Procedure Description
- Procedure Type (Analytical, Substantive, Tests of Control)
- Sample Size, Sampling Method
- Responsible Auditor
- Expected Evidence, Threshold for Issues
- Status (Planned, In Progress, Completed)
- Generated by (AI or Manual)

#### AIRecommendation
- ID, Engagement ID
- Recommendation Text, Category
- AI Model Used, Prompt Sent, Response Received
- Supervisor Review Status
- Approved/Modified/Rejected By, Date
- Reasoning and Justification

#### Document
- ID, Engagement ID
- Document Name, Type (PDF, Excel, Word, etc.)
- File Path, Upload Date
- Uploaded By, Version
- Classification (Public, Confidential, Restricted)

#### AuditLog
- ID, User ID, Action, Entity Type, Entity ID
- Timestamp, IP Address
- Old Value, New Value (for changes)
- Status (Success, Failure)

---

## 7. AUDIT WORKFLOW (Planning Phase)

### Step 1: Engagement Setup
1. Create new engagement
2. Define scope and objectives
3. Assign auditors and supervisors
4. Set engagement timeline

### Step 2: Data Collection & Upload
1. Upload financial statements (multiple periods)
2. Upload transaction data if needed
3. Validate data quality
4. Flag data issues for correction

### Step 3: Financial Analysis
1. Calculate financial ratios
2. Perform trend analysis
3. Identify unusual variances
4. Generate analytics dashboard

### Step 4: Materiality Determination
1. Conduct quantitative materiality calculation
2. Assess qualitative materiality factors
3. Document materiality justification
4. Get supervisor approval

### Step 5: Internal Control Assessment
1. Complete control questionnaire
2. Assess inherent and control risks
3. Rate control effectiveness
4. Identify control gaps

### Step 6: Risk Assessment
1. Identify inherent risks from financial analysis
2. Assess control effectiveness impact
3. Calculate ROMM (IR × CR)
4. Score and prioritize risks
5. Document risk justifications

### Step 7: AI-Assisted Planning
1. Submit risk profiles to Claude AI
2. Receive audit procedure recommendations
3. Review AI recommendations
4. Approve, modify, or reject recommendations
5. Store final procedures

### Step 8: Audit Plan Generation
1. Compile audit procedures
2. Determine sample sizes
3. Allocate resources (auditors, hours)
4. Define testing approach
5. Generate audit plan report

### Step 9: Sign-Off & Approval
1. Auditor prepares final plan
2. Supervisor reviews and approves
3. Management communication
4. Archiving for Phase 2 (Execution)

---

## 8. COMPLIANCE & AUDIT STANDARDS

### Standards to Follow
- **International Standards on Auditing (ISA)**
  - ISA 320: Materiality in Planning and Performing an Audit
  - ISA 330: The Auditor's Procedures in Response to Assessed Risks
  - ISA 400-499: Risk Assessment and Response to Assessed Risks
  
- **COSO Internal Control Framework**
  - Control Environment
  - Risk Assessment
  - Control Activities
  - Information & Communication
  - Monitoring
  
- **Data Protection & Privacy**
  - Secure handling of sensitive financial data
  - Audit trail for compliance
  - Access control logging

---

## 9. SUCCESS CRITERIA

### Phase 1 Completion Checklist
- ✅ All 12 functional areas implemented
- ✅ AI integration tested and working
- ✅ Database schema complete and normalized
- ✅ Authentication with 2FA operational
- ✅ Dashboards displaying correctly
- ✅ Audit trail logging 100% of actions
- ✅ Documentation complete
- ✅ Testing: 80%+ code coverage
- ✅ Performance: <2s dashboard load time
- ✅ User acceptance testing passed
- ✅ Security assessment passed
- ✅ Deployment to staging environment

---

## 10. IMPLEMENTATION TIMELINE (10 Weeks)

### Weeks 1-2: Foundation & Setup
- Project structure setup
- Database schema design
- API skeleton with authentication
- Frontend project initialization

### Weeks 3-4: Core Features - Data & Analytics
- Financial data upload and validation
- Financial ratio calculations
- Trend analysis engine
- Initial dashboards

### Weeks 5-6: Risk & Control Assessment
- Materiality calculator
- Internal control assessment module
- Risk assessment and scoring
- Risk dashboard

### Weeks 7-8: AI Integration & Advanced Features
- Claude API integration
- AI-assisted planning module
- Document management
- Audit trail implementation

### Week 9: Integration & Testing
- End-to-end testing
- Performance optimization
- Security audit
- User acceptance testing

### Week 10: Deployment & Documentation
- Production deployment
- Comprehensive documentation
- Training materials
- Knowledge transfer

---

## 11. DEPENDENCIES & ASSUMPTIONS

### Dependencies
- Anthropic Claude 3.5 Sonnet API access
- PostgreSQL 14+ availability
- Docker and Docker Compose
- GitHub repository access
- Internet connectivity for AI calls

### Assumptions
- Users have basic audit knowledge
- Financial data is provided in standard formats
- Internet connectivity is stable
- Database backups will be managed by ops team
- Production environment provided by organization

---

## 12. RISKS & MITIGATION

| Risk | Impact | Probability | Mitigation |
|------|--------|-------------|-----------|
| AI API rate limits | Delayed recommendations | Medium | Implement queue + caching |
| Data quality issues | Invalid analysis | High | Validation rules + manual review |
| Performance with large datasets | Slow dashboards | Medium | Indexing + caching + async processing |
| Security vulnerabilities | Data breach | Low | Regular security audits + OWASP compliance |
| Scope creep | Missed deadline | High | Strict change control + stakeholder alignment |

---

**Document Version:** 1.0  
**Last Updated:** 2026-08-16  
**Status:** Active - Project Planning Phase
