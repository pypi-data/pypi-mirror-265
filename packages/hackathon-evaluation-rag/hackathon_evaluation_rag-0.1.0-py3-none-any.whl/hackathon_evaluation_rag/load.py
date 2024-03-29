import ast
import csv

from typing import List

from datasets import Dataset
from dataclasses import dataclass, field


@dataclass
class Submission:
    sub: csv.DictReader
    _answers: List[str] = field(default_factory=list)
    _questions: List[str] = field(default_factory=list)
    _contexts: List[str] = field(default_factory=list)

    def __post_init__(self):

        for row in self.sub:
            try:
                if type(row["question"]) != str or type(row["answer"]) != str:
                    raise ValueError("Question and Answers should be a string")

                if type(ast.literal_eval(row["contexts"])) != list:
                    raise ValueError("Context should be a list of strings")

                self._questions.append(row["question"])
                self._answers.append(row["answer"])
                self._contexts.append(ast.literal_eval(row["contexts"]))

            except KeyError:
                raise ValueError(
                    "Submission file should have 'question', 'answer' and 'contexts' columns"
                )

        self.validate()

    def validate(self):
        if (
            len(self._questions) != len(self._answers)
            or len(self._questions) != len(self._contexts)
            or len(self._answers) != len(self._contexts)
        ):
            raise ValueError(
                "Mismatch of values (questions, answer, contexts), please check the submission file"
            )

    def __len__(self):
        return len(self.sub)


@dataclass
class GroundTruth:
    gt: csv.DictReader
    _answers: List[str] = field(default_factory=list)
    _questions: List[str] = field(default_factory=list)

    def __post_init__(self):

        for row in self.gt:
            self._questions.append(row["question"])
            self._answers.append(ast.literal_eval(row["groundtruth"]))

    def __len__(self):
        return len(self.gt)


def load_submission(sb):
    print("---LOADING SUBMISSION ---")
    submission = Submission(sub=csv.DictReader(open(sb)))
    return submission.__dict__


def load_groundtruth(groundtruth):
    print("---LOADING GROUNDTRUTH ---")
    groundtruth = GroundTruth(gt=csv.DictReader(open(groundtruth)))
    return groundtruth.__dict__


def validation_gt_sub(groundtruth, submission):

    print("---VALIDATING SUBMISSION AND GROUNDTRUTH ---")

    try:
        if len(groundtruth["_questions"]) != len(submission["_questions"]):
            raise ValueError(
                "Submission and Groundtruth have different number of questions"
            )

        for i in range(len(groundtruth["_questions"])):
            if groundtruth["_questions"][i] != submission["_questions"][i]:
                raise ValueError("Submission and Groundtruth have different questions")

        print("---VALIDATION SUCCESSFUL---")
    except:
        raise ValueError("---VALIDATION FAILED")


def load(sub, gt):

    groundtruth = load_groundtruth(gt)
    submission = load_submission(sub)

    validation_gt_sub(groundtruth, submission)

    dataset = Dataset.from_dict(
        {
            "question": groundtruth["_questions"],
            "answer": submission["_answers"],
            "contexts": submission["_contexts"],
            "ground_truth": groundtruth,
        }
    )

    return dataset
