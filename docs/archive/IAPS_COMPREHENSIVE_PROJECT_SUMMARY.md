# INTELLIGENT AUDIT PLANNING AND RISK ASSESSMENT SYSTEM (IAPS)
## Comprehensive Project Analysis & Summary

---

## DOCUMENT EXTRACTION SUMMARY

All 5 project documents have been successfully extracted and analyzed:
1. ✅ Project Overview.docx
2. ✅ Project Proposal - Jerry Lelumai.docx
3. ✅ System Design Specifications.docx
4. ✅ Background-Audit Process.docx
5. ✅ To my project implementation.docx

---

## PROJECT IDENTIFICATION

**Project Name:** Intelligent Audit Planning and Risk Assessment System (IAPS)

**Organization:** National Capital District Commission (NCDC) - Port Moresby, Papua New Guinea

**Developer:** Jerry Lelumai (Year 4 Student, Bachelor of Mathematics and Computing Science)

**Institution:** Divine Word University, Faculty of Business & Informatics

**Supervisor:** Mr. Lyall DALE (Head of Department)

**Project Duration:** 10 weeks (Agile/Scrum methodology)

**Project Type:** Final Year Research Project & Capstone Implementation

---

## PROJECT PURPOSE & SIGNIFICANCE

### Primary Purpose
To develop a web-based, AI-assisted audit planning and risk assessment system that automates and improves the audit planning phase for NCDC, addressing inefficiencies in manual, spreadsheet-based audit processes.

### Key Objectives
- Automate planning analytics and risk assessments
- Improve audit efficiency and consistency
- Enhance documentation quality
- Support data-driven decision making
- Maintain auditor professional judgment
- Support digital transformation in auditing
- Strengthen governance in public sector organizations

### Significance
- Addresses critical gaps in public sector audit tools (few systems tailored for public sector)
- Integrates AI, ML, and financial analytics into a single platform
- Provides practical, scalable foundation for future intelligent audit tools
- Particularly relevant to developing countries and PNG context
- Supports transparency and accountability in government operations

---

## CURRENT PROBLEM STATEMENT

### Challenges at NCDC
- **Manual Processes:** Audit planning done with spreadsheets, scattered documents, and manual notes
- **Time Inefficiency:** Slow, hard to review, heavily dependent on individual auditor experience
- **Repetitive Work:** Tasks like analytics, materiality calculation, control assessment repeated for each engagement
- **Lack of Integration:** No unified tool combining analytics, risk assessment, documentation, and AI support
- **Administrative Burden:** Auditors spend more time on administrative work than professional judgment
- **Quality Variation:** Planning quality and transparency vary between audits
- **No Existing Tools:** NCDC currently uses only Excel spreadsheets; no audit software exists

---

## SYSTEM SCOPE & BOUNDARIES

### In Scope
✅ Audit planning and risk assessments (planning phase only)
✅ User authentication and authorization
✅ Web-based decision support for engagements
✅ Automated analytics, materiality, and risk scoring
✅ AI-assisted recommendations and draft workpapers
✅ Secure document management and dashboards
✅ Auditor review and approval of all AI outputs
✅ Audit trail and activity logging

### Out of Scope
❌ Full fieldwork execution and testing automation
❌ Replacement of auditor professional judgment
❌ Live integration with client accounting/ERP systems
❌ Continuous or real-time audit monitoring
❌ Tax, consulting, or non-audit services
❌ Mobile app or public client portal
❌ Custom AI model training

---

## KEY FEATURES & FUNCTIONAL REQUIREMENTS

### 1. User Management
- Secure login with username and password
- Two-Factor Authentication (2FA)
- Role-based access control (RBAC)
  - **Auditor:** Full planning functionality
  - **Supervisor:** Review, assess, comment, and sign-off capabilities

### 2. Engagement Management
- Create/view engagements with stakeholders
- Store client details and engagement year
- Client intake and management
- Engagement acceptance and independence checklist

### 3. Data Collection & Upload
- Upload trial balance/financial statements (CSV/Excel)
- Enter internal control information
- Capture interview notes
- Financial data management and storage
- Prior-year data and comparative analysis

