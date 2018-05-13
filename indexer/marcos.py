from elasticsearch_dsl import analyzer

##TODO: add synonym token filter for query?
## maybe query should have two field? one is exact field (processed) and full_text field
html_strip = analyzer('html_strip',
    tokenizer="standard",
    filter=["standard", "lowercase", "stop", "snowball"],
    char_filter=["html_strip"]
)
