from dataclasses import dataclass, field
from ragas import evaluate

from ragas.metrics import (
    context_precision,
    faithfulness,
    context_recall,
    answer_relevancy,
    context_relevancy,
    answer_correctness,
    answer_similarity,
)
from ragas.metrics.critique import (
    harmfulness,
    conciseness,
    maliciousness,
    coherence,
    correctness,
)


@dataclass(frozen=False, kw_only=True, slots=True)
class Metrics:
    def __init__(self):
        pass

    def allmetrics(self):
        return [
            answer_similarity,
            context_precision,
            faithfulness,
            answer_relevancy,
            context_recall,
            context_relevancy,
            answer_correctness,
            coherence,
            conciseness,
            maliciousness,
            harmfulness,
            correctness,
        ]


def evaluate_results(llm, embedding_func, dataset):
    print("---EVALUATING RESULTS---")
    metrics = Metrics()

    result = evaluate(
        dataset=dataset,
        llm=llm,
        embeddings=embedding_func,
        metrics=metrics.allmetrics(),
    )
    return result
