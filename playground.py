from random import randint, choice
from datetime import datetime, timedelta


def text_gen(col: int):
    for _ in range(col):
        date = datetime.now() + timedelta(days=randint(0, 30))
        place = ['221B Baker Street, London',
                 '4 Privet Drive, Little Whinging',
                 '123 Sesame Street, New York',
                 'The Shire, Middle Earth',
                 '12 Grimmauld Place, London',
                 'Hogwarts School of Witchcraft',
                 'The Batcave, Gotham City',
                 'Neverland, Second star to the right',
                 'Arkham Asylum, Gotham City',
                 'The Death Star, Outer Space',
                 'The Matrix, Virtual Reality',
                 'Emerald City, Land of Oz',
                 'Xaviers School for Gifted Youngsters',
                 'The TARDIS, Time and Space',
                 'The Pentagon, Washington D.C.',
                 'Stark Tower, New York',
                 'Wayne Manor, Gotham City',
                 'Narnia, Beyond the wardrobe',
                 'Rivendell, Middle Earth',
                 'The Black Pearl, Caribbean Sea']
        desc = ['Kitchen fire, burnt toast',
                'Cigarette ignited trash can',
                'Electrical malfunction caused blaze',
                'Bonfire got out of control',
                'Gasoline explosion, garage destroyed',
                'Candle left unattended, scorched curtains',
                'Barbecue mishap, fence aflame',
                'Arson suspected, investigation underway',
                'Christmas lights sparked inferno',
                'Faulty wiring, house burned down',
                'Grease fire, stove ablaze',
                'Fireworks ignited dry grass',
                'Lightning strike, tree ignited',
                'Smoking in bed, mattress burned',
                'Overloaded outlet, sparks flew',
                'Space heater overheated, ignited',
                'Kids playing with matches, tragedy',
                'Wildfire started by campfire',
                'Sparklers caused hand burns',
                'Gas leak, explosion occurred']
        d_id = randint(0, 12)

        yield f'INSERT INTO RTIMonitor_incident (date, place, description, id_cfsdistrict_id) ' \
              f'VALUES ("{date:%Y-%m-%d 12:00:00}", "{choice(place)}", "{choice(desc)}", {d_id});'


if __name__ == '__main__':
    [print(i) for i in text_gen(100)]
