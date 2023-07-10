## Retrieval augmented generation

ask question about specific documents
`pip install langchain`

## PDF
`pip install pypdf` 

```python
from langchain.document_loaders import PyPDFLoader
loader = PyPDFLoader("path/to.pdf")
pages = loader.load()
page = pages[0]
page.page_content
page.metadata
```

## YouTube
`pip install yt_dlp`
`pip install pydub`

```python
from langchain.document_loaders.generic import GenericLoader
from langchain.document_loaders.parsers import OpenAIWhisperParser
from langchain.document_loaders.blob_loaders.youtube_audio import YoutubeAudioLoader
url = "https://www.youtub.com/watch?v=..."
save_dir = "docs/youtube"
loader = GenericLoader(
    YoutubeAudioLoader([url], save_dir),
    OpenAIWhisperParser()
)
docs = loader.load()
```

## URL

```python
from langchain.document_loaders import WebBaseLoader
loader = WebBaseLoader("https://github.com/")
docs = loader.load()
```

## Notion
Duplicate the page into your own Notion space and export as `Markdown` and `csv`.
Unzip it and save it below directory
```python
from langchain.document_loaders import NotionDirectoryLoader
loader = NotionDirectoryLoader("docs/NotionDB")
docs = loader.load()
```