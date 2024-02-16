from app.chat.redis import client
import random

def random_component_by_score(component_type, component_map):
    # make sure component_type is 'llm', 'retriever', or 'memory'
    if component_type not in ['llm', 'retriever', 'memory']:
        raise ValueError("Invalid component type")


    # from redis, get the hash containing the sum total scores for component type
    values = client.hgetall(f"{component_type}_score_values")

    # from redis, get the number of types each component has been voted on.
    counts = client.hgetall(f"{component_type}_score_counts")

    # get all valid component names from the component map
    names = component_map.keys()

    # Loop over the valid names and use them to calculate the average score
    # Add average score to a dictionary
    avg_scores = {}
    for name in names:
        score = int(values.get(name, 1))
        count = int(counts.get(name, 1))
        avg = score / count
        avg_scores[name] = max(avg, 0.1) # Don't want a case where first vote is a downvote and we never select it

    print(avg_scores)
    
    # Do a weighted random selection
    sum_scores = sum(avg_scores.values())
    random_val = random.uniform(0, sum_scores)
    cumulative = 0
    for name, score in avg_scores.items():
        cumulative += score
        if random_val <= cumulative:
            return name

def score_conversation(
    conversation_id: str, score: float, llm: str, retriever: str, memory: str
) -> None:
    score = min(max(score, 0), 1)

    # hincrby = increment hash by

    # to query connect to redis using redis-cli
    # HGETALL llm_score_values
    client.hincrby("llm_score_values", llm, score)
    client.hincrby("llm_score_counts", llm, 1)

    client.hincrby("retriever_score_values", llm, score)
    client.hincrby("retriever_score_counts", llm, 1)

    client.hincrby("memory_score_values", llm, score)
    client.hincrby("memory_score_counts", llm, 1)

def get_scores():
    aggregate = {"llm":{}, "retriever": {}, "memory": {}}

    for component_type in aggregate.keys():
        values = client.hgetall(f"{component_type}_score_values")
        counts = client.hgetall(f"{component_type}_score_counts")

        names = values.keys()

        for name in names:
            score = int(values.get(name, 1))
            count = int(counts.get(name, 1))
            avg = score / count
            aggregate[component_type][name] = [avg]

    return aggregate