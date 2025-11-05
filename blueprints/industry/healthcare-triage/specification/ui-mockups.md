# Healthcare AI Triage System - UI Mockups

**Token-efficient interface specifications using standardized ASCII box-drawing characters**

This document provides comprehensive UI mockups for the Healthcare AI Triage System using the KAPI ASCII mockup standard. These specifications enable clear visual understanding while minimizing token usage and providing direct implementation guidance.

## Design Principles

- **Clinical Workflow Optimization**: Interfaces designed for high-pressure healthcare environments
- **HIPAA Compliance**: Clear data handling and access control indicators
- **Accessibility**: WCAG 2.1 AA compliance with keyboard navigation
- **Mobile Responsive**: Adaptable layouts for tablets and mobile devices
- **Real-time Updates**: Live data synchronization and notification systems

## Color Scheme & Theming

```
Primary Colors:
- Emergency Red: #DC2626 (ESI Level 1-2, Critical alerts)
- Medical Blue: #2563EB (Primary actions, Navigation)
- Warning Amber: #D97706 (ESI Level 3, Cautions)
- Success Green: #059669 (Completed actions, ESI Level 4-5)
- Neutral Gray: #6B7280 (Secondary text, Borders)

Status Indicators:
- Critical: 🔴 Red indicator
- High: 🟡 Yellow/Amber indicator  
- Normal: 🟢 Green indicator
- Info: 🔵 Blue indicator
```

---

## 1. Patient Registration Interface

### New Patient Registration
```
┌─────────────────────────────────────────────────────────────────┐
│  🏥 Healthcare AI Triage - New Patient Registration            │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  📋 Patient Information                                         │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │ 🔍 Search Existing: [________________] [Search]        │   │
│  │                                                         │   │
│  │ 📝 New Patient Registration:                           │   │
│  │                                                         │   │
│  │ First Name: [_____________] Last Name: [_____________] │   │
│  │ DOB: [MM/DD/YYYY] Gender: [Male ▼] MRN: [Auto-Gen]   │   │
│  │                                                         │   │
│  │ 📞 Contact Information:                                │   │
│  │ Phone: [(___) ___-____] Email: [_______________]       │   │
│  │                                                         │   │
│  │ 🏠 Address:                                            │   │
│  │ Street: [_________________________________]            │   │
│  │ City: [_____________] State: [TX ▼] ZIP: [_____]      │   │
│  │                                                         │   │
│  │ 🚨 Emergency Contact:                                  │   │
│  │ Name: [_____________] Relationship: [Spouse ▼]        │   │
│  │ Phone: [(___) ___-____]                                │   │
│  │                                                         │   │
│  │ 💳 Insurance (Optional):                               │   │
│  │ Provider: [_____________] ID: [_____________]          │   │
│  │                                                         │   │
│  │ [🔒 Privacy Notice] [✅ Consent Forms]                 │   │
│  │                                                         │   │
│  │ [Clear] [📄 Save Draft] [✅ Register Patient]         │   │
│  └─────────────────────────────────────────────────────────┘   │
│                                                                 │
│  🔐 Security: All data encrypted • HIPAA compliant logging     │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### Patient Search and Selection
```
┌─────────────────────────────────────────────────────────────────┐
│  🔍 Patient Search Results                                      │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  Search: "John Doe" • Found 3 matches                          │
│                                                                 │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │ 👤 SMITH, JOHN MICHAEL                                 │   │
│  │ MRN: MRN-2024-001234 • DOB: 06/15/1985 • Male         │   │
│  │ Phone: (555) 123-4567 • Last Visit: 03/15/2024        │   │
│  │ ⚠️  Allergies: Penicillin • Insurance: Blue Cross      │   │
│  │ [Select Patient] [View History] [Update Info]          │   │
│  └─────────────────────────────────────────────────────────┘   │
│                                                                 │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │ 👤 DOE, JOHN WILLIAM                                   │   │
│  │ MRN: MRN-2024-005678 • DOB: 08/22/1990 • Male         │   │
│  │ Phone: (555) 987-6543 • Last Visit: 01/10/2024        │   │
│  │ 🟢 No known allergies • Insurance: Aetna               │   │
│  │ [Select Patient] [View History] [Update Info]          │   │
│  └─────────────────────────────────────────────────────────┘   │
│                                                                 │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │ 👤 JOHNSON, JOHN ROBERT                                │   │
│  │ MRN: MRN-2024-009876 • DOB: 12/03/1978 • Male         │   │
│  │ Phone: (555) 456-7890 • Last Visit: 11/20/2023        │   │
│  │ ⚠️  Diabetes, Hypertension • Insurance: Medicare       │   │
│  │ [Select Patient] [View History] [Update Info]          │   │
│  └─────────────────────────────────────────────────────────┘   │
│                                                                 │
│  [🔍 Refine Search] [➕ Register New Patient] [❌ Cancel]      │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## 2. Triage Assessment Interface

