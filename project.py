import subprocess

def main():
    # upgrade_database()
    check_database_version()
    start_app()


def upgrade_database():
    subprocess.run(['alembic', 'upgrade', 'head'])


def check_database_version():
    upgrade_database()
    output = subprocess.check_output(['alembic', 'current'], universal_newlines=True)

    lines = output.split('\n')
    current_revision = lines[0].strip()
    return current_revision
    


def start_app():
    subprocess.run(['uvicorn', 'app.main:app', '--host', 'localhost', '--port', '8000'])
    

if __name__ == "__main__":
    main()


