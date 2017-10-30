import os
import sys
import json
import datetime
import traceback
import logging

local_dir = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(local_dir, "./"))

# Outside a virtualenv, sys.real_prefix should not exist.
# if not in virtualenv, then we are running at aws
# and need to get parser from the lib dir
if not hasattr(sys, 'real_prefix'):
    sys.path.append(os.path.join(local_dir, "./lib"))

from recommender import Recommender
from classes.power import Power
from classes.segment import Segment

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def _get_headers():
    return {
        # Required for CORS support to work
        'Access-Control-Allow-Origin':
        '*',
        'Access-Control-Allow-Headers':
        'Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token,Cache-Control,X-ApiSession',
        # set to true when using cookies and authorization headers with HTTPS
        'Access-Control-Allow-Credentials':
        False
    }


def recommend(event, context=None):
    body = event["body"]

    if not body:
        error = "post body is null or empty"
        logger.error(error)
        return {"statusCode": 500, "body": json.dumps({"error": error})}

    segment = json.loads(body)

    logger.info(segment)

    recommender = Recommender()

    # @todo, pass influencer seeds as argument
    influencer = os.path.join(os.path.join(
        local_dir, 'seeds'), 'mike.json')

    with open(influencer) as json_data:
        influences = json.load(json_data)

    logger.info(influences)

    recommender.artists = [a['id'] for a in influences['artists']]

    recommender.tracks = [t['id'] for t in influences['tracks']]

    recommender.genres = influences['genres']

    segment = Segment(
        segment['start_time'],
        segment['end_time'],
        segment['segment_type'],
        Power(segment['power']['min_intensity'],
              segment['power']['max_intensity']),
        segment['cadence'])

    try:
        results = recommender.get_tracks_for_segment(segment)

        print ('got results from recommender.get_tracks_for_segment')

        logger.info(json.dumps(results, indent=4, sort_keys=True))

        return {
            "statusCode": 200,
            "headers": _get_headers(),
            "body": json.dumps(results, indent=4, sort_keys=True)
        }
    except Exception as e:
        logger.error(e.__doc__)
        logger.error(e.message)
        logger.error(traceback.format_exc())

        return {"statusCode": 500,
                "headers": _get_headers(),
                "body": json.dumps({"error": error})
                }
