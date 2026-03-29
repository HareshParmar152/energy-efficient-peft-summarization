# 📚 DATASET DESCRIPTIONS - COMPLETE DOCUMENTATION

**Date**: March 12, 2026  
**Purpose**: Detailed descriptions of all 5 datasets used in research  
**Status**: Complete

---

## DATASET 1: CNN/DAILYMAIL

### Overview
The CNN/DailyMail dataset is a large-scale dataset for text summarization, consisting of news articles from CNN and Daily Mail websites paired with human-written summaries.

### Source
- **Origin**: CNN.com and DailyMail.co.uk news articles
- **Collection Period**: 2007-2015
- **Citation**: Hermann, K. M., et al. (2015). "Teaching Machines to Read and Comprehend." NIPS.

### Statistics
- **Training Set**: 287,113 article-summary pairs
- **Validation Set**: 13,368 pairs
- **Test Set**: 11,490 pairs
- **Total**: 311,971 pairs

### Characteristics
- **Domain**: News/Journalism
- **Language**: English
- **Average Source Length**: 600-800 tokens (766 tokens average)
- **Average Target Length**: 100-150 tokens (56 tokens average)
- **Compression Ratio**: ~13:1
- **Summary Type**: Abstractive (bullet points from article highlights)

### Text Properties
- **Style**: Formal news writing
- **Structure**: Well-organized articles with clear narrative
- **Vocabulary**: General news vocabulary, proper nouns, locations
- **Complexity**: Medium difficulty
- **Topics**: Politics, sports, entertainment, world news, business

### Example
**Source (truncated)**:
"(CNN) -- Usain Bolt rounded off the world championships Sunday by claiming his third gold in Moscow as he anchored Jamaica to victory in the men's 4x100m relay. The fastest man in the world charged clear of United States rival Justin Gatlin as the Jamaican quartet of Nesta Carter, Kemar Bailey-Cole, Nickel Ashmeade and Bolt won in 37.36 seconds..."

**Target Summary**:
"Usain Bolt wins third gold at Moscow world championships. Jamaica wins men's 4x100m relay in 37.36 seconds. Bolt anchors team to victory ahead of United States."

### Research Relevance
- **Why Used**: Standard benchmark for news summarization
- **Difficulty**: Medium - well-structured text, clear summaries
- **Best Model**: BART (0.5599 ROUGE-1)
- **Challenges**: Maintaining factual accuracy, handling proper nouns

---

## DATASET 2: PUBMED

### Overview
The PubMed dataset consists of biomedical research article abstracts paired with their conclusions, designed for scientific text summarization.

### Source
- **Origin**: PubMed Central (PMC) open-access articles
- **Collection Period**: Various years of publication
- **Citation**: Cohan, A., et al. (2018). "A Discourse-Aware Attention Model for Abstractive Summarization of Long Documents." NAACL.

### Statistics
- **Training Set**: 119,924 abstract-conclusion pairs
- **Validation Set**: 6,633 pairs
- **Test Set**: 6,658 pairs
- **Total**: 133,215 pairs

### Characteristics
- **Domain**: Scientific/Biomedical
- **Language**: English (technical/scientific)
- **Average Source Length**: 200-300 tokens (450 tokens average)
- **Average Target Length**: 100-150 tokens (203 tokens average)
- **Compression Ratio**: ~2.2:1
- **Summary Type**: Abstractive (conclusions from abstracts)

### Text Properties
- **Style**: Formal scientific writing
- **Structure**: Structured abstracts (Background, Methods, Results, Conclusions)
- **Vocabulary**: Technical medical/biological terminology
- **Complexity**: High difficulty (domain-specific knowledge required)
- **Topics**: Medicine, biology, genetics, clinical trials, pharmacology

### Example
**Source (truncated)**:
"BACKGROUND: Hepatocellular carcinoma (HCC) is one of the most common malignancies worldwide. MicroRNAs (miRNAs) have been reported to play important roles in HCC development and progression. METHODS: We performed miRNA microarray analysis to identify differentially expressed miRNAs in HCC tissues..."

**Target Summary**:
"Our study demonstrates that miR-122 is significantly downregulated in HCC and functions as a tumor suppressor by targeting ADAM17. These findings suggest miR-122 as a potential therapeutic target for HCC treatment."

### Research Relevance
- **Why Used**: Tests model performance on technical/scientific text
- **Difficulty**: High - requires understanding of medical terminology
- **Best Model**: BART Adapters (0.3035 ROUGE-1)
- **Challenges**: Technical vocabulary, complex sentence structures

