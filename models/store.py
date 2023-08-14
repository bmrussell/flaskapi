from db import db

class StoreModel(db.Model):
    __tablename__ = "stores"
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=False, nullable=False)
    
    items = db.relationship("ItemModel", back_populates="store", lazy="dynamic") # lazy="dynamic" deferrs load of related tables increasing performance
    tags = db.relationship("TagModel", back_populates="store", lazy="dynamic")   # Cascade deletes, also see delete-orphan