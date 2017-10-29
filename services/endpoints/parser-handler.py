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

import zwoparser

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def parse(event, context=None):

    body = event["body"]

    # logger.info(body)

    if not body:
        error = "post body is null or empty"
        logger.error(error)
        return {"statusCode": 500, "body": json.dumps({"error": error})}

    segments = zwoparser.parse(body)

    segments_json = ','.join([x.toJSON() for x in segments])

    return {
        "statusCode": 200,
        "body": "[%s]" % segments_json
    }
