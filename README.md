# Radio Grid Run Helper Tools
Compute a team's territory based on the recorded what3words (w3w) codes

## 1. Setup and configuration

### 1.1 Dev dir setup

```
$ mkdir rgrHelper
$ virtualenv venv
$ source venv/bin/activate
$ vim setup.py
$ pip install -e .
```
For a good tutorial on how to setup venv see:
https://sourabhbajaj.com/mac-setup/Python/virtualenv.html

For a good example on how to use Setuptools see :
    https://godatadriven.com/blog/a-practical-guide-to-using-setup-py/

## 2. Configuration
vir
`conf/gameConfig.ini` contains the game information (to be edited for each game)

`conf/rgrHelper.ini` contains the default for the scripts 

add a `.env` file with the following key-pair value in `rgrHelper` folder.

    w3wapikey = ThisIsMyAPIkey

## 3. Usage

_Command `rgrHelper`_
```
Usage: rgrHelper [OPTIONS] COMMAND [ARGS]...

Options:
-v, --verbose  Showing various details of the process.
--help         Show this message and exit.

Commands:
computeterritory  Generate a geoJSON Feature Collections .json output...
hqpoint           Generate a geoJSON Point Feature .json output file...
testarea          Test for area function
testw3w           Sending a API call to w3w to check connection.
```
_Command `rgrHelper computeterritory [OPTIONS] INPUT TEAM`_
```
Usage: rgrHelper computeterritory [OPTIONS] INPUT TEAM

  Generate a geoJSON Feature Collections .json output file with    all Points
  and the related Polygon.    Used to generate a team's result, included the
  territoriy's area.

  INPUT  Relativ path to csv input file.

  TEAM   Identifier of the team (according to csv column 'team_id').

Options:
  --savesortedinput BOOLEAN  Save useful column of input data to a .CSV file
                             sorted by team and time.
  --help                     Show this message and exit.
```
`INPUT` accepts a .CSV file of **contacts** containing at least the following columns:

- `contact_time`: time of the contact
- `team_id`: unique identifier of the team
- `word1`: 1st word of the what3words address
- `word2`: 2nd word of the what3words address
- `word3`: 3rd word of the what3words address
- `Notes`: optional comment that can be empty
- `Added Time`: timestamp of the contact entry in the file


_Command `rgrHelper hqpoint [OPTIONS]`_

```
Usage: rgrHelper hqpoint [OPTIONS]

  Generate a geoJSON Point Feature .json output file for the Round
  Headquarter.
Options:
  --help  Show this message and exit.
```

## 4. Examples

### Input .CSV file

```
contact_time,team_id,word1,word2,word3,Notes,Added Time,Referrer Name,Task Owner
14-Sep-2023 17:48,1,carotte,decuplons,ecartant,,14-Sep-2023 17:04:11,https://forms.zoho.eu/radiogridrun/form/contacts/thankyou,info@radiogrid.run
```