### 4. Planning Analytics
- Ratio analysis (financial ratios)
- Trend analysis (year-over-year comparisons)
- Variance analysis (budget vs. actual)
- Output displayed in tables and charts
- Identifies significant fluctuations and unusual patterns

### 5. Materiality Calculation
- Measure and compute materiality
- Benchmark selection (assets, revenue, etc.)
- Materiality performance tracking
- Automated materiality determination based on engagement size

### 6. Internal Control Assessment
- Record internal control activities
- Capture control design and implementation
- Rate internal control effectiveness
- Assessment matrix for controls
- AI-assisted analysis of process walkthroughs to identify weaknesses

### 7. Risk Assessment & Scoring Engine
- Enter Inherent Risk (IR) by account/process
- Enter Control Risk (CR)
- Calculate Risk of Material Misstatement (ROMM)
- Highlight high-risk accounts on dashboard
- Risk ranking and prioritization
- AI-assisted risk analysis

### 8. AI-Assisted Planning
- **OpenAI API Integration:**
  - Generate draft planning memorandums
  - Summarize interview notes and findings
  - Suggest audit procedures based on risk profiles
  - Create workpaper templates and recommendations
- **Claude 3.5 Sonnet** for advanced reasoning
- **Key Feature:** Auditors review, edit, and approve all AI outputs before use
- **Vector Database (ChromaDB):** Retrieve context from prior notes and similar accounts

### 9. Document Management
- Upload, store, and organize planning documents
- Evidence storage and retrieval
- Document types: Engagement letters, financial statements, risk assessments, control documentation
- Centralized secure repository
- MinIO for object/document storage

### 10. Dashboard & Reporting
- Engagement status overview
- Materiality visualization
- Risk overview by account
- Planning progress tracking
- Interactive charts and status indicators
- Planning report generation
- Real-time audit planning situation view

### 11. Audit Trail & Compliance
- Record all important actions (data uploads, risk rating changes, approvals)
- Timestamp and user information for each action
- Supports accountability and governance requirements

### 12. Task Management & Review Sign-off
- Task tracking system
- Digital sign-off capabilities
- Supervisor review and approval workflow
- Progress monitoring

---

## NON-FUNCTIONAL REQUIREMENTS

### Performance
- Quick response to user actions (dashboard opening, form saving, analytics)
- No extended wait times for page loads or calculations
- Optimized for typical audit engagement workflows

### Security
- Secure authentication (username/password + 2FA)
- Role-based authorization
- HTTPS encryption for all data transmission
- Protection of sensitive financial and audit information
- Encrypted data storage
- API gateway security (Keycloak)

### Reliability
- Consistent system operation
- Graceful error handling (no silent failures)
- Clear error messages for user recovery
- Data integrity and backup mechanisms
- Fallback functionality when AI services unavailable

### Usability
- Simple, intuitive web-based interface
- Clear labels and simple menus
- Logical flow matching audit planning stages:
  1. Data Upload
  2. Analytics
  3. Internal Controls
  4. Risk Assessment
  5. AI Outputs
  6. Documents
- Helpful messages and input validation
- Minimal training requirements
- Support for non-technical users

### Maintainability
- Modular architecture
- Clear separation of concerns
- Well-documented code
- Containerized deployment (Docker)

---

## DATA MODELS & ENTITY RELATIONSHIPS

### Core Entities

**User**
- UserId, Username, Role (Auditor/Supervisor), Email
- Authentication credentials and permissions

**Client**
- ClientId, ClientName, Industry, Address, Contact Details
- Parent entity for all engagements

**Engagement**
- EngagementId, ClientId, YearEnd, Type, Status
- Central unit of audit work
- Links to all planning data for an audit

**FinancialData**
- TrialBalance entries, Chart of Accounts, Account Balances
- Pre-processed and cleaned financial statements
- Prior-year and current-year comparatives

**Planning Analytics**
- Calculated Ratios (liquidity, profitability, efficiency)
- Trends and variance analysis results
- Materiality calculations and benchmarks

**Control**
- ControlId, EngagementId, Description, Process Owner
- Design, Implementation, and Effectiveness rating
- Control risk assessment

**RiskAssessment**
- AccountId/ProcessId, InherentRisk, ControlRisk, ROMM
- Risk ratings and calculations
- Ranking and prioritization data

