from spotipy.oauth2 import SpotifyClientCredentials
import spotipy
import numpy as np
from scipy.stats import norm
import json

# recommends the next ten tracks
NUM_TRACKS = 20

with open('api.json') as api:
    api_obj = json.loads(api.read())

api_key = api_obj["api"]["key"]
api_secret = api_obj["api"]["secret"]

# initialize a single client
client_credentials = SpotifyClientCredentials(client_id=api_key, client_secret=api_secret)
sp = spotipy.Spotify(client_credentials_manager=client_credentials)


def recommend(curr_rate, target_rate, seed_tracks, cutoffs):
    """
        Generates a list of recommended songs.
        @param curr_rate: the current heart_rate
        @param target_rate: the projected target heart rate
        @param seed_tracks: the user-based seed tracks for each mode 
        @param cutoffs: the cutoffs for the user, based on activity
    """

    # The "to" probability value
    to_prob_val = dict((k, 0) for k in cutoffs.keys())

    # The "from" probability value
    from_prob_val = dict((k,0) for k in cutoffs.keys())

    # create a pseudoprobability value P(x, a) = N(x, a) / sum([N(x, b) for b in cutoffs])
    # Assume std of half of average difference between cutoffs
    avg_cutoffs = ((cutoffs["RUN"] - cutoffs["WEIGHTS"]) + (cutoffs["WEIGHTS"] - cutoffs["POST_WORKOUT"]) + (cutoffs["POST_WORKOUT"] - cutoffs["RELAX"])) / 3
    std = avg_cutoffs / 2
    for k in cutoffs.keys():
        mean = cutoffs[k]
        to_prob_val[k] = norm(mean, std).pdf(target_rate)
        from_prob_val[k] = norm(mean, std).pdf(curr_rate)
    
    # Now get the sum of all projected pseudoprobabilites in order to normalize to 1
    to_prob_tot = sum([i for i in to_prob_val.values()])
    from_prob_tot = sum([i for i in from_prob_val.values()])

    # normalize pseudoprobabilities
    to_prob_val = dict((k, v / to_prob_tot) for k, v in to_prob_val.items())
    from_prob_val = dict((k, v / from_prob_tot) for k, v in from_prob_val.items())

    # get the most probable from and to
    most_prob_to = max(to_prob_val, key=to_prob_val.get)
    most_prob_from = max(from_prob_val, key=from_prob_val.get)
    
    # now based on "how far away" the target is from the most prob centers, assign weights
    total_distance = (target_rate - cutoffs[most_prob_from]) + (target_rate - cutoffs[most_prob_to])
    weight_from = (target_rate - cutoffs[most_prob_from]) / total_distance
    weight_to = (target_rate - cutoffs[most_prob_to]) / total_distance

    # now to assign these weights in seed_tracks.
    # given seed tracks for from and to, take the minimum sized one as the seed base.
    # choose weight_from / seed_base tracks for from, weight_to / seed_base tracks for to

    seed_from = seed_tracks[most_prob_from]
    seed_to = seed_tracks[most_prob_to]
    seed_base = min(len(seed_from), len(seed_to))
    num_from_tracks = max(1, int(len(seed_from) * (weight_from / seed_base)))
    num_to_tracks = max(1, int(len(seed_to) * (weight_to / seed_base)))
    input_seed_tracks = list(np.random.choice(seed_from, num_from_tracks)) + list(np.random.choice(seed_to, num_to_tracks))
    print(input_seed_tracks)

    # use the input seed tracks to get recommendations
    results = sp.recommendations(seed_tracks=input_seed_tracks)
    return results["tracks"][:NUM_TRACKS]



if __name__ == "__main__":
    # testing data

    curr_rate = 160
    target_rate = 130
    cutoffs = {
        "RELAX": 75,
        "POST_WORKOUT": 95,
        "WEIGHTS": 120,
        "RUN": 160
    }
    seed_tracks = {
        "RELAX": [
            "spotify:track:4GKk1uNzpxIptBuaY97Dkj",
            "spotify:track:5M4yti0QxgqJieUYaEXcpw",
            "spotify:track:48ygvZn1YcxRP1gfHEDfsV",
            "spotify:track:7jnEVqyvscIaGLsJ8ezkEV",
            "spotify:track:6iZxpy5Z0BztLHsWE8cSzD",
        ],
        "POST_WORKOUT": [
            "spotify:track:2cnhi0n4UMWCXQIEaVjnm5",
            "spotify:track:5ANm5gWv5a65hjFAnDWMP3",
            "spotify:track:2gaZJDgE71VL9PzzUUlpMg",
            "spotify:track:3VdzKymHyCA7OQdUiDREKF"
        ],
        "WEIGHTS": [
            "spotify:track:4yGmiOowOj1ycFVd2E9Tj7",
            "spotify:track:2A49wpUOEgqWDWsE1qQ5Uv",
            "spotify:track:7ISL3LO8AWP3fKIXunvqTa",
            "spotify:track:1HhI5cx0VmyqclpbvYEwTV"
        ],
        "RUN": [
            "spotify:track:7vnYDHo16TCV9sE70zvB4b",
            "spotify:track:57bgtoPSgt236HzfBOd8kj",
            "spotify:track:57k0N16KmhOZVl5YFJebIw",
            "spotify:track:10s9tSE1e8RXSufhzw9Aw3",
            "spotify:track:39ZiU2QVBvDQzeepJjg8tp",
            "spotify:track:78lgmZwycJ3nzsdgmPPGNx",
            "spotify:track:2KHRENHQzTIQ001nlP9Gdc"
        ]
    }

    results = recommend(curr_rate, target_rate, seed_tracks, cutoffs)
    for r in results:
        print(r["name"])