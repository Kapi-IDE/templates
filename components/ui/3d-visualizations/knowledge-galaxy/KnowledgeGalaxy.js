// Knowledge Galaxy Visualization
import * as THREE from 'three';
import { OrbitControls } from 'three/addons/controls/OrbitControls.js';
import { EffectComposer } from 'three/addons/postprocessing/EffectComposer.js';
import { RenderPass } from 'three/addons/postprocessing/RenderPass.js';
import { UnrealBloomPass } from 'three/addons/postprocessing/UnrealBloomPass.js';

// Mock data for knowledge clusters based on domain
const aerospaceClusters = [
  {
    id: 1,
    name: "Design Specifications",
    domain: "engineering",
    size: 32,
    documents: 78,
    updated: "2024-11-08",
    subClusters: [3, 4, 5],
    position: { x: 4, y: 2, z: -3 },
    keyDocuments: [
      { id: 101, title: "System Architecture Overview", type: "PDF" },
      { id: 102, title: "Component Interface Specifications", type: "Excel" },
      { id: 103, title: "Design Constraints Document", type: "Word" }
    ]
  },
  {
    id: 2,
    name: "Manufacturing Processes",
    domain: "manufacturing",
    size: 28,
    documents: 64,
    updated: "2024-11-05",
    subClusters: [6, 7],
    position: { x: -5, y: -1, z: 2 },
    keyDocuments: [
      { id: 201, title: "Assembly Line Configuration", type: "PDF" },
      { id: 202, title: "Quality Control Procedures", type: "Word" },
      { id: 203, title: "Tooling Requirements", type: "Excel" }
    ]
  },
  {
    id: 3,
    name: "Electrical Systems",
    domain: "engineering",
    size: 18,
    documents: 42,
    updated: "2024-10-22",
    subClusters: [],
    position: { x: 7, y: 3, z: -1 },
    keyDocuments: [
      { id: 301, title: "Circuit Diagrams", type: "PDF" },
      { id: 302, title: "Power Distribution Analysis", type: "Excel" }
    ]
  },
  {
    id: 4,
    name: "Mechanical Components",
    domain: "engineering",
    size: 24,
    documents: 56,
    updated: "2024-10-28",
    subClusters: [],
    position: { x: 2, y: -2, z: -5 },
    keyDocuments: [
      { id: 401, title: "Fastener Specifications", type: "PDF" },
      { id: 402, title: "Material Properties Database", type: "Excel" },
      { id: 403, title: "Mechanical Testing Results", type: "Word" }
    ]
  },
  {
    id: 5,
    name: "Software Systems",
    domain: "engineering",
    size: 20,
    documents: 48,
    updated: "2024-11-01",
    subClusters: [],
    position: { x: 6, y: 1, z: -4 },
    keyDocuments: [
      { id: 501, title: "Software Architecture", type: "PDF" },
      { id: 502, title: "API Documentation", type: "Word" },
      { id: 503, title: "Test Coverage Report", type: "Excel" }
    ]
  },
  {
    id: 6,
    name: "Assembly Procedures",
    domain: "manufacturing",
    size: 16,
    documents: 38,
    updated: "2024-10-15",
    subClusters: [],
    position: { x: -7, y: 0, z: 3 },
    keyDocuments: [
      { id: 601, title: "Assembly Instructions", type: "PDF" },
      { id: 602, title: "Torque Specifications", type: "Excel" }
    ]
  },
  {
    id: 7,
    name: "Quality Control",
    domain: "manufacturing",
    size: 14,
    documents: 32,
    updated: "2024-10-18",
    subClusters: [],
    position: { x: -4, y: -3, z: 1 },
    keyDocuments: [
      { id: 701, title: "Inspection Procedures", type: "PDF" },
      { id: 702, title: "Defect Classification Guide", type: "Word" },
      { id: 703, title: "Statistical Process Control", type: "Excel" }
    ]
  },
  {
    id: 8,
    name: "Research Projects",
    domain: "research",
    size: 22,
    documents: 51,
    updated: "2024-11-03",
    subClusters: [9, 10],
    position: { x: 1, y: 5, z: 6 },
    keyDocuments: [
      { id: 801, title: "Research Roadmap", type: "PDF" },
      { id: 802, title: "Experiment Results", type: "Excel" },
      { id: 803, title: "Patent Applications", type: "Word" }
    ]
  },
  {
    id: 9,
    name: "Material Science",
    domain: "research",
    size: 15,
    documents: 36,
    updated: "2024-10-26",
    subClusters: [],
    position: { x: 3, y: 6, z: 4 },
    keyDocuments: [
      { id: 901, title: "Material Testing Results", type: "Excel" },
      { id: 902, title: "New Alloy Specifications", type: "PDF" }
    ]
  },
  {
    id: 10,
    name: "Advanced Electronics",
    domain: "research",
    size: 13,
    documents: 30,
    updated: "2024-10-30",
    subClusters: [],
    position: { x: 0, y: 4, z: 8 },
    keyDocuments: [
      { id: 1001, title: "Semiconductor Research", type: "PDF" },
      { id: 1002, title: "Prototype Test Results", type: "Excel" }
    ]
  },
  {
    id: 11,
    name: "Maintenance Procedures",
    domain: "operations",
    size: 18,
    documents: 43,
    updated: "2024-10-20",
    subClusters: [12, 13],
    position: { x: -2, y: -5, z: -4 },
    keyDocuments: [
      { id: 1101, title: "Maintenance Schedule", type: "Excel" },
      { id: 1102, title: "Repair Guidelines", type: "PDF" },
      { id: 1103, title: "Tool Inventory", type: "Word" }
    ]
  },
  {
    id: 12,
    name: "Preventive Maintenance",
    domain: "operations",
    size: 12,
    documents: 28,
    updated: "2024-10-12",
    subClusters: [],
    position: { x: -3, y: -6, z: -2 },
    keyDocuments: [
      { id: 1201, title: "Inspection Checklists", type: "PDF" },
      { id: 1202, title: "Lubrication Schedules", type: "Excel" }
    ]
  },
  {
    id: 13,
    name: "Repair Procedures",
    domain: "operations",
    size: 10,
    documents: 24,
    updated: "2024-10-16",
    subClusters: [],
    position: { x: -1, y: -4, z: -6 },
    keyDocuments: [
      { id: 1301, title: "Troubleshooting Guide", type: "PDF" },
      { id: 1302, title: "Repair Parts Catalog", type: "Excel" }
    ]
  }
];

const automotiveClusters = [
  {
    id: 1,
    name: "Vehicle Design Specifications",
    domain: "engineering",
    size: 36,
    documents: 85,
    updated: "2024-11-10",
    subClusters: [3, 4, 5],
    position: { x: 4, y: 2, z: -3 },
    keyDocuments: [
      { id: 101, title: "Vehicle Platform Architecture", type: "PDF" },
      { id: 102, title: "Chassis Design Specifications", type: "Excel" },
      { id: 103, title: "Body Design Requirements", type: "Word" }
    ]
  },
  {
    id: 2,
    name: "Production Line Processes",
    domain: "manufacturing",
    size: 32,
    documents: 70,
    updated: "2024-11-08",
    subClusters: [6, 7],
    position: { x: -5, y: -1, z: 2 },
    keyDocuments: [
      { id: 201, title: "Assembly Line Configuration", type: "PDF" },
      { id: 202, title: "JIT Manufacturing Procedures", type: "Word" },
      { id: 203, title: "Robotic Tooling Requirements", type: "Excel" }
    ]
  },
  {
    id: 3,
    name: "Powertrain Systems",
    domain: "engineering",
    size: 22,
    documents: 54,
    updated: "2024-10-25",
    subClusters: [],
    position: { x: 7, y: 3, z: -1 },
    keyDocuments: [
      { id: 301, title: "Engine Schematics", type: "PDF" },
      { id: 302, title: "Transmission Design Specs", type: "Excel" },
      { id: 303, title: "Hybrid Powertrain Integration", type: "Word" }
    ]
  },
  {
    id: 4,
    name: "Suspension & Chassis",
    domain: "engineering",
    size: 26,
    documents: 62,
    updated: "2024-10-29",
    subClusters: [],
    position: { x: 2, y: -2, z: -5 },
    keyDocuments: [
      { id: 401, title: "Suspension Geometry", type: "PDF" },
      { id: 402, title: "Structural Materials Database", type: "Excel" },
      { id: 403, title: "Ride Quality Testing", type: "Word" }
    ]
  },
  {
    id: 5,
    name: "Vehicle Electronics",
    domain: "engineering",
    size: 24,
    documents: 58,
    updated: "2024-11-05",
    subClusters: [],
    position: { x: 6, y: 1, z: -4 },
    keyDocuments: [
      { id: 501, title: "ECU Architecture", type: "PDF" },
      { id: 502, title: "Sensor Network Documentation", type: "Word" },
      { id: 503, title: "Software Testing Protocols", type: "Excel" }
    ]
  },
  {
    id: 6,
    name: "Paint & Finishing",
    domain: "manufacturing",
    size: 18,
    documents: 42,
    updated: "2024-10-18",
    subClusters: [],
    position: { x: -7, y: 0, z: 3 },
    keyDocuments: [
      { id: 601, title: "Paint Shop Procedures", type: "PDF" },
      { id: 602, title: "Corrosion Protection Standards", type: "Excel" },
      { id: 603, title: "Surface Finish Inspection", type: "Word" }
    ]
  },
  {
    id: 7,
    name: "Quality Assurance",
    domain: "manufacturing",
    size: 16,
    documents: 38,
    updated: "2024-10-22",
    subClusters: [],
    position: { x: -4, y: -3, z: 1 },
    keyDocuments: [
      { id: 701, title: "Final Vehicle Inspection", type: "PDF" },
      { id: 702, title: "Defect Classification Standards", type: "Word" },
      { id: 703, title: "Statistical Process Controls", type: "Excel" }
    ]
  },
  {
    id: 8,
    name: "EV Technology Research",
    domain: "research",
    size: 28,
    documents: 64,
    updated: "2024-11-07",
    subClusters: [9, 10],
    position: { x: 1, y: 5, z: 6 },
    keyDocuments: [
      { id: 801, title: "Battery Technology Roadmap", type: "PDF" },
      { id: 802, title: "EV Powertrain Performance Data", type: "Excel" },
      { id: 803, title: "Battery Management Patents", type: "Word" }
    ]
  },
  {
    id: 9,
    name: "Lightweight Materials",
    domain: "research",
    size: 18,
    documents: 42,
    updated: "2024-10-30",
    subClusters: [],
    position: { x: 3, y: 6, z: 4 },
    keyDocuments: [
      { id: 901, title: "Composite Material Testing", type: "Excel" },
      { id: 902, title: "Carbon Fiber Integration", type: "PDF" },
      { id: 903, title: "Aluminum Alloy Development", type: "Word" }
    ]
  },
  {
    id: 10,
    name: "Autonomous Systems",
    domain: "research",
    size: 20,
    documents: 48,
    updated: "2024-11-02",
    subClusters: [],
    position: { x: 0, y: 4, z: 8 },
    keyDocuments: [
      { id: 1001, title: "LIDAR Sensor Integration", type: "PDF" },
      { id: 1002, title: "Machine Vision Test Results", type: "Excel" },
      { id: 1003, title: "AI Decision Logic Documentation", type: "Word" }
    ]
  },
  {
    id: 11,
    name: "Service & Maintenance",
    domain: "operations",
    size: 22,
    documents: 52,
    updated: "2024-10-24",
    subClusters: [12, 13],
    position: { x: -2, y: -5, z: -4 },
    keyDocuments: [
      { id: 1101, title: "Service Interval Schedules", type: "Excel" },
      { id: 1102, title: "Dealer Service Procedures", type: "PDF" },
      { id: 1103, title: "Diagnostic Tool Documentation", type: "Word" }
    ]
  },
  {
    id: 12,
    name: "Warranty Management",
    domain: "operations",
    size: 15,
    documents: 36,
    updated: "2024-10-16",
    subClusters: [],
    position: { x: -3, y: -6, z: -2 },
    keyDocuments: [
      { id: 1201, title: "Warranty Claim Procedures", type: "PDF" },
      { id: 1202, title: "Component Reliability Data", type: "Excel" },
      { id: 1203, title: "Failure Analysis Guidelines", type: "Word" }
    ]
  },
  {
    id: 13,
    name: "Dealer Operations",
    domain: "operations",
    size: 12,
    documents: 28,
    updated: "2024-10-19",
    subClusters: [],
    position: { x: -1, y: -4, z: -6 },
    keyDocuments: [
      { id: 1301, title: "Service Bay Specifications", type: "PDF" },
      { id: 1302, title: "Parts Inventory Management", type: "Excel" },
      { id: 1303, title: "Customer Service Protocols", type: "Word" }
    ]
  }
];

