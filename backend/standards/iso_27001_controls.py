"""
ISO 27001:2022 Controls Database
93 controls organized by theme
"""

ISO_CONTROLS = {
    # Organizational Controls (5.1 - 5.37)
    "organizational": [
        {
            "id": "5.1",
            "title": "Policies for Information Security",
            "priority": "high",
            "estimated_hours": 4,
            "owner": "CISO / IT Manager",
            "deliverables": [
                "Information_Security_Policy.docx",
                "Policy_Approval_Form.pdf"
            ],
            "description": "Define and document information security policies approved by management"
        },
        {
            "id": "5.2",
            "title": "Information Security Roles and Responsibilities",
            "priority": "high",
            "estimated_hours": 3,
            "owner": "CISO / HR Manager",
            "deliverables": [
                "Roles_And_Responsibilities_Matrix.xlsx",
                "Job_Descriptions_Security_Roles.docx"
            ],
            "description": "Define and assign information security roles and responsibilities"
        },
        {
            "id": "5.3",
            "title": "Segregation of Duties",
            "priority": "medium",
            "estimated_hours": 2,
            "owner": "CISO / IT Manager",
            "deliverables": [
                "Segregation_Of_Duties_Policy.docx",
                "Access_Separation_Matrix.xlsx"
            ],
            "description": "Separate conflicting duties to reduce unauthorized or unintentional changes"
        },
        {
            "id": "5.7",
            "title": "Threat Intelligence",
            "priority": "high",
            "estimated_hours": 6,
            "owner": "Security Analyst / CISO",
            "deliverables": [
                "Threat_Intelligence_Procedure.docx",
                "Threat_Intelligence_Sources_List.xlsx"
            ],
            "description": "Collect and analyze threat intelligence information"
        },
        {
            "id": "5.15",
            "title": "Access Control",
            "priority": "high",
            "estimated_hours": 8,
            "owner": "IT Administrator",
            "deliverables": [
                "Access_Control_Policy.docx",
                "Access_Control_Matrix.xlsx",
                "Access_Review_Procedure.docx"
            ],
            "description": "Establish and document access control rules"
        },
        {
            "id": "5.16",
            "title": "Identity Management",
            "priority": "high",
            "estimated_hours": 6,
            "owner": "IT Administrator",
            "deliverables": [
                "Identity_Management_Policy.docx",
                "User_Lifecycle_Procedure.docx"
            ],
            "description": "Manage the full lifecycle of identities"
        },
        {
            "id": "5.17",
            "title": "Authentication Information",
            "priority": "high",
            "estimated_hours": 5,
            "owner": "IT Administrator",
            "deliverables": [
                "Password_Policy.docx",
                "MFA_Implementation_Guide.docx"
            ],
            "description": "Manage authentication information (passwords, tokens, etc.)"
        },
        {
            "id": "5.18",
            "title": "Access Rights",
            "priority": "high",
            "estimated_hours": 4,
            "owner": "IT Administrator / HR",
            "deliverables": [
                "Access_Rights_Procedure.docx",
                "Provisioning_Checklist.xlsx"
            ],
            "description": "Provision and de-provision access rights"
        },
        {
            "id": "5.23",
            "title": "Information Security for Use of Cloud Services",
            "priority": "medium",
            "estimated_hours": 8,
            "owner": "Cloud Architect / CISO",
            "deliverables": [
                "Cloud_Security_Policy.docx",
                "Cloud_Vendor_Assessment.xlsx"
            ],
            "description": "Secure information when using cloud services"
        },
        {
            "id": "5.30",
            "title": "ICT Readiness for Business Continuity",
            "priority": "medium",
            "estimated_hours": 12,
            "owner": "CISO / Operations Manager",
            "deliverables": [
                "Business_Continuity_Plan.docx",
                "Disaster_Recovery_Procedure.docx",
                "Recovery_Time_Objectives.xlsx"
            ],
            "description": "Ensure ICT readiness for business continuity"
        }
    ],
    
    # People Controls (6.1 - 6.8)
    "people": [
        {
            "id": "6.1",
            "title": "Screening",
            "priority": "high",
            "estimated_hours": 3,
            "owner": "HR Manager",
            "deliverables": [
                "Background_Check_Policy.docx",
                "Screening_Checklist.xlsx"
            ],
            "description": "Conduct background verification checks on candidates"
        },
        {
            "id": "6.2",
            "title": "Terms and Conditions of Employment",
            "priority": "high",
            "estimated_hours": 4,
            "owner": "HR Manager / Legal",
            "deliverables": [
                "Security_Employment_Agreement_Template.docx",
                "NDA_Template.docx"
            ],
            "description": "Include information security responsibilities in employment agreements"
        },
        {
            "id": "6.3",
            "title": "Information Security Awareness, Education and Training",
            "priority": "high",
            "estimated_hours": 10,
            "owner": "CISO / HR Manager",
            "deliverables": [
                "Security_Training_Plan.docx",
                "Awareness_Materials.pptx",
                "Training_Records.xlsx"
            ],
            "description": "Provide security awareness education and training"
        }
    ],
    
    # Physical Controls (7.1 - 7.14)
    "physical": [
        {
            "id": "7.1",
            "title": "Physical Security Perimeters",
            "priority": "medium",
            "estimated_hours": 6,
            "owner": "Facilities Manager",
            "deliverables": [
                "Physical_Security_Policy.docx",
                "Perimeter_Security_Assessment.xlsx"
            ],
            "description": "Define and implement physical security perimeters"
        },
        {
            "id": "7.4",
            "title": "Physical Security Monitoring",
            "priority": "medium",
            "estimated_hours": 5,
            "owner": "Facilities Manager / Security",
            "deliverables": [
                "Physical_Monitoring_Procedure.docx",
                "Camera_Coverage_Map.pdf"
            ],
            "description": "Monitor premises for unauthorized physical access"
        }
    ],
    
    # Technological Controls (8.1 - 8.34)
    "technological": [
        {
            "id": "8.1",
            "title": "User Endpoint Devices",
            "priority": "high",
            "estimated_hours": 6,
            "owner": "IT Administrator",
            "deliverables": [
                "Endpoint_Security_Policy.docx",
                "Device_Configuration_Standards.docx"
            ],
            "description": "Protect information on user endpoint devices"
        },
        {
            "id": "8.2",
            "title": "Privileged Access Rights",
            "priority": "high",
            "estimated_hours": 5,
            "owner": "IT Administrator",
            "deliverables": [
                "Privileged_Access_Policy.docx",
                "Admin_Access_Log.xlsx"
            ],
            "description": "Restrict and control privileged access rights"
        },
        {
            "id": "8.5",
            "title": "Secure Authentication",
            "priority": "high",
            "estimated_hours": 8,
            "owner": "IT Administrator",
            "deliverables": [
                "MFA_Implementation_Plan.docx",
                "Authentication_Configuration.docx"
            ],
            "description": "Implement secure authentication technologies and procedures"
        },
        {
            "id": "8.8",
            "title": "Management of Technical Vulnerabilities",
            "priority": "high",
            "estimated_hours": 10,
            "owner": "Security Analyst / IT",
            "deliverables": [
                "Vulnerability_Management_Policy.docx",
                "Patch_Management_Procedure.docx",
                "Vulnerability_Scan_Schedule.xlsx"
            ],
            "description": "Identify, assess, and manage technical vulnerabilities"
        },
        {
            "id": "8.9",
            "title": "Configuration Management",
            "priority": "medium",
            "estimated_hours": 8,
            "owner": "IT Administrator",
            "deliverables": [
                "Configuration_Management_Policy.docx",
                "Baseline_Configurations.xlsx"
            ],
            "description": "Establish and maintain configurations for security"
        },
        {
            "id": "8.10",
            "title": "Information Deletion",
            "priority": "medium",
            "estimated_hours": 4,
            "owner": "IT Administrator",
            "deliverables": [
                "Data_Deletion_Policy.docx",
                "Secure_Disposal_Procedure.docx"
            ],
            "description": "Delete information when no longer required"
        },
        {
            "id": "8.16",
            "title": "Monitoring Activities",
            "priority": "high",
            "estimated_hours": 12,
            "owner": "Security Analyst",
            "deliverables": [
                "Logging_And_Monitoring_Policy.docx",
                "Log_Review_Procedure.docx",
                "SIEM_Configuration.docx"
            ],
            "description": "Monitor networks, systems, and applications for security events"
        },
        {
            "id": "8.23",
            "title": "Web Filtering",
            "priority": "medium",
            "estimated_hours": 4,
            "owner": "IT Administrator",
            "deliverables": [
                "Web_Filtering_Policy.docx",
                "Blocked_Categories_List.xlsx"
            ],
            "description": "Control access to external websites"
        },
        {
            "id": "8.24",
            "title": "Use of Cryptography",
            "priority": "high",
            "estimated_hours": 8,
            "owner": "Security Architect / IT",
            "deliverables": [
                "Cryptography_Policy.docx",
                "Encryption_Standards.docx",
                "Key_Management_Procedure.docx"
            ],
            "description": "Define and implement rules for cryptographic controls"
        },
        {
            "id": "8.28",
            "title": "Secure Coding",
            "priority": "medium",
            "estimated_hours": 10,
            "owner": "Development Lead",
            "deliverables": [
                "Secure_Coding_Standards.docx",
                "Code_Review_Checklist.xlsx"
            ],
            "description": "Apply secure coding principles in software development"
        }
    ]
}


def get_all_controls():
    """Get all controls as a flat list."""
    all_controls = []
    for theme, controls in ISO_CONTROLS.items():
        for control in controls:
            control["theme"] = theme
            all_controls.append(control)
    return sorted(all_controls, key=lambda x: x["id"])


def get_high_priority_controls():
    """Get only high-priority controls."""
    all_controls = get_all_controls()
    return [c for c in all_controls if c.get("priority") == "high"]


def get_control_by_id(control_id: str):
    """Get a specific control by ID."""
    all_controls = get_all_controls()
    for control in all_controls:
        if control["id"] == control_id:
            return control
    return None

