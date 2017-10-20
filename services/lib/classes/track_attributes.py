class TrackAttributes:
    '''
    TrackAttributes to pass to the recommendations API.

    Danceability - describes how suitable a track is for dancing based on a combination of musical elements including 
    tempo, rhythm stability, beat strength, and overall regularity. A value of 0.0 is least danceable and 1.0 is
    most danceable.

    Energy  - a measure from 0.0 to 1.0 and represents a perceptual measure of intensity and activity. 
    Typically, energetic tracks feel fast, loud, and noisy. For example, death metal has high energy, 
    while a Bach prelude scores low on the scale. Perceptual features contributing to this attribute include 
    dynamic range, perceived loudness, timbre, onset rate, and general entropy.

    Popularity - The value will be between 0 and 100, with 100 being the most popular. 
    The popularity is calculated by algorithm and is based, in the most part, on the total number of plays 
    the track has had and how recent those plays are.

    Note: When applying track relinking via the market parameter, it is expected to find relinked tracks with 
    popularities that do not match min_*, max_*and target_* popularities. These relinked tracks are accurate 
    replacements for unplayable tracks with the expected popularity scores. Original, 
    non-relinked tracks are available via the linked_from attribute of the relinked track response.

    Tempo - The overall estimated tempo of a track in beats per minute (BPM). In musical terminology, 
    tempo is the speed or pace of a given piece and derives directly from the average beat duration.

    A measure from 0.0 to 1.0 describing the musical positiveness conveyed by a track. 
    Tracks with high valence sound more positive (e.g. happy, cheerful, euphoric), 
    while tracks with low valence sound more negative (e.g. sad, depressed, angry).

    '''

    def __init__(self, genres=None, duration_ms=None, danceability=None, energy=None, popularity=None, min_tempo=None, max_tempo=None, target_tempo=None, valence=None, speechiness=None):
        if genres is None:
            self.genres = ['electro', 'work-out', 'house', 'pop']
        else:
            self.genres = genres

        if duration_ms is None:
            self.duration_ms = 3.5 * 60 * 1000
        else:
            self.duration_ms = duration_ms

        if danceability is None:
            self.danceability = 0.8
        else:
            self.danceability = danceability

        if energy is None:
            self.energy = 0.7
        else:
            self.energy = energy

        if popularity is None:
            self.popularity = 80
        else:
            self.popularity = popularity

        if min_tempo is None:
            self.min_tempo = 80
        else:
            self.min_tempo = min_tempo

        if max_tempo is None:
            self.max_tempo = 140
        else:
            self.max_tempo = max_tempo

        if target_tempo is None:
            self.target_tempo = 120
        else:
            self.target_tempo = target_tempo

        if valence is None:
            self.valence = 0.8
        else:
            self.valence = valence

        if speechiness is None:
            self.speechiness = 0.5
        else:
            self.speechiness = speechiness