// Set default clusters
let knowledgeClusters = aerospaceClusters;

// Domain-specific knowledge gaps
const aerospaceGaps = [
  {
    id: 101,
    significance: "high",
    connectedClusters: [1, 8],
    identified: "2024-11-04",
    position: { x: 2.5, y: 3.5, z: 1.5 },
    questions: [
      { id: 10101, text: "How do design specifications integrate with research findings?", importance: "high", impact: "Critical for ensuring new research is incorporated into product designs. Could reduce design iterations by 30% if properly addressed." },
      { id: 10102, text: "What mechanisms exist for research feedback to influence design?", importance: "medium", impact: "Would enable more innovative design approaches and improve knowledge transfer between departments." },
      { id: 10103, text: "Are there documented procedures for applying research innovations to design?", importance: "high", impact: "Could resolve significant inefficiencies in the product development cycle and reduce time-to-market." }
    ]
  },
  {
    id: 102,
    significance: "medium",
    connectedClusters: [2, 11],
    identified: "2024-10-25",
    position: { x: -3.5, y: -3, z: -1 },
    questions: [
      { id: 10201, text: "How do manufacturing processes account for maintenance requirements?", importance: "medium", impact: "Could reduce maintenance downtime by designing manufacturing processes with maintenance in mind." },
      { id: 10202, text: "Is there a feedback mechanism from maintenance to manufacturing?", importance: "low", impact: "Would help identify recurring issues that could be addressed in the manufacturing phase." }
    ]
  },
  {
    id: 103,
    significance: "high",
    connectedClusters: [3, 10],
    identified: "2024-11-02",
    position: { x: 3.5, y: 5, z: 3.5 },
    questions: [
      { id: 10301, text: "How are advanced electronics research findings applied to electrical systems?", importance: "high", impact: "Critical for incorporating cutting-edge technology into product electrical systems. Could provide significant competitive advantage." },
      { id: 10302, text: "What is the timeline for research technologies to be implemented in products?", importance: "medium", impact: "Would help create realistic roadmaps and set appropriate customer expectations for feature availability." },
      { id: 10303, text: "Are there compatibility studies between new research and existing electrical systems?", importance: "high", impact: "Could prevent integration issues and reduce costly redesigns later in the development cycle." }
    ]
  },
  {
    id: 104,
    significance: "medium",
    connectedClusters: [4, 7],
    identified: "2024-10-28",
    position: { x: -1, y: -2.5, z: -2 },
    questions: [
      { id: 10401, text: "How do quality control procedures verify mechanical component specifications?", importance: "medium", impact: "Could improve detection of non-conforming parts before they enter the assembly process." },
      { id: 10402, text: "What tolerance standards are applied across mechanical components?", importance: "medium", impact: "Standardized tolerances could improve interchangeability and reduce assembly issues." }
    ]
  },
  {
    id: 105,
    significance: "low",
    connectedClusters: [5, 6],
    identified: "2024-10-22",
    position: { x: -0.5, y: 0.5, z: -0.5 },
    questions: [
      { id: 10501, text: "How do software systems support assembly procedures?", importance: "low", impact: "Digital work instructions could improve assembly efficiency and reduce errors." },
      { id: 10502, text: "Is there a digital twin of the assembly process?", importance: "low", impact: "Would provide valuable simulation capabilities for optimizing assembly procedures." }
    ]
  },
  {
    id: 106,
    significance: "high",
    connectedClusters: [9, 12],
    identified: "2024-11-01",
    position: { x: 0, y: 0, z: 1 },
    questions: [
      { id: 10601, text: "How do material science innovations influence preventive maintenance schedules?", importance: "high", impact: "New materials could significantly alter maintenance requirements and schedules. Could extend component lifespans by 20-40% if properly addressed." },
      { id: 10602, text: "Are maintenance procedures updated to reflect new material properties?", importance: "high", impact: "Outdated maintenance procedures could damage new materials, leading to premature failures and increased costs." },
      { id: 10603, text: "What testing is done to validate maintenance procedures for new materials?", importance: "medium", impact: "Validation would ensure maintenance activities are effective and non-damaging to new materials." }
    ]
  }
];

const automotiveGaps = [
  {
    id: 101,
    significance: "high",
    connectedClusters: [1, 8],
    identified: "2024-11-06",
    position: { x: 2.5, y: 3.5, z: 1.5 },
    questions: [
      { id: 10101, text: "How do vehicle design specifications integrate with EV research findings?", importance: "high", impact: "Critical for ensuring new battery technology is properly integrated into vehicle platforms. Could improve range efficiency by 25% if properly addressed." },
      { id: 10102, text: "What design changes are needed to support new battery technologies?", importance: "high", impact: "Structural modifications may be required to accommodate larger or differently shaped battery packs." },
      { id: 10103, text: "Are there documented thermal management guidelines for EV battery integration?", importance: "high", impact: "Could prevent overheating issues and improve battery longevity and safety." }
    ]
  },
  {
    id: 102,
    significance: "medium",
    connectedClusters: [2, 11],
    identified: "2024-10-29",
    position: { x: -3.5, y: -3, z: -1 },
    questions: [
      { id: 10201, text: "How do production line processes align with service requirements?", importance: "medium", impact: "Could improve vehicle serviceability by considering maintenance access during assembly design." },
      { id: 10202, text: "Is there a feedback loop from dealer service to manufacturing?", importance: "medium", impact: "Would help identify recurring service issues that could be addressed during production." },
      { id: 10203, text: "What assembly techniques impact future serviceability?", importance: "high", impact: "Some fastening methods may make parts difficult to service or replace in the field." }
    ]
  },
  {
    id: 103,
    significance: "high",
    connectedClusters: [3, 10],
    identified: "2024-11-04",
    position: { x: 3.5, y: 5, z: 3.5 },
    questions: [
      { id: 10301, text: "How do powertrain systems integrate with autonomous driving technology?", importance: "high", impact: "Critical for ensuring powertrains can respond appropriately to autonomous control inputs." },
      { id: 10302, text: "What modifications are needed for powertrains under autonomous control?", importance: "medium", impact: "Different driving patterns may require revised transmission control logic." },
      { id: 10303, text: "Is there a testing protocol for powertrain behavior under autonomous control?", importance: "high", impact: "Could prevent unexpected powertrain responses during autonomous operation." }
    ]
  },
  {
    id: 104,
    significance: "high",
    connectedClusters: [4, 9],
    identified: "2024-10-31",
    position: { x: -1, y: -2.5, z: -2 },
    questions: [
      { id: 10401, text: "How do lightweight materials impact suspension performance?", importance: "high", impact: "New materials could significantly alter suspension dynamics and require recalibration." },
      { id: 10402, text: "What are the fatigue characteristics of composite chassis components?", importance: "high", impact: "Long-term durability of lightweight materials is critical for chassis applications." },
      { id: 10403, text: "Are there new testing methodologies needed for composite structural parts?", importance: "medium", impact: "Traditional metal testing procedures may not be applicable to composite materials." }
    ]
  },
  {
    id: 105,
    significance: "medium",
    connectedClusters: [5, 7],
    identified: "2024-10-26",
    position: { x: -0.5, y: 0.5, z: -0.5 },
    questions: [
      { id: 10501, text: "How do vehicle electronics systems support quality assurance testing?", importance: "medium", impact: "Self-diagnostic capabilities could streamline final vehicle inspection." },
      { id: 10502, text: "Is there an automated way to verify all electronic systems during production?", importance: "medium", impact: "Comprehensive testing during assembly could reduce defect rates." },
      { id: 10503, text: "What data from production testing should be retained for warranty analysis?", importance: "low", impact: "Production test data could help identify trends in field failures." }
    ]
  },
  {
    id: 106,
    significance: "high",
    connectedClusters: [6, 12],
    identified: "2024-11-02",
    position: { x: 0, y: 0, z: 1 },
    questions: [
      { id: 10601, text: "How do paint and finishing processes impact warranty claims?", importance: "high", impact: "Paint quality issues are a significant source of warranty claims and customer dissatisfaction." },
      { id: 10602, text: "Are there better corrosion protection methods that could reduce warranty claims?", importance: "high", impact: "Improved corrosion resistance could significantly reduce long-term warranty costs." },
      { id: 10603, text: "What is the correlation between paint process variables and long-term durability?", importance: "medium", impact: "Understanding key process variables could improve finish quality and consistency." }
    ]
  }
];

