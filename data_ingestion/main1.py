# from .config.rss_sources import RSS_SOURCES
from .config.vc_sources import VC_BLOG_SOURCES
# from .config.pdf_sources import PDF_SOURCES

# from .pipelines.ingest_rss import ingest_rss_feed
from .pipelines.ingest_vc_blogs import ingest_vc_blog
# from .pipelines.ingest_pdfs import ingest_pdf


# RSS ingestion
# for name, url in RSS_SOURCES.items():
#     ingest_rss_feed(name, url)

# VC blogs ingestion
for name, url in VC_BLOG_SOURCES.items():
    ingest_vc_blog(name, url)

# PDF ingestion
# for name, url in PDF_SOURCES.items():
#     ingest_pdf(name, url)