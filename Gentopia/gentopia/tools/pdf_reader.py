from typing import AnyStr
from gentopia.tools.basetool import *
from gentopia.tools.utils.document_loaders.text_loader import TextLoader
from gentopia.tools.utils.vector_store import VectorstoreIndexCreator


class ParsePdf(BaseTool):
    name = "parse_pdf"
    description: str = ("parses a pdf and returns a page.."
                   "input a url to a pdf you found on the internet."
                   "if you want more pages, you can repeat calling the function to get next page."
                   )

    def _run(self, doc_path, query) -> AnyStr:
        loader = TextLoader(doc_path)
        vector_store = VectorstoreIndexCreator().from_loaders([loader])
        evidence = vector_store.similarity_search(query, k=1)[0].page_content
        return evidence

    async def _arun(self, *args: Any, **kwargs: Any) -> Any:
        raise NotImplementedError


if __name__ == "__main__":
    ans = ParsePdf()._run("http://broiler.astrometry.net/~kilian/The_Art_of_Computer_Programming%20-%20Vol%201.pdf")
    print("output")
    print(ans)
