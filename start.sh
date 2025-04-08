#!/bin/bash

echo "📦 Starting setup for original project..."

# 1. Unzip templates only if needed
if [ ! -d "templates/registration" ] && [ -f "setup/templates.zip" ]; then
  echo "🎨 Unzipping templates..."
  unzip -o setup/templates.zip -d .
else
  echo "✅ Templates already present or zip not found."
fi

# 2. Clean old migrations (safe for dev)
echo "🔄 Cleaning old migrations..."
find . -path "*/migrations/*.py" -not -name "__init__.py" -delete
find . -path "*/migrations/*.pyc" -delete
rm -f db.sqlite3

# 3. Migrate
echo "🧱 Applying migrations..."
python manage.py makemigrations
python manage.py migrate

# 4. Load optional sample data
if [ -f "setup/backup.json" ]; then
  echo "📥 Loading sample data..."
  python manage.py loaddata setup/backup.json
fi

# 5. Start server
echo "🚀 Starting development server..."
python manage.py runserver
