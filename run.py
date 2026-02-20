from app import create_app
from app.scheduler.backup_scheduler import start_scheduler

app = create_app()

start_scheduler(app)

if __name__ == "__main__":
    # Apenas para debug/local
    app.run(host="0.0.0.0", port=9000, debug=True)
