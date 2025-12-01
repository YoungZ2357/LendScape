
import os

class Config:
    # POSTGRESQL_HOST = 'db.jdpqxgdwjpkoegolxabi.supabase.co'
    # POSTGRESQL_PORT = 5432
    # POSTGRESQL_USER = 'postgres'
    # POSTGRESQL_PASSWORD = '123456'
    # DATABASE = "postgres"

    POSTGRESQL_HOST = 'aws-1-ca-central-1.pooler.supabase.com'
    POSTGRESQL_PORT = 6543
    POSTGRESQL_USER = 'postgres.nrvwkdppdznvorrwhogs'
    POSTGRESQL_PASSWORD = 'WFtO4QZwWaYhePXo'
    DATABASE = "postgres"
    SECRET_KEY = os.urandom(32)
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = f"postgresql+psycopg2://{POSTGRESQL_USER}:{POSTGRESQL_PASSWORD}@{POSTGRESQL_HOST}:{POSTGRESQL_PORT}/{DATABASE}"
    SUPABASE_URL = os.environ.get('SUPABASE_URL') or \
                   'https://nrvwkdppdznvorrwhogs.supabase.co'
    SUPABASE_ANON_KEY = os.environ.get('SUPABASE_ANON_KEY') or \
                        'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Im5ydndrZHBwZHpudm9ycndob2dzIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjM0NjkxOTMsImV4cCI6MjA3OTA0NTE5M30.MUzz48qCj_fv01SrhgpWVp_MmdBbueclhQXeS7yqdpo'