### Initial Triage Assessment
```
┌─────────────────────────────────────────────────────────────────┐
│  🏥 Emergency Triage Assessment - SMITH, John M.               │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  👤 Patient: John Smith • MRN: MRN-2024-001234 • Age: 39      │
│  🕐 Arrival: 14:32 • Method: Walk-in • Nurse: Sarah Johnson   │
│                                                                 │
│  📝 Chief Complaint & History                                  │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │ What brings you in today?                               │   │
│  │ [____________________________________________]          │   │
│  │ [____________________________________________]          │   │
│  │ [____________________________________________]          │   │
│  │                                                         │   │
│  │ When did symptoms start? [2 hours ago ▼]               │   │
│  │ Pain level (0-10): [●●●●●○○○○○] 5/10                   │   │
│  │                                                         │   │
│  │ 🤖 AI Assistant: "I understand you're experiencing     │   │
│  │ chest discomfort. Can you describe the pain? Is it     │   │
│  │ sharp, crushing, burning, or aching?"                  │   │
│  └─────────────────────────────────────────────────────────┘   │
│                                                                 │
│  🩺 Vital Signs                                                │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │ Temperature: [98.6°F] BP: [140/90 mmHg] ⚠️              │   │
│  │ Heart Rate: [88 BPM] Resp: [20/min] O2 Sat: [95%] ⚠️   │   │
│  │ Weight: [185 lbs] Height: [5'10"]                       │   │
│  │                                                         │   │
│  │ 🟡 Alert: Elevated BP and low O2 saturation detected   │   │
│  │ [📊 Trend Chart] [🔄 Retake Vitals] [📝 Add Notes]    │   │
│  └─────────────────────────────────────────────────────────┘   │
│                                                                 │
│  🧠 AI Triage Assessment                                       │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │ 🎯 Preliminary ESI Level: 2 (High Risk)                │   │
│  │ 🤖 Confidence: 92%                                     │   │
│  │                                                         │   │
│  │ 📋 Recommended Actions:                                 │   │
│  │ • Immediate 12-lead ECG                                │   │
│  │ • Continuous cardiac monitoring                        │   │
│  │ • IV access and blood draw                             │   │
│  │ • Chest X-ray                                          │   │
│  │                                                         │   │
│  │ ⚠️  Red Flags Detected:                                 │   │
│  │ • Chest pain with hemodynamic changes                  │   │
│  │ • Potential acute coronary syndrome                    │   │
│  └─────────────────────────────────────────────────────────┘   │
│                                                                 │
│  [🔍 View Protocols] [📞 Call Provider] [✅ Complete Triage]   │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### Quick Triage Dashboard
```
┌─────────────────────────────────────────────────────────────────┐
│  🏥 Emergency Department - Live Triage Dashboard               │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  📊 Current Status • Updated: 14:35:22                         │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │ 🔴 ESI 1: 1 patient  🟡 ESI 2: 3 patients              │   │
│  │ 🟠 ESI 3: 7 patients  🟢 ESI 4: 4 patients              │   │
│  │ ⚪ ESI 5: 2 patients  ⏱️  Avg Wait: 23 min              │   │
│  └─────────────────────────────────────────────────────────┘   │
│                                                                 │
│  🎯 Active Triage Queue                                        │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │ 🔴 TRAUMA BAY 1    │ WILSON, Sarah    │ ESI 1 │ 00:05   │   │
│  │ 💔 Cardiac arrest  │ Age: 67          │       │         │   │
│  │ ────────────────────────────────────────────────────────│   │
│  │ 🟡 BED 3          │ GARCIA, Miguel   │ ESI 2 │ 00:12   │   │
│  │ 🫁 Chest pain     │ Age: 45          │       │         │   │
│  │ ────────────────────────────────────────────────────────│   │
│  │ 🟡 BED 7          │ CHEN, Lisa       │ ESI 2 │ 00:08   │   │
│  │ 🤕 Head injury    │ Age: 32          │       │         │   │
│  │ ────────────────────────────────────────────────────────│   │
│  │ 🟠 WAITING ROOM   │ BROWN, David     │ ESI 3 │ 00:34   │   │
│  │ 🤒 Fever/cough    │ Age: 28          │       │         │   │
│  │ ────────────────────────────────────────────────────────│   │
│  │ 🟠 FAST TRACK     │ JONES, Emily     │ ESI 3 │ 00:15   │   │
│  │ 🦵 Ankle sprain   │ Age: 24          │       │         │   │
│  └─────────────────────────────────────────────────────────┘   │
│                                                                 │
│  [➕ New Patient] [🔄 Refresh] [📊 Reports] [⚙️ Settings]      │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## 3. AI Agent Interaction Interface

