import os
import sys
import json
import datetime
import logging

localDir = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(localDir, "./"))

# Outside a virtualenv, sys.real_prefix should not exist.
# if not in virtualenv, then we are running at aws
# and need to get parser from the lib dir
if not hasattr(sys, 'real_prefix'):
    sys.path.append(os.path.join(localDir, "lib"))

from recommender import Recommender
from classes.power import Power
from classes.segment import Segment

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def recommend(event, context=None):
    body = event["body"]

    if not body:
        error = "post body is null or empty"
        logger.error(error)
        return {"statusCode": 500, "body": json.dumps({"error": error})}

    segment = json.loads(body)

    logger.info(segment)

    recommender = Recommender()

    influencer = os.path.join(os.path.join(
        localDir, 'seeds'), 'mike_hanney.json')

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

        logger.info(json.dumps(results['tracks'], indent=4, sort_keys=True))

        return {
            "statusCode": 200,
            "body": json.dumps(results['tracks'], indent=4, sort_keys=True)
        }
    except:
        error = "Failed to get recommendations from spotify"
        logger.error(error)
        return {"statusCode": 500, "body": json.dumps({"error": error})}
