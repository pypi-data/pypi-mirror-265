from crewai_tools import (
    CodeDocsSearchTool, CSVSearchTool, DirectorySearchTool, DOCXSearchTool, DirectoryReadTool,
    FileReadTool, TXTSearchTool, JSONSearchTool, MDXSearchTool, PDFSearchTool, RagTool,
    ScrapeElementFromWebsiteTool, ScrapeWebsiteTool, WebsiteSearchTool, XMLSearchTool, YoutubeChannelSearchTool,
    YoutubeVideoSearchTool
)
from typing import Any
from autogen import register_function

def autogen_CodeDocsSearchTool(assistant, user_proxy):
    def register_code_docs_search_tool(tool_class, tool_name, tool_description, assistant, user_proxy):
        def tool_func(docs_url: str, search_query: str) -> Any:
            tool_instance = tool_class(docs_url=docs_url, search_query=search_query)
            return tool_instance.run()
        register_function(tool_func, caller=assistant, executor=user_proxy, name=tool_name, description=tool_description)
    register_code_docs_search_tool(CodeDocsSearchTool, "code_docs_search_tool", "Search a Code Docs content(search_query: 'string', docs_url: 'string') - A tool that can be used to semantic search a query from a Code Docs content.", assistant, user_proxy)

def autogen_CSVSearchTool(assistant, user_proxy):
    def register_csv_search_tool(tool_class, tool_name, tool_description, assistant, user_proxy):
        def tool_func(csv: str, search_query: str) -> Any:
            tool_instance = tool_class(csv=csv, search_query=search_query)
            return tool_instance.run()
        register_function(tool_func, caller=assistant, executor=user_proxy, name=tool_name, description=tool_description)
    register_csv_search_tool(CSVSearchTool, "csv_search_tool", "Search a CSV's content(search_query: 'string', csv: 'string') - A tool that can be used to semantic search a query from a CSV's content.", assistant, user_proxy)

def autogen_DirectorySearchTool(assistant, user_proxy):
    def register_directory_search_tool(tool_class, tool_name, tool_description, assistant, user_proxy):
        def tool_func(directory: str, search_query: str) -> Any:
            tool_instance = tool_class(directory=directory, search_query=search_query)
            return tool_instance.run()
        register_function(tool_func, caller=assistant, executor=user_proxy, name=tool_name, description=tool_description)
    register_directory_search_tool(DirectorySearchTool, "directory_search_tool", "Search a directory's content(search_query: 'string', directory: 'string') - A tool that can be used to semantic search a query from a directory's content.", assistant, user_proxy)

def autogen_DOCXSearchTool(assistant, user_proxy):
    def register_docx_search_tool(tool_class, tool_name, tool_description, assistant, user_proxy):
        def tool_func(docx: str, search_query: str) -> Any:
            tool_instance = tool_class(docx=docx, search_query=search_query)
            return tool_instance.run()
        register_function(tool_func, caller=assistant, executor=user_proxy, name=tool_name, description=tool_description)
    register_docx_search_tool(DOCXSearchTool, "docx_search_tool", "Search a DOCX's content(search_query: 'string', docx: 'string') - A tool that can be used to semantic search a query from a DOCX's content.", assistant, user_proxy)

# DirectoryReadTool
def autogen_DirectoryReadTool(assistant, user_proxy):
    def register_directory_read_tool(tool_class, tool_name, tool_description, assistant, user_proxy):
        def tool_func(directory: str) -> Any:
            tool_instance = tool_class(directory=directory)
            return tool_instance.run()
        register_function(tool_func, caller=assistant, executor=user_proxy, name=tool_name, description=tool_description)
    register_directory_read_tool(DirectoryReadTool, "directory_read_tool", "List files in directory(directory: 'string') - A tool that can be used to recursively list a directory's content.", assistant, user_proxy)

