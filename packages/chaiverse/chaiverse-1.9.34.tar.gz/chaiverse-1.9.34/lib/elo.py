from math import log10

# a player that never lost a game will have elo score of 1e30 and elo_rating of 9999
# a player that never win a game will have elo score of 1e-30 and elo_rating of 0
HIGHEST_ELO_SCORE = 1e30
LOWEST_ELO_SCORE = 1e-30
HIGHEST_ELO_RATING = 9999
LOWEST_ELO_RATING = 0

# Upperbound estimate of delta ELO_RATING per delta ELO_SCORE:
# If ELO change from 2000 to 2000.1, the score_ratio=ln10(elo/400), and it will change by 2e-5
# so the delta(ELO)/delta(score_ratio) is about 5e4. Making it 1e6 to be safe.
MAX_DELTA_ELO_RATING_PER_DELTA_SCORE_RATIO = 1e6


def get_mle_elo_scores(initial_elo_scores, wins_dict, elo_rating_error_bar=0.1):
    """
    Calculate elo_scores using MLE algorithm.
    MLE refers to maximum likelyhood estimation. The elo_score here is proportional to win odd, and
      elo_rating = elo_base + elo_scale * log10(elo_score)
    
    Let's say there are two models, i, j, and a third model k as arbitrary chosen baseline, and
    let's call p(i>j) is probability that i wins j:
      elo_score(i) = win_odd(i,k) * 2
      elo_score(k) = 1
      win_odd(i,j) = win_odd(i,k) * win_odd(k,j)  -> this is required to be true if score exists
      win_odd(i,j) = p(i>j) / (1-p(i>j))
      p(i>j) = elo_score(i) / (elo_score(i) + elo_score(j))
      
    Reference of the algorithm
    https://en.wikipedia.org/wiki/Bradley%E2%80%93Terry_model
    https://jmlr.org/papers/volume24/22-1086/22-1086.pdf

    Different algorithms converges at different speed. The algorithm used here is proposed in 2023
    in the paper referenced. It is 100x faster than previous Zermelo. The implementation below is also
    efficient with sparse matrix.
    """
    new_elo_scores = initial_elo_scores
    rating_error = elo_rating_error_bar
    for _ in range(100):
        prev_elo_scores = new_elo_scores.copy()
        for player in new_elo_scores.keys():
            new_elo_scores[player] = _get_updated_elo_score(new_elo_scores, player, wins_dict)
        rating_error = _get_elo_rating_error_bar(new_elo_scores, prev_elo_scores)
        if rating_error < elo_rating_error_bar:
            break
    if rating_error >= elo_rating_error_bar:
        raise ValueError('elo failed to converage with error={rating_error}')
    new_elo_scores = _normalize_elo_scores(new_elo_scores)
    return new_elo_scores


def _get_updated_elo_score(new_elo_scores, competitor_id, wins_dict):
    numerator = 0
    denominator = 0
    for opponent_id in wins_dict.get(competitor_id, {}).keys():
        score_sum = new_elo_scores[competitor_id] + new_elo_scores[opponent_id]
        numerator += wins_dict[competitor_id][opponent_id] * new_elo_scores[opponent_id] / score_sum
    for opponent_id in wins_dict.keys():
        score_sum = new_elo_scores[competitor_id] + new_elo_scores[opponent_id]
        denominator += wins_dict[opponent_id].get(competitor_id, 0) / score_sum
    score = LOWEST_ELO_SCORE
    if numerator > 0:
        score = numerator / denominator if denominator > 0 else HIGHEST_ELO_SCORE
    return score


def _get_elo_rating_error_bar(new_elo_scores, elo_scores):
    rating_error = 0
    if len(new_elo_scores):
        elo_score_diffs = [new_elo_scores[player] - elo_scores[player] for player in new_elo_scores.keys()]
        max_elo_score_diff = max(elo_score_diffs)
        min_finite_elo_scores = min([value for value in new_elo_scores.values() if value > LOWEST_ELO_SCORE])
        rating_error = max_elo_score_diff / min_finite_elo_scores * MAX_DELTA_ELO_RATING_PER_DELTA_SCORE_RATIO
    return rating_error


def _normalize_elo_scores(scores_dict):
    scores_to_average = [
        score for score in scores_dict.values()
        if 0 < score < HIGHEST_ELO_SCORE
    ]
    normalized = scores_dict
    if len(scores_to_average):
        average_elo_score = sum(scores_to_average) / len(scores_to_average)
        normalized = { 
            player: score/average_elo_score if LOWEST_ELO_SCORE < score < HIGHEST_ELO_SCORE else score
            for player, score in scores_dict.items()
        }
    return normalized


def get_elo_ratings(scores, elo_base_score, elo_base_rating):
    elo_ratings = {
        player: _get_elo_rating(score, elo_base_score, elo_base_rating)
        for player, score in scores.items()
    }
    return elo_ratings


def _get_elo_rating(score, elo_base_score, elo_base_rating):
    if score <= LOWEST_ELO_SCORE:
        rating = LOWEST_ELO_RATING
    elif score >= HIGHEST_ELO_SCORE:
        rating = HIGHEST_ELO_RATING
    else:
        rating = 400 * log10(score / elo_base_score) + elo_base_rating
        rating = max(rating, LOWEST_ELO_RATING)
        rating = min(rating, HIGHEST_ELO_RATING)
    return rating
