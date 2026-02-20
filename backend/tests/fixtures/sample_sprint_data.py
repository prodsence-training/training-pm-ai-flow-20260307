"""
Sample test data for GetJiraSprintValues Google Sheets table
Mimics the 9-column structure (A:I)
"""

# Sample GetJiraSprintValues - 9 fields per row (A:I)
SAMPLE_SPRINT_DATA_BASIC = [
    ["Board ID", "Board Name", "Sprint Name", "Sprint ID", "Sprint State", "Sprint Goal",
     "Start Date", "End Date", "Complete Date"],  # Header row

    ["10", "Development Board", "Sprint 1", "101", "active", "Complete user authentication",
     "2025-01-01", "2025-01-14", ""],
    ["10", "Development Board", "Sprint 2", "102", "future", "Implement dashboard features",
     "2025-01-15", "2025-01-28", ""],
    ["10", "Development Board", "Sprint 3", "103", "closed", "Bug fixes and optimization",
     "2024-12-15", "2024-12-28", "2024-12-28"],
]

# Sample with duplicate sprint names (should append Sprint ID)
SAMPLE_SPRINT_DATA_DUPLICATES = [
    ["Board ID", "Board Name", "Sprint Name", "Sprint ID", "Sprint State", "Sprint Goal",
     "Start Date", "End Date", "Complete Date"],

    ["10", "Development Board", "Sprint 1", "11", "active", "Goal A",
     "2025-01-01", "2025-01-14", ""],
    ["10", "Development Board", "Sprint 1", "15", "closed", "Goal B",
     "2024-12-01", "2024-12-14", "2024-12-14"],
    ["10", "Development Board", "Sprint 2", "20", "future", "Goal C",
     "2025-01-15", "2025-01-28", ""],
    ["11", "Testing Board", "Sprint 1", "25", "active", "Goal D",
     "2025-01-01", "2025-01-14", ""],  # Another duplicate "Sprint 1"
]

# Sample with many sprints (sorting test)
SAMPLE_SPRINT_DATA_MANY = [
    ["Board ID", "Board Name", "Sprint Name", "Sprint ID", "Sprint State", "Sprint Goal",
     "Start Date", "End Date", "Complete Date"],

    ["10", "Board", "Development Sprint", "201", "active", "Dev work",
     "2025-01-01", "2025-01-14", ""],
    ["10", "Board", "Testing Sprint", "202", "active", "QA work",
     "2025-01-01", "2025-01-14", ""],
    ["10", "Board", "Bugfix Sprint", "203", "closed", "Fixes",
     "2024-12-15", "2024-12-28", "2024-12-28"],
    ["10", "Board", "Release Sprint", "204", "future", "Prepare release",
     "2025-01-15", "2025-01-28", ""],
]

# Empty sprint data (only header)
SAMPLE_SPRINT_DATA_EMPTY = [
    ["Board ID", "Board Name", "Sprint Name", "Sprint ID", "Sprint State", "Sprint Goal",
     "Start Date", "End Date", "Complete Date"],
]