# FileReadTool
def autogen_FileReadTool(assistant, user_proxy):
    def register_file_read_tool(tool_class, tool_name, tool_description, assistant, user_proxy):
        def tool_func(file_path: str) -> Any:
            tool_instance = tool_class(file_path=file_path)
            return tool_instance.run()
        register_function(tool_func, caller=assistant, executor=user_proxy, name=tool_name, description=tool_description)
    register_file_read_tool(FileReadTool, "file_read_tool", "Read a file's content(file_path: 'string') - A tool that can be used to read a file's content.", assistant, user_proxy)

# TXTSearchTool
def autogen_TXTSearchTool(assistant, user_proxy):
    def register_txt_search_tool(tool_class, tool_name, tool_description, assistant, user_proxy):
        def tool_func(txt: str, search_query: str) -> Any:
            tool_instance = tool_class(txt=txt, search_query=search_query)
            return tool_instance.run()
        register_function(tool_func, caller=assistant, executor=user_proxy, name=tool_name, description=tool_description)
    register_txt_search_tool(TXTSearchTool, "txt_search_tool", "Search a txt's content(search_query: 'string', txt: 'string') - A tool that can be used to semantic search a query from a txt's content.", assistant, user_proxy)

def autogen_JSONSearchTool(assistant, user_proxy):
    def register_json_search_tool(tool_class, tool_name, tool_description, assistant, user_proxy):
        def tool_func(json_path: str, search_query: str) -> Any:
            tool_instance = tool_class(json_path=json_path, search_query=search_query)
            return tool_instance.run()
        register_function(tool_func, caller=assistant, executor=user_proxy, name=tool_name, description=tool_description)
    register_json_search_tool(JSONSearchTool, "json_search_tool", "Search a JSON's content(search_query: 'string', json_path: 'string') - A tool that can be used to semantic search a query from a JSON's content.", assistant, user_proxy)

def autogen_MDXSearchTool(assistant, user_proxy):
    def register_mdx_search_tool(tool_class, tool_name, tool_description, assistant, user_proxy):
        def tool_func(mdx: str, search_query: str) -> Any:
            tool_instance = tool_class(mdx=mdx, search_query=search_query)
            return tool_instance.run()
        register_function(tool_func, caller=assistant, executor=user_proxy, name=tool_name, description=tool_description)
    register_mdx_search_tool(MDXSearchTool, "mdx_search_tool", "Search a MDX's content(search_query: 'string', mdx: 'string') - A tool that can be used to semantic search a query from a MDX's content.", assistant, user_proxy)

def autogen_PDFSearchTool(assistant, user_proxy):
    def register_pdf_search_tool(tool_class, tool_name, tool_description, assistant, user_proxy):
        def tool_func(pdf: str, search_query: str) -> Any:
            tool_instance = tool_class(pdf=pdf, search_query=search_query)
            return tool_instance.run()
        register_function(tool_func, caller=assistant, executor=user_proxy, name=tool_name, description=tool_description)
    register_pdf_search_tool(PDFSearchTool, "pdf_search_tool", "Search a PDF's content(search_query: 'string', pdf: 'string') - A tool that can be used to semantic search a query from a PDF's content.", assistant, user_proxy)

def autogen_RagTool(assistant, user_proxy):
    def register_rag_tool(tool_class, tool_name, tool_description, assistant, user_proxy):
        def tool_func(query: str, data: Any) -> Any:
            tool_instance = tool_class(query=query, data=data)
            return tool_instance.run()
        register_function(tool_func, caller=assistant, executor=user_proxy, name=tool_name, description=tool_description)
    register_rag_tool(RagTool, "rag_tool", "Knowledge base(query: 'string', data: Any) - A knowledge base that can be used to answer questions.", assistant, user_proxy)

