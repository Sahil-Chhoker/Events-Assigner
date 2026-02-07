set -e

echo "Running migrations..."
python photographer_assignment/manage.py migrate

echo "Creating sample data (safe to re-run)..."
python photographer_assignment/manage.py create_sample_data || true

echo "Starting server..."
exec python photographer_assignment/manage.py runserver 0.0.0.0:8000
    