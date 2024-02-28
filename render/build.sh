set -o errexit -o nounset -o pipefail
pip install -r requirements.txt
python manage.py collectstatic --noinput
python manage.py migrate
python manage.py tailwind build