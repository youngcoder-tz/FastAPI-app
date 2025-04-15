class CitizenEngagementScorer:
    POINT_RULES = {
        "complaint_submitted": 10,
        "feedback_provided": 5,
        "promise_verified": 20,
        "event_participation": 15
    }

    def update_scores(self):
        """Daily batch update of citizen scores"""
        with get_db_session() as db:
            citizens = db.query(User).filter(User.role == "citizen")
            for citizen in citizens:
                new_score = self._calculate_score(citizen.id)
                citizen.engagement_score = new_score
                self._assign_badges(citizen, new_score)
            db.commit()

    def _calculate_score(self, user_id: UUID) -> int:
        activities = get_activities(user_id)
        return sum(
            self.POINT_RULES[activity.type] * activity.count 
            for activity in activities
        )