### Multi-Agent Conversation
```
┌─────────────────────────────────────────────────────────────────┐
│  🤖 AI Triage Agents - Patient: SMITH, John M.                 │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  🧠 Agent Status: All systems operational • Response time: 1.2s│
│                                                                 │
│  💬 Conversation History                                        │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │ 👨‍⚕️ Nurse Sarah: Patient reports severe chest pain       │   │
│  │ 14:30                                                   │   │
│  │                                                         │   │
│  │ 🤖 Intake Agent: I'll help gather comprehensive        │   │
│  │ symptom information. Can you tell me:                  │   │
│  │ • When did the chest pain start?                       │   │
│  │ • Rate the pain from 1-10                              │   │
│  │ • Does anything make it better or worse?               │   │
│  │ 14:30 • Confidence: 95%                                │   │
│  │                                                         │   │
│  │ 👨‍⚕️ Nurse Sarah: Started 2 hours ago, 7/10 intensity, │   │
│  │ radiating to left arm, worse with movement             │   │
│  │ 14:31                                                   │   │
│  │                                                         │   │
│  │ 🧠 Knowledge Agent: Based on symptoms, reviewing:      │   │
│  │ • Acute coronary syndrome protocols                    │   │
│  │ • Chest pain differential diagnosis                    │   │
│  │ • Current medications: Lisinopril, Metformin          │   │
│  │ 14:31 • Knowledge base: 847 relevant articles          │   │
│  │                                                         │   │
│  │ 🎯 Triage Agent: Assessment complete:                  │   │
│  │ • ESI Level 2 (High Priority)                          │   │
│  │ • Immediate cardiac workup indicated                   │   │
│  │ • Estimated bed assignment: 8 minutes                  │   │
│  │ 14:32 • Confidence: 92%                                │   │
│  │                                                         │   │
│  │ 🚨 Escalation Agent: Notifying:                        │   │
│  │ • Dr. Martinez (Cardiology) - Paged                    │   │
│  │ • Charge Nurse - Bed assignment pending               │   │
│  │ • Lab/Radiology - Orders queued                        │   │
│  │ 14:32 • All notifications sent successfully            │   │
│  └─────────────────────────────────────────────────────────┘   │
│                                                                 │
│  💬 Ask the AI Team:                                           │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │ [____________________________________________________]  │   │
│  │ "What are the contraindications for nitroglycerin?"    │   │
│  │                                                         │   │
│  │ 🎯 Quick Actions:                                       │   │
│  │ [Drug Interactions] [Treatment Protocols] [Guidelines] │   │
│  │ [ESI Recalculation] [Provider Notification] [Notes]    │   │
│  └─────────────────────────────────────────────────────────┘   │
│                                                                 │
│  🔄 Agent Performance: Intake(1.1s) Triage(0.8s) Knowledge(2.1s)│
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### Knowledge Search Interface
```
┌─────────────────────────────────────────────────────────────────┐
│  🧠 Medical Knowledge Search                                    │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  🔍 Search: "chest pain protocol emergency department"          │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │ 📊 Results: 23 protocols • 156 articles • 34 guidelines   │   │
│  │ 🎯 Relevance: 95% • Search time: 0.3s                     │   │
│  └─────────────────────────────────────────────────────────┘   │
│                                                                 │
│  📚 Top Results                                                │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │ 🏥 AHA/ACC Chest Pain Protocol (2023)                  │   │
│  │ • Emergency department acute chest pain evaluation     │   │
│  │ • Evidence Level: A • Updated: 03/2023                 │   │
│  │ • Risk stratification and treatment pathways           │   │
│  │ [📖 View Full Protocol] [⭐ Save] [📤 Share]           │   │
│  │ ─────────────────────────────────────────────────────── │   │
│  │ 💊 Contraindications: Nitroglycerin                    │   │
│  │ • Hypotension (SBP < 90 mmHg)                          │   │
│  │ • Recent PDE5 inhibitor use (24-48 hours)             │   │
│  │ • Severe aortic stenosis                               │   │
│  │ [📖 View Details] [⚠️ Add Alert] [🔗 Related Drugs]   │   │
│  │ ─────────────────────────────────────────────────────── │   │
│  │ 🧬 Drug Interaction: Metformin + Contrast             │   │
│  │ • Hold metformin 48 hours post-contrast               │   │
│  │ • Monitor renal function • Risk: Lactic acidosis      │   │
│  │ [⚠️ Patient Alert] [📋 Protocol] [📞 Pharmacy]        │   │
│  │ ─────────────────────────────────────────────────────── │   │
│  │ 📈 ESI Level 2 Criteria                                │   │
│  │ • High-risk chest pain with normal vitals             │   │
│  │ • Target time to physician: 10 minutes                │   │
│  │ • Required monitoring: Continuous cardiac             │   │
│  │ [✅ Apply Protocol] [📊 Track Compliance] [📝 Notes]  │   │
│  └─────────────────────────────────────────────────────────┘   │
│                                                                 │
│  🔍 [Refine Search] [📌 Save Search] [📊 Analytics] [❌ Close] │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## 4. Provider Dashboard Interface