---

## DATASET 3: XSUM

### Overview
The XSum (Extreme Summarization) dataset consists of BBC news articles paired with single-sentence summaries, representing extreme compression.

### Source
- **Origin**: BBC news articles
- **Collection Period**: 2010-2017
- **Citation**: Narayan, S., et al. (2018). "Don't Give Me the Details, Just the Summary!" EMNLP.

### Statistics
- **Training Set**: 204,045 article-summary pairs
- **Validation Set**: 11,332 pairs
- **Test Set**: 11,334 pairs
- **Total**: 226,711 pairs

### Characteristics
- **Domain**: News/Journalism
- **Language**: English
- **Average Source Length**: 300-400 tokens (431 tokens average)
- **Average Target Length**: 20-30 tokens (23 tokens average)
- **Compression Ratio**: ~19:1 (extreme compression)
- **Summary Type**: Abstractive (single sentence)

### Text Properties
- **Style**: Formal news writing (BBC style)
- **Structure**: News articles with inverted pyramid structure
- **Vocabulary**: General news vocabulary, British English
- **Complexity**: Very high difficulty (extreme compression required)
- **Topics**: UK and world news, politics, business, technology, health

### Example
**Source (truncated)**:
"The full cost of damage in Newton Stewart, one of the areas worst affected, is still being assessed. Repair work is ongoing in Hawick and many roads in Peeblesshire remain badly affected by standing water. Trains on the west coast mainline face disruption due to damage at the Lamington Viaduct..."

**Target Summary**:
"Clean-up operations are continuing across the Scottish Borders and Dumfries and Galloway after flooding caused by Storm Frank."

### Research Relevance
- **Why Used**: Tests extreme compression and abstraction capabilities
- **Difficulty**: Very high - requires significant abstraction
- **Best Model**: BART Adapters (0.3444 ROUGE-1)
- **Challenges**: Extreme compression, maintaining key information

---

## DATASET 4: SAMSUM

### Overview
The SAMSum dataset consists of messenger-like conversations paired with human-written summaries, designed for dialogue summarization.

### Source
- **Origin**: Linguists created conversations similar to messenger chats
- **Collection Period**: 2018-2019
- **Citation**: Gliwa, B., et al. (2019). "SAMSum Corpus: A Human-annotated Dialogue Dataset for Abstractive Summarization." EMNLP Workshop.

### Statistics
- **Training Set**: 14,732 conversation-summary pairs
- **Validation Set**: 818 pairs
- **Test Set**: 819 pairs
- **Total**: 16,369 pairs

### Characteristics
- **Domain**: Conversational/Dialogue
- **Language**: English (informal)
- **Average Source Length**: 400-600 tokens (94 tokens average)
- **Average Target Length**: 50-100 tokens (23 tokens average)
- **Compression Ratio**: ~4:1
- **Summary Type**: Abstractive (narrative summaries of conversations)

### Text Properties
- **Style**: Informal conversational text
- **Structure**: Multi-turn dialogues with 2-6 participants
- **Vocabulary**: Casual language, slang, abbreviations, emojis
- **Complexity**: Medium difficulty (understanding context and relationships)
- **Topics**: Everyday conversations (plans, gossip, arrangements, discussions)

### Example
**Source**:
```
Hannah: Hey, do you have Betty's number?
Amanda: Lemme check
Hannah: <file_gif>
Amanda: Sorry, can't find it.
Amanda: Ask Larry
Amanda: He called her last time we were at the park together
Hannah: I don't know him well
Hannah: <file_gif>
Amanda: Don't be shy, he's very nice
Hannah: If you say so..
Hannah: I'd rather you texted him
Amanda: Just text him 🙂
Hannah: Urgh.. Alright
Hannah: Bye
Amanda: Bye bye
```

**Target Summary**:
"Hannah needs Betty's number but Amanda doesn't have it. She needs to contact Larry."

### Research Relevance
- **Why Used**: Tests model performance on informal, conversational text
- **Difficulty**: Medium - requires understanding dialogue context
- **Best Model**: T5 LoRA (0.4555 ROUGE-1) - HIGHEST OVERALL!
- **Challenges**: Informal language, multiple speakers, context understanding

---

## DATASET 5: BILLSUM

### Overview
The BillSum dataset consists of US Congressional and California state bills paired with human-written summaries, designed for long-document legal text summarization.

