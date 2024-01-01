from typing import Optional
from pydantic import Field
from langchain.callbacks.manager import CallbackManagerForToolRun
from langchain.tools.base import BaseTool
from langchain.utilities.pubmed import PubMedAPIWrapper


# class PubmedQueryRun(BaseTool):
#     """Tool that searches the PubMed API."""

#     name = "PubMed"
#     description = (
#         "A wrapper around PubMed. "
#         "Useful for when you need to answer questions about medicine, health, "
#         "and biomedical topics "
#         "from biomedical literature, MEDLINE, life science journals, and online books. "
#         "Input should be a search query."
#     )
#     api_wrapper: PubMedAPIWrapper = Field(default_factory=PubMedAPIWrapper)

#     def _run(
#         self,
#         query: str,
#         run_manager: Optional[CallbackManagerForToolRun] = None,
#     ) -> str:
#         """Use the PubMed tool."""
#         return self.api_wrapper.run(query)


def pubmed_query_run(query: str, run_manager: Optional[CallbackManagerForToolRun] = None) -> str:
    """Tool that searches the PubMed API."""
    from langchain.utilities.pubmed import PubMedAPIWrapper

    api_wrapper = PubMedAPIWrapper()
    return api_wrapper.run(query)
    

# 测试代码
if __name__ == "__main__":
    query = "apple"
    result = pubmed_query_run(query)
    print(result)