// Set default gaps
let knowledgeGaps = aerospaceGaps;

// Check URL parameter for domain selection
function initDomainBasedData() {
  try {
    // Get domain from URL parameters
    const urlParams = new URLSearchParams(window.location.search);
    const domain = urlParams.get('domain');
    
    console.log("Detected domain parameter:", domain);
    
    // Switch data based on domain
    if (domain === 'automotive') {
      console.log("Loading automotive domain data");
      knowledgeClusters = automotiveClusters;
      knowledgeGaps = automotiveGaps;
    } else {
      console.log("Loading aerospace_plm domain data (default)");
      knowledgeClusters = aerospaceClusters;
      knowledgeGaps = aerospaceGaps;
    }
  } catch (error) {
    console.error("Error initializing domain data:", error);
    // Fallback to default data
    knowledgeClusters = aerospaceClusters;
    knowledgeGaps = aerospaceGaps;
  }
}

// Call domain initialization on load
initDomainBasedData();

// Original knowledge gaps definition (kept for backward compatibility)
const originalKnowledgeGaps = [
  {
    id: 101,
    significance: "high",
    connectedClusters: [1, 8],
    identified: "2024-11-04",
    position: { x: 2.5, y: 3.5, z: 1.5 },
    questions: [
      { id: 10101, text: "How do design specifications integrate with research findings?", importance: "high", impact: "Critical for ensuring new research is incorporated into product designs. Could reduce design iterations by 30% if properly addressed." },
      { id: 10102, text: "What mechanisms exist for research feedback to influence design?", importance: "medium", impact: "Would enable more innovative design approaches and improve knowledge transfer between departments." },
      { id: 10103, text: "Are there documented procedures for applying research innovations to design?", importance: "high", impact: "Could resolve significant inefficiencies in the product development cycle and reduce time-to-market." }
    ]
  },
  {
    id: 102,
    significance: "medium",
    connectedClusters: [2, 11],
    identified: "2024-10-25",
    position: { x: -3.5, y: -3, z: -1 },
    questions: [
      { id: 10201, text: "How do manufacturing processes account for maintenance requirements?", importance: "medium", impact: "Could reduce maintenance downtime by designing manufacturing processes with maintenance in mind." },
      { id: 10202, text: "Is there a feedback mechanism from maintenance to manufacturing?", importance: "low", impact: "Would help identify recurring issues that could be addressed in the manufacturing phase." }
    ]
  },
  {
    id: 103,
    significance: "high",
    connectedClusters: [3, 10],
    identified: "2024-11-02",
    position: { x: 3.5, y: 5, z: 3.5 },
    questions: [
      { id: 10301, text: "How are advanced electronics research findings applied to electrical systems?", importance: "high", impact: "Critical for incorporating cutting-edge technology into product electrical systems. Could provide significant competitive advantage." },
      { id: 10302, text: "What is the timeline for research technologies to be implemented in products?", importance: "medium", impact: "Would help create realistic roadmaps and set appropriate customer expectations for feature availability." },
      { id: 10303, text: "Are there compatibility studies between new research and existing electrical systems?", importance: "high", impact: "Could prevent integration issues and reduce costly redesigns later in the development cycle." }
    ]
  },
  {
    id: 104,
    significance: "medium",
    connectedClusters: [4, 7],
    identified: "2024-10-28",
    position: { x: -1, y: -2.5, z: -2 },
    questions: [
      { id: 10401, text: "How do quality control procedures verify mechanical component specifications?", importance: "medium", impact: "Could improve detection of non-conforming parts before they enter the assembly process." },
      { id: 10402, text: "What tolerance standards are applied across mechanical components?", importance: "medium", impact: "Standardized tolerances could improve interchangeability and reduce assembly issues." }
    ]
  },
  {
    id: 105,
    significance: "low",
    connectedClusters: [5, 6],
    identified: "2024-10-22",
    position: { x: -0.5, y: 0.5, z: -0.5 },
    questions: [
      { id: 10501, text: "How do software systems support assembly procedures?", importance: "low", impact: "Digital work instructions could improve assembly efficiency and reduce errors." },
      { id: 10502, text: "Is there a digital twin of the assembly process?", importance: "low", impact: "Would provide valuable simulation capabilities for optimizing assembly procedures." }
    ]
  },
  {
    id: 106,
    significance: "high",
    connectedClusters: [9, 12],
    identified: "2024-11-01",
    position: { x: 0, y: 0, z: 1 },
    questions: [
      { id: 10601, text: "How do material science innovations influence preventive maintenance schedules?", importance: "high", impact: "New materials could significantly alter maintenance requirements and schedules. Could extend component lifespans by 20-40% if properly addressed." },
      { id: 10602, text: "Are maintenance procedures updated to reflect new material properties?", importance: "high", impact: "Outdated maintenance procedures could damage new materials, leading to premature failures and increased costs." },
      { id: 10603, text: "What testing is done to validate maintenance procedures for new materials?", importance: "medium", impact: "Validation would ensure maintenance activities are effective and non-damaging to new materials." }
    ]
  }
];

// Global variables
let scene, camera, renderer, controls, composer;
let clusterObjects = {}, gapObjects = {}, questionObjects = {};
let raycaster, mouse, selectedObject = null, hoveredObject = null;

// DOM elements
const galaxyCanvas = document.getElementById('galaxy-canvas');
const detailsPanel = document.querySelector('.details-panel');
const clusterDetails = document.getElementById('cluster-details');
const gapDetails = document.getElementById('gap-details');
const questionDetails = document.getElementById('question-details');
const detailsTitle = document.getElementById('details-title');

// Initialize the visualization
function initGalaxy() {
  console.log("Initializing galaxy visualization");
  
  // Create scene
  scene = new THREE.Scene();
  scene.background = new THREE.Color(0x0d1117);
  
  // Create camera
  const aspectRatio = galaxyCanvas.clientWidth / galaxyCanvas.clientHeight;
  camera = new THREE.PerspectiveCamera(60, aspectRatio, 0.1, 1000);
  camera.position.set(0, 15, 25);
  camera.lookAt(0, 0, 0);
  
  // Create renderer
  try {
    console.log("Setting up WebGL renderer");
    if (galaxyCanvas.clientWidth === 0 || galaxyCanvas.clientHeight === 0) {
      throw new Error("Galaxy canvas has zero dimensions");
    }
    
    renderer = new THREE.WebGLRenderer({ 
      antialias: true,
      alpha: true, // Allow transparency
      powerPreference: "high-performance" // Request the best GPU performance
    });
    renderer.setSize(galaxyCanvas.clientWidth, galaxyCanvas.clientHeight);
    renderer.setPixelRatio(window.devicePixelRatio);
    
    // Make sure the renderer's canvas is properly styled
    renderer.domElement.style.display = 'block';
    renderer.domElement.style.width = '100%';
    renderer.domElement.style.height = '100%';
    
    // Clear any existing content
    galaxyCanvas.innerHTML = '';
    galaxyCanvas.appendChild(renderer.domElement);
    
    // Add ambient light
    const ambientLight = new THREE.AmbientLight(0x333333);
    scene.add(ambientLight);
    
    // Add directional light
    const directionalLight = new THREE.DirectionalLight(0xffffff, 1);
    directionalLight.position.set(1, 1, 1);
    scene.add(directionalLight);
    
    // Add orbit controls
    console.log("Setting up orbit controls");
    controls = new OrbitControls(camera, renderer.domElement);
    controls.enableDamping = true;
    controls.dampingFactor = 0.05;
    controls.rotateSpeed = 0.5;
    controls.minDistance = 10;
    controls.maxDistance = 50;
    
    // Set up post-processing for bloom effect
    console.log("Setting up post-processing");
    setupPostProcessing();
    
    // Create raycaster for interaction
    raycaster = new THREE.Raycaster();
    mouse = new THREE.Vector2();
    
    console.log("Creating scene elements");
    // Add galaxy background
    createGalaxyBackground();
    
    // Add knowledge clusters
    console.log("Creating knowledge clusters");
    createKnowledgeClusters();
    
    // Add knowledge gaps
    console.log("Creating knowledge gaps");
    createKnowledgeGaps();
    
    // Add questions
    console.log("Creating questions");
    createQuestions();
    
    // Add connections between related clusters
    console.log("Creating connections");
    createConnections();
    
    // Add event listeners
    console.log("Adding event listeners");
    addEventListeners();
    
    // Animation loop
    animate();
    
    // Handle window resize
    window.addEventListener('resize', onWindowResize);
    
    console.log("Galaxy visualization initialization completed");
  } catch (error) {
    console.error("Error initializing galaxy visualization:", error);
    // Provide a fallback display
    const errorMessage = document.createElement('div');
    errorMessage.style.width = '100%';
    errorMessage.style.height = '100%';
    errorMessage.style.display = 'flex';
    errorMessage.style.alignItems = 'center';
    errorMessage.style.justifyContent = 'center';
    errorMessage.style.backgroundColor = '#0d1117';
    errorMessage.style.color = '#ffffff';
    errorMessage.style.padding = '20px';
    errorMessage.style.textAlign = 'center';
    errorMessage.innerHTML = `
      <div>
        <h3>Visualization Error</h3>
        <p>Sorry, there was an error initializing the 3D visualization.</p>
        <p style="color: #aaa; font-size: 14px;">Details: ${error.message}</p>
      </div>
    `;
    
    // Replace canvas or add error message
    if (galaxyCanvas.firstChild) {
      galaxyCanvas.removeChild(galaxyCanvas.firstChild);
    }
    galaxyCanvas.appendChild(errorMessage);
  }
}

