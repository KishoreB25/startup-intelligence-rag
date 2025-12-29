# from data_ingestion.config.rss_sources import RSS_SOURCES
from data_ingestion.config.pdf_sources import PDF_SOURCES
# from data_ingestion.config.vc_sources import VC_BLOG_SOURCES

# from data_ingestion.pipelines.ingest_rss import ingest_rss_feed
from data_ingestion.pipelines.ingest_pdfs import ingest_pdf
# from data_ingestion.pipelines.ingest_vc_blogs import ingest_blog


# for name, url in RSS_SOURCES.items():
#     ingest_rss_feed(name, url)

for name, url in PDF_SOURCES.items():
    ingest_pdf(name, url)

# for name, url in VC_BLOG_SOURCES.items():
#     ingest_blog(name, url)