### Physician Overview Dashboard
```
┌─────────────────────────────────────────────────────────────────┐
│  👨‍⚕️ Dr. Martinez - Emergency Medicine Dashboard                │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  📊 Shift Overview • 7:00 AM - 7:00 PM • Patients Seen: 14    │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │ 🎯 My Queue (5 patients)  ⏱️ Avg Time/Patient: 18 min     │   │
│  │ 📈 Efficiency: 92%        🎯 Quality Score: 4.8/5        │   │
│  └─────────────────────────────────────────────────────────┘   │
│                                                                 │
│  🚨 Priority Alerts                                            │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │ 🔴 CRITICAL: Bed 3 - GARCIA, Miguel                    │   │
│  │ • ST elevation on ECG • Cardiology consult requested   │   │
│  │ • Door-to-balloon time: 47 minutes                     │   │
│  │ [🏃‍♂️ Respond Now] [📞 Call Cath Lab] [📋 Orders]      │   │
│  │ ─────────────────────────────────────────────────────── │   │
│  │ 🟡 HIGH: Bed 7 - CHEN, Lisa                            │   │
│  │ • Head CT shows cerebral edema • Neurosurg notified    │   │
│  │ • ICP monitoring recommended                            │   │
│  │ [👀 Review] [📞 Call Neuro] [📝 Document]              │   │
│  └─────────────────────────────────────────────────────────┘   │
│                                                                 │
│  📋 Patient Queue                                              │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │ Bed │ Patient        │ Chief Complaint │ ESI │ Wait      │   │
│  │ ──── │ ────────────── │ ─────────────── │ ─── │ ──────    │   │
│  │ 3    │ GARCIA, M.(45) │ Chest pain      │ 2   │ ⏰ 52min │   │
│  │ 7    │ CHEN, L.(32)   │ Head injury     │ 2   │ ⏰ 45min │   │
│  │ 12   │ BROWN, D.(28)  │ Fever/cough     │ 3   │ ⏱️ 28min │   │
│  │ 15   │ TAYLOR, R.(65) │ Abdominal pain  │ 3   │ ⏱️ 15min │   │
│  │ FT-2 │ JONES, E.(24)  │ Ankle sprain    │ 4   │ ⏱️ 8min  │   │
│  └─────────────────────────────────────────────────────────┘   │
│                                                                 │
│  🤖 AI Recommendations                                         │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │ • Consider bed reassignment for Garcia (Bed 3→CCU)     │   │
│  │ • Brown's symptoms suggest viral syndrome - rapid test │   │
│  │ • Jones cleared for discharge with ankle care plan     │   │
│  │ • 3 patients ready for disposition review              │   │
│  └─────────────────────────────────────────────────────────┘   │
│                                                                 │
│  [📊 Analytics] [👥 Handoff] [📞 Consults] [⚙️ Preferences]   │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### Quality Metrics Dashboard
```
┌─────────────────────────────────────────────────────────────────┐
│  📊 Department Quality Metrics - Emergency Medicine            │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  📈 Real-time Performance (Last 24 Hours)                      │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │ 🎯 Target vs Actual Performance                            │   │
│  │                                                         │   │
│  │ ESI 1 (Resuscitation): Target <1min    Actual: 0.8min ✅│   │
│  │ ████████████████████████████████████████████████████    │   │
│  │                                                         │   │
│  │ ESI 2 (Emergent): Target <10min        Actual: 8.2min ✅│   │
│  │ ████████████████████████████████████████████            │   │
│  │                                                         │   │
│  │ ESI 3 (Urgent): Target <30min          Actual: 34min ⚠️ │   │
│  │ ████████████████████████████████████████████████████    │   │
│  │                                                         │   │
│  │ Door-to-Provider: Target <20min        Actual: 16min ✅ │   │
│  │ ████████████████████████████████████                    │   │
│  │                                                         │   │
│  │ Length of Stay: Target <4hrs           Actual: 3.2hrs ✅│   │
│  │ ████████████████████████████                            │   │
│  └─────────────────────────────────────────────────────────┘   │
│                                                                 │
│  🤖 AI System Performance                                      │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │ Triage Accuracy: 94.2% ✅     Response Time: 1.8s ✅    │   │
│  │ Agent Confidence: 91.5% ✅     Error Rate: 0.3% ✅      │   │
│  │ Knowledge Retrieval: 0.4s ✅  User Satisfaction: 4.7/5 ✅│   │
│  └─────────────────────────────────────────────────────────┘   │
│                                                                 │
│  📊 Patient Flow Analytics                                     │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │           Today's Volume by Hour                        │   │
│  │   30 |     ▅                                           │   │
│  │   25 |   ▅ █ ▅                                         │   │
│  │   20 | ▅ █ █ █ ▅                                       │   │
│  │   15 | █ █ █ █ █ ▅ ▅                                   │   │
│  │   10 | █ █ █ █ █ █ █ ▅ ▅                               │   │
│  │    5 | █ █ █ █ █ █ █ █ █ ▅ ▅                           │   │
│  │    0 └─┴─┴─┴─┴─┴─┴─┴─┴─┴─┴─┴─┴─┴─┴─┴─┴─┴─┴─┴─┴─┴─┴─┴─│   │
│  │      6a 8a 10a 12p 2p 4p 6p 8p 10p 12a 2a 4a 6a       │   │
│  │                                                         │   │
│  │ Peak Hours: 10a-2p • Lowest: 2a-6a • Avg Wait: 23min  │   │
│  └─────────────────────────────────────────────────────────┘   │
│                                                                 │
│  [📈 Detailed Reports] [🎯 Quality Improvement] [📊 Export]    │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## 5. Mobile Responsive Interface

