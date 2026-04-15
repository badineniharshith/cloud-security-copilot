"""
Simple script to run the Cloud Security Copilot
"""
import subprocess
import sys
import os

def check_dependencies():
    """Check if required packages are installed"""
    required = ['flask', 'flask_cors', 'pandas', 'numpy']
    missing = []
    
    for package in required:
        try:
            __import__(package.replace('-', '_'))
        except ImportError:
            missing.append(package)
    
    if missing:
        print(f"❌ Missing packages: {missing}")
        print("📦 Installing missing packages...")
        for package in missing:
            subprocess.check_call([sys.executable, "-m", "pip", "install", package])
        print("✅ All packages installed!")
        return True
    return True

def generate_data():
    """Generate sample data"""
    print("📊 Generating sample cloud data...")
    try:
        from data_generator import CloudDataGenerator
        generator = CloudDataGenerator()
        data = generator.generate_complete_dataset()
        
        # Save to data folder
        os.makedirs('../data', exist_ok=True)
        import json
        with open('../data/simulated_data.json', 'w') as f:
            json.dump(data, f, indent=2)
        print("✅ Sample data generated successfully!")
        return True
    except Exception as e:
        print(f"❌ Error generating data: {e}")
        return False

if __name__ == "__main__":
    print("🚀 Cloud Security Copilot - Setup & Run")
    print("=" * 50)
    
    # Check dependencies
    check_dependencies()
    
    # Generate data
    generate_data()
    
    print("\n✅ Setup complete!")
    print("🌐 Starting server on http://localhost:5001")
    print("📝 Press Ctrl+C to stop the server")
    print("=" * 50)
    
    # Run the app
    from app import app
    app.run(debug=True, port=5001)