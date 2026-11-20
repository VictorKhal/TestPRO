from mistralai import agents

from prompts import (
    BUSINESS_ANALYST_INSTRUCTIONS,
    FULLSTACK_DEVELOPER_INSTRUCTIONS,
    MARKETING_MANAGER_INSTRUCTIONS,
    ORCHESTRATOR_INSTRUCTIONS,
    PRODUCT_MANAGER_INSTRUCTIONS,
    QA_ENGINEER_INSTRUCTIONS,
    SALES_MANAGER_INSTRUCTIONS,
)

NO_NESTED_SUBAGENTS = agents.Builtins(subagents=False)


def _subagent(name: str, description: str, instructions: str) -> agents.Subagent:
    return agents.Subagent(
        name=name,
        description=description,
        instructions=instructions,
        builtins=NO_NESTED_SUBAGENTS,
    )


agent = agents.Agent(
    model="mistral-large-4",
    name="cto-orchestrator",
    instructions=ORCHESTRATOR_INSTRUCTIONS,
    subagents=[
        _subagent(
            name="product-manager",
            description=(
                "User Stories + Acceptance Criteria + Edge Cases, "
                "MoSCoW-бэклог MVP, метрики, отсечение оверинжиниринга."
            ),
            instructions=PRODUCT_MANAGER_INSTRUCTIONS,
        ),
        _subagent(
            name="business-analyst",
            description=(
                "Спецификации: PostgreSQL/Supabase DDL + RLS, JSON-схемы ИИ, "
                "контракты API, бизнес-правила режимов и лимиты."
            ),
            instructions=BUSINESS_ANALYST_INSTRUCTIONS,
        ),
        _subagent(
            name="fullstack-developer",
            description=(
                "Код Next.js 14+/TypeScript/Supabase: Server Components, Server "
                "Actions, Route Handlers, LLM-интеграция, безопасность ключей и ответов."
            ),
            instructions=FULLSTACK_DEVELOPER_INSTRUCTIONS,
        ),
        _subagent(
            name="qa-engineer",
            description=(
                "Чек-листы и тест-кейсы: Functional, UI/UX, Security (RLS, утечка "
                "правильных ответов), AI Edge Cases. Баги по шаблону."
            ),
            instructions=QA_ENGINEER_INSTRUCTIONS,
        ),
        _subagent(
            name="marketing-manager",
            description=(
                "Позиционирование B2B/B2C, заголовки 4U, структура лендинга, "
                "онбординг-письма, бюджетные гипотезы привлечения."
            ),
            instructions=MARKETING_MANAGER_INSTRUCTIONS,
        ),
        _subagent(
            name="sales-manager",
            description=(
                "Скрипты касаний (Telegram/LinkedIn/Email), квалификация SPIN/BANT, "
                "возражения, карточка обратной связи для PM."
            ),
            instructions=SALES_MANAGER_INSTRUCTIONS,
        ),
    ],
    subagent_policy=agents.SubagentPolicy(concurrent_child_turn_limit=6),
)


if __name__ == "__main__":
    import asyncio

    async def main() -> None:
        session = await agent.start_session()
        state = await session.run("Собери бэклог MVP и тест-план для фичи: загрузка регламента -> тест.")
        if isinstance(state, agents.Completed):
            print(state.text)
        await session.cancel()

    asyncio.run(main())