"""
Sample test data for rawData Google Sheets table
Mimics the 23-column structure (A:W, indices 0-22)
"""

# Sample rawData for testing - 23 fields per row
SAMPLE_RAW_DATA_BASIC = [
    ["Key", "Issue Type", "Summary", "Description", "Priority", "Status", "Sprint", "Assignee", "Reporter",
     "Created", "Updated", "Due Date", "Labels", "Components", "Fix Versions", "Story Points", "Original Estimate",
     "Remaining Estimate", "Time Spent", "Epic Link", "Parent", "Custom Field 1", "Custom Field 2"],  # Header row

    # Issue 1: Done, with story points
    ["PROJ-001", "Story", "Implement login", "User login feature", "High", "Done", "Sprint 1", "John Doe", "Jane Smith",
     "2025-01-01", "2025-01-10", "2025-01-15", "backend,auth", "Authentication", "v1.0", "5", "8h",
     "0h", "8h", "EPIC-1", "", "value1", "value2"],

    # Issue 2: In Progress, with story points
    ["PROJ-002", "Task", "Setup database", "Configure PostgreSQL", "High", "In Progress", "Sprint 1", "John Doe", "Jane Smith",
     "2025-01-02", "2025-01-11", "2025-01-16", "backend,db", "Backend", "v1.0", "3", "5h",
     "2h", "3h", "EPIC-1", "", "value1", "value2"],

    # Issue 3: Done, with story points
    ["PROJ-003", "Bug", "Fix login bug", "Login button not working", "Critical", "Done", "Sprint 1", "Jane Smith", "John Doe",
     "2025-01-03", "2025-01-12", "2025-01-17", "frontend,bug", "UI", "v1.0", "2", "3h",
     "0h", "3h", "EPIC-1", "", "value1", "value2"],

    # Issue 4: To Do, with story points
    ["PROJ-004", "Story", "User dashboard", "Create user dashboard page", "Medium", "To Do", "Sprint 2", "John Doe", "Jane Smith",
     "2025-01-04", "2025-01-13", "2025-01-18", "frontend", "UI", "v1.0", "8", "12h",
     "12h", "0h", "EPIC-2", "", "value1", "value2"],

    # Issue 5: Done, no story points
    ["PROJ-005", "Task", "Documentation", "Update README", "Low", "Done", "", "Jane Smith", "John Doe",
     "2025-01-05", "2025-01-14", "2025-01-19", "docs", "Documentation", "v1.0", "0", "2h",
     "0h", "2h", "", "", "value1", "value2"],

    # Issue 6: Waiting, with story points
    ["PROJ-006", "Story", "Payment integration", "Integrate Stripe", "High", "Waiting", "Sprint 2", "John Doe", "Jane Smith",
     "2025-01-06", "2025-01-15", "2025-01-20", "backend,payment", "Backend", "v1.1", "13", "20h",
     "20h", "0h", "EPIC-2", "", "value1", "value2"],
]

