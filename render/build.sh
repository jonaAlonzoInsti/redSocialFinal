set -o errexit -o nounset -o pipefail
pip install -r requirements.txt
# npm install
npm install -g tailwindcss
# db-migrate -e prod up
python manage.py tailwind start
npm install -g rimraf
# npx tailwindcss  -i ./static/src/input.css -o ./static/src/output.css
python manage.py collectstatic --noinput
python manage.py migrate

# python manage.py tailwind build
