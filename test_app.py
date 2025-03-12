from app import create_app, db

def test_app_creation():
    print("Testing Flask app creation...")
    try:
        app = create_app('development')
        print("Flask app created successfully!")
        
        # Test database connection
        with app.app_context():
            try:
                db.engine.connect()
                print("Database connection successful!")
                
                # Get table names to verify schema
                inspector = db.inspect(db.engine)
                tables = inspector.get_table_names()
                print(f"Database tables: {tables}")
                
            except Exception as e:
                print(f"Database connection error: {e}")
    except Exception as e:
        print(f"Error creating Flask app: {e}")

if __name__ == "__main__":
    test_app_creation() 