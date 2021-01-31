
from dejavu import Dejavu
from dejavu.logic.recognizer.file_recognizer import FileRecognizer

DB_NAME = "postgress"
DB_PASSWORD = "password"

config = {
    "database": {
    "host": "127.0.0.1",
    "user": "root",
    "password": DB_PASSWORD,
    "database": DB_NAME,
    }
}

djv = Dejavu(config)


song = djv.recognize(FileRecognizer, "David Guetta - Memories.mp3")
