from pathlib import Path
import os
from django.contrib.messages import constants

BASE_DIR = Path(__file__).resolve().parent.parent.parent
SECRET_KEY = os.getenv(
    "SECRET_KEY", "django-insecure-tr(+6ip-hfg*&fh_!pog%@+#-1ui8zij0zj0powuo#szg1_%@7"
)

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.getenv("DEBUG", 1)

ALLOWED_HOSTS: list[str] = ["*"]

ROOT_URLCONF = "project.urls"

WSGI_APPLICATION = "project.wsgi.application"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"


REST_FRAMEWORK = {
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.LimitOffsetPagination",
    "PAGE_SIZE": 10,
}
