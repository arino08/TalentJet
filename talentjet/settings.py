# Make sure these settings are correct
DEBUG = True

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'talentjet',  # Make sure this is listed
]

# Check static files settings
STATIC_URL = '/static/'

STATICFILES_DIRS = [
    BASE_DIR / "static",
    # Add any other directories if needed
]

# During development, no need for STATIC_ROOT

# Media files (uploads)
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Maximum file upload size (5MB)
DATA_UPLOAD_MAX_MEMORY_SIZE = 5242880
FILE_UPLOAD_MAX_MEMORY_SIZE = 5242880
