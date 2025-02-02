from unitxt.blocks import (
    LoadHF,
    TaskCard,
)
from unitxt.catalog import add_to_catalog
from unitxt.collections_operators import Get, Slice
from unitxt.operators import IndexOf, ListFieldValues, Set, ShuffleFieldValues
from unitxt.string_operators import Join, Replace, Split, Strip
from unitxt.test_utils.card import test_card

card = TaskCard(
    loader=LoadHF(path="Anthropic/hh-rlhf"),
    preprocess_steps=[
        "splitters.small_no_dev",
        Strip(field="chosen"),
        Replace(field="chosen", old="\n\n", new="\n"),
        Split(field="chosen", by="\nAssistant:"),
        Get(field="chosen", item=-1, to_field="output_choice"),
        Slice(field="chosen", stop=-1),
        Join(field="chosen", by="\nAssistant:", to_field="input"),
        Split(field="rejected", by="\nAssistant:"),
        Get(field="rejected", item=-1, to_field="output_rejected"),
        ListFieldValues(
            fields=["output_choice", "output_rejected"],
            to_field="choices",
        ),
        ShuffleFieldValues(field="choices"),
        Set(
            fields={
                "input_type": "dialog",
                "output_type": "response",
                "instruction": "Respond the following dialog in an helpful and harmfull way.",
            }
        ),
        IndexOf(
            search_in="choices", index_of="output_choice", to_field="output_choice"
        ),
    ],
    task="tasks.evaluation.preference",
    templates="templates.evaluation.preference.all",
    __tags__={
        "arxiv": "2204.05862",
        "flags": ["human-feedback"],
        "license": "mit",
        "region": "us",
    },
    __description__=(
        "This repository provides access to two different kinds of data: \n"
        "1) Human preference data about helpfulness and harmlessness from Training a Helpful and Harmless Assistant with Reinforcement Learning from Human Feedback. These data are meant to train preference (or reward) models for subsequent RLHF training. These data are not meant for supervised training of dialogue agents. Training dialogue agents on these data is likely… See the full description on the dataset page: https://huggingface.co/datasets/Anthropic/hh-rlhf."
    ),
)

test_card(card, strict=False)
add_to_catalog(card, "cards.hh_rlhf", overwrite=True)
