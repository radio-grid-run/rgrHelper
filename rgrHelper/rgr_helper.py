import click
import configparser
import os
from datetime import datetime
from jinja2 import Environment, PackageLoader
from dotenv import load_dotenv
import time
import csv
import uuid
import what3words
from area import area
import geojson
from hashlib import blake2b

"""
Helper tools for Radio Grid Run activities

Radio Grid Run, Frédéric Noyer 2023
"""


class Config(object):

    def __init__(self):
        self.verbose = False
        self.default = configparser.ConfigParser()
        self.game = configparser.ConfigParser()
        load_dotenv()
        self.myAPIkey = os.getenv('w3wapikey')
        cwd = os.path.dirname(__file__)
        conf_path = os.path.join(cwd, "conf")
        self.default.read(os.path.join(conf_path, 'rgrHelper.ini'))
        self.game.read(os.path.join(conf_path, 'gameConfig.ini'))
        self.strt_time = time.time()


# passing config object to sub-commands
pass_config = click.make_pass_decorator(Config, ensure=True)

# Jinja2 Environement creation
J2env = Environment(
    loader=PackageLoader('rgr_helper', 'conf'),
    trim_blocks=True,
    lstrip_blocks=True,
)


@click.group()
@click.option('--verbose', '-v', is_flag=True,
              help='Showing various details of the process.')
@pass_config
def cli(config, verbose):
    """Command line interface for Radio Grid Run Helper tools. Version

        FILENAME is the name of the file to check.
    """ + \
        config.default['general']['version']
    config.verbose = verbose
    round_hash_id = blake2b(digest_size=4)
    round_id_str = config.game['round']['startTime']+config.game['round']['hqw3w']
    round_hash_id.update(round_id_str.encode('utf-8'))
    config.roundhash = round_hash_id

@cli.command()
@pass_config
def testw3w(config):
    """Sending a API call to w3w to check connection."""

    geocoder = what3words.Geocoder(config.myAPIkey)
    col_sep = chr(int(config.default['CSV_conventions']['column_separator']))
    geocoder = what3words.Geocoder(config.myAPIkey)

    suggSet = geocoder.autosuggest(
        'souriante.démonter.capteur', clip_to_country=config.default['geo']['lst_clip_to_country'])
    print(suggSet)
    res = geocoder.convert_to_coordinates('souriante.démonter.capteur')
    print(res)


@cli.command()
@pass_config
def testarea(config):
    """Test for area function"""

    # obj = {
    #         'type': 'Feature',
    #         'geometry': {
    #             'type': 'Polygon',
    #             'coordinates': [
    #                 (7.118023, 46.961554),
    #                 (7.120988, 46.968211),
    #                 (7.110887, 46.965731)
    #                 ]
    #         }
    #     }
    myPoly = geojson.Polygon([[
        (7.118023, 46.961554),
        (7.120988, 46.968211),
        (7.110887, 46.965731)
    ]])
    myArea = area(myPoly)
    print(myArea)


