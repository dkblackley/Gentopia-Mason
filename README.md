# Gentopia-Mason

**IMPORTANT NOTICE: This code repository was adapted from [Gentopia.AI](https://github.com/Gentopia-AI) to support Mason Activities.** 

Authors: Ziyu Yao (ziyuyao@gmu.edu) and Murong Yue (myue@gmu.edu)

Copyright and license should go to Gentopia.AI.

## My additions
All I added was a file for parsing pdfs (as requested in the HW, that agent is called pdf_search_scholar) and I also thought it'd be interesting to give an LLM access to headlines and search news articles. I initially trhought this would be different from what we already did, but upon achieving the news_scraper.py file, I found that it's not all that different from the scholar scraping, just with bore bs4 code. Regardless, you can access an LLM that has access to news and google search like so:

```
cd GentPool
python assemble news_agent
```

This uses playwright for scraping, so after you install requirements.txt make sure you alsorun `playwright install`!

Here's an example prompt and it's output:

```
User: I'm thinking of going down to Florida for a holiday, anything interesting going on?
news_agent:

Florida is currently recovering from Hurricane Milton:

    The hurricane has caused significant damage, with at least 16 people reported dead and over two million homes and businesses without power. Rescue workers are navigating floodwaters and debris, while many residents have returned to find their homes destroyed or badly flooded.

    Emergency management officials are urging residents and visitors to stay clear of affected areas to allow rescue and recovery teams to operate efficiently. Despite the devastation, there are also stories of hope, such as the birth of a baby girl in a Pinellas County hurricane shelter.

    The Florida National Guard has been activated, assisting in rescue operations, clearing routes, and removing debris. The American Athletic Conference has moved a football game from Tampa to Orlando due to the hurricane, and all University of South Florida campuses are closed until further notice.

    Disaster relief organizations like the Salvation Army are delivering emergency supplies to those in need. Some areas, like Sarasota, have reported less damage than initially feared.

Please note: This is a rapidly evolving situation, so monitoring the news for the latest updates is recommended.
```

Or if you just want some headlines:
```
User: Can you summarise the world wides news for me?

news_agent:

Here are some of the top headlines from around the world:

From BBC News:

    The UK government is appalled by Israel's attacks on UN bases in Lebanon.
    Florida residents are struggling with recovery after Hurricane Milton.
    Japanese atomic bomb survivors have won the Nobel Peace Prize.
    Canada is planning to cover the cost of contraception and diabetes drugs.
    A family has expressed relief after a 1924 climber’s foot was found on Everest.

From ABC News:

    There's an interview with Tim Walz.
    Studies suggest that Hurricane Milton's lasting impact on health is just beginning.
    Gas shortages caused by Hurricane Milton are expected to last a while.

From CNN:

    The Northern lights have been dazzling.
    A teenager has summited the world’s highest peaks.
    Obama’s remarks were directed at traditional Republicans and the male voters who form Trump’s base.
    Trump, on a lying spree, made at least 40 separate false claims in two Pennsylvania speeches.

From Fox News:

    A new poll shows where Trump, Harris stand in seven battleground states.
    Undecided Latino voters grilled VP Harris during a town hall.
    A donor has pulled his millions from his Ivy League alma mater.
    A tech titan has unveiled a self-driving car for the ‘glorious future’.
    Swing state's Democrats deliver a massive blow to Harris, say Trump offers better policies.
```


To use the pdf agent:

```
cd GentPool
python assemble.py pdf_search_scholar
```

Try something like:

```
User: Can you summarise David Wu's paper on SPIRAL? Check out the first couple pages as well
Response of pdf_search_scholar:

David Wu's paper titled "Spiral: Fast, High-Rate Single-Server PIR via FHE Composition" introduces a new family of single-server private information retrieval (PIR) protocols called SPIRAL, focusing on improving the efficiency of single-server PIR systems that allow a client to retrieve data without revealing which specific record is accessed.

Key Contributions:

    Lattice-Based Homomorphic Encryption: SPIRAL combines the Regev encryption scheme and the Gentry-Sahai-Waters encryption scheme, enabling new techniques for ciphertext translation and allowing trade-offs in communication and computation.
    Performance Improvements: The basic version of SPIRAL achieves:
        4.5× reduction in query size.
        1.5× increase in response size.
        2× increase in server throughput compared to previous systems like OnionPIR.
    Streaming Optimization: A variant optimized for streaming applications achieves a server throughput of 1.9 GB/s for databases with over a million records, greatly surpassing prior protocols.
    Cost Efficiency: For streaming large records, the estimated monetary cost of using SPIRAL is only 1.9× greater than directly downloading the desired record without privacy.

Technical Details:

    SPIRAL operates in two phases: an offline phase for generating public parameters and an online phase where the client sends queries and receives responses.
    The paper presents variants of SPIRAL optimized for different scenarios, discussing trade-offs in the process.

Limitations:

    SPIRAL requires larger public parameters compared to previous schemes, which may impact its practicality in some applications.

Overall: The SPIRAL protocol is a significant advancement in private information retrieval, enhancing efficiency and privacy for single-server systems using advanced encryption techniques.
```

## Installation 💻
First, clone this repository:
```
git clone git@github.com:LittleYUYU/Gentopia-Mason.git
cd Gentopia-Mason
```
Next, we will create a virtual environment and install the library:
```
conda create --name gentenv python=3.10
conda activate gentenv
pip install -r requirements.txt
```

Most of the agent construction and execution activities will happen within `GentPool`. For the `gentopia` library to be used within `GentPool`, set up the global environment:
```
export PYTHONPATH="$PWD/Gentopia:$PYTHONPATH"
```
In addition, since we will be using OpenAI's API, we also need to create a `.env` file under `GentPool` and put the API Key inside. The key will be registered as environmental variables at run time.
```
cd GentPool
touch .env
echo "OPENAI_API_KEY=<your_openai_api_key>" >> .env
```
Now you are all set! Let's create your first Gentopia Agent.


## Quick Start: Clone a Vanilla LLM Agent
GentPool has provided multiple template LLM agents. To get started, we will clone the "vanilla agent" from `GentPool/gentpool/pool/vanilla_template` with the following command:
```
./clone_agent vanilla_template <your_agent_name> 
```
This command will initiate an agent template under `./GentPool/gentpool/pool/<your_agent_name>`. The agent configuration can be found in `./GentPool/gentpool/pool/<your_agent_name>/agent.yaml` (note the agent type `vanilla`). The vanilla prompt it uses can be found in the source code of `Gentopia`; see `./Gentopia/gentopia/prompt/vanilla.py`.

You can now run your agent via:
```
python assemble.py <your_agent_name>
```
This vanilla agent simply sends the received user query to the backend LLM and returns its output. Therefore, for many complicated tasks, such as those requiring accessing the latest materials, it will fail. 

## Implement a Scholar LLM Agent with Tool Augmentation
In the second trial, we will create a Scholar agent which is augmented with multiple functions to access Google Scholar in real time.

This is based on the `scholar` agent we have created in the pool. As before, in this demo we simply clone it:
```
./clone_agent scholar <your_agent_name> 
```
Like before, this command created an agent under `./GentPool/gentpool/pool/<your_agent_name>`. Note from its configuration that scholar is an `openai`-type agent. As stated in its [Gentopia's implementation](./Gentopia/gentopia/agent/openai), this type of agent allows for function calling:
> OpenAIFunctionChatAgent class inherited from BaseAgent. Implementing OpenAI function call api as agent.

The available functions to the scholar agent have been listed in its configuration file `./GentPool/gentpool/pool/<your_agent_name>/agent.yaml`, and the implementation of these tools can be found in Gentopia's source code (mostly coming from the [google_scholar.py](./Gentopia/gentopia/tools/google_scholar.py) file, in this example).

Now, you are all set to query this scholar agent for the latest papers by certain authors, the summary of a certain paper, paper citations, etc.


## Remove an Agent
Sometimes an agent can upset you. To wipe it out completely,
```
./delete_agent <your_agent_name> 
```