**AIOutput**
- OutputId, EngagementId, Type (memorandum, procedures, summary)
- Draft content from Claude API
- Status (draft, reviewed, approved)

**Document**
- DocumentId, EngagementId, Type, UploadedBy, UploadDate
- Engagement letters, financial statements, evidence
- Storage reference and access permissions

**AuditTrail**
- TrailId, UserId, Action, Timestamp, Details
- Complete history of system actions for accountability

---

## SYSTEM ARCHITECTURE & DESIGN

### Architectural Approach: **Microservices with API Gateway Pattern**

### Three-Tier Architecture

#### **Presentation Layer (Frontend)**
- **Technology:** HTML5, Bootstrap or React
- **Interface Type:** Web-based browser application
- **Screens:**
  - Login page
  - Engagement list page
  - Engagement details page with tabbed interface
  - Dashboard with charts and status indicators
  - Reporting and export pages

#### **API Gateway & Security Layer**
- **API Gateway:** Traefik (request routing)
- **Identity & Access Management:** Keycloak
  - RBAC (Role-Based Access Control)
  - 2FA (Two-Factor Authentication)
  - Single security control point for entire system

#### **Application Layer (Microservices)**
Four independent service groups, each containerized:

1. **Client & Document Service**
   - Document ingestion and OCR (Docling + Tesseract)
   - Client data management
   - Evidence storage coordination

2. **Financial Analytics Service**
   - Ratio calculations (Pandas, NumPy)
   - Trend analysis
   - Variance analysis
   - Materiality computation
   - Data visualization

3. **Risk & Rules Engine Service**
   - Deterministic IR/CR/ROMM scoring
   - Risk ranking algorithms
   - Independent of AI service (fallback capability)
   - Custom Python rules engine

4. **AI Reasoning Service**
   - Claude 3.5 Sonnet API integration
   - ChromaDB for vector search and context retrieval
   - Draft document generation
   - Recommendation engine
   - Summary and analysis tools

#### **Data & Storage Layer**
- **Relational Database:** PostgreSQL (structured records)
- **Vector Store:** ChromaDB (semantic search and context)
- **Object Storage:** MinIO (evidence and document files)
- **Cache & Task Queue:** Redis + Celery (async tasks)
- **Observability:** Prometheus + Grafana

### Technology Stack

| Layer | Technology |
|-------|-----------|
| **Frontend** | HTML5, Bootstrap/React, JavaScript |
| **API Gateway** | Traefik |
| **Identity & Auth** | Keycloak (RBAC, 2FA) |
| **Backend Services** | Python, Django, Django REST Framework |
| **Document Processing** | Docling, Tesseract OCR |
| **Data Processing** | Pandas, NumPy |
| **Vector Embeddings** | sentence-transformers (all-MiniLM-L6-v2) |
| **AI/LLM** | Claude 3.5 Sonnet API |
| **Vector Database** | ChromaDB (self-hosted) |
| **Database** | PostgreSQL |
| **Object Storage** | MinIO |
| **Caching/Queues** | Redis, Celery |
| **Workpaper Gen** | python-docx, ReportLab |
| **Containerization** | Docker, Docker Compose |
| **CI/CD** | GitHub Actions |
| **Code Security** | Semgrep |
| **Monitoring** | Prometheus, Grafana |
| **Version Control** | Git, GitHub |

### Architectural Design Principles

**Key Design Idea:** Risk scoring and analytics function independently of AI services
- If Claude API is unavailable, materiality and risk calculations still work
- AI only enhances outputs with drafted memos and recommendations
- Maintains system reliability and professional judgment autonomy

**Data Flow Pattern:**
1. Auditor uploads engagement data
2. System pre-processes and cleans data
3. Analytics engine calculates ratios, trends, materiality
4. Risk engine computes IR/CR/ROMM deterministically
5. AI service generates recommendations based on calculated data
6. Dashboard and reports aggregate all outputs
7. Auditor reviews and approves all AI-generated content

---

## WORKFLOW & PROCESS FLOW

### Audit Planning Workflow (5 Stages)

#### **Stage 1: Data Collection (Audit Inputs)**
- Client and engagement information (entity name, year-end, industry, type)
- Financial statements and trial balance (CSV/Excel upload or manual entry)
- Prior-year figures and comparative data
- Internal control information (processes, activities, owners)
- Risk and materiality parameters
- Interview notes from auditors and specialists