# Sample rawData with all 9 statuses
SAMPLE_RAW_DATA_ALL_STATUSES = [
    ["Key", "Issue Type", "Summary", "Description", "Priority", "Status", "Sprint", "Assignee", "Reporter",
     "Created", "Updated", "Due Date", "Labels", "Components", "Fix Versions", "Story Points", "Original Estimate",
     "Remaining Estimate", "Time Spent", "Epic Link", "Parent", "Custom Field 1", "Custom Field 2"],

    # Backlog (2 issues)
    ["PROJ-101", "Story", "Feature A", "Description A", "Medium", "Backlog", "Sprint 1", "Dev1", "PM1",
     "2025-01-01", "2025-01-02", "", "feature", "Component1", "", "3", "", "", "", "", "", "", ""],
    ["PROJ-102", "Task", "Task B", "Description B", "Low", "Backlog", "Sprint 1", "Dev2", "PM1",
     "2025-01-01", "2025-01-02", "", "", "Component1", "", "2", "", "", "", "", "", "", ""],

    # Evaluated (1 issue)
    ["PROJ-103", "Story", "Feature C", "Description C", "High", "Evaluated", "Sprint 1", "Dev1", "PM1",
     "2025-01-01", "2025-01-02", "", "feature", "Component2", "", "5", "", "", "", "", "", "", ""],

    # To Do (3 issues)
    ["PROJ-104", "Task", "Task D", "Description D", "Medium", "To Do", "Sprint 1", "Dev2", "PM1",
     "2025-01-01", "2025-01-02", "", "", "Component2", "", "2", "", "", "", "", "", "", ""],
    ["PROJ-105", "Bug", "Bug E", "Description E", "High", "To Do", "Sprint 1", "Dev3", "PM1",
     "2025-01-01", "2025-01-02", "", "bug", "Component1", "", "1", "", "", "", "", "", "", ""],
    ["PROJ-106", "Story", "Feature F", "Description F", "Medium", "To Do", "Sprint 2", "Dev1", "PM1",
     "2025-01-01", "2025-01-02", "", "feature", "Component3", "", "5", "", "", "", "", "", "", ""],

    # In Progress (5 issues)
    ["PROJ-107", "Task", "Task G", "Description G", "High", "In Progress", "Sprint 1", "Dev2", "PM1",
     "2025-01-01", "2025-01-02", "", "", "Component2", "", "3", "", "", "", "", "", "", ""],
    ["PROJ-108", "Story", "Feature H", "Description H", "Medium", "In Progress", "Sprint 1", "Dev3", "PM1",
     "2025-01-01", "2025-01-02", "", "feature", "Component3", "", "8", "", "", "", "", "", "", ""],
    ["PROJ-109", "Bug", "Bug I", "Description I", "Critical", "In Progress", "Sprint 1", "Dev1", "PM1",
     "2025-01-01", "2025-01-02", "", "bug", "Component1", "", "2", "", "", "", "", "", "", ""],
    ["PROJ-110", "Task", "Task J", "Description J", "Medium", "In Progress", "Sprint 2", "Dev2", "PM1",
     "2025-01-01", "2025-01-02", "", "", "Component2", "", "3", "", "", "", "", "", "", ""],
    ["PROJ-111", "Story", "Feature K", "Description K", "High", "In Progress", "Sprint 2", "Dev3", "PM1",
     "2025-01-01", "2025-01-02", "", "feature", "Component3", "", "5", "", "", "", "", "", "", ""],

    # Waiting (2 issues)
    ["PROJ-112", "Task", "Task L", "Description L", "Medium", "Waiting", "Sprint 1", "Dev1", "PM1",
     "2025-01-01", "2025-01-02", "", "", "Component1", "", "2", "", "", "", "", "", "", ""],
    ["PROJ-113", "Bug", "Bug M", "Description M", "High", "Waiting", "Sprint 2", "Dev2", "PM1",
     "2025-01-01", "2025-01-02", "", "bug", "Component2", "", "1", "", "", "", "", "", "", ""],

    # Ready to Verify (4 issues)
    ["PROJ-114", "Story", "Feature N", "Description N", "Medium", "Ready to Verify", "Sprint 1", "Dev3", "PM1",
     "2025-01-01", "2025-01-02", "", "feature", "Component3", "", "5", "", "", "", "", "", "", ""],
    ["PROJ-115", "Task", "Task O", "Description O", "Low", "Ready to Verify", "Sprint 1", "Dev1", "PM1",
     "2025-01-01", "2025-01-02", "", "", "Component1", "", "2", "", "", "", "", "", "", ""],
    ["PROJ-116", "Bug", "Bug P", "Description P", "High", "Ready to Verify", "Sprint 2", "Dev2", "PM1",
     "2025-01-01", "2025-01-02", "", "bug", "Component2", "", "1", "", "", "", "", "", "", ""],
    ["PROJ-117", "Story", "Feature Q", "Description Q", "Medium", "Ready to Verify", "Sprint 2", "Dev3", "PM1",
     "2025-01-01", "2025-01-02", "", "feature", "Component3", "", "3", "", "", "", "", "", "", ""],

    # Done (8 issues)
    ["PROJ-118", "Task", "Task R", "Description R", "High", "Done", "Sprint 1", "Dev1", "PM1",
     "2025-01-01", "2025-01-02", "", "", "Component1", "", "3", "", "", "", "", "", "", ""],
    ["PROJ-119", "Story", "Feature S", "Description S", "Medium", "Done", "Sprint 1", "Dev2", "PM1",
     "2025-01-01", "2025-01-02", "", "feature", "Component2", "", "5", "", "", "", "", "", "", ""],
    ["PROJ-120", "Bug", "Bug T", "Description T", "Critical", "Done", "Sprint 1", "Dev3", "PM1",
     "2025-01-01", "2025-01-02", "", "bug", "Component3", "", "2", "", "", "", "", "", "", ""],
    ["PROJ-121", "Task", "Task U", "Description U", "Medium", "Done", "Sprint 1", "Dev1", "PM1",
     "2025-01-01", "2025-01-02", "", "", "Component1", "", "3", "", "", "", "", "", "", ""],
    ["PROJ-122", "Story", "Feature V", "Description V", "High", "Done", "Sprint 2", "Dev2", "PM1",
     "2025-01-01", "2025-01-02", "", "feature", "Component2", "", "8", "", "", "", "", "", "", ""],
    ["PROJ-123", "Bug", "Bug W", "Description W", "High", "Done", "Sprint 2", "Dev3", "PM1",
     "2025-01-01", "2025-01-02", "", "bug", "Component3", "", "1", "", "", "", "", "", "", ""],
    ["PROJ-124", "Task", "Task X", "Description X", "Low", "Done", "Sprint 2", "Dev1", "PM1",
     "2025-01-01", "2025-01-02", "", "", "Component1", "", "2", "", "", "", "", "", "", ""],
    ["PROJ-125", "Story", "Feature Y", "Description Y", "Medium", "Done", "", "Dev2", "PM1",
     "2025-01-01", "2025-01-02", "", "feature", "Component2", "", "3", "", "", "", "", "", "", ""],

    # Invalid (1 issue)
    ["PROJ-126", "Bug", "Bug Z", "Description Z", "Low", "Invalid", "Sprint 1", "Dev3", "PM1",
     "2025-01-01", "2025-01-02", "", "bug", "Component3", "", "0", "", "", "", "", "", "", ""],

    # Routine (1 issue)
    ["PROJ-127", "Task", "Task AA", "Description AA", "Low", "Routine", "Sprint 2", "Dev1", "PM1",
     "2025-01-01", "2025-01-02", "", "", "Component1", "", "1", "", "", "", "", "", "", ""],
]

