import os
from pynamodb.models import Model
from pynamodb.attributes import (
    UnicodeAttribute, UnicodeSetAttribute, BooleanAttribute
)

CURRENT_ENV = os.environ.get('CURRENT_ENV', 'dev')

class Database(Model):
    class Meta:
        table_name = 'SecureBoxClients'
        read_capacity_units = 2
        write_capacity_units = 2
        if CURRENT_ENV == 'dev':
            host = 'http://127.0.0.1:8001'
        else:
            region = 'us-east-2'

    box_id = UnicodeAttribute(hash_key=True)
    tracking_id = UnicodeSetAttribute(null=True)
    locked = BooleanAttribute()
    phone_number = UnicodeAttribute()
    email = UnicodeAttribute()
    password = UnicodeAttribute()