#### **Stage 2: Data Pre-Processing (Planning Data Preparation)**
- Data cleaning and validation
- Duplicate removal
- Missing value handling
- Account balance mapping to standard categories
- Standardization of control descriptions and risk ratings
- Formatting interview notes for AI analysis

#### **Stage 3: Analytics & AI-Assisted Planning**
- **Planning Analytics:**
  - Ratio analysis (liquidity, solvency, profitability, efficiency)
  - Trend analysis (year-over-year comparisons)
  - Variance analysis (budget vs. actual)
  - Identification of significant fluctuations

- **Risk Assessment:**
  - Inherent Risk scoring by account/cycle
  - Control Risk assessment
  - ROMM calculation
  - High-risk area identification

- **AI-Assisted Support:**
  - Summary of planning findings
  - Summarized interview notes
  - Suggested audit procedures based on risk profiles
  - Draft planning memorandums
  - Workpaper templates and recommendations

#### **Stage 4: Database Storage (Audit Planning Repository)**
- Client and engagement records storage
- Financial datasets and analytics results
- Control descriptions and risk scores
- AI-generated drafts and recommendations
- User accounts, roles, and activity logs
- Complete audit trail

#### **Stage 5: Decision Support System (User Interface & Outputs)**
- Interactive dashboards (materiality, risk scores, high-risk accounts, progress)
- Planning documents (memorandums, risk summaries, audit plans)
- Analytics visualization (graphs, trends, risk levels)
- Alerts and prompts for incomplete items
- Task tracking and supervisor sign-off
- Report generation and export

### Planning Phase Activities (Detailed)

**Client Setup**
- Create entity file for client (auditee)
- Import/enter client data, charts of accounts
- Store financial statements and prior year files
- Establish permanent client record for multi-year audits

**Risk Assessment**
- Understand auditee operations and business context
- Conduct current year vs. prior year financial comparatives
- Perform budget-to-actuals analysis
- System tools assist these procedures including AI analysis
- Determine materiality levels

**Scope Definition**
- Document operational process walkthroughs
- Identify and assess internal controls (existence and effectiveness)
- System analyzes walkthroughs to flag control weaknesses
- Assign team roles and responsibilities
- Set milestone deadlines and task assignments
- Track project progress

**Program Creation**
- Design audit programs based on risk assessment
- Select standard audit programs and checklists
- Develop testing procedures
- Create test methodology based on materiality and risk
- Devise comprehensive audit strategy and audit plan

---

## AUDIT PROCESS CONTEXT (From Background-Audit Document)

### Full Audit Phases (System Foundation for Future Expansion)
1. **Planning Phase** (Current Implementation)
   - Client setup and data management
   - Risk assessment and materiality determination
   - Scope definition and team assignment
   - Audit program creation

2. **Execution Phase** (Future)
   - Data collection and evidence gathering
   - Substantive and controls testing
   - Workpaper documentation
   - Review and sign-off

3. **Reporting Phase** (Future)
   - Issue summary and findings
   - Draft audit report
   - Final sign-off and archiving

### Reference Framework
- **Audit Software Reference:** TeamMate (industry standard)
- **Standards:** INTOSAI principles of public-sector auditing
- **Scope:** NCDC's internal audit function
  - Chief Internal Auditor (CIA) leadership
  - Senior Internal Auditors (SIAs)
  - 3 audit teams: Financial, Systems, Compliance & Investigations

---

## SYSTEM USERS & ROLES

### Primary Actors

**Auditor**
- Login access with 2FA
- Create new engagements
- Upload financial data and control information
- Perform planning analytics
- Record and assess internal controls
- Input risk assessments
- Request AI-generated planning outputs
- Upload and view documents
- Review and edit AI outputs
- Create and manage tasks
- Generate and export reports

**Supervisor**
- Login and review access
- Monitor engagements and progress
- Examine dashboards and reports
- Review AI outputs quality
- Approve or sign-off on planning documents
- Comment and provide feedback
- Ensure compliance with audit standards

### Secondary Actors
- **Client/Auditee:** Information provider (indirect interaction)
- **System Administrator:** Manage users and system configuration

---

