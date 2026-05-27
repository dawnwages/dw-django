import os
import sys
import django
from django.conf import settings

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dawnwagesinfo.settings.deploy')

# Add current directory to path
current_dir = os.getcwd()
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)

print("Current directory:", current_dir)
print("DJANGO_SETTINGS_MODULE:", os.environ.get('DJANGO_SETTINGS_MODULE'))

try:
    django.setup()
    print("✅ Django setup successful")
    
    # Test backend import the way Django does it
    from django.db.utils import load_backend
    
    print("\nTesting backend loading:")
    backend_name = 'dawnwagesinfo.simple_backend'
    print(f"Trying to load backend: {backend_name}")
    
    backend = load_backend(backend_name)
    print(f"✅ Backend loaded successfully: {backend}")
    
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()
