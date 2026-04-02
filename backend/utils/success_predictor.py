def predict_success(match_score, semantic_score):
    # weighted score
    score = (match_score * 0.6) + (semantic_score * 0.4)

    # normalize (optional safety)
    if score > 100:
        score = 100

    return round(score, 2)