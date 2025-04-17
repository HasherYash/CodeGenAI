from app.services.database import init_db, create_database_if_not_exists

# Run everything in DB

if __name__ == "__main__":

    create_database_if_not_exists()

    init_db() 