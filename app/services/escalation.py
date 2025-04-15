from datetime import datetime  
from enum import IntEnum
from app.models.complaint import Complaint

class EscalationLevel(IntEnum):
    LOW = 1          # Regular department handling
    MEDIUM = 2       # Cross-department coordination
    HIGH = 3         # Executive attention
    CRITICAL = 4     # Minister/President level

class EscalationEngine:
    ESCALATION_RULES = {
        "priority_score > 0.8": EscalationLevel.HIGH,
        "days_pending > 7": EscalationLevel.MEDIUM,
        "sentiment < -0.6": EscalationLevel.CRITICAL
    }

    def determine_escalation(self, complaint: Complaint) -> EscalationLevel:
        days_pending = (datetime.now() - complaint.created_at).days
    
        if complaint.priority_score > 0.8:
            return EscalationLevel.HIGH
        elif days_pending > 7:
            return EscalationLevel.MEDIUM
        elif complaint.sentiment_score < -0.6:
            return EscalationLevel.CRITICAL
        return EscalationLevel.LOW