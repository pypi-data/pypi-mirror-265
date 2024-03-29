import os

from surge.projects import Project
from surge.tasks import Task
from surge.teams import Team
from surge.reports import Report

api_key = os.environ.get("SURGE_API_KEY", None)
base_url = "http://localhost:3000/api"#os.environ.get("SURGE_BASE_URL", "https://app.surgehq.ai/api")
