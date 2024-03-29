import click

from hackathon_evaluation_rag.load import load
from hackathon_evaluation_rag.llm import load_evaluator
from hackathon_evaluation_rag.results import save_results
from hackathon_evaluation_rag.evaluate import evaluate_results


@click.command()
@click.option("--submission", help="The submission file", required=True)
@click.option("--groundtruth", help="The ground truth key", required=True)
@click.option("--env", help="Environment Key files", required=True)
def main(submission, groundtruth, env):

    dataset = load(submission, groundtruth)

    evaluating_llm, embedding_function = load_evaluator(env)

    result = evaluate_results(evaluating_llm, embedding_function, dataset)

    save_results(result)

    print("---EVALUATION COMPLETE---")


if __name__ == "__main__":

    main()