### Source
- **Origin**: US Congressional bills and California state bills
- **Collection Period**: 1993-2018 (US), 2015-2018 (CA)
- **Citation**: Kornilova, A., & Eidelman, V. (2019). "BillSum: A Corpus for Automatic Summarization of US Legislation." EMNLP Workshop.

### Statistics
- **Training Set**: 18,949 bill-summary pairs
- **Validation Set**: 1,237 pairs
- **Test Set**: 1,237 pairs
- **Total**: 21,423 pairs

### Characteristics
- **Domain**: Legal/Legislative
- **Language**: English (legal/formal)
- **Average Source Length**: 1000-1500 tokens (1,813 tokens average)
- **Average Target Length**: 100-200 tokens (206 tokens average)
- **Compression Ratio**: ~9:1
- **Summary Type**: Abstractive (official bill summaries)

### Text Properties
- **Style**: Formal legal language
- **Structure**: Structured legal documents with sections and subsections
- **Vocabulary**: Legal terminology, formal language, citations
- **Complexity**: Very high difficulty (long documents, legal language)
- **Topics**: Legislation (healthcare, education, defense, taxation, etc.)

### Example
**Source (truncated)**:
"SECTION 1. SHORT TITLE. This Act may be cited as the 'Protecting Consumers from Unreasonable Credit Rates Act of 2009'. SEC. 2. FINDINGS. Congress finds the following: (1) Short-term, small dollar lending is a growing industry in the United States..."

**Target Summary**:
"Protecting Consumers from Unreasonable Credit Rates Act of 2009 - Amends the Truth in Lending Act to prohibit a creditor from extending credit to a consumer in the form of a payday loan with an annual percentage rate that exceeds 36%."

### Research Relevance
- **Why Used**: Tests model performance on long documents and legal text
- **Difficulty**: Very high - long documents, legal terminology
- **Best Model**: T5 Adapters (0.4608 ROUGE-1)
- **Challenges**: Long sequences (>1024 tokens), legal language, maintaining accuracy

---

## COMPARATIVE ANALYSIS

### Dataset Difficulty Ranking (by ROUGE-1 scores)
1. **BillSum**: 0.4608 (Easiest - structured legal text)
2. **SAMSum**: 0.4555 (Medium - conversational)
3. **CNN/DailyMail**: 0.5599 (Easy - well-structured news)
4. **XSum**: 0.3444 (Hard - extreme compression)
5. **PubMed**: 0.3035 (Hardest - technical content)

### Dataset Characteristics Summary

| Dataset | Domain | Avg Tokens | Compression | Difficulty | Best Model |
|---------|--------|-----------|-------------|------------|------------|
| CNN/DailyMail | News | 766→56 | 13:1 | Medium | BART |
| PubMed | Scientific | 450→203 | 2.2:1 | High | BART |
| XSum | News | 431→23 | 19:1 | Very High | BART |
| SAMSum | Dialogue | 94→23 | 4:1 | Medium | T5 |
| BillSum | Legal | 1813→206 | 9:1 | Very High | T5 |

### Why These Datasets?

**Diversity**: 
- 5 different domains (news, scientific, dialogue, legal)
- 3 text lengths (short, medium, long)
- 3 styles (formal, informal, technical)

**Benchmarking**:
- All are standard benchmarks in summarization research
- Enable comparison with prior work
- Cover diverse real-world applications

**Challenges**:
- Test different model capabilities
- Evaluate generalization across domains
- Assess handling of different text types

---

## DATA AVAILABILITY

### Access
- **CNN/DailyMail**: Hugging Face Datasets (`cnn_dailymail`)
- **PubMed**: Hugging Face Datasets (`scientific_papers`)
- **XSum**: Hugging Face Datasets (`xsum`)
- **SAMSum**: Hugging Face Datasets (`samsum`)
- **BillSum**: Hugging Face Datasets (`billsum`)

### Licenses
- **CNN/DailyMail**: Apache 2.0
- **PubMed**: Public Domain (US Government)
- **XSum**: MIT License
- **SAMSum**: CC BY-NC-ND 4.0
- **BillSum**: Public Domain (US Government)

### Preprocessing
All datasets were preprocessed using:
- Tokenization: Model-specific tokenizers (BART, T5, GPT-2)
- Max source length: 1024 tokens (512 for XSum)
- Max target length: 256 tokens (128 for XSum)
- Truncation: Enabled
- Padding: Dynamic padding

---

**Status**: Complete ✅  
**Date**: March 12, 2026  
**Ready for**: Research paper submission