## IMPLEMENTATION APPROACH & PROJECT PLAN

### Methodology: **Agile (Scrum)**
- Iterative development with 2-4 week sprints
- Incremental feature delivery
- Continuous testing and feedback integration
- Well-suited for 10-week development timeline

### 10-Week Development Schedule

| Week | Activity | Deliverable |
|------|----------|------------|
| 1 | Project proposal, requirements gathering, literature review | Approved proposal |
| 2 | System analysis and requirements specification | System requirements documentation |
| 3 | System architecture, database, API, and UI design | Design documentation |
| 4 | Database implementation and backend setup | Functional database and backend |
| 5 | Financial data processing module development | Data processing module |
| 6 | Machine Learning and risk scoring model | Risk scoring module |
| 7 | Dashboard and reporting module development | User dashboard prototype |
| 8 | System integration and API testing | Integrated system prototype |
| 9 | System testing, debugging, and refinement | Tested and refined system |
| 10 | Documentation, final report, and presentation | Final project submission |

### Key Deliverables
1. Approved project proposal with objectives and plan
2. Comprehensive literature review
3. System requirements specification (functional & non-functional)
4. System design documentation (architecture, database, APIs, UI prototypes)
5. Fully functional PostgreSQL database
6. Working backend API with Django
7. Data processing and analytics modules
8. Risk assessment and scoring engine
9. Interactive dashboards and reporting
10. Comprehensive system testing report
11. Complete documentation and final project report
12. Working prototype demonstration

---

## TECHNOLOGY STACK SUMMARY

### Frontend Development
- **Framework:** Bootstrap or React
- **Language:** JavaScript, HTML5, CSS3

### Backend & APIs
- **Framework:** Django + Django REST Framework
- **Language:** Python 3.x
- **API Gateway:** Traefik
- **Authentication:** Keycloak (with RBAC and 2FA)

### Data Processing & Analytics
- **Libraries:** Pandas, NumPy
- **OCR & Document Processing:** Docling, Tesseract
- **Workpaper Generation:** python-docx, ReportLab

### AI & Machine Learning
- **LLM Provider:** Claude 3.5 Sonnet (OpenAI API integration)
- **Vector Search:** ChromaDB (self-hosted)
- **Embeddings:** sentence-transformers (all-MiniLM-L6-v2)
- **Rules Engine:** Custom Python implementation

### Database & Storage
- **Relational:** PostgreSQL
- **Object Storage:** MinIO
- **Vector Store:** ChromaDB
- **Cache:** Redis
- **Task Queue:** Celery

### DevOps & Deployment
- **Containerization:** Docker, Docker Compose
- **CI/CD:** GitHub Actions
- **Code Security:** Semgrep
- **Monitoring:** Prometheus, Grafana
- **Version Control:** Git, GitHub

### Development Tools
- **IDE:** Visual Studio Code
- **Platform:** Docker-based microservices
- **Optional Scale:** k3s (lightweight Kubernetes)

---

## AUDIT & COMPLIANCE REQUIREMENTS

### Compliance Objectives
- Ensure accountability in public fund usage
- Promote transparency in government operations
- Support good governance and public confidence
- Comply with INTOSAI principles of public-sector auditing
- Maintain audit trail for accountability
- Support independence and professional judgment

### Data Protection & Security
- Secure storage of sensitive financial information
- Access control based on roles and responsibilities
- Audit trail for all actions and changes
- Encryption of data in transit (HTTPS) and at rest
- Two-factor authentication for user access

### Documentation & Evidence Management
- Centralized storage of audit evidence
- Timestamped action logs
- Approval workflows with digital sign-off
- Audit trail demonstrating review and authorization
- Export capabilities for regulatory reporting

---

## IMPLEMENTATION NOTES & RECOMMENDATIONS

### Key Success Factors (from "To my project implementation" document)

1. **Structured Implementation Plan Needed**
   - Clear phases from setup to testing and deployment
   - Essential for maintenance and progress tracking
   - Enables clear understanding of next steps

