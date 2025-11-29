import flask_sqlalchemy
from sqlalchemy import text


def test_db_connection(db: flask_sqlalchemy.SQLAlchemy):
    """
    :param db:
    Usage: Put the following code into app/__init__.py

    from tests.utils import test_db_connection
    with app.app_context():
        result = test_db_connection(db)

    """
    try:

        db.session.execute(text('SELECT 1'))
        print("✅ Supabase connection successful")

        schemas_result = db.session.execute(
            text("SELECT schema_name FROM information_schema.schemata")
        ).fetchall()
        schemas = [schema[0] for schema in schemas_result]

        current_schema = db.session.execute(text("SELECT current_schema()")).fetchone()
        current = current_schema[0] if current_schema else None

        tables_result = db.session.execute(
            text("SELECT tablename FROM pg_tables WHERE schemaname='public'")
        ).fetchall()
        tables = [table[0] for table in tables_result]

        print(f"Current schema: {current}")
        print(f"All schemas ({len(schemas)}): {', '.join(schemas)}")
        print(f"Tables in public schema ({len(tables)}): {', '.join(tables)}")

        return {
            'connected': True,
            'current_schema': current,
            'all_schemas': schemas,
            'tables': tables
        }

    except Exception as e:
        print(f"Failed to connect Supabase: {e}")
        return {
            'connected': False,
            'error': str(e)
        }


