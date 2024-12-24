from crewai import LLM, Agent, Task, Crew, Process
from pydantic import BaseModel

llm = LLM(model="deepseek/deepseek-chat",
          base_url='https://api.deepseek.com',
          # temperature=0,
          api_key='sk-a16ee52937d44fbdb4132f867bfc666c')


class StructuredOutput(BaseModel):
    string_source: str
    llm_config: dict

    @classmethod
    def run(cls,
            llm_config: dict,
            ):
        agent = Agent(
            role="Text Extraction Assistant",
            goal="You understand all the information in the text.",
            backstory="""You are a master at understanding the content of the text. For every question they ask, you can find 
            the corresponding information within the text.""",
            verbose=True,
            allow_delegation=False,
            llm=llm,
        )
        qa_task = Task(
            description="Answer the following questions about the user: {question}",
            expected_output="An answer to the question.",
            agent=agent,
        )

        task = Task(
            description="Extract the answer and, based on the user's question, extract the value that matches the "
                        "rules from the answer.Finally, convert the value to the corresponding type. If there are arithmetic "
                        "operations or units, please convert them to the smallest unit for output."
                        "question: {question}\n"
                        "answer: answer\n"
                        "rule: {rule}\n"
                        "value_type: int",
            expected_output="",
            agent=agent
        )

        crew = Crew(
            agents=[agent],
            tasks=[qa_task, task],
            verbose=True,
            process=Process.sequential,
            knowledge_sources=[string_source],
            # Enable knowledge by adding the sources here. You can also add more sources to the sources list.
        )

        result = crew.kickoff(inputs={"question": "Extract the revenue for revenue_forecast",
                                      "rule": "Extract the accurate value from the text."})
        print(result)
