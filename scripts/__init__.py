#!/usr/bin/env python3
"""
Database initialization script for TideScore
"""

import sys
import os

# Add the parent directory to Python path so we can import models
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from models import (
    users_collection, lenders_collection, scores_collection,
    consents_collection, transactions_collection,
    employment_collection, guarantors_collection, api_requests_collection
)
from models.lender import Lender

def init_database():
    """Initialize database with indexes"""
    print("Creating database indexes...")
    
    try:
        # Users collection indexes
        users_collection.create_index('email', unique=True)
        users_collection.create_index('phone')
        users_collection.create_index('created_at')
        print("✓ Users collection indexes created")
        
        # Lenders collection indexes
        lenders_collection.create_index('api_key', unique=True)
        lenders_collection.create_index('contact_email')
        print("✓ Lenders collection indexes created")
        
        # Scores collection indexes
        scores_collection.create_index('user_id', unique=True)
        scores_collection.create_index('last_calculated')
        scores_collection.create_index('valid_until')
        print("✓ Scores collection indexes created")
        
        # Consents collection indexes
        consents_collection.create_index([('user_id', 1), ('lender_id', 1)])
        consents_collection.create_index('valid_until')
        print("✓ Consents collection indexes created")
        
        # Transactions collection indexes
        transactions_collection.create_index([('user_id', 1), ('timestamp', -1)])
        transactions_collection.create_index([('user_id', 1), ('type', 1)])
        print("✓ Transactions collection indexes created")
        
        # Employment collection indexes
        employment_collection.create_index('user_id', unique=True)
        print("✓ Employment collection indexes created")
        
        # Guarantors collection indexes
        guarantors_collection.create_index('user_id')
        print("✓ Guarantors collection indexes created")
        
        # API requests collection indexes
        api_requests_collection.create_index([('identifier', 1), ('timestamp', 1)])
        api_requests_collection.create_index('timestamp', expireAfterSeconds=86400)  # Auto-delete after 24h
        print("✓ API requests collection indexes created")
        
        print("✅ All database indexes created successfully!")
        
    except Exception as e:
        print(f"❌ Error creating indexes: {e}")
        return False
    
    return True

def create_sample_lender():
    """Create a sample lender for testing"""
    try:
        lender_data = {
            'name': 'Sample Microfinance Bank',
            'contact_email': 'loans@samplebank.com'
        }
        
        lender = Lender.create(lender_data)
        if lender:
            print(f"✅ Sample lender created:")
            print(f"   Lender ID: {lender['_id']}")
            print(f"   API Key: {lender['api_key']}")
            return True
        else:
            print("❌ Failed to create sample lender")
            return False
    except Exception as e:
        print(f"❌ Error creating sample lender: {e}")
        return False

if __name__ == '__main__':
    print("🚀 Initializing TideScore Database...")
    print("-" * 50)
    
    if init_database():
        create_sample_lender()
        print("-" * 50)
        print("✅ Database initialization completed!")
        print("\n📝 Next steps:")
        print("1. Run: python app.py")
        print("2. Test the API endpoints")
    else:
        print("❌ Database initialization failed!")
