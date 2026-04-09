from kroyka.db.session import engine, Base
import kroyka.db.models  # noqa: F401 - ensure models are registered

def init_db():
    Base.metadata.create_all(bind=engine)
    print('Database tables created')

if __name__ == '__main__':
    init_db()
