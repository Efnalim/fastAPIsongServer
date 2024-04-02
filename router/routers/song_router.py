from router.config.db import db

class SongRouter():
    def getAllSongs(self):
        return db.songs.find()