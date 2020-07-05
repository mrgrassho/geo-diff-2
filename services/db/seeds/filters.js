db.createCollection("filters");
db.filters.insert( { _id: 1, name: 'RAW', longName: 'Raw Image', active: true });
db.filters.insert( { _id: 2, name: 'DESERT', longName: 'Desert filtered Image', active: true });
db.filters.insert( { _id: 3, name: 'FOREST-JUNGLE', longName: 'Forest/Jungle filtered Image', active: true });
db.filters.insert( { _id: 4, name: 'URBAN', longName: 'Urbanization filtered Image', active: false });
db.filters.insert( { _id: 5, name: 'OCEAN-SEA', longName: 'Ocean/Sea filtered Image', active: true });