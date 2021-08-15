from os import environ

class Config:
    DEBUG = False
    DEVELOPMENT = False
    AKEY = environ['AKEY']
    ASKEY = environ['ASKEY']
    ATKEY = environ['ATKEY']
    ATSKEY = environ['ATSKEY']

class ProductionConfig(Config):
    pass

class StagingConfig(Config):
    DEBUG = True

class DevelopmentConfig(Config):
    DEBUG = True
    DEVELOPMENT = True