// Set up post-processing for glow effect
function setupPostProcessing() {
  // Create composer
  composer = new EffectComposer(renderer);
  
  // Add render pass
  const renderPass = new RenderPass(scene, camera);
  composer.addPass(renderPass);
  
  // Add bloom pass
  const bloomPass = new UnrealBloomPass(
    new THREE.Vector2(galaxyCanvas.clientWidth, galaxyCanvas.clientHeight),
    0.7,   // strength
    0.4,   // radius
    0.85   // threshold
  );
  composer.addPass(bloomPass);
}

// Create a galaxy background with stars
function createGalaxyBackground() {
  // Create a particle system for background stars
  const starsGeometry = new THREE.BufferGeometry();
  const starsMaterial = new THREE.PointsMaterial({
    color: 0xffffff,
    size: 0.05,
    transparent: true,
    blending: THREE.AdditiveBlending
  });
  
  // Generate random star positions
  const starsCount = 2000;
  const starsPositions = new Float32Array(starsCount * 3);
  
  for (let i = 0; i < starsCount * 3; i += 3) {
    // Generate random positions in a sphere
    const radius = 80 + Math.random() * 50;
    const theta = Math.random() * Math.PI * 2;
    const phi = Math.acos(2 * Math.random() - 1);
    
    starsPositions[i] = radius * Math.sin(phi) * Math.cos(theta);
    starsPositions[i + 1] = radius * Math.sin(phi) * Math.sin(theta);
    starsPositions[i + 2] = radius * Math.cos(phi);
  }
  
  starsGeometry.setAttribute('position', new THREE.BufferAttribute(starsPositions, 3));
  const stars = new THREE.Points(starsGeometry, starsMaterial);
  scene.add(stars);
  
  // Add a subtle nebula effect (large, colored, transparent sphere)
  const nebulaGeometry = new THREE.SphereGeometry(60, 32, 32);
  const nebulaMaterial = new THREE.MeshBasicMaterial({
    color: 0x0a2463,
    transparent: true,
    opacity: 0.05,
    side: THREE.BackSide
  });
  const nebula = new THREE.Mesh(nebulaGeometry, nebulaMaterial);
  scene.add(nebula);
  
  // Add a second nebula layer for more depth and color variation
  const nebula2Geometry = new THREE.SphereGeometry(40, 32, 32);
  const nebula2Material = new THREE.MeshBasicMaterial({
    color: 0x3e92cc,
    transparent: true,
    opacity: 0.03,
    side: THREE.BackSide
  });
  const nebula2 = new THREE.Mesh(nebula2Geometry, nebula2Material);
  scene.add(nebula2);
}

// Create knowledge cluster visualization
function createKnowledgeClusters() {
  knowledgeClusters.forEach(cluster => {
    // Determine color based on domain
    const color = getDomainColor(cluster.domain);
    
    // Create cluster representation (sphere with particles)
    const clusterGroup = new THREE.Group();
    
    // Main sphere
    const geometry = new THREE.SphereGeometry(cluster.size / 20, 32, 32);
    const material = new THREE.MeshPhongMaterial({
      color: color,
      emissive: color,
      emissiveIntensity: 0.2,
      transparent: true,
      opacity: 0.8
    });
    const sphere = new THREE.Mesh(geometry, material);
    
    // Add particles around the main sphere for a nebulous effect
    const particlesGeometry = new THREE.BufferGeometry();
    const particleMaterial = new THREE.PointsMaterial({
      color: color,
      size: 0.1,
      transparent: true,
      opacity: 0.6,
      blending: THREE.AdditiveBlending
    });
    
    // Generate random particle positions in a spherical shell around the cluster
    const particleCount = cluster.size * 5;
    const particlePositions = new Float32Array(particleCount * 3);
    
    for (let i = 0; i < particleCount * 3; i += 3) {
      // Use spherical coordinates to distribute particles
      const radius = (cluster.size / 20) * (1 + Math.random() * 0.5);
      const theta = Math.random() * Math.PI * 2;
      const phi = Math.acos(2 * Math.random() - 1);
      
      particlePositions[i] = radius * Math.sin(phi) * Math.cos(theta);
      particlePositions[i + 1] = radius * Math.sin(phi) * Math.sin(theta);
      particlePositions[i + 2] = radius * Math.cos(phi);
    }
    
    particlesGeometry.setAttribute('position', new THREE.BufferAttribute(particlePositions, 3));
    const particles = new THREE.Points(particlesGeometry, particleMaterial);
    
    // Add sphere and particles to the group
    clusterGroup.add(sphere);
    clusterGroup.add(particles);
    
    // Position the cluster
    clusterGroup.position.set(
      cluster.position.x,
      cluster.position.y,
      cluster.position.z
    );
    
    // Add metadata
    clusterGroup.userData = {
      type: 'cluster',
      id: cluster.id,
      name: cluster.name,
      domain: cluster.domain,
      documents: cluster.documents,
      updated: cluster.updated,
      data: cluster
    };
    
    // Store reference
    clusterObjects[cluster.id] = clusterGroup;
    
    // Add to scene
    scene.add(clusterGroup);
  });
}

// Create knowledge gap visualization
function createKnowledgeGaps() {
  knowledgeGaps.forEach(gap => {
    const gapGroup = new THREE.Group();
    
    // Create a translucent sphere to represent the gap
    const geometry = new THREE.SphereGeometry(0.8, 32, 32);
    const material = new THREE.MeshPhongMaterial({
      color: 0x000000,
      transparent: true,
      opacity: 0.1,
      side: THREE.DoubleSide,
      wireframe: true
    });
    const sphere = new THREE.Mesh(geometry, material);
    
    // Add a pulsating highlight effect around the gap
    const highlightGeometry = new THREE.SphereGeometry(1, 24, 24);
    const highlightMaterial = new THREE.MeshBasicMaterial({
      color: getSignificanceColor(gap.significance),
      transparent: true,
      opacity: 0.3,
      wireframe: true
    });
    const highlight = new THREE.Mesh(highlightGeometry, highlightMaterial);
    
    // Store the original size for animation
    highlight.userData.originalScale = 1;
    highlight.userData.pulseSpeed = 0.5 + (Math.random() * 0.5);
    highlight.userData.pulseAmount = 0.2;
    
    // Add sphere and highlight to the group
    gapGroup.add(sphere);
    gapGroup.add(highlight);
    
    // Position the gap
    gapGroup.position.set(
      gap.position.x,
      gap.position.y,
      gap.position.z
    );
    
    // Add metadata
    gapGroup.userData = {
      type: 'gap',
      id: gap.id,
      significance: gap.significance,
      connectedClusters: gap.connectedClusters,
      identified: gap.identified,
      data: gap
    };
    
    // Store reference
    gapObjects[gap.id] = gapGroup;
    
    // Add to scene
    scene.add(gapGroup);
  });
}

// Create question visualization
function createQuestions() {
  knowledgeGaps.forEach(gap => {
    if (gap.questions && gap.questions.length > 0) {
      const gapPosition = new THREE.Vector3(
        gap.position.x,
        gap.position.y,
        gap.position.z
      );
      
      gap.questions.forEach((question, index) => {
        // Calculate position for question (emanating from the gap)
        const angle = (index / gap.questions.length) * Math.PI * 2;
        const radius = 1.5;
        const questionPosition = new THREE.Vector3(
          gapPosition.x + Math.cos(angle) * radius,
          gapPosition.y + 1 + (index * 0.2),
          gapPosition.z + Math.sin(angle) * radius
        );
        
        // Create a glowing point for the question
        const questionGroup = new THREE.Group();
        
        // Main point
        const geometry = new THREE.SphereGeometry(0.15, 16, 16);
        const color = getImportanceColor(question.importance);
        
        // Use MeshStandardMaterial instead for better compatibility
        const material = new THREE.MeshStandardMaterial({
          color: color,
          emissive: color,
          emissiveIntensity: 0.5,
          metalness: 0.3,
          roughness: 0.4
        });
        const sphere = new THREE.Mesh(geometry, material);
        
        // Add a subtle glow effect
        const glowGeometry = new THREE.SphereGeometry(0.2, 16, 16);
        const glowMaterial = new THREE.MeshBasicMaterial({
          color: color,
          transparent: true,
          opacity: 0.4
        });
        const glow = new THREE.Mesh(glowGeometry, glowMaterial);
        
        // Store the original size for animation
        glow.userData.originalScale = 1;
        glow.userData.pulseSpeed = 0.5 + (Math.random() * 1);
        glow.userData.pulseAmount = 0.3;
        
        // Add sphere and glow to the group
        questionGroup.add(sphere);
        questionGroup.add(glow);
        
        // Position the question
        questionGroup.position.copy(questionPosition);
        
        // Add metadata
        questionGroup.userData = {
          type: 'question',
          id: question.id,
          text: question.text,
          importance: question.importance,
          impact: question.impact,
          gapId: gap.id,
          data: question
        };
        
        // Store reference
        questionObjects[question.id] = questionGroup;
        
        // Add to scene
        scene.add(questionGroup);
        
        // Create connection to the gap
        const connectionMaterial = new THREE.LineBasicMaterial({
          color: color,
          transparent: true,
          opacity: 0.3
        });
        
        const connectionPoints = [
          questionPosition,
          gapPosition
        ];
        
        const connectionGeometry = new THREE.BufferGeometry().setFromPoints(connectionPoints);
        const connection = new THREE.Line(connectionGeometry, connectionMaterial);
        scene.add(connection);
      });
    }
  });
}

