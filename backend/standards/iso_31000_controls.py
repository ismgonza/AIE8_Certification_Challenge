"""
ISO 31000:2018 Risk Management Controls
Based on Principles, Framework, and Process structure
"""

ISO_31000_CONTROLS = {
    # Principles (Clause 4)
    "principles": [
        {
            "id": "4.1",
            "title": "Integrated",
            "priority": "high",
            "estimated_hours": 8,
            "owner": "Risk Manager / CISO",
            "deliverables": [
                "Risk_Integration_Strategy.docx",
                "Organizational_Integration_Plan.pdf"
            ],
            "description": "Risk management is an integral part of all organizational activities"
        },
        {
            "id": "4.2",
            "title": "Structured and Comprehensive",
            "priority": "high",
            "estimated_hours": 6,
            "owner": "Risk Manager",
            "deliverables": [
                "Risk_Management_Framework.docx",
                "Structured_Approach_Guide.pdf"
            ],
            "description": "A structured and comprehensive approach to risk management contributes to consistent and comparable results"
        },
        {
            "id": "4.3",
            "title": "Customized",
            "priority": "high",
            "estimated_hours": 5,
            "owner": "Risk Manager / Senior Management",
            "deliverables": [
                "Organizational_Context_Analysis.docx",
                "Customization_Criteria.xlsx"
            ],
            "description": "The risk management framework and process are customized and proportionate to the organization's external and internal context"
        },
        {
            "id": "4.4",
            "title": "Inclusive",
            "priority": "medium",
            "estimated_hours": 4,
            "owner": "Risk Manager / Department Heads",
            "deliverables": [
                "Stakeholder_Engagement_Plan.docx",
                "Stakeholder_Register.xlsx"
            ],
            "description": "Appropriate and timely involvement of stakeholders enables their knowledge, views and perceptions to be considered"
        },
        {
            "id": "4.5",
            "title": "Dynamic",
            "priority": "medium",
            "estimated_hours": 6,
            "owner": "Risk Manager",
            "deliverables": [
                "Risk_Monitoring_Procedure.docx",
                "Dynamic_Review_Schedule.xlsx"
            ],
            "description": "Risks can emerge, change or disappear as an organization's external and internal context changes"
        },
        {
            "id": "4.6",
            "title": "Best Available Information",
            "priority": "high",
            "estimated_hours": 5,
            "owner": "Risk Manager / Data Analyst",
            "deliverables": [
                "Information_Sources_Document.docx",
                "Data_Quality_Assessment.xlsx"
            ],
            "description": "The inputs to risk management are based on historical and current information, as well as future expectations"
        },
        {
            "id": "4.7",
            "title": "Human and Cultural Factors",
            "priority": "medium",
            "estimated_hours": 4,
            "owner": "HR Manager / Risk Manager",
            "deliverables": [
                "Risk_Culture_Assessment.docx",
                "Training_Plan.pdf"
            ],
            "description": "Human behavior and culture significantly influence all aspects of risk management at each level and stage"
        },
        {
            "id": "4.8",
            "title": "Continual Improvement",
            "priority": "medium",
            "estimated_hours": 5,
            "owner": "Risk Manager / Quality Manager",
            "deliverables": [
                "Continuous_Improvement_Plan.docx",
                "Lessons_Learned_Register.xlsx"
            ],
            "description": "Risk management is continually improved through learning and experience"
        }
    ],
    
    # Framework (Clause 5)
    "framework": [
        {
            "id": "5.3",
            "title": "Leadership and Commitment",
            "priority": "high",
            "estimated_hours": 6,
            "owner": "CEO / Senior Management",
            "deliverables": [
                "Risk_Management_Commitment_Statement.pdf",
                "Risk_Governance_Charter.docx",
                "Management_Review_Schedule.xlsx"
            ],
            "description": "Top management and oversight bodies should ensure risk management is integrated into all organizational activities"
        },
        {
            "id": "5.4.1",
            "title": "Integration into Organizational Processes",
            "priority": "high",
            "estimated_hours": 10,
            "owner": "Risk Manager / Process Owners",
            "deliverables": [
                "Process_Integration_Plan.docx",
                "Risk_Workflow_Procedures.pdf",
                "Integration_Roadmap.xlsx"
            ],
            "description": "Risk management should be integrated into all parts of the organization's structure"
        },
        {
            "id": "5.4.2",
            "title": "Design of Framework for Managing Risk",
            "priority": "high",
            "estimated_hours": 12,
            "owner": "Risk Manager / Senior Management",
            "deliverables": [
                "Risk_Management_Framework_Document.docx",
                "Framework_Design_Specifications.pdf",
                "Accountability_Matrix.xlsx"
            ],
            "description": "Understanding the organization and its context, establishing risk management policy, and defining accountability"
        },
        {
            "id": "5.5",
            "title": "Implementation of Risk Management",
            "priority": "high",
            "estimated_hours": 15,
            "owner": "Risk Manager / All Departments",
            "deliverables": [
                "Implementation_Plan.docx",
                "Training_Materials.pptx",
                "Implementation_Timeline.xlsx",
                "Communication_Strategy.pdf"
            ],
            "description": "Implement the risk management framework including timeframe, resources, and communication plan"
        },
        {
            "id": "5.6",
            "title": "Evaluation of Risk Management Framework",
            "priority": "medium",
            "estimated_hours": 8,
            "owner": "Risk Manager / Internal Audit",
            "deliverables": [
                "Framework_Evaluation_Report.docx",
                "Performance_Metrics.xlsx",
                "Effectiveness_Assessment.pdf"
            ],
            "description": "Periodically measure risk management framework performance against its purpose, plans, and KPIs"
        },
        {
            "id": "5.7",
            "title": "Improvement of Risk Management Framework",
            "priority": "medium",
            "estimated_hours": 6,
            "owner": "Risk Manager",
            "deliverables": [
                "Improvement_Action_Plan.docx",
                "Framework_Enhancement_Proposals.pdf"
            ],
            "description": "Continually improve the suitability, adequacy and effectiveness of the risk management framework"
        }
    ],
    
    # Process (Clause 6)
    "process": [
        {
            "id": "6.2",
            "title": "Communication and Consultation",
            "priority": "high",
            "estimated_hours": 6,
            "owner": "Risk Manager / Communications",
            "deliverables": [
                "Communication_Plan.docx",
                "Stakeholder_Communication_Matrix.xlsx",
                "Consultation_Procedures.pdf"
            ],
            "description": "Facilitate factual, timely, relevant and accurate exchange of information regarding risk"
        },
        {
            "id": "6.3",
            "title": "Scope, Context and Criteria",
            "priority": "high",
            "estimated_hours": 10,
            "owner": "Risk Manager / Senior Management",
            "deliverables": [
                "Scope_Definition_Document.docx",
                "External_Context_Analysis.pdf",
                "Internal_Context_Analysis.pdf",
                "Risk_Criteria_Matrix.xlsx"
            ],
            "description": "Define scope, understand external and internal context, and establish risk criteria"
        },
        {
            "id": "6.4.1",
            "title": "Risk Identification",
            "priority": "high",
            "estimated_hours": 12,
            "owner": "Risk Manager / Department Heads",
            "deliverables": [
                "Risk_Identification_Procedure.docx",
                "Risk_Register.xlsx",
                "Risk_Identification_Workshop_Guide.pptx",
                "Risk_Library.xlsx"
            ],
            "description": "Find, recognize and describe risks that might help or prevent achieving objectives"
        },
        {
            "id": "6.4.2",
            "title": "Risk Analysis",
            "priority": "high",
            "estimated_hours": 10,
            "owner": "Risk Manager / Risk Analysts",
            "deliverables": [
                "Risk_Analysis_Methodology.docx",
                "Likelihood_Impact_Matrix.xlsx",
                "Risk_Heat_Map.pdf",
                "Analysis_Templates.xlsx"
            ],
            "description": "Comprehend the nature of risk and determine the level of risk through analysis of consequences and likelihood"
        },
        {
            "id": "6.4.3",
            "title": "Risk Evaluation",
            "priority": "high",
            "estimated_hours": 8,
            "owner": "Risk Manager / Senior Management",
            "deliverables": [
                "Risk_Evaluation_Criteria.docx",
                "Risk_Prioritization_Matrix.xlsx",
                "Risk_Acceptance_Guidelines.pdf",
                "Evaluation_Report.docx"
            ],
            "description": "Compare results of risk analysis with risk criteria to determine if risk is acceptable or requires treatment"
        },
        {
            "id": "6.5",
            "title": "Risk Treatment",
            "priority": "high",
            "estimated_hours": 15,
            "owner": "Risk Owners / Risk Manager",
            "deliverables": [
                "Risk_Treatment_Plan.docx",
                "Treatment_Options_Analysis.xlsx",
                "Implementation_Roadmap.pdf",
                "Residual_Risk_Assessment.xlsx",
                "Treatment_Action_Tracker.xlsx"
            ],
            "description": "Select and implement options for addressing risk (avoid, modify, share, or retain)"
        },
        {
            "id": "6.6",
            "title": "Monitoring and Review",
            "priority": "high",
            "estimated_hours": 10,
            "owner": "Risk Manager / Risk Owners",
            "deliverables": [
                "Monitoring_Review_Procedure.docx",
                "KRI_Dashboard.xlsx",
                "Review_Schedule.xlsx",
                "Monitoring_Report_Template.docx"
            ],
            "description": "Monitor and review risk management process and its outcomes through continual surveillance"
        },
        {
            "id": "6.7",
            "title": "Recording and Reporting",
            "priority": "high",
            "estimated_hours": 8,
            "owner": "Risk Manager",
            "deliverables": [
                "Recording_Reporting_Procedure.docx",
                "Risk_Report_Templates.docx",
                "Risk_Dashboard.xlsx",
                "Board_Report_Template.pptx"
            ],
            "description": "Document the risk management process, results, and communicate them to stakeholders"
        }
    ]
}


def get_all_controls():
    """Get all controls as a flat list."""
    all_controls = []
    for theme, controls in ISO_31000_CONTROLS.items():
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