### Mobile Triage Assessment
```
┌─────────────────────────┐
│  🏥 Triage - SMITH, J.  │
├─────────────────────────┤
│                         │
│ 👤 MRN: MRN-2024-001234 │
│ 🕐 14:32 • Walk-in      │
│                         │
│ 📝 Chief Complaint:     │
│ ┌─────────────────────┐ │
│ │ Chest pain, 2hrs    │ │
│ │ ago, 7/10 severity  │ │
│ └─────────────────────┘ │
│                         │
│ 🩺 Vitals:              │
│ • BP: 140/90 ⚠️         │
│ • HR: 88 • T: 98.6°F   │
│ • RR: 20 • O2: 95% ⚠️   │
│                         │
│ 🤖 AI Assessment:       │
│ ┌─────────────────────┐ │
│ │ 🟡 ESI Level 2      │ │
│ │ High Priority       │ │
│ │ Confidence: 92%     │ │
│ │                     │ │
│ │ 📋 Actions:         │ │
│ │ • ECG immediately   │ │
│ │ • IV access         │ │
│ │ • Cardiac monitor   │ │
│ └─────────────────────┘ │
│                         │
│ [🔍 Protocols]          │
│ [📞 Call MD]            │
│ [✅ Complete]           │
│                         │
└─────────────────────────┘
```