// Create connections between related clusters and gaps
function createConnections() {
  // Create connections between clusters and their sub-clusters
  knowledgeClusters.forEach(cluster => {
    if (cluster.subClusters && cluster.subClusters.length > 0) {
      const clusterPosition = clusterObjects[cluster.id].position;
      
      cluster.subClusters.forEach(subClusterId => {
        if (clusterObjects[subClusterId]) {
          const subClusterPosition = clusterObjects[subClusterId].position;
          
          const connectionMaterial = new THREE.LineBasicMaterial({
            color: getDomainColor(cluster.domain),
            transparent: true,
            opacity: 0.3
          });
          
          const connectionPoints = [
            clusterPosition,
            subClusterPosition
          ];
          
          const connectionGeometry = new THREE.BufferGeometry().setFromPoints(connectionPoints);
          const connection = new THREE.Line(connectionGeometry, connectionMaterial);
          scene.add(connection);
        }
      });
    }
  });
  
  // Create connections between gaps and connected clusters
  knowledgeGaps.forEach(gap => {
    if (gap.connectedClusters && gap.connectedClusters.length > 0) {
      const gapPosition = gapObjects[gap.id].position;
      
      gap.connectedClusters.forEach(clusterId => {
        if (clusterObjects[clusterId]) {
          const clusterPosition = clusterObjects[clusterId].position;
          
          const connectionMaterial = new THREE.LineDashedMaterial({
            color: getSignificanceColor(gap.significance),
            dashSize: 0.3,
            gapSize: 0.1,
            transparent: true,
            opacity: 0.3
          });
          
          const connectionPoints = [
            gapPosition,
            clusterPosition
          ];
          
          const connectionGeometry = new THREE.BufferGeometry().setFromPoints(connectionPoints);
          const connection = new THREE.Line(connectionGeometry, connectionMaterial);
          connection.computeLineDistances(); // Required for dashed lines
          scene.add(connection);
        }
      });
    }
  });
}

// Add event listeners for interactivity
function addEventListeners() {
  // Mouse move event for raycasting
  galaxyCanvas.addEventListener('mousemove', onMouseMove);
  
  // Click event for selection
  galaxyCanvas.addEventListener('click', onMouseClick);
  
  // Close details panel button
  document.getElementById('close-details').addEventListener('click', () => {
    // Hide details panel content
    clusterDetails.style.display = 'none';
    gapDetails.style.display = 'none';
    questionDetails.style.display = 'none';
    
    // Deselect current object
    if (selectedObject) {
      resetHighlight(selectedObject);
      selectedObject = null;
    }
    
    // Reset title
    detailsTitle.textContent = 'Select a cluster or gap';
  });
  
  // Zoom controls
  document.getElementById('zoom-in').addEventListener('click', () => {
    controls.dollyIn(1.2);
  });
  
  document.getElementById('zoom-out').addEventListener('click', () => {
    controls.dollyOut(1.2);
  });
  
  document.getElementById('reset-view').addEventListener('click', () => {
    camera.position.set(0, 15, 25);
    camera.lookAt(0, 0, 0);
    controls.update();
  });
  
  // Fullscreen controls
  const galaxyContainer = document.querySelector('.galaxy-container');
  const galaxyControls = document.querySelector('.galaxy-controls');
  const detailsPanel = document.querySelector('.details-panel');
  const fullscreenBtn = document.getElementById('toggle-fullscreen');
  
  // Help modal controls
  const helpModal = document.getElementById('fullscreen-help');
  const closeHelpBtn = document.getElementById('close-help');
  
  // Close help modal
  closeHelpBtn.addEventListener('click', () => {
    helpModal.style.display = 'none';
    
    // Save that the user has seen the help
    localStorage.setItem('galaxyHelpShown', 'true');
  });
  
  // Toggle fullscreen
  fullscreenBtn.addEventListener('click', () => {
    const isEnteringFullscreen = !galaxyContainer.classList.contains('fullscreen');
    
    // Enter fullscreen
    if (isEnteringFullscreen) {
      console.log("Entering fullscreen mode");
      
      // Add fullscreen class
      galaxyContainer.classList.add('fullscreen');
      
      // Update button appearance
      fullscreenBtn.innerHTML = '<i class="fas fa-compress"></i>';
      fullscreenBtn.title = 'Exit Fullscreen';
      
      // Show help modal the first time user enters fullscreen
      const helpShown = localStorage.getItem('galaxyHelpShown');
      if (!helpShown) {
        setTimeout(() => {
          helpModal.style.display = 'flex';
        }, 500);
      }
      
      // Force renderer resize after transition
      setTimeout(() => {
        console.log("Resizing after entering fullscreen");
        onWindowResize();
        
        // Force redraw
        renderer.render(scene, camera);
      }, 300);
    } 
    // Exit fullscreen
    else {
      console.log("Exiting fullscreen mode");
      
      // Reset panels when exiting fullscreen
      galaxyControls.classList.remove('visible');
      detailsPanel.classList.remove('visible');
      
      // Remove fullscreen class
      galaxyContainer.classList.remove('fullscreen');
      
      // Update button appearance
      fullscreenBtn.innerHTML = '<i class="fas fa-expand"></i>';
      fullscreenBtn.title = 'Enter Fullscreen';
      
      // Hide help modal if it's open
      helpModal.style.display = 'none';
      
      // Force renderer resize after transition
      setTimeout(() => {
        console.log("Resizing after exiting fullscreen");
        onWindowResize();
        
        // Force redraw
        renderer.render(scene, camera);
      }, 300);
    }
  });
  
  // Track original camera position
  let originalCameraPosition = null;
  
  // Function to animate camera movement
  function animateCamera(targetX, duration = 500) {
    if (typeof anime !== 'undefined') {
      // Use anime.js if available
      anime({
        targets: camera.position,
        x: targetX,
        duration: duration,
        easing: 'easeOutQuad',
        update: function() {
          camera.updateProjectionMatrix();
        }
      });
    } else {
      // Fallback animation
      const startX = camera.position.x;
      const distance = targetX - startX;
      const startTime = Date.now();
      
      function animateStep() {
        const currentTime = Date.now();
        const elapsed = currentTime - startTime;
        const progress = Math.min(elapsed / duration, 1);
        
        // Simple easing function
        const easeProgress = 1 - Math.pow(1 - progress, 2);
        
        camera.position.x = startX + distance * easeProgress;
        camera.updateProjectionMatrix();
        
        if (progress < 1) {
          requestAnimationFrame(animateStep);
        }
      }
      
      requestAnimationFrame(animateStep);
    }
  }
  
  // Toggle controls panel in fullscreen mode
  document.getElementById('toggle-controls').addEventListener('click', () => {
    const wasVisible = galaxyControls.classList.contains('visible');
    galaxyControls.classList.toggle('visible');
    
    // If both panels are open, close the other one
    if (galaxyControls.classList.contains('visible') && detailsPanel.classList.contains('visible')) {
      detailsPanel.classList.remove('visible');
    }
    
    // Adjust camera when left panel is toggled
    if (galaxyContainer.classList.contains('fullscreen')) {
      // Store original position if not already stored
      if (originalCameraPosition === null) {
        originalCameraPosition = new THREE.Vector3().copy(camera.position);
      }
      
      if (galaxyControls.classList.contains('visible') && !wasVisible) {
        // Calculate offset based on panel width
        const panelWidth = galaxyControls.offsetWidth;
        const offsetX = Math.min(panelWidth / 80, 8); // Scale the camera movement
        
        // Move camera right when left panel appears
        animateCamera(camera.position.x + offsetX);
      } else if (!galaxyControls.classList.contains('visible') && wasVisible) {
        // Move camera back when left panel disappears
        animateCamera(originalCameraPosition.x);
      }
    }
  });
  
  // Toggle details panel in fullscreen mode
  document.getElementById('toggle-details').addEventListener('click', () => {
    const wasVisible = detailsPanel.classList.contains('visible');
    detailsPanel.classList.toggle('visible');
    
    // If both panels are open, close the other one
    if (detailsPanel.classList.contains('visible') && galaxyControls.classList.contains('visible')) {
      galaxyControls.classList.remove('visible');
    }
    
    // Adjust camera when right panel is toggled
    if (galaxyContainer.classList.contains('fullscreen')) {
      // Store original position if not already stored
      if (originalCameraPosition === null) {
        originalCameraPosition = new THREE.Vector3().copy(camera.position);
      }
      
      if (detailsPanel.classList.contains('visible') && !wasVisible) {
        // Calculate offset based on panel width
        const panelWidth = detailsPanel.offsetWidth;
        const offsetX = Math.min(panelWidth / 80, 8); // Scale the camera movement
        
        // Move camera left when right panel appears
        animateCamera(camera.position.x - offsetX);
      } else if (!detailsPanel.classList.contains('visible') && wasVisible) {
        // Move camera back when right panel disappears
        animateCamera(originalCameraPosition.x);
      }
    }
  });
  
  // Filter controls
  document.getElementById('domain-filter').addEventListener('change', applyFilters);
  document.getElementById('department-filter').addEventListener('change', applyFilters);
  document.getElementById('time-filter').addEventListener('change', applyFilters);
  
  // View options
  document.getElementById('highlight-gaps').addEventListener('change', toggleGapHighlights);
  document.getElementById('show-questions').addEventListener('change', toggleQuestions);
  document.getElementById('auto-rotate').addEventListener('change', toggleAutoRotate);
  
  // Action buttons for gaps
  document.getElementById('assign-gap').addEventListener('click', () => {
    openAssignmentDialog('gap', selectedObject ? selectedObject.userData.data : null);
  });
  
  document.getElementById('export-gap').addEventListener('click', () => {
    alert('This would export the gap analysis in a production system.');
  });
  
  // Action buttons for questions
  document.getElementById('answer-question').addEventListener('click', () => {
    alert('This would initiate an AI response to the question in a production system.');
  });
  
  document.getElementById('assign-question').addEventListener('click', () => {
    openAssignmentDialog('question', selectedObject ? selectedObject.userData.data : null);
  });
  
  // Handle keyboard shortcuts
  document.addEventListener('keydown', (event) => {
    // 'F' key for fullscreen toggle
    if (event.key === 'f' || event.key === 'F') {
      fullscreenBtn.click();
    }
    
    // 'Escape' key to exit fullscreen
    if (event.key === 'Escape' && galaxyContainer.classList.contains('fullscreen')) {
      fullscreenBtn.click();
    }
    
    // 'Escape' key to close assignment dialog
    if (event.key === 'Escape' && document.getElementById('assignment-dialog').style.display === 'flex') {
      closeAssignmentDialog();
    }
    
    // '1' key to toggle controls panel
    if (event.key === '1' && galaxyContainer.classList.contains('fullscreen')) {
      document.getElementById('toggle-controls').click();
    }
    
    // '2' key to toggle details panel
    if (event.key === '2' && galaxyContainer.classList.contains('fullscreen')) {
      document.getElementById('toggle-details').click();
    }
  });
  
  // Assignment dialog event listeners
  document.getElementById('close-assignment').addEventListener('click', closeAssignmentDialog);
  document.getElementById('cancel-assignment').addEventListener('click', closeAssignmentDialog);
  document.getElementById('search-users-btn').addEventListener('click', searchUsers);
  document.getElementById('user-search').addEventListener('keyup', (event) => {
    if (event.key === 'Enter') {
      searchUsers();
    }
  });
  document.getElementById('confirm-assignment').addEventListener('click', confirmAssignment);
}