def autogen_ScrapeElementFromWebsiteTool(assistant, user_proxy):
    def register_scrape_element_from_website_tool(tool_class, tool_name, tool_description, assistant, user_proxy):
        def tool_func(website_url: str, element_query: str) -> Any:
            tool_instance = tool_class(website_url=website_url, element_query=element_query)
            return tool_instance.run()
        register_function(tool_func, caller=assistant, executor=user_proxy, name=tool_name, description=tool_description)
    register_scrape_element_from_website_tool(ScrapeElementFromWebsiteTool, "scrape_element_from_website_tool", "Scrape an element from a website(element_query: 'string', website_url: 'string') - A tool that can be used to scrape an element from a website.", assistant, user_proxy)

def autogen_ScrapeWebsiteTool(assistant, user_proxy):
    def register_scrape_website_tool(tool_class, tool_name, tool_description, assistant, user_proxy):
        def tool_func(website_url: str) -> Any:
            tool_instance = tool_class(website_url=website_url)
            return tool_instance.run()
        register_function(tool_func, caller=assistant, executor=user_proxy, name=tool_name, description=tool_description)
    register_scrape_website_tool(ScrapeWebsiteTool, "scrape_website_tool", "Read website content(website_url: 'string') - A tool that can be used to read content from a specified website.", assistant, user_proxy)

def autogen_WebsiteSearchTool(assistant, user_proxy):
    def register_website_search_tool(tool_class, tool_name, tool_description, assistant, user_proxy):
        def tool_func(website: str, search_query: str) -> Any:
            tool_instance = tool_class(website=website, search_query=search_query)
            return tool_instance.run()
        register_function(tool_func, caller=assistant, executor=user_proxy, name=tool_name, description=tool_description)
    register_website_search_tool(WebsiteSearchTool, "website_search_tool", "Search in a specific website(search_query: 'string', website: 'string') - A tool that can be used to semantic search a query from a specific URL content.", assistant, user_proxy)

def autogen_XMLSearchTool(assistant, user_proxy):
    def register_xml_search_tool(tool_class, tool_name, tool_description, assistant, user_proxy):
        def tool_func(xml: str, search_query: str) -> Any:
            tool_instance = tool_class(xml=xml, search_query=search_query)
            return tool_instance.run()
        register_function(tool_func, caller=assistant, executor=user_proxy, name=tool_name, description=tool_description)
    register_xml_search_tool(XMLSearchTool, "xml_search_tool", "Search a XML's content(search_query: 'string', xml: 'string') - A tool that can be used to semantic search a query from a XML's content.", assistant, user_proxy)

def autogen_YoutubeChannelSearchTool(assistant, user_proxy):
    def register_youtube_channel_search_tool(tool_class, tool_name, tool_description, assistant, user_proxy):
        def tool_func(youtube_channel_handle: str, search_query: str) -> Any:
            tool_instance = tool_class(youtube_channel_handle=youtube_channel_handle, search_query=search_query)
            return tool_instance.run()
        register_function(tool_func, caller=assistant, executor=user_proxy, name=tool_name, description=tool_description)
    register_youtube_channel_search_tool(YoutubeChannelSearchTool, "youtube_channel_search_tool", "Search a Youtube Channels content(search_query: 'string', youtube_channel_handle: 'string') - A tool that can be used to semantic search a query from a Youtube Channels content.", assistant, user_proxy)

def autogen_YoutubeVideoSearchTool(assistant, user_proxy):
    def register_youtube_video_search_tool(tool_class, tool_name, tool_description, assistant, user_proxy):
        def tool_func(youtube_video_url: str, search_query: str) -> Any:
            tool_instance = tool_class(youtube_video_url=youtube_video_url, search_query=search_query)
            return tool_instance.run()
        register_function(tool_func, caller=assistant, executor=user_proxy, name=tool_name, description=tool_description)
    register_youtube_video_search_tool(YoutubeVideoSearchTool, "youtube_video_search_tool", "Search a Youtube Video content(search_query: 'string', youtube_video_url: 'string') - A tool that can be used to semantic search a query from a Youtube Video content.", assistant, user_proxy)