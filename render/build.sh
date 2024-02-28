set -o errexit -o nounset -o pipefail
pip install -r requirements.txt
# db-migrate -e prod up
python manage.py tailwind start
npm install -g rimraf
python manage.py collectstatic --noinput
python manage.py migrate
python manage.py tailwind build
