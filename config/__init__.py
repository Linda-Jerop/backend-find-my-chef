"""
Configuration package for Find My Chef
"""
from config.settings import Settings, settings

__all__ = ['Settings', 'settings']
# Exporting names expected elsewhere: aliasing Settings->Config and settings->config
Config = Settings  # Providing backwards-compatible name 'Config'
config = settings  # Providing backwards-compatible name 'config'

__all__ = ['settings']
