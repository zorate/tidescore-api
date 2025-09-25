from datetime import datetime
from models import transactions_collection, employment_collection, guarantors_collection

class ScoringService:
    MAX_SCORE = 740  # Maximum possible score
    
    @staticmethod
    def calculate_score(user_id):
        """Calculate TideScore based on available data"""
        # Get user data from various collections
        transactions = list(transactions_collection.find({'user_id': user_id}))
        employment = employment_collection.find_one({'user_id': user_id})
        guarantors = list(guarantors_collection.find({'user_id': user_id}))
        
        score_breakdown = {}
        total_score = 0
        data_points_used = 0
        
        # 1. Employment Stability (Max: 100 points)
        employment_score = ScoringService._calculate_employment_score(employment)
        score_breakdown['employment'] = employment_score
        total_score += employment_score
        if employment_score > 0:
            data_points_used += 1
        
        # 2. Transaction Consistency (Max: 200 points)
        transaction_score = ScoringService._calculate_transaction_score(transactions)
        score_breakdown['transactions'] = transaction_score
        total_score += transaction_score
        if transaction_score > 0:
            data_points_used += 1
        
        # 3. Airtime Usage Pattern (Max: 150 points)
        airtime_score = ScoringService._calculate_airtime_score(transactions)
        score_breakdown['airtime'] = airtime_score
        total_score += airtime_score
        if airtime_score > 0:
            data_points_used += 1
        
        # 4. Bill Payments (Max: 150 points)
        bill_score = ScoringService._calculate_bill_score(transactions)
        score_breakdown['bills'] = bill_score
        total_score += bill_score
        if bill_score > 0:
            data_points_used += 1
        
        # 5. Guarantors/Social Proof (Max: 140 points)
        guarantor_score = ScoringService._calculate_guarantor_score(guarantors)
        score_breakdown['guarantors'] = guarantor_score
        total_score += guarantor_score
        if guarantor_score > 0:
            data_points_used += 1
        
        # Determine status and advice
        status, advice = ScoringService._get_status_and_advice(total_score, data_points_used)
        
        return {
            'score': total_score,
            'status': status,
            'advice': advice,
            'breakdown': score_breakdown,
            'data_points_used': data_points_used,
            'max_possible': ScoringService.MAX_SCORE
        }
    
    @staticmethod
    def _calculate_employment_score(employment):
        if not employment:
            return 0
        
        score = 0
        # Employment status
        status = employment.get('status', '').lower()
        if status == 'employed':
            score += 60
        elif status == 'self-employed':
            score += 40
        elif status == 'student':
            score += 20
        
        # Monthly income scoring
        income = employment.get('monthly_income', 0)
        if income >= 500000:
            score += 40
        elif income >= 200000:
            score += 30
        elif income >= 100000:
            score += 20
        elif income >= 50000:
            score += 10
        
        return min(score, 100)
    
    @staticmethod
    def _calculate_transaction_score(transactions):
        if not transactions or len(transactions) < 3:
            return 0
        
        # Analyze transaction frequency and consistency
        recent_txns = [t for t in transactions if t.get('timestamp')]
        if len(recent_txns) < 3:
            return 0
        
        # Score based on transaction frequency and amount consistency
        score = min(len(recent_txns) * 5, 100)  # Up to 100 points for frequency
        
        # Add points for transaction amount consistency
        amounts = [t.get('amount', 0) for t in recent_txns if t.get('amount', 0) > 0]
        if amounts:
            avg_amount = sum(amounts) / len(amounts)
            # Reward consistent spending patterns
            score += min(avg_amount / 1000, 100)  # Up to 100 points for amount
        
        return min(score, 200)
    
    @staticmethod
    def _calculate_airtime_score(transactions):
        airtime_txns = [t for t in transactions if t.get('type') == 'airtime']
        if not airtime_txns:
            return 0
        
        # Score based on airtime purchase frequency and amount
        score = min(len(airtime_txns) * 10, 100)  # Up to 100 points for frequency
        
        # Average airtime purchase amount
        amounts = [t.get('amount', 0) for t in airtime_txns]
        if amounts:
            avg_amount = sum(amounts) / len(amounts)
            if avg_amount >= 5000:
                score += 50
            elif avg_amount >= 2000:
                score += 30
            elif avg_amount >= 1000:
                score += 20
        
        return min(score, 150)
    
    @staticmethod
    def _calculate_bill_score(transactions):
        bill_txns = [t for t in transactions if t.get('type') in ['electricity', 'water', 'internet', 'cable']]
        if not bill_txns:
            return 0
        
        # Score based on bill payment consistency
        score = min(len(bill_txns) * 15, 120)  # Up to 120 points for frequency
        
        # Variety of bill types
        bill_types = set(t.get('type') for t in bill_txns)
        score += len(bill_types) * 10  # Up to 30 points for variety
        
        return min(score, 150)
    
    @staticmethod
    def _calculate_guarantor_score(guarantors):
        if not guarantors:
            return 0
        
        # Score based on number and quality of guarantors
        score = len(guarantors) * 30  # 30 points per guarantor
        
        # Additional points for verified guarantors
        verified_guarantors = [g for g in guarantors if g.get('verified')]
        score += len(verified_guarantors) * 20
        
        return min(score, 140)
    
    @staticmethod
    def _get_status_and_advice(score, data_points_used):
        if data_points_used < 2:
            return "Insufficient Data", "Submit more financial information to get your score"
        
        if score >= 600:
            return "Excellent", "Maintain your good financial habits"
        elif score >= 450:
            return "Good", "Continue building your financial history"
        elif score >= 300:
            return "Fair", "Focus on consistent bill payments"
        else:
            return "Needs Improvement", "Start with regular airtime purchases and bill payments"