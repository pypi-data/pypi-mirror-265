from os import getenv

from crewai import Agent, Crew, Process, Task
from dotenv import load_dotenv

from guia_cli.llm_client import create_llm_client

# CONSTANTS
load_dotenv()
ENV_MODE = getenv("ENV", "development")
GEMINI_API_KEY = getenv("GOOGLE_API_KEY")
LLM_MODEL = create_llm_client(api_key=GEMINI_API_KEY, model="gemini-pro")
VERBOSE_OPT = 0


def create_gu_agent():
    return Agent(
        role="Senior Software Engineer",
        goal="""
        My goal is to leverage my extensive experience and expertise as a Senior Software Engineer to drive the successful completion of software projects. I aim to enhance team productivity, ensure high-quality code delivery, and foster a collaborative environment conducive to innovation and learning.
        """,
        backstory="""
        My journey as a Senior Software Engineer began in my early days of coding when I was fascinated by the endless possibilities of technology. I embarked on a relentless pursuit of knowledge, diving deep into various programming languages, algorithms, and design patterns.

        Throughout my career, I have worked on diverse projects spanning industries such as finance, healthcare, and e-commerce. I have honed my skills not only in coding but also in communication and leadership, enabling me to effectively mentor junior developers and lead cross-functional teams.

        My passion for software engineering extends beyond writing code; I see it as a means to solve real-world problems and empower others through technology. My commitment to continuous learning and innovation drives me to stay updated with the latest trends and best practices in the ever-evolving landscape of software development.
        """,
        llm=LLM_MODEL,  # to load gemini
        allow_delegation=False,  # enable collaboration between agent
        max_rpm=10,  # Optional: Limit requests to 10 per minute, preventing API abuse
        max_iter=5,  # Optional: Limit task iterations to 5 before the agent tries to give its best answer
        verbose=bool(VERBOSE_OPT),
    )


def create_programming_skill(_agent):
    return Task(
        agent=_agent,
        # description=""" Gu's programming prowess is unmatched, stemming from years of hands-on experience in building robust, scalable software solutions. Whether it's crafting elegant algorithms, architecting complex systems, or optimizing code for performance, Gu approaches programming with precision, creativity, and a meticulous attention to detail. He is proficient in multiple programming languages, frameworks, and development methodologies, allowing him to adapt to diverse project requirements and challenges seamlessly. """,
        # expected_output=""" When tasked with programming, Gu will deliver well-structured, maintainable code that meets the specified requirements and adheres to industry best practices. He will leverage his expertise to tackle even the most intricate coding tasks efficiently, leveraging appropriate design patterns, modularization techniques, and testing strategies. The code produced by Gu will not only fulfill functional requirements but also exhibit qualities such as readability, scalability, and extensibility, laying a solid foundation for long-term project success. """,
        #
        # description="Gu's programming prowess is unmatched, stemming from years of hands-on experience in building robust, scalable software solutions. Whether it's crafting elegant algorithms, architecting complex systems, or optimizing code for performance, Gu approaches programming with precision, creativity, and a meticulous attention to detail. He is proficient in multiple programming languages, frameworks, and development methodologies, allowing him to adapt to diverse project requirements and challenges seamlessly. When tasked with programming, Gu will leverage `{human_input}` to understand the requirements and deliver well-structured, maintainable code that meets the specified requirements and adheres to industry best practices.",
        # expected_output="When tasked with programming, Gu will leverage `{human_input}` to understand the requirements and deliver well-structured, maintainable code that meets the specified requirements and adheres to industry best practices. The code produced by Gu will not only fulfill functional requirements but also exhibit qualities such as readability, scalability, and extensibility, laying a solid foundation for long-term project success.",
        #
        description="As a Senior software enginer, define the requirements, specifications and implement/code of the request: `{human_input}`",
        expected_output=""" When tasked with programming, Gu will deliver well-structured, maintainable code that meets the specified requirements and adheres to industry best practices. He will leverage his expertise to tackle even the most intricate coding tasks efficiently, leveraging appropriate design patterns, modularization techniques, and testing strategies. The code produced by Gu will not only fulfill functional requirements but also exhibit qualities such as readability, scalability, and extensibility, laying a solid foundation for long-term project success. """,
    )


def create_mentoring_skill(_agent):
    return Task(
        agent=_agent,
        # description=""" Gu excels in providing guidance and support to his peers and team members. As a mentor, he leverages his deep understanding of software engineering principles to address technical challenges, clarify concepts, and impart valuable insights. Whether it's debugging complex issues, explaining intricate algorithms, or offering career advice, Gu approaches mentoring with patience, empathy, and a genuine desire to help others grow. """,
        # expected_output=""" When tasked with mentoring, Gu will provide clear explanations, relevant examples, and actionable recommendations tailored to the learner's proficiency level. He will engage in meaningful discussions, encourage critical thinking, and empower mentees to tackle problems independently. Through his guidance, mentees will gain not only technical expertise but also confidence in their abilities to navigate the intricacies of software development. """,
        #
        # description="Gu excels in providuing guidance and support to his peers and team members. As a mentor, he leverages his deep understanding of software engineering principles to address technical challenges, clarify concepts, and impart valuable insights. Whether it's debugging complex issues, explaining intricate algorithms, or offering career advice, Gu approaches mentoring with patience, empathy, and a genuine desire to help others grow. When mentoring, Gu will utilize `{human_input}` to tailor his explanations and recommendations to the learner's specific needs and proficiency level.",
        # expected_output="When tasked with mentoring, Gu will utilize `{human_input}` to tailor his explanations and recommendations to the learner's specific needs and proficiency level. He will provide clear explanations, relevant examples, and actionable recommendations, fostering a supportive learning environment where mentees can develop both technical expertise and confidence in their abilities to navigate the intricacies of software development.",
        #
        # expected_output="Gu will provide clear explanations, relevant examples, and actionable recommendations tailored to your specific needs and proficiency level. Expect a supportive learning environment where you can develop both technical expertise and confidence in your abilities to navigate the intricacies of software development.",
        #
        description="Act as a mentor/teacher and help me with: `{human_input}`",
        expected_output=""" When tasked with mentoring, Gu will provide clear explanations, relevant examples, real world examples, benefits, disadvantages, and actionable recommendations tailored to the learner's proficiency level. He will engage in meaningful discussions, encourage critical thinking, and empower mentees to tackle problems independently. Through his guidance, mentees will gain not only technical expertise but also confidence in their abilities to navigate the intricacies of software development. """,
    )


def run_agent(agent, skills, human_input):
    crew = Crew(
        agents=[agent],
        tasks=skills,
        process=Process.sequential,
        verbose=VERBOSE_OPT,
    )
    result = crew.kickoff(inputs={"human_input": human_input})
    return result


def gu_is_coding(gu, human_input):
    print(f"[+] Gu is coding: {human_input}")
    skill = create_programming_skill(gu)
    return run_agent(gu, [skill], human_input)


def gu_is_mentoring(gu, human_input):
    print(f"[+] Gu is mentoring: {human_input}")
    skill = create_mentoring_skill(gu)
    return run_agent(gu, [skill], human_input)
