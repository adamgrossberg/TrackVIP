from app.Organization import *
from app.control_utils import load_organization

org = load_organization()

def get_organization_dependency():
    """
    Dependency for FastAPI
    """
    return org