// Mouse move handler
function onMouseMove(event) {
  // Calculate mouse position in normalized device coordinates (-1 to +1)
  const rect = galaxyCanvas.getBoundingClientRect();
  mouse.x = ((event.clientX - rect.left) / galaxyCanvas.clientWidth) * 2 - 1;
  mouse.y = -((event.clientY - rect.top) / galaxyCanvas.clientHeight) * 2 + 1;
  
  // Update the raycaster
  raycaster.setFromCamera(mouse, camera);
  
  // Get intersecting objects
  const intersects = raycaster.intersectObjects(scene.children, true);
  
  // Reset current hover state
  if (hoveredObject && hoveredObject !== selectedObject) {
    resetHighlight(hoveredObject);
  }
  
  hoveredObject = null;
  galaxyCanvas.style.cursor = 'default';
  
  // Check for hover
  if (intersects.length > 0) {
    // Find the first object with userData (skip particles and connections)
    for (let i = 0; i < intersects.length; i++) {
      const intersectedObject = getParentWithUserData(intersects[i].object);
      if (intersectedObject && intersectedObject.userData && 
         (intersectedObject.userData.type === 'cluster' || 
          intersectedObject.userData.type === 'gap' || 
          intersectedObject.userData.type === 'question')) {
        
        hoveredObject = intersectedObject;
        galaxyCanvas.style.cursor = 'pointer';
        
        if (hoveredObject !== selectedObject) {
          highlightObject(hoveredObject);
        }
        
        break;
      }
    }
  }
}

// Mouse click handler
function onMouseClick() {
  if (hoveredObject) {
    // Deselect previous object
    if (selectedObject) {
      resetHighlight(selectedObject);
    }
    
    // Select new object
    selectedObject = hoveredObject;
    highlightObject(selectedObject, true);
    
    // Show details based on object type
    showDetails(selectedObject);
  }
}

// Show details for the selected object
function showDetails(object) {
  // Hide all detail panels
  clusterDetails.style.display = 'none';
  gapDetails.style.display = 'none';
  questionDetails.style.display = 'none';
  
  // Show appropriate details based on object type
  if (object.userData.type === 'cluster') {
    showClusterDetails(object);
  } else if (object.userData.type === 'gap') {
    showGapDetails(object);
  } else if (object.userData.type === 'question') {
    showQuestionDetails(object);
  }
}

// Show cluster details
function showClusterDetails(object) {
  const cluster = object.userData.data;
  
  // Update title
  detailsTitle.textContent = cluster.name;
  
  // Update details
  document.getElementById('cluster-domain').textContent = formatDomainName(cluster.domain);
  document.getElementById('cluster-documents').textContent = cluster.documents;
  document.getElementById('cluster-updated').textContent = formatDate(cluster.updated);
  
  // Update key documents list
  const documentsList = document.getElementById('key-documents');
  documentsList.innerHTML = '';
  
  cluster.keyDocuments.forEach(doc => {
    const listItem = document.createElement('li');
    
    // Add icon based on document type
    const icon = document.createElement('i');
    icon.className = `document-icon fas ${getDocumentIcon(doc.type)}`;
    listItem.appendChild(icon);
    
    // Add document title
    const titleSpan = document.createElement('span');
    titleSpan.textContent = doc.title;
    listItem.appendChild(titleSpan);
    
    documentsList.appendChild(listItem);
  });
  
  // Show cluster details panel
  clusterDetails.style.display = 'block';
}

// Show gap details
function showGapDetails(object) {
  const gap = object.userData.data;
  
  // Update title
  detailsTitle.textContent = 'Knowledge Gap';
  
  // Update details
  document.getElementById('gap-significance').textContent = formatSignificance(gap.significance);
  
  // Get connected cluster names
  const connectedClusterNames = gap.connectedClusters.map(id => {
    const cluster = knowledgeClusters.find(c => c.id === id);
    return cluster ? cluster.name : 'Unknown';
  }).join(', ');
  
  document.getElementById('gap-clusters').textContent = connectedClusterNames;
  document.getElementById('gap-identified').textContent = formatDate(gap.identified);
  
  // Update questions list
  const questionsList = document.getElementById('gap-questions');
  questionsList.innerHTML = '';
  
  gap.questions.forEach(question => {
    const listItem = document.createElement('li');
    listItem.textContent = question.text;
    
    // Add importance badge
    const badge = document.createElement('div');
    badge.className = `question-importance ${question.importance}`;
    badge.textContent = formatImportance(question.importance);
    listItem.appendChild(badge);
    
    // Add click handler to show question details
    listItem.addEventListener('click', () => {
      // Find and select the question object
      if (questionObjects[question.id]) {
        if (selectedObject) {
          resetHighlight(selectedObject);
        }
        
        selectedObject = questionObjects[question.id];
        highlightObject(selectedObject, true);
        
        showQuestionDetails(selectedObject);
      }
    });
    
    questionsList.appendChild(listItem);
  });
  
  // Show gap details panel
  gapDetails.style.display = 'block';
}

// Show question details
function showQuestionDetails(object) {
  const question = object.userData.data;
  
  // Update title
  detailsTitle.textContent = 'Question Details';
  
  // Update details
  document.getElementById('question-text').textContent = question.text;
  document.getElementById('question-importance').textContent = formatImportance(question.importance);
  
  // Get related gap and connected clusters
  const gap = knowledgeGaps.find(g => g.id === object.userData.gapId);
  
  if (gap) {
    const connectedClusterNames = gap.connectedClusters.map(id => {
      const cluster = knowledgeClusters.find(c => c.id === id);
      return cluster ? cluster.name : 'Unknown';
    }).join(', ');
    
    document.getElementById('question-related').textContent = connectedClusterNames;
  } else {
    document.getElementById('question-related').textContent = 'Unknown';
  }
  
  // Update impact text
  document.getElementById('question-impact').textContent = question.impact || 'No impact analysis available.';
  
  // Show question details panel
  questionDetails.style.display = 'block';
}

// Apply filters to visualization
function applyFilters() {
  const domainFilter = document.getElementById('domain-filter').value;
  const departmentFilter = document.getElementById('department-filter').value;
  const timeFilter = document.getElementById('time-filter').value;
  
  // Filter clusters
  Object.values(clusterObjects).forEach(clusterObj => {
    const cluster = clusterObj.userData.data;
    let visible = true;
    
    // Apply domain filter
    if (domainFilter !== 'all' && cluster.domain !== domainFilter) {
      visible = false;
    }
    
    // Apply time filter
    if (timeFilter !== 'all') {
      const updateDate = new Date(cluster.updated);
      const now = new Date();
      
      if (timeFilter === 'last-month' && (now - updateDate > 30 * 24 * 60 * 60 * 1000)) {
        visible = false;
      } else if (timeFilter === 'last-quarter' && (now - updateDate > 90 * 24 * 60 * 60 * 1000)) {
        visible = false;
      } else if (timeFilter === 'last-year' && (now - updateDate > 365 * 24 * 60 * 60 * 1000)) {
        visible = false;
      }
    }
    
    // Apply visibility
    clusterObj.visible = visible;
  });
  
  // TODO: Department filter would require additional metadata in the real implementation
  
  // Update related elements visibility
  updateGapVisibility();
  updateQuestionVisibility();
}

// Update gap visibility based on connected clusters
function updateGapVisibility() {
  Object.values(gapObjects).forEach(gapObj => {
    const gap = gapObj.userData.data;
    let visible = false;
    
    // A gap is visible if at least one connected cluster is visible
    if (gap.connectedClusters) {
      for (const clusterId of gap.connectedClusters) {
        if (clusterObjects[clusterId] && clusterObjects[clusterId].visible) {
          visible = true;
          break;
        }
      }
    }
    
    gapObj.visible = visible;
  });
}

// Update question visibility based on gaps
function updateQuestionVisibility() {
  Object.values(questionObjects).forEach(questionObj => {
    const gapId = questionObj.userData.gapId;
    questionObj.visible = gapObjects[gapId] ? gapObjects[gapId].visible : false;
  });
}

// Toggle highlight for knowledge gaps
function toggleGapHighlights() {
  const highlight = document.getElementById('highlight-gaps').checked;
  
  Object.values(gapObjects).forEach(gapObj => {
    const children = gapObj.children;
    
    // The second child is the highlight mesh
    if (children.length > 1) {
      children[1].visible = highlight;
    }
  });
}

