from datetime import datetime
from models import transactions_collection

class Transaction:
    @staticmethod
    def create(user_id, transaction_data):
        """Create a new transaction record"""
        transaction = {
            'user_id': user_id,
            'type': transaction_data.get('type'),  # airtime, electricity, water, transfer, etc.
            'amount': float(transaction_data.get('amount', 0)),
            'description': transaction_data.get('description'),
            'timestamp': transaction_data.get('timestamp', datetime.utcnow()),
            'metadata': transaction_data.get('metadata', {}),
            'created_at': datetime.utcnow()
        }
        
        result = transactions_collection.insert_one(transaction)
        return transaction if result.inserted_id else None

    @staticmethod
    def bulk_create(user_id, transactions_data):
        """Create multiple transactions at once"""
        transactions = []
        for data in transactions_data:
            transaction = {
                'user_id': user_id,
                'type': data.get('type'),
                'amount': float(data.get('amount', 0)),
                'description': data.get('description'),
                'timestamp': data.get('timestamp', datetime.utcnow()),
                'metadata': data.get('metadata', {}),
                'created_at': datetime.utcnow()
            }
            transactions.append(transaction)
        
        if transactions:
            result = transactions_collection.insert_many(transactions)
            return len(result.inserted_ids)
        return 0

    @staticmethod
    def find_by_user_id(user_id, limit=100, transaction_type=None):
        """Find transactions for a user, optionally filtered by type"""
        query = {'user_id': user_id}
        if transaction_type:
            query['type'] = transaction_type
        
        return list(transactions_collection.find(query)
                                 .sort('timestamp', -1)
                                 .limit(limit))

    @staticmethod
    def get_transaction_stats(user_id):
        """Get transaction statistics for a user"""
        pipeline = [
            {'$match': {'user_id': user_id}},
            {'$group': {
                '_id': '$type',
                'count': {'$sum': 1},
                'total_amount': {'$sum': '$amount'},
                'avg_amount': {'$avg': '$amount'},
                'last_transaction': {'$max': '$timestamp'}
            }}
        ]
        
        return list(transactions_collection.aggregate(pipeline))