2. **Microservice Architecture Benefits**
   - Independent service deployment and scaling
   - Resilience (one service failure doesn't crash system)
   - Flexibility for future expansion to Execution and Reporting phases
   - Docker containerization ensures consistency

3. **AI as Decision Support, Not Replacement**
   - All AI outputs must be reviewed by auditors
   - System enhances, not replaces, professional judgment
   - Maintains auditor accountability and control

4. **Fallback Design Pattern**
   - Risk engine works without AI service
   - Ensures system reliability for critical operations
   - Graceful degradation when external services unavailable

5. **Scalability & Future Expansion**
   - Current implementation covers planning phase
   - Architecture supports future addition of:
     - Execution phase (fieldwork and testing)
     - Reporting phase (findings and audit opinions)
   - k3s option for scaling beyond Docker Compose

### Risk Mitigation Strategies
- API reliability: Fallback to deterministic risk scoring
- Data quality: Comprehensive data validation and cleansing
- User adoption: Intuitive UI and minimal training requirements
- Security: Multiple layers (Keycloak, HTTPS, encryption, audit trail)

### Integration Considerations
- Future integration with NCDC's accounting/ERP systems
- Extensibility for additional audit procedures or business logic
- Modular design allows plugin architecture for custom requirements
- API-driven approach supports integration with other tools

---

## PROJECT CONTEXT & SIGNIFICANCE

### Organization Profile: NCDC
- **Type:** Local Government Authority
- **Responsibility:** Governing and managing Port Moresby, Papua New Guinea's capital
- **Services:** Infrastructure development, sanitation, public health, urban planning
- **Financial Scale:** Large number of financial transactions requiring regular auditing

### Internal Audit Function
- **Structure:** Chief Internal Auditor + 3 teams (Financial, Systems, Compliance)
- **Teams:** Each has Senior Internal Auditor + 2 Internal Auditors
- **Challenges:** Manual processes, high volume, complexity, resource constraints

### Strategic Importance
- **Digital Transformation:** Part of PNG public sector modernization
- **Governance:** Strengthens transparency and accountability in government
- **Efficiency Gains:** Reduces audit time and manual effort significantly
- **Quality Improvement:** Ensures consistent and professional audit approach
- **Scalability:** Foundation for similar implementations in other PNG agencies

---

## SUMMARY MATRIX

| Aspect | Details |
|--------|---------|
| **Project Name** | Intelligent Audit Planning and Risk Assessment System (IAPS) |
| **Organization** | NCDC (National Capital District Commission), Papua New Guinea |
| **Developer** | Jerry Lelumai (Year 4 Computer Science Student) |
| **Duration** | 10 weeks (Agile/Scrum) |
| **Phase Focus** | Planning phase only (foundation for future execution/reporting) |
| **Primary Users** | Auditors, Supervisors |
| **Core Value Prop** | Automate audit planning, improve efficiency, enable AI-assisted decision support |
| **Architecture** | Microservices with API Gateway, 3-tier design |
| **Tech Stack** | Python/Django, PostgreSQL, React/Bootstrap, Docker, Claude 3.5 Sonnet |
| **Key Features** | 12 major feature areas (auth, analytics, risk, AI, dashboards, etc.) |
| **AI Integration** | Claude 3.5 Sonnet for recommendations, document generation, summarization |
| **Database Entities** | 8 core: User, Client, Engagement, FinancialData, Control, RiskAssessment, AIOutput, Document |
| **Security Model** | Keycloak (RBAC + 2FA), HTTPS, audit trail |
| **Status** | Year 4 capstone project - actively under implementation |

---

## CONCLUSION

The Intelligent Audit Planning and Risk Assessment System (IAPS) represents a significant digital transformation initiative for NCDC. By integrating advanced technologies like AI/ML, financial analytics, and centralized document management, the system addresses critical inefficiencies in manual, spreadsheet-based audit processes.

The project demonstrates a well-thought-out approach to:
- **Problem-Solving:** Directly addresses NCDC's audit planning challenges
- **Technology Integration:** Thoughtfully combines multiple technologies (AI, analytics, security)
- **User-Centric Design:** Maintains auditor control and professional judgment
- **Scalability:** Designed as foundation for future expansion
- **Governance:** Supports accountability and transparency in public sector operations

The 10-week implementation timeline with Agile methodology, combined with modern microservices architecture and careful attention to security, usability, and reliability requirements, positions IAPS as a practical and effective solution for modernizing audit functions in PNG's public sector.
