"""
Multi-standard support: ISO 27001, ISO 31000, ISO 19011, etc.
"""

STANDARDS = {
    "ISO_27001": {
        "id": "ISO_27001",
        "name": "ISO/IEC 27001:2022",
        "title": "Information Security Management",
        "description": "Requirements for establishing, implementing, maintaining and continually improving an information security management system",
        "icon": "🔒",
        "color": "blue",
        "controls_module": "iso_27001_controls"  # References iso_controls.py
    },
    "ISO_31000": {
        "id": "ISO_31000",
        "name": "ISO 31000:2018",
        "title": "Risk Management",
        "description": "Guidelines for risk management to help organizations develop a risk management strategy",
        "icon": "⚠️",
        "color": "orange",
        "controls_module": "iso_31000_controls"
    },
    "ISO_19011": {
        "id": "ISO_19011",
        "name": "ISO 19011:2018",
        "title": "Auditing Management Systems",
        "description": "Guidelines for auditing management systems, including principles of auditing and managing audit programs",
        "icon": "📋",
        "color": "green",
        "controls_module": "iso_19011_controls",  # Future: create this file
        "status": "coming_soon"
    },
    "ISO_9001": {
        "id": "ISO_9001",
        "name": "ISO 9001:2015",
        "title": "Quality Management",
        "description": "Requirements for a quality management system",
        "icon": "✅",
        "color": "purple",
        "controls_module": "iso_9001_controls",  # Future: create this file
        "status": "coming_soon"
    }
}


def get_available_standards():
    """Get all standards with their status."""
    return [
        {
            **standard,
            "is_available": standard.get("status") != "coming_soon"
        }
        for standard in STANDARDS.values()
    ]


def get_standard_info(standard_id: str):
    """Get information about a specific standard."""
    return STANDARDS.get(standard_id)


def get_controls_for_standard(standard_id: str):
    """
    Get controls for a specific standard.
    Returns controls from the appropriate module.
    """
    standard = STANDARDS.get(standard_id)
    if not standard:
        return []
    
    # Dynamic import based on standard
    if standard_id == "ISO_27001":
        from standards.iso_27001_controls import get_all_controls
        controls = get_all_controls()
        # Add standard_id to each control
        for control in controls:
            control["standard_id"] = "ISO_27001"
        return controls
    
    # Future standards loaded from standards/ folder
    elif standard_id == "ISO_31000":
        from standards.iso_31000_controls import get_all_controls
        controls = get_all_controls()
        # Add standard_id to each control
        for control in controls:
            control["standard_id"] = "ISO_31000"
        return controls
    # elif standard_id == "ISO_19011":
    #     from standards.iso_19011_controls import get_all_controls
    #     return get_all_controls()
    
    return []

