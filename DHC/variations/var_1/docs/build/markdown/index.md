---
generator: "Docutils 0.17.1: http://docutils.sourceforge.net/"
title: DHC/var_1 documentation
viewport:
- width=device-width, initial-scale=1.0
- width=device-width, initial-scale=0.9, maximum-scale=0.9
---

::: document
::: documentwrapper
::: bodywrapper
::: {.body role="main"}
::: {#welcome-to-dhc-var-1-s-documentation .section}
# Welcome to DHC/var_1's documentation![¶](#welcome-to-dhc-var-1-s-documentation "Permalink to this headline"){.headerlink}

::: {.toctree-wrapper .compound}
[]{#document-modules}

::: {#var-1 .section}
## var_1[¶](#var-1 "Permalink to this headline"){.headerlink}

::: {.toctree-wrapper .compound}
[]{#document-clean}

::: {#module-clean .section}
[]{#clean-module}

### clean module[¶](#module-clean "Permalink to this headline"){.headerlink}

initial_clean.py: Remove extra whitespaces, non-utf-8 characters and
carry out substitutions.

[[clean.]{.pre}]{.sig-prename .descclassname}[[clean]{.pre}]{.sig-name .descname}[(]{.sig-paren}*[[text]{.pre}]{.n}*, *[[\*\*]{.pre}]{.o}[[kwargs]{.pre}]{.n}*[)]{.sig-paren}[¶](#clean.clean "Permalink to this definition"){.headerlink}

:   Clean unwanted characters, extra whitespaces, unnecessary
    punctuations and sentence splits.

    text[str]{.classifier}

    :   Text to process.

    text[str]{.classifier}

    :   Processed text.

    Return type

    :   `str`{.xref .py .py-class .docutils .literal .notranslate}

```{=html}
<!-- -->
```

[[clean.]{.pre}]{.sig-prename .descclassname}[[main]{.pre}]{.sig-name .descname}[(]{.sig-paren}[)]{.sig-paren}[¶](#clean.main "Permalink to this definition"){.headerlink}

:   
:::

[]{#document-extract_statutes}

::: {#module-extract_statutes .section}
[]{#extract-statutes-module}

### extract_statutes module[¶](#module-extract_statutes "Permalink to this headline"){.headerlink}

extract_statutes.py: Extract statutes from documents.

[[extract_statutes.]{.pre}]{.sig-prename .descclassname}[[check_exists]{.pre}]{.sig-name .descname}[(]{.sig-paren}*[[actsec]{.pre}]{.n}*, *[[statutes]{.pre}]{.n}*[)]{.sig-paren}[¶](#extract_statutes.check_exists "Permalink to this definition"){.headerlink}

:   Return valid cited statutes.

    actsec[set]{.classifier}

    :   Set of statutes cited and their spans.

    statutues: dict

    :   Dictionary of statutes to reference.

    cleaned[set]{.classifier}

    :   Valid set of statutes and their spans.

    Return type

    :   `set`{.xref .py .py-class .docutils .literal .notranslate}

```{=html}
<!-- -->
```

[[extract_statutes.]{.pre}]{.sig-prename .descclassname}[[clean]{.pre}]{.sig-name .descname}[(]{.sig-paren}*[[act_sec]{.pre}]{.n}*[)]{.sig-paren}[¶](#extract_statutes.clean "Permalink to this definition"){.headerlink}

:   Clean up given set of extracted sections to standard format.

    actsec[set]{.classifier}

    :   Set containing statutes and their spans.

    actsec[set]{.classifier}

    :   Set containing formatted statutes and their spans.

    Return type

    :   `set`{.xref .py .py-class .docutils .literal .notranslate}

```{=html}
<!-- -->
```

[[extract_statutes.]{.pre}]{.sig-prename .descclassname}[[extract_statutes]{.pre}]{.sig-name .descname}[(]{.sig-paren}*[[text]{.pre}]{.n}*, *[[per_sentence]{.pre}]{.n}[[=]{.pre}]{.o}[[True]{.pre}]{.default_value}*[)]{.sig-paren}[¶](#extract_statutes.extract_statutes "Permalink to this definition"){.headerlink}

:   Finds all statutes mentioned in the given text.

    text[str or dict]{.classifier}

    :   Text to extract statutes from.

    per_sentence[bool, default]{.classifier}[True]{.classifier}

    :   Whether to find the statutes for each sentence. (Only works when
        a dictionary is passed to text.)

    secs[dict]{.classifier}

    :   Dictionary of cited statutes.

    Return type

    :   `dict`{.xref .py .py-class .docutils .literal .notranslate}

```{=html}
<!-- -->
```

[[extract_statutes.]{.pre}]{.sig-prename .descclassname}[[get_statutes]{.pre}]{.sig-name .descname}[(]{.sig-paren}*[[text]{.pre}]{.n}*, *[[actlist]{.pre}]{.n}*, *[[unit]{.pre}]{.n}*[)]{.sig-paren}[¶](#extract_statutes.get_statutes "Permalink to this definition"){.headerlink}

:   Find all statutes cited in text.

    text[str]{.classifier}

    :   Text to find statutes from.

    actlist[list]{.classifier}

    :   List of acts to use for reference.

    unit[str]{.classifier}

    :   Article or section.

    actsec[set]{.classifier}

    :   Set containing cited statutes and spans.

    Return type

    :   `set`{.xref .py .py-class .docutils .literal .notranslate}

```{=html}
<!-- -->
```

[[extract_statutes.]{.pre}]{.sig-prename .descclassname}[[main]{.pre}]{.sig-name .descname}[(]{.sig-paren}[)]{.sig-paren}[¶](#extract_statutes.main "Permalink to this definition"){.headerlink}

:   

```{=html}
<!-- -->
```

[[extract_statutes.]{.pre}]{.sig-prename .descclassname}[[sentence_align]{.pre}]{.sig-name .descname}[(]{.sig-paren}*[[sentence_dict]{.pre}]{.n}*, *[[orig]{.pre}]{.n}*[)]{.sig-paren}[¶](#extract_statutes.sentence_align "Permalink to this definition"){.headerlink}

:   Align citations to sentences.

    sentence_dict[dict]{.classifier}

    :   Dictionary of statute citations.

    orig[dict]{.classifier}

    :   Dictionary of sentences.

    orig[dict]{.classifier}

    :   Dictionary with sections given for each sentence.

    Return type

    :   `dict`{.xref .py .py-class .docutils .literal .notranslate}
:::

[]{#document-mask}

::: {#module-mask .section}
[]{#mask-module}

### mask module[¶](#module-mask "Permalink to this headline"){.headerlink}

mask.py: Mask various patterns for given data.

[[mask.]{.pre}]{.sig-prename .descclassname}[[main]{.pre}]{.sig-name .descname}[(]{.sig-paren}[)]{.sig-paren}[¶](#mask.main "Permalink to this definition"){.headerlink}

:   

```{=html}
<!-- -->
```

[[mask.]{.pre}]{.sig-prename .descclassname}[[mask]{.pre}]{.sig-name .descname}[(]{.sig-paren}*[[text]{.pre}]{.n}*, *[[patterns]{.pre}]{.n}*[)]{.sig-paren}[¶](#mask.mask "Permalink to this definition"){.headerlink}

:   Mask given patterns by given mask strings.

    text[str]{.classifier}

    :   Text to process.

    patterns[List\[Tuple\[str, Pattern, str\]\]]{.classifier}

    :   List of regex patterns and replacement tokens.

    text[str]{.classifier}

    :   Processed text.

    Return type

    :   `str`{.xref .py .py-class .docutils .literal .notranslate}
:::

[]{#document-process}

::: {#module-process .section}
[]{#process-module}

### process module[¶](#module-process "Permalink to this headline"){.headerlink}

script.py: Run all pre-processing scripts

[[process.]{.pre}]{.sig-prename .descclassname}[[main]{.pre}]{.sig-name .descname}[(]{.sig-paren}[)]{.sig-paren}[¶](#process.main "Permalink to this definition"){.headerlink}

:   
:::

[]{#document-segment}

::: {#module-segment .section}
[]{#segment-module}

### segment module[¶](#module-segment "Permalink to this headline"){.headerlink}

segment.py: Segments documents into sentences.

[[segment.]{.pre}]{.sig-prename .descclassname}[[custom_sentencizer]{.pre}]{.sig-name .descname}[(]{.sig-paren}*[[doc]{.pre}]{.n}*[)]{.sig-paren}[¶](#segment.custom_sentencizer "Permalink to this definition"){.headerlink}

:   Custom sentencizer to ignore brackets as sentence boundaries.

    doc[str]{.classifier}

    :   Text to process.

    doc[spacy.Doc]{.classifier}

    :   spacy document with sentence boundaries.

    Return type

    :   `object`{.xref .py .py-class .docutils .literal .notranslate}

```{=html}
<!-- -->
```

[[segment.]{.pre}]{.sig-prename .descclassname}[[fix_sentence_boundaries]{.pre}]{.sig-name .descname}[(]{.sig-paren}*[[sentence_dict]{.pre}]{.n}*[)]{.sig-paren}[¶](#segment.fix_sentence_boundaries "Permalink to this definition"){.headerlink}

:   Fix sentence boundaries to account for extra spaces ignored by
    spacy.

    sentence_dict: dict

    :   Dictionary containing sentence text and spans.

    sent_dict: dict

    :   Dictionary containing sentence texts and rectified spans.

    Return type

    :   `dict`{.xref .py .py-class .docutils .literal .notranslate}

```{=html}
<!-- -->
```

[[segment.]{.pre}]{.sig-prename .descclassname}[[main]{.pre}]{.sig-name .descname}[(]{.sig-paren}[)]{.sig-paren}[¶](#segment.main "Permalink to this definition"){.headerlink}

:   

```{=html}
<!-- -->
```

[[segment.]{.pre}]{.sig-prename .descclassname}[[segment]{.pre}]{.sig-name .descname}[(]{.sig-paren}*[[text]{.pre}]{.n}*, *[[nlp]{.pre}]{.n}*[)]{.sig-paren}[¶](#segment.segment "Permalink to this definition"){.headerlink}

:   Segment sentences by boundary.

    text[str]{.classifier}

    :   Text to process.

    nlp[spacy object(?)]{.classifier}

    :   Spacy object to use for segmentation.

    sent_dict[dict]{.classifier}

    :   Dictionary containing each sentence and their span.

    Return type

    :   `dict`{.xref .py .py-class .docutils .literal .notranslate}
:::

[]{#document-utils}

::: {#module-utils .section}
[]{#utils-module}

### utils module[¶](#module-utils "Permalink to this headline"){.headerlink}

utils.py: Utilities for processing

*[class]{.pre}[ ]{.w}*[[utils.]{.pre}]{.sig-prename .descclassname}[[DotDict]{.pre}]{.sig-name .descname}[¶](#utils.DotDict "Permalink to this definition"){.headerlink}

:   Bases: `dict`{.xref .py .py-class .docutils .literal .notranslate}

    dot.notation access to dictionary attributes

```{=html}
<!-- -->
```

[[utils.]{.pre}]{.sig-prename .descclassname}[[get_text]{.pre}]{.sig-name .descname}[(]{.sig-paren}*[[path]{.pre}]{.n}*[)]{.sig-paren}[¶](#utils.get_text "Permalink to this definition"){.headerlink}

:   Load html data and return text of the data.

    Return type

    :   `str`{.xref .py .py-class .docutils .literal .notranslate}

```{=html}
<!-- -->
```

[[utils.]{.pre}]{.sig-prename .descclassname}[[save_format]{.pre}]{.sig-name .descname}[(]{.sig-paren}*[[path]{.pre}]{.n}*, *[[flname]{.pre}]{.n}*, *[[data]{.pre}]{.n}*[)]{.sig-paren}[¶](#utils.save_format "Permalink to this definition"){.headerlink}

:   Saves data to the given path depending on the data type.

```{=html}
<!-- -->
```

[[utils.]{.pre}]{.sig-prename .descclassname}[[set_logger]{.pre}]{.sig-name .descname}[(]{.sig-paren}*[[log_path]{.pre}]{.n}*[)]{.sig-paren}[¶](#utils.set_logger "Permalink to this definition"){.headerlink}

:   Set logger to log information to the terminal and the specified
    path.

    log_path[str]{.classifier}

    :   Path to log run-stats to.
:::
:::
:::
:::
:::
:::
:::
:::

::: {.sphinxsidebar role="navigation" aria-label="main navigation"}
::: sphinxsidebarwrapper
# [DHC/var_1](#) {#dhcvar_1 .logo}

### Navigation

[Contents:]{.caption-text}

-   [var_1](index.html#document-modules){.reference .internal}

::: relations
### Related Topics

-   [Documentation overview](#)
:::
:::
:::

::: clearer
:::
:::

::: footer
©2022, Upal Bhattacharya. \| Powered by [Sphinx
4.3.2](http://sphinx-doc.org/) & [Alabaster
0.7.12](https://github.com/bitprophet/alabaster)
:::
