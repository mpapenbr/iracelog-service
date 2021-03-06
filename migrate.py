from dbArchiver import ENV_DB_URL
from sys import int_info
from sqlalchemy.orm import create_session
from storage.schema import Event,WampData
import codecs
import os
import json
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
ENV_DB_URL="DB_URL"

def import_data(event_key=None):
    with codecs.open(f"logs/json/data-{event_key}.json", "r", encoding='utf-8') as data_file, \
        codecs.open(f"logs/json/info-{event_key}.json", "r", encoding='utf-8') as info_file, \
        codecs.open(f"logs/json/manifest-{event_key}.json", "r", encoding='utf-8') as manifest_file:
    
        eng = create_engine(os.environ.get(ENV_DB_URL))
        Session = sessionmaker(eng)
        with eng.connect() as con:
            with Session(bind=con) as session:
                m = json.loads(manifest_file.readline())
                event_data = dict()
                event_data['manifests'] = m[0]
                event_data['info'] = json.loads(info_file.readline())
                e = Event(Name="test", EventKey=event_key, Data=event_data)
                session.add(e)
                session.flush()
                print(e.Id)
                to_insert = []
                for line in data_file:
                    j = json.loads(line)
                    w = WampData(EventId=e.Id, Data=j)
                    to_insert.append(w)
                print(f"{len(to_insert)} items read")
                session.bulk_save_objects(to_insert)
                print(f"save objects done")
                session.commit()


if __name__ == '__main__':
    for event in ["1", "3","neo", "68d4ff7adbb3412b8da2ab53daf01453", "26ceac390dcac80d439992c98b0a9db8"]:
        import_data(event)



