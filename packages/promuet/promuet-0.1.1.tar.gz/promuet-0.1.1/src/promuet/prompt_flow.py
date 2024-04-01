import textwrap
from copy import deepcopy
from itertools import chain

import openai
from loguru import logger
from pydantic import BaseModel

from promuet.match_items import ListMatchItem, TemplateMatchItem, VariableMatchItem, VarType, parse_template
from promuet.prompt_message import PromptMessage


class Prompt(BaseModel):
    messages: list[PromptMessage]
    response_format: str
    is_continuation: bool = False
    description: str = ''

    def __init__(
        self,
        messages: list[PromptMessage],
        response_format: str,
        *,
        is_continuation: bool = False,
        description: str = '',
    ):
        super().__init__(
            messages=messages,
            response_format=textwrap.dedent(response_format),
            is_continuation=is_continuation,
            description=description,
        )

    def execute(
        self, variables: dict[str, VarType], prior_messages: list[PromptMessage] | None = None
    ) -> dict[str, VarType]:
        template = TemplateMatchItem(self.response_format)
        var_names = [x.var_name for x in template.children if isinstance(x, VariableMatchItem | ListMatchItem)]
        if all(x in variables for x in var_names):
            return {x: variables[x] for x in var_names}
        prior_messages = (prior_messages or []) if self.is_continuation else []
        if self.is_continuation and not prior_messages:
            msg = 'Expected continuation of prior messages'
            raise ValueError(msg)
        chat_messages = [x.to_chat_message(variables) for x in chain(prior_messages, self.messages)]
        response = openai.chat.completions.create(model='gpt-3.5-turbo', messages=chat_messages)
        response_text = response.choices[0].message.content
        response_text = response_text.strip()
        if response_text.startswith('```\n') and response_text.endswith('\n```'):
            response_text = response_text.removeprefix('```\n').removesuffix('\n```')
        return parse_template(self.response_format, response_text)


class PromptFlow(BaseModel):
    prompts: list[Prompt]

    def __init__(self, *prompts: Prompt):
        super().__init__(prompts=list(prompts))

    def run(self, variables: dict[str, VarType]) -> dict[str, VarType]:
        prior_messages = []
        variables = deepcopy(variables)
        all_new_vars = {}
        for prompt in self.prompts:
            if not prompt.is_continuation:
                prior_messages.clear()
            logger.info("Running prompt '{}'...", prompt.description)
            new_vars = prompt.execute(variables, prior_messages)
            logger.debug('Extracted variables:\n\n{}', new_vars)
            variables.update(new_vars)
            all_new_vars.update(new_vars)
            prior_messages.extend(prompt.messages)
        return all_new_vars
