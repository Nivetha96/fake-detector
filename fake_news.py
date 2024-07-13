from langchain_openai import ChatOpenAI
from langchain.utilities import GoogleSerperAPIWrapper
from langchain.agents import Tool
from langchain.tools import WikipediaQueryRun
from langchain.utilities import WikipediaAPIWrapper
from langchain.agents import initialize_agent
from langchain_community.document_loaders import YoutubeLoader
from langchain.chains.summarize import load_summarize_chain

class FakeNews:
    #Create singleton instance
    __agent = None
    def init():
        api_key = "sk-proj-dRY6fYGIgprgvvc3mPLUT3BlbkFJEHALR7S6wZ2176AmCDqg"
        llm = ChatOpenAI(api_key=api_key, temperature=0,model="gpt-4")

        wikipedia = WikipediaQueryRun(api_wrapper=WikipediaAPIWrapper())
        serper_api_key = "9c64996bddbef44a7f3727e4f708fa953d729285"
        google_search = GoogleSerperAPIWrapper(serper_api_key=serper_api_key, type='news', k=5)

        def summarize_text(docs):
            chain = load_summarize_chain(llm, chain_type="stuff")
            result = chain.invoke(docs)
            return result

        def get_transcript(url):
            loader = YoutubeLoader.from_youtube_url(
            url, add_video_info=True
            )
            docs = loader.load()
            if len(docs) == 0:
                return []
            else:
                return summarize_text(docs)

        tools = [
        Tool(
            name="Google Search",
            func=google_search.results,
            description="Useful to search in Google.",
        )
        ]
        tools.append(
            Tool(
                name="Wikipedia",
                func=wikipedia.run,
                description="Useful to search in Wikipedia.",
            )
            )
        tools.append(
            Tool(
                name="Youtube Transcript",
                func=get_transcript,
                description="Useful to get transcript from Youtube.",
            )
            )

        agent = initialize_agent(
        tools, llm, agent="zero-shot-react-description", verbose=True,
        handle_parsing_error=True
        )
        FakeNews.__agent = agent

    def get_information(query):
        if FakeNews.__agent is None:
            FakeNews.init()
        prompt = f"""Can you fact-check the following statement?
        {query}
        Please provide a TRUE or FALSE response. Provide reference urls if possible. Provide a TRUE response only if its verifiable from trusted sources otherwise provide a FALSE response.
        """
        return FakeNews.__agent.run(prompt)