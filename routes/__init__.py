# Routes package initialization
from .lenders import lenders_bp
from .users import users_bp
from .admin import admin_bp

__all__ = ['lenders_bp', 'users_bp', 'admin_bp']