### Output geoJSON Point Feature (ex. hqpoint)
```
{
    "type": "Feature",
    "geometry": {
        "coordinates": [
            7.11739,
            46.963468
        ],
        "type": "Point"
    },
    "properties": {
        "type": "round headquarter",
        "time": "14-09-2023T17:36:57",
        "uuid": "7906a058-b8ef-45e7-96b6-ebefe1300ab6",
        "roundID": "70a7bc7c",
        "w3wAddress": {
            "country": "CH",
            "nearestPlace": "Bas-Vully, Fribourg",
            "words": "indéchirable.glaçage.pivert",
            "word1": "indéchirable",
            "word2": "glaçage",
            "word3": "pivert",
            "language": "fr",
            "map": "https://w3w.co/ind%C3%A9chirable.gla%C3%A7age.pivert"
        }
    }
}
```
### Output geoJSON Polygone Feature (Team Territory)
```
{
    "type": "FeatureCollection",
    "features": [
        {
    "type": "Feature",
    "geometry": {
        "type": "Point",
        "coordinates": [7.120988, 46.968211]
        },
    "properties": {
        "type": "contact",
        "time": "14-Sep-2023 17:04",
        "uuid": "2117f80f-c8b5-4491-9f30-07c22df8eb6c",
        "w3wAddress": {
            "country": "CH",
            "nearestPlace": "Bas-Vully, Fribourg",
            "words": "défendable.échappons.émulons",
            "word1": "défendable",
            "word2": "échappons",
            "word3": "émulons",
            "language": "fr",
            "map": "https://w3w.co/d%C3%A9fendable.%C3%A9chappons.%C3%A9mulons"
        }
    }
},{
    "type": "Feature",
    "geometry": {
        "type": "Point",
        "coordinates": [7.110867, 46.965731]
        },
    "properties": {
        "type": "contact",
        "time": "14-Sep-2023 17:19",
        "uuid": "163c0511-f4f6-452d-aebe-e27cb59a3074",
        "w3wAddress": {
            "country": "CH",
            "nearestPlace": "Bas-Vully, Fribourg",
            "words": "élection.talquer.décante",
            "word1": "élection",
            "word2": "talquer",
            "word3": "décante",
            "language": "fr",
            "map": "https://w3w.co/%C3%A9lection.talquer.d%C3%A9cante"
        }
    }
},{
    "type": "Feature",
    "geometry": {
        "type": "Point",
        "coordinates": [7.118023, 46.961554]
        },
    "properties": {
        "type": "contact",
        "time": "14-Sep-2023 17:48",
        "uuid": "2603a295-0cd4-4d48-bc06-09951afa0a59",
        "w3wAddress": {
            "country": "CH",
            "nearestPlace": "Bas-Vully, Fribourg",
            "words": "carotte.décuplons.écartant",
            "word1": "carotte",
            "word2": "décuplons",
            "word3": "écartant",
            "language": "fr",
            "map": "https://w3w.co/carotte.d%C3%A9cuplons.%C3%A9cartant"
        }
    }
},{
        "type": "Feature",
        "geometry": {
          "type": "Polygon",
          "coordinates": [
            [ [7.120988, 46.968211], [7.110867, 46.965731], [7.118023, 46.961554], [7.120988, 46.968211]]
          ]
        },
    "properties": {
        "type": "territory",
        "uuid": "356ac77e-0110-4f6e-93ea-1d545081588e",
        "roundID": "70a7bc7c",
        "area": "253802.3970606503",
        "w3wAddress": {
            "country": "CH",
            "nearestPlace": "Bas-Vully, Fribourg",
            "words": "indéchirable.glaçage.pivert",
            "word1": "indéchirable",
            "word2": "glaçage",
            "word3": "pivert",
            "language": "fr",
            "map": "https://w3w.co/ind%C3%A9chirable.gla%C3%A7age.pivert"
        },
        "team": {
            "name": "ClubFribourg",
            "id": "HB9FG.ch"
        }
    }
}
    ],
    "properties": {
        "type": "round",
        "time": "14-09-2023T17:36:57",
        "uuid": "2ce576ba-932f-4b4a-9680-57248650732b",
        "roundID": "70a7bc7c",
        "w3wAddress": {
            "country": "CH",
            "ßnearestPlace": "Bas-Vully, Fribourg",
            "words": "indéchirable.glaçage.pivert",
            "word1": "indéchirable",
            "word2": "glaçage",
            "word3": "pivert",
            "language": "fr",
            "map": "https://w3w.co/ind%C3%A9chirable.gla%C3%A7age.pivert"
        },
        "team": {
            "name": "ClubFribourg",
            "id": "HB9FG.ch"
        }   
    }
}
```

---

### Author
Frédéric Noyer, HB9HWF

### License
This work is licensed under a Creative Commons Attribution-ShareAlike 4.0 International License.
[License Details](https://creativecommons.org/licenses/by-sa/4.0/)

### Original Work
GitHub source code repository: [github.com/radio-grid-run/rgrHelper](https://github.com/radio-grid-run/rgrHelper)

For more information about Radio Grid Run itself, see: [https://radiogrid.run](https://radiogrid.run)


### Date of Creation:
September 26, 2023

### Contact Information:
[Author's ham radio operator personal page](https://www.qrz.com/db/hb9hwf)

For further information about the rules and the sport itself: [info@radiogrid.run](mailto://info@radiogrid.run)

