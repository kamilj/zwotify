## Zwift workout file .zwo to Spotify playlist

Using the duration, intensity and cadence information in the Zwift workout xml file, the Spotify recommendations API is called seeded with genres, artists and tracks, min, max and target tempo, energy, danceability and valence (happy/sad) and a playlist is created using the tracks ordered to match the duration of each workout segment (as best as possible).

The front-end is React, bootstrapped with [Create React App](https://github.com/facebookincubator/create-react-app).

The hosting is AWS Route 53, CloudFront, S3

The back-end is AWS Lambda (Python)

