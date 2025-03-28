# topsis.py
import numpy as np

def topsis_score(feature_vector, all_feature_vectors, weights=None):
    """
    Calculate the TOPSIS score for one participant given all participants.
    We assume each row in all_feature_vectors is [pitch, tempo, tempo_consistency, pitch_quality, pace].
    feature_vector is the same shape as rows in all_feature_vectors.
    weights is a list of the same length as the feature vector indicating relative importance.
    """

    # Convert to numpy array
    A = np.array(all_feature_vectors, dtype=float)
    if weights is None:
        # Equal weights by default
        weights = np.ones(A.shape[1])
    
    # 1. Normalize matrix
    norm_A = A / np.sqrt((A**2).sum(axis=0))

    # 2. Weighted normalized matrix
    W = np.array(weights) / np.sum(weights)  # normalized weights
    weighted_norm_A = norm_A * W

    # 3. Ideal (best) and negative-ideal (worst) solutions
    ideal_solution = np.max(weighted_norm_A, axis=0)
    negative_ideal_solution = np.min(weighted_norm_A, axis=0)

    # 4. Distance to ideal and negative-ideal for each row
    dist_to_ideal = np.sqrt(((weighted_norm_A - ideal_solution) ** 2).sum(axis=1))
    dist_to_negative_ideal = np.sqrt(((weighted_norm_A - negative_ideal_solution) ** 2).sum(axis=1))

    # 5. Topsis score = dist_to_negative / (dist_to_negative + dist_to_positive)
    dist_sum = dist_to_ideal + dist_to_negative_ideal
    topsis_scores = np.where(dist_sum == 0, 0, dist_to_negative_ideal / dist_sum)

    # 6. Now find the index of the current feature_vector in all_feature_vectors
    # We do the same transformations for the single "feature_vector"
    all_vectors_list = all_feature_vectors
    # We'll find that row's index to get its position in the topsis_scores
    for idx, row in enumerate(all_vectors_list):
        if np.allclose(row, feature_vector):
            # Return the single score and rank
            single_score = topsis_scores[idx]
            # Rank the scores in descending order (higher = better) 
            # The rank of the current item is 1-based
            sorted_scores = sorted(topsis_scores, reverse=True)
            rank = sorted_scores.index(single_score) + 1
            return single_score, rank

    return 0.0, None
