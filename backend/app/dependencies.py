from app.Organization import *

org = Organization('gttrack', 'Georgia Tech Track')

def get_organization_dependency():
    """
    Dependency for FastAPI
    """
    return org