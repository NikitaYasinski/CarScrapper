import pymongo

from staticjinja import Site

if __name__ == "__main__":
    conn = pymongo.MongoClient(
            'localhost',
            27017
    )
    data = []
    db = conn['cars']
    collection = db['cars_tb']
    for car in collection.find({}, {"_id":0, "name": 1, "price": 1, "img": 1}):
        data.append(car)
    
    site = Site.make_site(env_globals={'cars': data})

    site.render()