from unitxt import add_to_catalog
from unitxt.templates import InputOutputTemplate

add_to_catalog(
    InputOutputTemplate(
        instruction="""Read the following three parts: (A) Document, (B) Conversation between the user and the agent occurring in multiple turns. The user and agent alternate the conversation where the user asks a question, the agent gives a response to that question, and the user poses an inquiry at the end, (C) the Response (of the agent) to the last turn user query that continues the conversation from part 2. Your task is to evaluate if the Response (C) is completely grounded in the Document with one of three answers [yes, no, unsure], followed by an explanation. To make this determination, you can consider the response as consisting of a set of claims.\nIf all the claims are explicitly mentioned and appear word for word in the Document (A), you must answer yes and identify the part of document in the explanation output.\nIf at least one of the claims does not appear in the document content or you think it can be indirectly inferred, you must answer no.\nIf for at least one of the claims you cannot determine yes or no, and none of the other claims are ungrounded, you must answer unsure.\n\nFollow your answer with an explanation. Try to be concise. Limit your answer and explanation to at most 200 words.""",
        input_format="\n\nConversation:\n{question}\n\nResponse:\n{answer}\n\n\nOutput:",
        output_format="[[{rating}]]",
        postprocessors=[
            "processors.take_first_word",
            "processors.lower_case",
            "processors.yes_no_to_int",
            "processors.cast_to_float_return_0_5_if_failed",
        ],
    ),
    "templates.response_assessment.judges.grounded.v11",
    overwrite=True,
)