### Mobile Dashboard
```
┌─────────────────────────┐
│  🏥 ED Dashboard        │
├─────────────────────────┤
│                         │
│ 📊 Current: 14:35       │
│ 🔴 ESI 1: 1  🟡 ESI 2: 3│
│ 🟠 ESI 3: 7  🟢 ESI 4: 4│
│ ⚪ ESI 5: 2  ⏱️ Wait: 23m│
│                         │
│ 🎯 My Queue (5):        │
│                         │
│ 🔴 Bed 3 • GARCIA, M.   │
│ Chest pain • 52min      │
│ [View] [Call] [Orders]  │
│                         │
│ 🟡 Bed 7 • CHEN, L.     │
│ Head injury • 45min     │
│ [View] [Call] [Orders]  │
│                         │
│ 🟠 Bed 12 • BROWN, D.   │
│ Fever/cough • 28min     │
│ [View] [Call] [Orders]  │
│                         │
│ [➕ New] [🔄 Refresh]   │
│ [📊 Reports] [⚙️ Menu]  │
│                         │
└─────────────────────────┘
```

---

## 6. Accessibility Features

### Screen Reader Compatible Interface
```
┌─────────────────────────────────────────────────────────────────┐
│  🏥 Healthcare Triage - Accessibility Mode                     │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  🔊 Screen Reader Navigation:                                   │
│  • Tab Order: Patient Info → Vitals → AI Assessment → Actions │
│  • Keyboard Shortcuts: Ctrl+N (New), Ctrl+S (Save), Esc (Exit)│
│  • Voice Commands: "Start assessment", "Read vitals", "Call MD"│
│                                                                 │
│  🎯 High Contrast Mode                                         │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │ ████ WHITE TEXT ON BLACK BACKGROUND ████                │   │
│  │                                                         │   │
│  │ [PATIENT: SMITH, JOHN]                                  │   │
│  │ [STATUS: ESI LEVEL 2 - HIGH PRIORITY]                  │   │
│  │ [VITAL SIGNS: ABNORMAL - ATTENTION REQUIRED]           │   │
│  │                                                         │   │
│  │ ▓▓▓▓ ACTIONS AVAILABLE ▓▓▓▓                            │   │
│  │ [1] VIEW PROTOCOLS                                      │   │
│  │ [2] CALL PHYSICIAN                                      │   │
│  │ [3] COMPLETE ASSESSMENT                                 │   │
│  └─────────────────────────────────────────────────────────┘   │
│                                                                 │
│  🔤 Large Text Mode (200% zoom)                                │
│  🎨 Color Blind Support (patterns + text labels)              │
│  🖱️ Motor Accessibility (large click targets, sticky drag)    │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## 7. Error States and Notifications

### System Error Interface
```
┌─────────────────────────────────────────────────────────────────┐
│  ⚠️ System Alert - Healthcare Triage                           │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  🔴 CRITICAL SYSTEM ERROR                                       │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │ AI Agent Communication Failure                         │   │
│  │                                                         │   │
│  │ 🤖 Triage Agent: ❌ Offline (Connection Lost)          │   │
│  │ 🧠 Knowledge Agent: ⚠️ Degraded (Slow Response)       │   │
│  │ 📞 Escalation Agent: ✅ Online                         │   │
│  │                                                         │   │
│  │ 🏥 Fallback Mode Activated:                            │   │
│  │ • Manual triage protocols enabled                      │   │
│  │ • Senior nurse notification sent                       │   │
│  │ • All assessments require MD review                    │   │
│  │                                                         │   │
│  │ ⏱️ Estimated Recovery: 3-5 minutes                     │   │
│  │ 📞 IT Support: Extension 5555 (Auto-notified)         │   │
│  │                                                         │   │
│  │ [📖 Manual Protocols] [📞 Call Support] [🔄 Retry]    │   │
│  └─────────────────────────────────────────────────────────┘   │
│                                                                 │
│  ⚠️ Patient Safety Notice:                                      │
│  All current patients have been flagged for immediate manual   │
│  review. No triage decisions should be made without physician  │
│  consultation until systems are restored.                      │
│                                                                 │
│  [🚨 Notify Medical Director] [📋 Incident Report] [❌ Close]  │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### Success and Confirmation States
```
┌─────────────────────────────────────────────────────────────────┐
│  ✅ Assessment Complete - SMITH, John M.                       │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  🎯 Triage Assessment Successfully Completed                    │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │ ✅ Patient: SMITH, John M. (MRN-2024-001234)           │   │
│  │ ✅ ESI Level: 2 (High Priority)                        │   │
│  │ ✅ Bed Assignment: Bed 8 (Cardiac monitoring)          │   │
│  │ ✅ Provider Notification: Dr. Martinez (Notified)      │   │
│  │ ✅ Orders Entered: ECG, CBC, BMP, Troponin, CXR       │   │
│  │                                                         │   │
│  │ 📋 Next Steps Automatically Initiated:                 │   │
│  │ • Continuous cardiac monitoring started                │   │
│  │ • IV access obtained                                   │   │
│  │ • Blood samples drawn                                  │   │
│  │ • ECG completed - results pending                      │   │
│  │                                                         │   │
│  │ ⏱️ Time to Provider: Target 10 min • ETA: 6 minutes    │   │
│  │ 🔄 Status Updates: Real-time via system notifications  │   │
│  └─────────────────────────────────────────────────────────┘   │
│                                                                 │
│  📊 Performance Metrics:                                       │
│  • Assessment Time: 4 minutes 32 seconds                      │
│  • AI Confidence: 92%                                         │
│  • Protocol Compliance: 100%                                  │
│                                                                 │
│  [👀 View Patient] [📊 Track Progress] [➕ Next Patient]      │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## Implementation Notes

### CSS Framework Requirements
```css
/* Key responsive breakpoints */
@media (min-width: 768px) { /* Tablet */ }
@media (min-width: 1024px) { /* Desktop */ }
@media (min-width: 1440px) { /* Large Desktop */ }