// Toggle visibility of questions
function toggleQuestions() {
  const show = document.getElementById('show-questions').checked;
  
  Object.values(questionObjects).forEach(questionObj => {
    questionObj.visible = show && (gapObjects[questionObj.userData.gapId] ? gapObjects[questionObj.userData.gapId].visible : false);
  });
}

// Toggle auto-rotation
function toggleAutoRotate() {
  controls.autoRotate = document.getElementById('auto-rotate').checked;
  
  if (controls.autoRotate) {
    controls.autoRotateSpeed = 0.5;
  }
}

// Highlight an object when hovered or selected
function highlightObject(object, isSelected = false) {
  const type = object.userData.type;
  
  if (type === 'cluster') {
    if (object.children.length > 0) {
      // Increase emissive intensity for the main sphere
      const mainSphere = object.children[0];
      // Check if the material has the emissiveIntensity property
      if (mainSphere.material.type === 'MeshPhongMaterial' || 
          mainSphere.material.type === 'MeshStandardMaterial') {
        mainSphere.material.emissiveIntensity = isSelected ? 0.8 : 0.5;
      } else {
        // For other material types, just brighten the color
        const originalColor = getDomainColor(object.userData.domain);
        const brightenFactor = isSelected ? 1.5 : 1.3;
        const brightenedColor = new THREE.Color(originalColor).multiplyScalar(brightenFactor);
        mainSphere.material.color.set(brightenedColor);
      }
      
      // Scale up slightly
      const scale = isSelected ? 1.15 : 1.1;
      object.scale.set(scale, scale, scale);
    }
  } else if (type === 'gap') {
    if (object.children.length > 1) {
      // Increase the highlight opacity
      const highlight = object.children[1];
      highlight.material.opacity = isSelected ? 0.7 : 0.5;
      
      // Scale up
      const scale = isSelected ? 1.3 : 1.2;
      object.scale.set(scale, scale, scale);
    }
  } else if (type === 'question') {
    if (object.children.length > 0) {
      // Increase the glow opacity and intensity
      const mainSphere = object.children[0];
      // Check material type for appropriate property manipulation
      if (mainSphere.material.type === 'MeshPhongMaterial' || 
          mainSphere.material.type === 'MeshStandardMaterial') {
        mainSphere.material.emissiveIntensity = isSelected ? 1.0 : 0.8;
        mainSphere.material.shininess = isSelected ? 200 : 100;
      } else {
        // For basic materials, increase brightness
        const originalColor = getImportanceColor(object.userData.importance);
        const brightenFactor = isSelected ? 1.5 : 1.3;
        const brightenedColor = new THREE.Color(originalColor).multiplyScalar(brightenFactor);
        mainSphere.material.color.set(brightenedColor);
      }
      
      // Also increase the glow sphere's opacity if it exists
      if (object.children.length > 1) {
        const glowSphere = object.children[1];
        glowSphere.material.opacity = isSelected ? 0.6 : 0.4;
      }
      
      // Scale up
      const scale = isSelected ? 1.5 : 1.3;
      object.scale.set(scale, scale, scale);
    }
  }
}

// Reset highlight state
function resetHighlight(object) {
  const type = object.userData.type;
  
  if (type === 'cluster') {
    if (object.children.length > 0) {
      // Reset appearance
      const mainSphere = object.children[0];
      // Check material type
      if (mainSphere.material.type === 'MeshPhongMaterial' || 
          mainSphere.material.type === 'MeshStandardMaterial') {
        mainSphere.material.emissiveIntensity = 0.2;
      } else {
        // For basic materials, reset color
        const originalColor = getDomainColor(object.userData.domain);
        mainSphere.material.color.set(originalColor);
      }
      
      // Reset scale
      object.scale.set(1, 1, 1);
    }
  } else if (type === 'gap') {
    if (object.children.length > 1) {
      // Reset highlight opacity
      const highlight = object.children[1];
      highlight.material.opacity = 0.3;
      
      // Reset scale
      object.scale.set(1, 1, 1);
    }
  } else if (type === 'question') {
    if (object.children.length > 0) {
      // Reset appearance
      const mainSphere = object.children[0];
      // Check material type
      if (mainSphere.material.type === 'MeshPhongMaterial' || 
          mainSphere.material.type === 'MeshStandardMaterial') {
        mainSphere.material.emissiveIntensity = 0.5;
        mainSphere.material.shininess = 100;
      } else {
        // For basic materials, reset color
        const originalColor = getImportanceColor(object.userData.importance);
        mainSphere.material.color.set(originalColor);
      }
      
      // Reset glow sphere if it exists
      if (object.children.length > 1) {
        const glowSphere = object.children[1];
        glowSphere.material.opacity = 0.4;
      }
      
      // Reset scale
      object.scale.set(1, 1, 1);
    }
  }
}

// Get the parent object with userData (useful for raycasting)
function getParentWithUserData(object) {
  let current = object;
  
  while (current && (!current.userData || !current.userData.type)) {
    current = current.parent;
  }
  
  return current;
}

// Animation loop
function animate() {
  requestAnimationFrame(animate);
  
  try {
    // Update controls
    if (controls) {
      controls.update();
    }
    
    // Animate gap highlights (pulsing effect)
    Object.values(gapObjects).forEach(gapObj => {
      if (gapObj && gapObj.visible && gapObj.children && gapObj.children.length > 1) {
        const highlight = gapObj.children[1];
        if (highlight && highlight.userData && highlight.userData.originalScale) {
          const time = Date.now() * 0.001;
          const pulse = 1 + Math.sin(time * highlight.userData.pulseSpeed) * highlight.userData.pulseAmount;
          
          highlight.scale.set(pulse, pulse, pulse);
        }
      }
    });
    
    // Animate question glows (pulsing effect)
    Object.values(questionObjects).forEach(questionObj => {
      if (questionObj && questionObj.visible && questionObj.children && questionObj.children.length > 1) {
        const glow = questionObj.children[1];
        if (glow && glow.userData && glow.userData.originalScale) {
          const time = Date.now() * 0.001;
          const pulse = 1 + Math.sin(time * glow.userData.pulseSpeed) * glow.userData.pulseAmount;
          
          glow.scale.set(pulse, pulse, pulse);
        }
      }
    });
    
    // Render with post-processing if available
    if (composer && scene && camera) {
      composer.render();
    } else if (renderer && scene && camera) {
      // Fallback to regular rendering if composer fails
      renderer.render(scene, camera);
    }
  } catch (error) {
    console.error("Error in animation loop:", error);
    // Don't stop the animation loop completely, just log errors
  }
}

// Handle window resize
function onWindowResize() {
  try {
    // Check if all required elements exist
    if (!galaxyCanvas || !camera || !renderer) {
      console.warn("Cannot resize: Missing core elements");
      return;
    }
    
    // Update canvas size
    const width = galaxyCanvas.clientWidth;
    const height = galaxyCanvas.clientHeight;
    
    // Update camera
    camera.aspect = width / height;
    camera.updateProjectionMatrix();
    
    // Update renderer and composer
    renderer.setSize(width, height);
    
    if (composer) {
      composer.setSize(width, height);
      
      // When in fullscreen mode, make sure we adjust the bloom effect
      if (document.querySelector('.galaxy-container').classList.contains('fullscreen')) {
        // Adjust bloom effect to look better in fullscreen mode
        if (composer.passes && composer.passes.length > 1) {
          const bloomPass = composer.passes[1]; // The bloom pass is the second pass
          if (bloomPass && typeof bloomPass.strength !== 'undefined') {
            bloomPass.strength = 0.8; // Increase the bloom strength
            bloomPass.radius = 0.5;   // Slightly increased radius
            bloomPass.threshold = 0.8; // Adjusted threshold
          }
        }
      } else {
        // Reset bloom effect for normal mode
        if (composer.passes && composer.passes.length > 1) {
          const bloomPass = composer.passes[1];
          if (bloomPass && typeof bloomPass.strength !== 'undefined') {
            bloomPass.strength = 0.7;
            bloomPass.radius = 0.4;
            bloomPass.threshold = 0.85;
          }
        }
      }
    }
    
    console.log(`Resized visualization to ${width}x${height}`);
  } catch (error) {
    console.error("Error handling window resize:", error);
  }
}

// Helper function to get domain color
function getDomainColor(domain) {
  switch (domain) {
    case 'engineering':
      return 0x4285F4; // Blue
    case 'manufacturing':
      return 0x34A853; // Green
    case 'research':
      return 0xEA4335; // Red
    case 'operations':
      return 0xFBBC05; // Amber
    default:
      return 0xCCCCCC; // Gray for unknown
  }
}

// Helper function to get significance color
function getSignificanceColor(significance) {
  switch (significance) {
    case 'high':
      return 0xFF5252; // Red
    case 'medium':
      return 0xFFA726; // Orange
    case 'low':
      return 0x66BB6A; // Green
    default:
      return 0xCCCCCC; // Gray for unknown
  }
}

// Helper function to get importance color
function getImportanceColor(importance) {
  switch (importance) {
    case 'high':
      return 0xFF9800; // Orange
    case 'medium':
      return 0xFFEB3B; // Yellow
    case 'low':
      return 0x8BC34A; // Light Green
    default:
      return 0xCCCCCC; // Gray for unknown
  }
}

// Helper function to get document icon
function getDocumentIcon(type) {
  if (!type) return 'fa-file';
  
  const lowerType = type.toLowerCase();
  if (lowerType.includes('pdf')) return 'fa-file-pdf';
  if (lowerType.includes('excel') || lowerType.includes('spreadsheet')) return 'fa-file-excel';
  if (lowerType.includes('word') || lowerType.includes('doc')) return 'fa-file-word';
  if (lowerType.includes('powerpoint') || lowerType.includes('presentation')) return 'fa-file-powerpoint';
  if (lowerType.includes('image')) return 'fa-file-image';
  if (lowerType.includes('code')) return 'fa-file-code';
  
  return 'fa-file-alt';
}

