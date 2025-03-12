import os
import sys
import traceback

print("Current working directory:", os.getcwd())
print("Python executable:", sys.executable)
print("Python version:", sys.version)
print("Environment variables:", os.environ.get('FLASK_APP'), os.environ.get('FLASK_ENV'))

try:
    print("Attempting to import from app...")
    from app import create_app, db
    print("Import successful")
    
    def test_app_creation():
        print("Testing Flask app creation...")
        try:
            app = create_app('development')
            print("Flask app created successfully!")
            print("App config:", app.config)
            
            # Test database connection
            with app.app_context():
                try:
                    print("Attempting database connection...")
                    connection = db.engine.connect()
                    print("Database connection successful!")
                    connection.close()
                    
                    # Get table names to verify schema
                    inspector = db.inspect(db.engine)
                    tables = inspector.get_table_names()
                    print(f"Database tables: {tables}")
                    
                except Exception as e:
                    print(f"Database connection error: {e}")
                    traceback.print_exc()
        except Exception as e:
            print(f"Error creating Flask app: {e}")
            traceback.print_exc()

    if __name__ == "__main__":
        test_app_creation()
except Exception as e:
    print(f"Import error: {e}")
    traceback.print_exc() 