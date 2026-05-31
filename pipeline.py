from agents import build_reader_agent , build_search_agent,critic_chain,writer_chain

def run_research_pipeline(topic:str)->dict:
    state={}
    #search_agent working
    print("\n"+"="*50)
    print("step1 - search working....")
    print("="*50)
    search_agent=build_search_agent()
    search_result=search_agent.invoke({
        "messages":[('user',f"Find recent, reliable and detailed information about: {topic}")]
    })
    state['search_results']=search_result['messages'][-1].content 
    print("\n search results",state['search_results'])

    #reader agent 

    print("\n"+"="*50)
    print("step 2 - reader agent scraping....")
    print("="*50)

    reader_agent=build_reader_agent()
    reader_result = reader_agent.invoke({
        "messages": [("user",
            f"Based on the following search results about '{topic}', "
            f"pick the most relevant URL and scrape it for deeper content.\n\n"
            f"Search Results:\n{state['search_results'][:800]}"
        )]
    })

    state['scraped_content']=reader_result['messages'][-1].content

    print('\n scraped content :\n',state["scraped_content"])

    #step 3-writer chain

    print("\n"+"="*50)
    print("step 3- writer drafting a report ...")
    print("="*50)
    
    research_combined=(
        f'SEARCH RESULT :\n {state["search_results"]}\n \n'
        f"SCRAPED RESUlT : \n{state['scraped_content']}"

    )

    state['report']=writer_chain.invoke({
        "topic":topic,
        "research":research_combined
    })

    print('\n FINAl REPORT \n',state['report'])

    #critic report
    print("\n"+"="*50)
    print("step 4 - critic report....")
    print("="*50)

    state['feedback']=critic_chain.invoke({
        "report":state['report']
    })

    print('\n CRITIC REPORT \n',state['feedback'])
    
    return state

if __name__=="__main__":
    topic=input("\n Enter research topic")
    run_research_pipeline(topic)