// Helper function to format domain name
function formatDomainName(domain) {
  if (!domain) return 'Unknown';
  
  // Capitalize first letter
  return domain.charAt(0).toUpperCase() + domain.slice(1);
}

// Helper function to format date
function formatDate(dateString) {
  if (!dateString) return 'Unknown';
  
  const date = new Date(dateString);
  return date.toLocaleDateString('en-US', { 
    year: 'numeric', 
    month: 'short', 
    day: 'numeric' 
  });
}

// Helper function to format significance
function formatSignificance(significance) {
  if (!significance) return 'Unknown';
  
  switch (significance) {
    case 'high':
      return 'High';
    case 'medium':
      return 'Medium';
    case 'low':
      return 'Low';
    default:
      return significance.charAt(0).toUpperCase() + significance.slice(1);
  }
}

// Helper function to format importance
function formatImportance(importance) {
  if (!importance) return 'Unknown';
  
  switch (importance) {
    case 'high':
      return 'High';
    case 'medium':
      return 'Medium';
    case 'low':
      return 'Low';
    default:
      return importance.charAt(0).toUpperCase() + importance.slice(1);
  }
}

// Mock user data for the assignment dialog
const mockUsers = [
  {
    id: 1,
    name: "Sarah Johnson",
    role: "Engineering Lead",
    department: "Engineering",
    avatar: null
  },
  {
    id: 2,
    name: "Michael Chen",
    role: "Senior Engineer",
    department: "Engineering",
    avatar: null
  },
  {
    id: 3,
    name: "Jessica Patel",
    role: "Data Scientist",
    department: "Research",
    avatar: null
  },
  {
    id: 4,
    name: "David Rodriguez",
    role: "QA Engineer",
    department: "Quality",
    avatar: null
  },
  {
    id: 5,
    name: "Alex Williams",
    role: "Product Manager",
    department: "Product",
    avatar: null
  },
  {
    id: 6,
    name: "Priya Sharma",
    role: "Research Lead",
    department: "Research",
    avatar: null
  },
  {
    id: 7,
    name: "Carlos Mendez",
    role: "Manufacturing Engineer",
    department: "Operations",
    avatar: null
  },
  {
    id: 8,
    name: "Emma Wilson",
    role: "Documentation Specialist",
    department: "Engineering",
    avatar: null
  }
];

// State variables for the assignment dialog
let currentAssignmentType = null;
let currentAssignmentItem = null;
let selectedUser = null;

// Open the assignment dialog
function openAssignmentDialog(type, item) {
  currentAssignmentType = type;
  currentAssignmentItem = item;
  selectedUser = null;
  
  // Set the dialog title based on type
  const titleElement = document.getElementById('assignment-title');
  titleElement.textContent = type === 'gap' ? 'Assign Knowledge Gap Follow-up' : 'Assign Question Follow-up';
  
  // Populate item info
  const itemInfoElement = document.getElementById('assignment-item-info');
  if (item) {
    let infoHtml = '';
    
    if (type === 'gap') {
      // Format connected clusters
      const connectedClusterNames = item.connectedClusters.map(id => {
        const cluster = knowledgeClusters.find(c => c.id === id);
        return cluster ? cluster.name : 'Unknown';
      }).join(', ');
      
      infoHtml = `
        <h4>Knowledge Gap Details</h4>
        <p><strong>Significance:</strong> ${formatSignificance(item.significance)}</p>
        <p><strong>Connected Areas:</strong> ${connectedClusterNames}</p>
        <p><strong>Identified:</strong> ${formatDate(item.identified)}</p>
        <p><strong>Questions:</strong> ${item.questions ? item.questions.length : 0} generated</p>
      `;
    } else if (type === 'question') {
      infoHtml = `
        <h4>Question Details</h4>
        <p><strong>Question:</strong> "${item.text}"</p>
        <p><strong>Importance:</strong> ${formatImportance(item.importance)}</p>
        <p><strong>Impact:</strong> ${item.impact}</p>
      `;
    }
    
    itemInfoElement.innerHTML = infoHtml;
  } else {
    itemInfoElement.innerHTML = '<p>No item details available.</p>';
  }
  
  // Clear search results and search input
  document.getElementById('user-search').value = '';
  document.getElementById('user-search-results').innerHTML = '';
  
  // Set default due date to 2 weeks from today
  const dueDate = new Date();
  dueDate.setDate(dueDate.getDate() + 14);
  document.getElementById('due-date').valueAsDate = dueDate;
  
  // Clear notes
  document.getElementById('assignment-notes').value = '';
  
  // Show the dialog
  const dialog = document.getElementById('assignment-dialog');
  dialog.style.display = 'flex';
}

// Close the assignment dialog
function closeAssignmentDialog() {
  document.getElementById('assignment-dialog').style.display = 'none';
  currentAssignmentType = null;
  currentAssignmentItem = null;
  selectedUser = null;
}

// Search for users
function searchUsers() {
  const searchTerm = document.getElementById('user-search').value.toLowerCase().trim();
  const resultsContainer = document.getElementById('user-search-results');
  
  // Clear previous results
  resultsContainer.innerHTML = '';
  
  if (searchTerm === '') {
    // Show all users if no search term
    displaySearchResults(mockUsers);
    return;
  }
  
  // Filter users based on search term
  const filteredUsers = mockUsers.filter(user => 
    user.name.toLowerCase().includes(searchTerm) || 
    user.role.toLowerCase().includes(searchTerm) || 
    user.department.toLowerCase().includes(searchTerm)
  );
  
  displaySearchResults(filteredUsers);
}

// Display search results
function displaySearchResults(users) {
  const resultsContainer = document.getElementById('user-search-results');
  
  if (users.length === 0) {
    resultsContainer.innerHTML = '<p class="no-results">No matching users found</p>';
    return;
  }
  
  // Create user cards
  users.forEach(user => {
    const userCard = document.createElement('div');
    userCard.className = 'user-card';
    userCard.dataset.userId = user.id;
    
    // Create avatar element
    const avatar = document.createElement('div');
    avatar.className = 'user-avatar';
    
    if (user.avatar) {
      const img = document.createElement('img');
      img.src = user.avatar;
      img.alt = user.name;
      avatar.appendChild(img);
    } else {
      // Use initials if no avatar
      const initials = user.name.split(' ')
        .map(word => word[0])
        .slice(0, 2)
        .join('');
      avatar.textContent = initials;
    }
    
    // Create user info element
    const userInfo = document.createElement('div');
    userInfo.className = 'user-info';
    
    const userName = document.createElement('div');
    userName.className = 'user-name';
    userName.textContent = user.name;
    
    const userRole = document.createElement('div');
    userRole.className = 'user-role';
    userRole.textContent = `${user.role} • ${user.department}`;
    
    userInfo.appendChild(userName);
    userInfo.appendChild(userRole);
    
    // Add elements to user card
    userCard.appendChild(avatar);
    userCard.appendChild(userInfo);
    
    // Add click handler
    userCard.addEventListener('click', () => {
      // Remove selection from all cards
      document.querySelectorAll('.user-card.selected').forEach(card => {
        card.classList.remove('selected');
      });
      
      // Select this card
      userCard.classList.add('selected');
      selectedUser = user;
    });
    
    // Add to results container
    resultsContainer.appendChild(userCard);
  });
}

// Confirm the assignment
function confirmAssignment() {
  if (!selectedUser) {
    alert('Please select a team member to assign this to.');
    return;
  }
  
  const dueDate = document.getElementById('due-date').value;
  const priority = document.getElementById('assignment-priority').value;
  const notes = document.getElementById('assignment-notes').value;
  
  let successMessage = '';
  
  if (currentAssignmentType === 'gap') {
    successMessage = `Knowledge Gap successfully assigned to ${selectedUser.name}.\n\nDue: ${dueDate}\nPriority: ${priority}`;
  } else if (currentAssignmentType === 'question') {
    successMessage = `Question successfully assigned to ${selectedUser.name}.\n\nDue: ${dueDate}\nPriority: ${priority}`;
  }
  
  alert(successMessage);
  closeAssignmentDialog();
}

// Initialize when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
  // Initialize domain data first
  initDomainBasedData();
  
  // Update page title based on domain
  const urlParams = new URLSearchParams(window.location.search);
  const domain = urlParams.get('domain');
  if (domain === 'automotive') {
    document.title = "Automotive Knowledge Galaxy | BrahmaSumm";
    // Update any domain-specific UI elements
    const titleElements = document.querySelectorAll('.sec-title_heading, h1');
    titleElements.forEach(el => {
      if (el.textContent.includes('Aerospace')) {
        el.textContent = el.textContent.replace('Aerospace', 'Automotive');
      }
    });
  }
  
  // Add a short delay to ensure everything is rendered
  setTimeout(() => {
    // Check if the canvas element exists and has dimensions
    const canvas = document.getElementById('galaxy-canvas');
    if (!canvas) {
      console.error("Galaxy canvas element not found");
      return;
    }
    
    const width = canvas.clientWidth;
    const height = canvas.clientHeight;
    
    if (width === 0 || height === 0) {
      console.warn("Galaxy canvas has zero dimensions. Width:", width, "Height:", height);
      console.log("Container visibility may be an issue. Adding a retry...");
      
      // Retry after a longer delay
      setTimeout(() => {
        console.log("Retrying galaxy initialization...");
        if (canvas.clientWidth > 0 && canvas.clientHeight > 0) {
          initGalaxy();
        } else {
          console.error("Galaxy canvas still has zero dimensions after retry");
        }
      }, 1000);
      
      return;
    }
    
    console.log("Galaxy canvas dimensions: Width:", width, "Height:", height);
    
    // Update stats based on domain
    if (domain === 'automotive') {
      document.getElementById('total-clusters').textContent = "24";
      document.getElementById('total-gaps').textContent = "45";
      document.getElementById('total-questions').textContent = "112";
      document.getElementById('critical-insights').textContent = "18";
    }
    
    initGalaxy();
  }, 100);
});