@cli.command()
@click.option('--savesortedinput', default=True, help='Save useful column of input data to a .CSV file sorted by team and time.')
@click.argument('input', type=click.Path(exists=True, file_okay=True))
@click.argument('team')
@pass_config
def computeterritory(config, savesortedinput, input, team):
    """Generate a geoJSON Feature Collections .json output file with all Points and the related Polygon.

    INPUT  Relativ path to csv input file.

    TEAM   Identifier of the team (according to csv column 'team_id').
    """

    
    ## Intialization
    #

    geocoder = what3words.Geocoder(config.myAPIkey)

    # String of geoJSON Points and the related
    # Polygon to be injected into geoJSON FeatureCollection
    features_string = ''    
    
    # Coordinates array for Polygon geoJSON Feature
    poly_coord = []
    
    # Count of contact for the team selected in argument TEAM
    contact_count = 0

    # number of decimal place to round the resulting area surface
    # = nombre de chiffres significatifs
    # normally the area are in the 1-2 square kilometer range
    # it seems coherent to go down to 1 square meter. Which is the 8th decimal.
    decPlaces = 0

    ## Opening input csv input file
    with open(input, newline='', encoding='utf-8-sig') as inputFile:
        ## Reading input data
        indata = csv.DictReader(
            inputFile, delimiter=',', quotechar='"', skipinitialspace=True)
        
        ## Sorting input data
        # sort criterias:
        #       1. team ID
        #       2. timestamp of the contact 
        sortedInData = sorted(indata, key=lambda row: (
            row['team_id'], row['contact_time']))
        
        ## IF Option --saveSortedInput
        # writing sorted input data to *.csv file
        # 
        if savesortedinput:
            with open(config.roundhash.hexdigest() + '_' + config.game['output']['filename_inputData_sorted'], 'w', encoding='utf8') as sorted_data_copy:
                myfieldnames = ["team_id", "word1", "word2","word3","Notes","Added Time"]
                # sorted_data_writer = csv.DictWriter(sorted_data_copy, fieldnames=config.default['CSV_conventions']['useful_column'], extrasaction='ignore')
                sorted_data_writer = csv.DictWriter(sorted_data_copy, fieldnames=myfieldnames, extrasaction='ignore')
                sorted_data_writer.writeheader()
                for row_sorted in sortedInData:
                    sorted_data_writer.writerow(row_sorted)
                    
        ## Computing contacts from selected team 
        #   geoJSON FeaturesCollection representing a game round.
        #   Each contact as a geoJSON Point Feature.
        #   Finally, a geoJSON Polygon made of Points is add with it's
        #   area computed and documented as a Feature property.
        for row in sortedInData:
            if row['team_id'] == team:
                contact_count = contact_count+1
                ## resolving what3words address through w3w API
                # among those are the square coordinate 
                res = geocoder.convert_to_coordinates(
                    row['word1'] + "." + row['word2'] + "." + row['word3'])
                # creating Point feature with geojson
                onePoint = "{\"type\": \"Feature\",\"geometry\":" + str(
                    geojson.Point((res['coordinates']['lng'], res['coordinates']['lat']))) + "}"
                
                # DEBUG
                if config.verbose:
                    print(onePoint)
                
                ## computation of geoJSON Point
                #   Feature based on Jinja2 template
                point_template = J2env.get_template(
                    config.default['template']['template_point_contact_filename']
                )
                point_data = point_template.render(
                    point_coord='[' + str(
                        res['coordinates']['lng']) + ', ' + str(res['coordinates']['lat']) + ']',
                    contact_time=row['contact_time'],
                    # uuid is random
                    feature_uuid=uuid.uuid4(),
                    contact_country=res['country'],
                    contact_nrstPlace=res['nearestPlace'],
                    contact_w3w=res['words'],
                    contact_w1=res['words'].split('.')[0],
                    contact_w2=res['words'].split('.')[1],
                    contact_w3=res['words'].split('.')[2],
                    contact_lng=res['language'],
                    contact_map=res['map']
                )
                ## insert Point Feature into string of Features
                #  to be inserted into FeatureCollection
                features_string += point_data + ','

                ## Point coordinate inserted into array for the Polygon Feature
                #  has to be inserted as a tuple
                poly_coord.append(
                    tuple((res['coordinates']['lng'], res['coordinates']['lat'])))

    ## If the selected team has at least recorded one contact,
    #   computes the area and generates a geoJSON Feature collection
    #   expoted as a JSON file
    #  If a team has 1 or 2 contacts, the Polygon will not be valid
    #   and the area will be 0. 
    if contact_count > 0:
       
        ## resolving what3words address of game HQ through w3w API
        # Game Headquarter what3word is recorded in gameConfig.ini
        res_hq = geocoder.convert_to_coordinates(
            config.game['round']['hqw3w'])
        print(res_hq)

        ## computation of geoJSON Polygon
        #   Feature made of the contact Points based on Jinja2 template
        featurePolygon_template = J2env.get_template(
            config.default['template']['template_polygon_filename']
        )

        ## first and last point of the Polygone have to be the same to close it
        poly_coord.append(poly_coord[0])
        
        #replace '(' by '[' and replace ')' by ']' to get a valid geoJSON Polygon
        poly_coord_string = '['
        for oneCoord in poly_coord:
            poly_coord_string = poly_coord_string + ' ['+ str(oneCoord) +'],'
        poly_coord_string = poly_coord_string[0:-1] + ']'
        
        # Convert Coordinates to Polygon to get area
        teamPoly = geojson.Polygon([poly_coord])
        # computing Polygon aera in sqare kilometers
        myArea = round(area(teamPoly))
        myArea_separated = f"{myArea:,}"
        myArea_rounded_approx =round(myArea,-2)
        # DEBUG
        if config.verbose:
            print(myArea_separated)
        
        poly_string = featurePolygon_template.render(
            polygon_coords=poly_coord_string.replace('(','').replace(')',''),  # array of Points coords
            feature_uuid=uuid.uuid4(),  # random generated UUID
            round_identifier=config.roundhash.hexdigest(),   # round hash based on startTime and hqw3w
            polygon_area=myArea_separated,       
            polygon_area_approx="about " + str(round(myArea_rounded_approx)/1000000) + " square kilometers",       
            hq_w3w=res_hq['words'],     # w3w address of Polygon is based on HQ w3w address 
            hq_w1=config.game['round']['hqw3w'].split('.')[0],
            hq_w2=config.game['round']['hqw3w'].split('.')[1],
            hq_w3=config.game['round']['hqw3w'].split('.')[2],
            hq_nrstPlace=res_hq['nearestPlace'],    # w3w properties of square address
            hq_country=res_hq['country'],           # w3w properties of square address
            hq_lng=res_hq['language'],              # w3w properties of square address
            hq_map=res_hq['map'],                    # w3w properties of square address,            
            # team -> click argument value, ['name'] -> config key 
            team_name=config.game[str(team)]['name'],
            # team -> click argument value, ['id'] -> config key 
            team_ID=config.game[str(team)]['id']
        )
        ## adding geoJSON Polygon Feature to the Points Features 
        features_string += poly_string

        featureCollection_template = J2env.get_template(
            config.default['template']['template_featureColl_filename']
        )
        ## computation of geoJSON FeatureCollection
        #   Feature based on Jinja2 template.
        #   Represents the team's results territory 

        featureColl_data = featureCollection_template.render(
            features=features_string,           # Points and Polygon geoJSON Feature
            start_time=config.game['round']['startTime'],
            feature_uuid=uuid.uuid4(),          # random generated UUID
            round_identifier=config.roundhash.hexdigest(),   # round hash based on startTime and hqw3w
            hq_country=res_hq['country'],
            hq_nrstPlace=res_hq['nearestPlace'],
            hq_w3w=res_hq['words'],             # w3w address of Polygon is based on HQ w3w address
            hq_w1=config.game['round']['hqw3w'].split('.')[0],
            hq_w2=config.game['round']['hqw3w'].split('.')[1],
            hq_w3=config.game['round']['hqw3w'].split('.')[2],
            hq_lng=res_hq['language'],
            hq_map=res_hq['map'],
            # team -> click argument value, ['name'] -> config key 
            team_name=config.game[str(team)]['name'],
            # team -> click argument value, ['id'] -> config key 
            team_ID=config.game[str(team)]['id']
        )
        # writing output to file
        with open(config.roundhash.hexdigest() + '_' + config.game['output']['filename_teamTerritory_description']+'_team'+team+'.json', 'w', encoding='utf8') as out_file:
            out_file.write(featureColl_data)
        out_file.close()
    else:
        print('Sorry, there are no contact recorded for team ' + team + '.')

