import pandas as pd
from sklearn.linear_model import LinearRegression

class PolicyAnalyzer:
    def measure_impact(self, policy_date: date, location: str) -> dict:
        """Compare pre/post-policy complaint metrics"""
        pre_data = get_complaints_window(
            start=policy_date - timedelta(days=90),
            end=policy_date,
            location=location
        )
        post_data = get_complaints_window(
            start=policy_date,
            end=policy_date + timedelta(days=90),
            location=location
        )
        
        # Statistical significance testing
        result = ttest_ind(
            pre_data['priority_scores'],
            post_data['priority_scores']
        )
        
        return {
            "priority_change": post_data['priority_scores'].mean() - pre_data['priority_scores'].mean(),
            "volume_change": len(post_data) - len(pre_data),
            "p_value": result.pvalue,
            "is_significant": result.pvalue < 0.05
        }