/* Accessibility requirements */
:focus { outline: 3px solid #2563EB; }
.high-contrast { background: #000; color: #FFF; }
.large-text { font-size: 1.5rem; }

/* Healthcare-specific colors */
.esi-1 { background-color: #DC2626; } /* Critical Red */
.esi-2 { background-color: #F59E0B; } /* High Amber */
.esi-3 { background-color: #EAB308; } /* Urgent Yellow */
.esi-4 { background-color: #22C55E; } /* Less Urgent Green */
.esi-5 { background-color: #6B7280; } /* Non-urgent Gray */
```

### Interactive Elements
- **Real-time Updates**: WebSocket connections for live data synchronization
- **Voice Input**: Speech-to-text for hands-free operation
- **Barcode Scanning**: Patient ID and medication verification
- **Touch Gestures**: Swipe navigation for mobile devices
- **Keyboard Shortcuts**: Power user efficiency features

### Security Indicators
- **🔒 HIPAA Compliant**: Visual indicators for secure data handling
- **🔐 Encrypted**: End-to-end encryption status display
- **👤 User Session**: Active session and timeout warnings
- **📊 Audit Trail**: Comprehensive logging notifications

---

**These UI mockups provide comprehensive visual specifications for building a production-ready healthcare AI triage system that prioritizes clinical workflow efficiency, patient safety, and regulatory compliance.**