@cli.command()
@pass_config
def hqpoint(config):
    """Generate a geoJSON Point Feature .json output file for the Round Headquarter.

    """

    geocoder = what3words.Geocoder(config.myAPIkey)

    # Initialization

    ## resolving what3words address through w3w API
    # among those are the square coordinate 
    res_hq = geocoder.convert_to_coordinates(
        config.game['round']['hqw3w'])
    # creating Point feature with geojson
    feature_hq_point = "{\"type\": \"Feature\",\"geometry\":" + str(
        geojson.Point((res_hq['coordinates']['lng'], res_hq['coordinates']['lat']))) + "}"
    
    # DEBUG
    if config.verbose:
        print(feature_hq_point)
    
    ## computation of geoJSON Point
    #   Feature based on Jinja2 template
    point_template = J2env.get_template(
        config.default['template']['template_point_hq_filename']
    )
    hq_data = point_template.render(
           feature_point=feature_hq_point[0:-1],           # Points goeJSON Feature of headquarter
            round_time=config.game['round']['startTime'],
            feature_uuid=uuid.uuid4(),          # random generated UUID
            round_identifier=config.roundhash.hexdigest(),   # round hash based on startTime and hqw3w
            hq_country=res_hq['country'],
            hq_nrstPlace=res_hq['nearestPlace'],
            hq_w3w=res_hq['words'],             # w3w address of Polygon is based on HQ w3w address
            hq_w1=config.game['round']['hqw3w'].split('.')[0],
            hq_w2=config.game['round']['hqw3w'].split('.')[1],
            hq_w3=config.game['round']['hqw3w'].split('.')[2],
            hq_lng=res_hq['language'],
            hq_map=res_hq['map']
    )

    # print(config.roundhash.hexdigest())
    # writing output to file
    with open(config.roundhash.hexdigest() + '_' + config.game['output']['filename_roundHQ_description'], 'w', encoding='utf8') as out_file:
        out_file.write(hq_data)
    out_file.close()

if __name__ == '__main__':
    cli()
