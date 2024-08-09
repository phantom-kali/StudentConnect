#!/bin/bash

# Initialize git repository
git init

# Add a .gitignore file
echo "__pycache__/
*.pyc
db.sqlite3
media/
static/
" > .gitignore
git add .gitignore
git commit -m "Add .gitignore"

# Define the files and directories to be committed in smaller batches
commits=(
  "Add initial project structure: manage.py, requirements.txt, config/"
  "Add utils: decorators.py, print_models.py"
  "Add accounts app models, views, and forms"
  "Add accounts app admin, urls, and management commands"
  "Add accounts app migrations"
  "Add confessions app models, views, and forms"
  "Add confessions app admin, urls, and migrations"
  "Add dining app models, views, and forms"
  "Add dining app admin, urls, and migrations"
  "Add events app models, views, and forms"
  "Add events app admin, urls, and migrations"
  "Add feed app models, views, forms, and templatetags"
  "Add feed app admin, urls, and migrations"
  "Add groups app models, views, and forms"
  "Add groups app admin, urls, and migrations"
  "Add jobs app models, views, and forms"
  "Add jobs app admin, urls, and migrations"
  "Add marketplace app models, views, and forms"
  "Add marketplace app admin, urls, and migrations"
  "Add messaging app models, views, and forms"
  "Add messaging app admin, urls, and migrations"
  "Add notifications app models, views, and forms"
  "Add notifications app admin, urls, and migrations"
  "Add search app models, views, and forms"
  "Add search app admin, urls, and migrations"
  "Add stories app models, views, and forms"
  "Add stories app admin, urls, and migrations"
  "Add templates for accounts app"
  "Add templates for confessions app"
  "Add templates for dining app"
  "Add templates for events app"
  "Add templates for feed app"
  "Add templates for groups app"
  "Add templates for jobs app"
  "Add templates for marketplace app"
  "Add templates for messaging app"
  "Add templates for notifications app"
  "Add templates for search app"
  "Add templates for stories app"
  "Add base template"
  "Add static files: CSS and JS"
  "Add project settings: base.py, development.py, production.py"
  "Add URLs and WSGI settings"
  "Add ASGI settings"
  "Final adjustments and fixes"
)

# Array of files/directories to be added in batches
files=(
  "manage.py requirements.txt config/"
  "utils/decorators.py utils/print_models.py"
  "apps/accounts/models.py apps/accounts/views.py apps/accounts/forms.py"
  "apps/accounts/admin.py apps/accounts/urls.py apps/accounts/management/"
  "apps/accounts/migrations/"
  "apps/confessions/models.py apps/confessions/views.py apps/confessions/forms.py"
  "apps/confessions/admin.py apps/confessions/urls.py apps/confessions/migrations/"
  "apps/dining/models.py apps/dining/views.py apps/dining/forms.py"
  "apps/dining/admin.py apps/dining/urls.py apps/dining/migrations/"
  "apps/events/models.py apps/events/views.py apps/events/forms.py"
  "apps/events/admin.py apps/events/urls.py apps/events/migrations/"
  "apps/feed/models.py apps/feed/views.py apps/feed/forms.py apps/feed/templatetags/"
  "apps/feed/admin.py apps/feed/urls.py apps/feed/migrations/"
  "apps/groups/models.py apps/groups/views.py apps/groups/forms.py"
  "apps/groups/admin.py apps/groups/urls.py apps/groups/migrations/"
  "apps/jobs/models.py apps/jobs/views.py apps/jobs/forms.py"
  "apps/jobs/admin.py apps/jobs/urls.py apps/jobs/migrations/"
  "apps/marketplace/models.py apps/marketplace/views.py apps/marketplace/forms.py"
  "apps/marketplace/admin.py apps/marketplace/urls.py apps/marketplace/migrations/"
  "apps/messaging/models.py apps/messaging/views.py apps/messaging/forms.py"
  "apps/messaging/admin.py apps/messaging/urls.py apps/messaging/migrations/"
  "apps/notifications/models.py apps/notifications/views.py apps/notifications/forms.py"
  "apps/notifications/admin.py apps/notifications/urls.py apps/notifications/migrations/"
  "apps/search/models.py apps/search/views.py apps/search/forms.py"
  "apps/search/admin.py apps/search/urls.py apps/search/migrations/"
  "apps/stories/models.py apps/stories/views.py apps/stories/forms.py"
  "apps/stories/admin.py apps/stories/urls.py apps/stories/migrations/"
  "templates/accounts/"
  "templates/confessions/"
  "templates/dining/"
  "templates/events/"
  "templates/feed/"
  "templates/groups/"
  "templates/jobs/"
  "templates/marketplace/"
  "templates/messaging/"
  "templates/notifications/"
  "templates/search/"
  "templates/stories/"
  "templates/base.html"
  "static/css/ static/js/"
  "config/settings/base.py config/settings/development.py config/settings/production.py"
  "config/urls.py config/wsgi.py"
  "config/asgi.py"
  "."
)

# Loop through the files and commit each batch
for i in "${!files[@]}"; do
  git add ${files[i]}
  git commit -m "${commits[i]}"
done

# Push to your remote repository
git remote add origin https://github.com/phantom-kali/StudentConnect.git
git push -u origin main