# Sample with invalid statuses (for edge case testing)
SAMPLE_RAW_DATA_INVALID_STATUS = [
    ["Key", "Issue Type", "Summary", "Description", "Priority", "Status", "Sprint", "Assignee", "Reporter",
     "Created", "Updated", "Due Date", "Labels", "Components", "Fix Versions", "Story Points", "Original Estimate",
     "Remaining Estimate", "Time Spent", "Epic Link", "Parent", "Custom Field 1", "Custom Field 2"],

    ["PROJ-201", "Story", "Feature", "Description", "High", "Done", "Sprint 1", "Dev1", "PM1",
     "2025-01-01", "2025-01-02", "", "", "", "", "5", "", "", "", "", "", "", ""],
    ["PROJ-202", "Task", "Task", "Description", "Medium", "In Progress", "Sprint 1", "Dev2", "PM1",
     "2025-01-01", "2025-01-02", "", "", "", "", "3", "", "", "", "", "", "", ""],

    # Invalid statuses - should be excluded from chart but included in total count
    ["PROJ-203", "Bug", "Bug", "Description", "High", "Unknown", "Sprint 1", "Dev3", "PM1",
     "2025-01-01", "2025-01-02", "", "", "", "", "2", "", "", "", "", "", "", ""],
    ["PROJ-204", "Story", "Feature", "Description", "Medium", "Testing", "Sprint 1", "Dev1", "PM1",
     "2025-01-01", "2025-01-02", "", "", "", "", "5", "", "", "", "", "", "", ""],
    ["PROJ-205", "Task", "Task", "Description", "Low", "Archived", "Sprint 1", "Dev2", "PM1",
     "2025-01-01", "2025-01-02", "", "", "", "", "1", "", "", "", "", "", "", ""],
]

# Sample with non-numeric story points
SAMPLE_RAW_DATA_NON_NUMERIC_POINTS = [
    ["Key", "Issue Type", "Summary", "Description", "Priority", "Status", "Sprint", "Assignee", "Reporter",
     "Created", "Updated", "Due Date", "Labels", "Components", "Fix Versions", "Story Points", "Original Estimate",
     "Remaining Estimate", "Time Spent", "Epic Link", "Parent", "Custom Field 1", "Custom Field 2"],

    # Valid numeric story points
    ["PROJ-301", "Story", "Feature", "Description", "High", "Done", "Sprint 1", "Dev1", "PM1",
     "2025-01-01", "2025-01-02", "", "", "", "", "5", "", "", "", "", "", "", ""],
    ["PROJ-302", "Task", "Task", "Description", "Medium", "In Progress", "Sprint 1", "Dev2", "PM1",
     "2025-01-01", "2025-01-02", "", "", "", "", "3.5", "", "", "", "", "", "", ""],

    # Non-numeric story points - should be treated as 0
    ["PROJ-303", "Bug", "Bug", "Description", "High", "Done", "Sprint 1", "Dev3", "PM1",
     "2025-01-01", "2025-01-02", "", "", "", "", "TBD", "", "", "", "", "", "", ""],
    ["PROJ-304", "Story", "Feature", "Description", "Medium", "To Do", "Sprint 1", "Dev1", "PM1",
     "2025-01-01", "2025-01-02", "", "", "", "", "N/A", "", "", "", "", "", "", ""],
    ["PROJ-305", "Task", "Task", "Description", "Low", "Backlog", "Sprint 1", "Dev2", "PM1",
     "2025-01-01", "2025-01-02", "", "", "", "", "", "", "", "", "", "", "", ""],  # Empty
]

# Empty data (only header)
SAMPLE_RAW_DATA_EMPTY = [
    ["Key", "Issue Type", "Summary", "Description", "Priority", "Status", "Sprint", "Assignee", "Reporter",
     "Created", "Updated", "Due Date", "Labels", "Components", "Fix Versions", "Story Points", "Original Estimate",
     "Remaining Estimate", "Time Spent", "Epic Link", "Parent", "Custom Field 1", "Custom Field 2"],
]
