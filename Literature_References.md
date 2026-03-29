# 📖 LITERATURE REFERENCES - COMPLETE BIBLIOGRAPHY

**Date**: March 12, 2026  
**Purpose**: Complete list of papers to cite in research  
**Status**: Ready for compilation into PDF

---

## PEFT METHODS (Core Papers)

### 1. LoRA: Low-Rank Adaptation
**Citation**: Hu, E. J., Shen, Y., Wallis, P., Allen-Zhu, Z., Li, Y., Wang, S., Wang, L., & Chen, W. (2021). LoRA: Low-Rank Adaptation of Large Language Models. *arXiv preprint arXiv:2106.09685*.

**Key Points**:
- Introduces low-rank decomposition for efficient fine-tuning
- Reduces trainable parameters by 10,000x
- Maintains or improves performance
- **Relevance**: Core method evaluated in this research

---

### 2. QLoRA: Quantized LoRA
**Citation**: Dettmers, T., Pagnoni, A., Holtzman, A., & Zettlemoyer, L. (2023). QLoRA: Efficient Finetuning of Quantized LLMs. *arXiv preprint arXiv:2305.14314*.

**Key Points**:
- Combines 4-bit quantization with LoRA
- Enables fine-tuning on single GPU
- Reduces memory requirements significantly
- **Relevance**: Core method evaluated in this research

---

### 3. Adapters: Parameter-Efficient Transfer Learning
**Citation**: Houlsby, N., Giurgiu, A., Jastrzebski, S., Morrone, B., De Laroussilhe, Q., Gesmundo, A., Attariyan, M., & Gelly, S. (2019). Parameter-Efficient Transfer Learning for NLP. *In International Conference on Machine Learning* (pp. 2790-2799). PMLR.

**Key Points**:
- Introduces adapter modules for transfer learning
- Adds small trainable layers between frozen layers
- Achieves competitive performance with few parameters
- **Relevance**: Core method evaluated in this research

---

## TRANSFORMER MODELS

### 4. BART: Denoising Sequence-to-Sequence Pre-training
**Citation**: Lewis, M., Liu, Y., Goyal, N., Ghazvininejad, M., Mohamed, A., Levy, O., Stoyanov, V., & Zettlemoyer, L. (2019). BART: Denoising Sequence-to-Sequence Pre-training for Natural Language Generation, Translation, and Comprehension. *arXiv preprint arXiv:1910.13461*.

**Key Points**:
- Encoder-decoder architecture
- Pre-trained with denoising objective
- Excellent for text generation tasks
- **Relevance**: Best model for news summarization (0.5599 ROUGE-1)

---

### 5. T5: Text-to-Text Transfer Transformer
**Citation**: Raffel, C., Shazeer, N., Roberts, A., Lee, K., Narang, S., Matena, M., Zhou, Y., Li, W., & Liu, P. J. (2019). Exploring the Limits of Transfer Learning with a Unified Text-to-Text Transformer. *arXiv preprint arXiv:1910.10683*.

**Key Points**:
- Unified text-to-text framework
- Pre-trained on C4 corpus
- Versatile for multiple NLP tasks
- **Relevance**: Best model for structured tasks (SAMSum, BillSum)

---

### 6. GPT-2: Language Models are Unsupervised Multitask Learners
**Citation**: Radford, A., Wu, J., Child, R., Luan, D., Amodei, D., & Sutskever, I. (2019). Language Models are Unsupervised Multitask Learners. *OpenAI blog*, 1(8), 9.

**Key Points**:
- Decoder-only transformer architecture
- Pre-trained on WebText corpus
- Strong language modeling capabilities
- **Relevance**: Evaluated but unsuitable for summarization

---

### 7. TinyLlama (Used for CNN/DailyMail)
**Citation**: Zhang, P., Zeng, G., Wang, T., & Lu, W. (2024). TinyLlama: An Open-Source Small Language Model. *arXiv preprint arXiv:2401.02385*.

**Key Points**:
- Compact 1.1B parameter model
- Llama architecture
- Efficient for resource-constrained environments
- **Relevance**: Used for CNN/DailyMail experiments

---

## DATASETS

### 8. CNN/DailyMail Dataset
**Citation**: Hermann, K. M., Kocisky, T., Grefenstette, E., Espeholt, L., Kay, W., Suleyman, M., & Blunsom, P. (2015). Teaching Machines to Read and Comprehend. *In Advances in Neural Information Processing Systems* (pp. 1693-1701).

**Key Points**:
- Large-scale news summarization dataset
- 311,971 article-summary pairs
- Standard benchmark for summarization
- **Relevance**: Achieved highest scores (0.5599 ROUGE-1)

---

### 9. PubMed Dataset
**Citation**: Cohan, A., Dernoncourt, F., Kim, D. S., Bui, T., Kim, S., Chang, W., & Goharian, N. (2018). A Discourse-Aware Attention Model for Abstractive Summarization of Long Documents. *In Proceedings of the 2018 Conference of the North American Chapter of the Association for Computational Linguistics: Human Language Technologies* (pp. 615-621).

**Key Points**:
- Scientific paper summarization
- 133,215 abstract-conclusion pairs
- Tests technical domain understanding
- **Relevance**: Tests model on scientific text

---

### 10. XSum Dataset
**Citation**: Narayan, S., Cohen, S. B., & Lapata, M. (2018). Don't Give Me the Details, Just the Summary! Topic-Aware Convolutional Neural Networks for Extreme Summarization. *In Proceedings of the 2018 Conference on Empirical Methods in Natural Language Processing* (pp. 1797-1807).

**Key Points**:
- Extreme summarization (single sentence)
- 226,711 BBC news articles
- Tests extreme compression capability
- **Relevance**: Tests abstraction capabilities

---

### 11. SAMSum Dataset
**Citation**: Gliwa, B., Mochol, I., Biesek, M., & Wawer, A. (2019). SAMSum Corpus: A Human-annotated Dialogue Dataset for Abstractive Summarization. *In Proceedings of the 2nd Workshop on New Frontiers in Summarization* (pp. 70-79).

**Key Points**:
- Dialogue summarization dataset
- 16,369 conversation-summary pairs
- Tests conversational understanding
- **Relevance**: Achieved highest T5 scores (0.4555 ROUGE-1)

---

### 12. BillSum Dataset
**Citation**: Kornilova, A., & Eidelman, V. (2019). BillSum: A Corpus for Automatic Summarization of US Legislation. *In Proceedings of the 2nd Workshop on New Frontiers in Summarization* (pp. 48-56).

**Key Points**:
- Legal document summarization
- 21,423 US Congressional bills
- Tests long-document processing
- **Relevance**: Tests model on legal text

---

## EVALUATION METRICS

### 13. ROUGE: Recall-Oriented Understudy for Gisting Evaluation
**Citation**: Lin, C. Y. (2004). ROUGE: A Package for Automatic Evaluation of Summaries. *In Text Summarization Branches Out* (pp. 74-81).

**Key Points**:
- Standard metric for summarization evaluation
- Measures n-gram overlap with reference summaries
- ROUGE-1, ROUGE-2, ROUGE-L variants
- **Relevance**: Primary evaluation metric used

---

## RELATED WORK - PEFT

### 14. Prefix Tuning
**Citation**: Li, X. L., & Liang, P. (2021). Prefix-Tuning: Optimizing Continuous Prompts for Generation. *In Proceedings of the 59th Annual Meeting of the Association for Computational Linguistics* (pp. 4582-4597).

**Key Points**:
- Prepends trainable prefix vectors
- Alternative PEFT approach
- Competitive with fine-tuning
- **Relevance**: Related PEFT method

---

### 15. Prompt Tuning
**Citation**: Lester, B., Al-Rfou, R., & Constant, N. (2021). The Power of Scale for Parameter-Efficient Prompt Tuning. *In Proceedings of the 2021 Conference on Empirical Methods in Natural Language Processing* (pp. 3045-3059).

**Key Points**:
- Learns soft prompts for tasks
- Scales well with model size
- Simple and effective
- **Relevance**: Related PEFT method

---

### 16. BitFit: Simple Parameter-efficient Fine-tuning
**Citation**: Ben Zaken, E., Ravfogel, S., & Goldberg, Y. (2022). BitFit: Simple Parameter-efficient Fine-tuning for Transformer-based Masked Language-models. *In Proceedings of the 60th Annual Meeting of the Association for Computational Linguistics* (pp. 1-9).

**Key Points**:
- Fine-tunes only bias terms
- Extremely parameter-efficient
- Competitive performance
- **Relevance**: Related PEFT method

---

## RELATED WORK - SUMMARIZATION

### 17. Abstractive Summarization Survey
**Citation**: Shi, T., Keneshloo, Y., Ramakrishnan, N., & Reddy, C. K. (2021). Neural Abstractive Text Summarization with Sequence-to-Sequence Models: A Survey. *ACM Computing Surveys (CSUR)*, 54(2), 1-39.

**Key Points**:
- Comprehensive survey of neural summarization
- Covers seq2seq models and transformers
- Discusses evaluation metrics
- **Relevance**: Background on summarization

---

### 18. Pre-trained Models for Summarization
**Citation**: Zhang, J., Zhao, Y., Saleh, M., & Liu, P. (2020). PEGASUS: Pre-training with Extracted Gap-sentences for Abstractive Summarization. *In International Conference on Machine Learning* (pp. 11328-11339). PMLR.

**Key Points**:
- Pre-training specifically for summarization
- Gap sentence generation objective
- State-of-the-art results
- **Relevance**: Related summarization model

---

### 19. Long Document Summarization
**Citation**: Beltagy, I., Peters, M. E., & Cohan, A. (2020). Longformer: The Long-Document Transformer. *arXiv preprint arXiv:2004.05150*.

**Key Points**:
- Handles long documents efficiently
- Attention mechanism for long sequences
- Useful for BillSum-like datasets
- **Relevance**: Related to long-document processing

---

## ENERGY EFFICIENCY

### 20. Energy and Policy Considerations for Deep Learning
**Citation**: Strubell, E., Ganesh, A., & McCallum, A. (2019). Energy and Policy Considerations for Deep Learning in NLP. *In Proceedings of the 57th Annual Meeting of the Association for Computational Linguistics* (pp. 3645-3650).

**Key Points**:
- Analyzes energy consumption of NLP models
- Discusses environmental impact
- Advocates for efficiency research
- **Relevance**: Motivation for PEFT research

---

### 21. Green AI
**Citation**: Schwartz, R., Dodge, J., Smith, N. A., & Etzioni, O. (2020). Green AI. *Communications of the ACM*, 63(12), 54-63.

**Key Points**:
- Advocates for energy-efficient AI
- Proposes reporting energy consumption
- Discusses trade-offs
- **Relevance**: Motivation for efficiency focus

---

### 22. CodeCarbon: Tracking Carbon Emissions
**Citation**: Schmidt, V., Goyal, K., Joshi, A., Feld, B., Conell, L., Laskaris, N., ... & Bengio, Y. (2021). CodeCarbon: Estimate and Track Carbon Emissions from Machine Learning Computing. *Zenodo*.

**Key Points**:
- Tool for tracking ML carbon emissions
- Estimates energy consumption
- Promotes awareness
- **Relevance**: Tool used for energy tracking (if enabled)

---

## BENCHMARKING & EVALUATION

### 23. Benchmarking Neural Network Robustness
**Citation**: Hendrycks, D., & Dietterich, T. (2019). Benchmarking Neural Network Robustness to Common Corruptions and Perturbations. *In International Conference on Learning Representations*.

**Key Points**:
- Importance of robust evaluation
- Multiple dataset testing
- Generalization assessment
- **Relevance**: Justifies multi-dataset approach

---

### 24. Beyond Accuracy: Behavioral Testing of NLP Models
**Citation**: Ribeiro, M. T., Wu, T., Guestrin, C., & Singh, S. (2020). Beyond Accuracy: Behavioral Testing of NLP Models with CheckList. *In Proceedings of the 58th Annual Meeting of the Association for Computational Linguistics* (pp. 4902-4912).

**Key Points**:
- Comprehensive model evaluation
- Beyond single metrics
- Behavioral testing
- **Relevance**: Evaluation methodology

---

## HARDWARE & OPTIMIZATION

### 25. Mixed Precision Training
**Citation**: Micikevicius, P., Narang, S., Alben, J., Diamos, G., Elsen, E., Garcia, D., ... & Wu, H. (2017). Mixed Precision Training. *arXiv preprint arXiv:1710.03740*.

**Key Points**:
- FP16 training for efficiency
- Reduces memory usage
- Maintains accuracy
- **Relevance**: Optimization technique used

---

### 26. Gradient Checkpointing
**Citation**: Chen, T., Xu, B., Zhang, C., & Guestrin, C. (2016). Training Deep Nets with Sublinear Memory Cost. *arXiv preprint arXiv:1604.06174*.

**Key Points**:
- Trades computation for memory
- Enables larger batch sizes
- Memory-efficient training
- **Relevance**: Optimization technique used

---

## ADDITIONAL REFERENCES

### 27. Attention Is All You Need (Transformer Architecture)
**Citation**: Vaswani, A., Shazeer, N., Parmar, N., Uszkoreit, J., Jones, L., Gomez, A. N., ... & Polosukhin, I. (2017). Attention Is All You Need. *In Advances in Neural Information Processing Systems* (pp. 5998-6008).

**Key Points**:
- Introduces transformer architecture
- Foundation for BART, T5, GPT-2
- Self-attention mechanism
- **Relevance**: Foundation of all models used

---

### 28. Hugging Face Transformers Library
**Citation**: Wolf, T., Debut, L., Sanh, V., Chaumond, J., Delangue, C., Moi, A., ... & Rush, A. M. (2020). Transformers: State-of-the-Art Natural Language Processing. *In Proceedings of the 2020 Conference on Empirical Methods in Natural Language Processing: System Demonstrations* (pp. 38-45).

**Key Points**:
- Open-source NLP library
- Provides pre-trained models
- Enables reproducible research
- **Relevance**: Implementation framework used

---

### 29. PyTorch Framework
**Citation**: Paszke, A., Gross, S., Massa, F., Lerer, A., Bradbury, J., Chanan, G., ... & Chintala, S. (2019). PyTorch: An Imperative Style, High-Performance Deep Learning Library. *In Advances in Neural Information Processing Systems* (pp. 8026-8037).

**Key Points**:
- Deep learning framework
- Dynamic computation graphs
- GPU acceleration
- **Relevance**: Implementation framework used

---

### 30. PEFT Library
**Citation**: Mangrulkar, S., Gugger, S., Debut, L., Belkada, Y., & Paul, S. (2022). PEFT: State-of-the-art Parameter-Efficient Fine-Tuning methods. *GitHub repository*.

**Key Points**:
- Implements LoRA, QLoRA, Adapters
- Integrates with Transformers
- Simplifies PEFT implementation
- **Relevance**: Implementation library used

---

## CITATION SUMMARY

**Total References**: 30

**By Category**:
- PEFT Methods: 6 papers
- Models: 4 papers
- Datasets: 5 papers
- Evaluation: 2 papers
- Related Work: 7 papers
- Energy Efficiency: 3 papers
- Implementation: 3 papers

**Key Papers to Highlight**:
1. LoRA (Hu et al., 2021)
2. QLoRA (Dettmers et al., 2023)
3. Adapters (Houlsby et al., 2019)
4. BART (Lewis et al., 2019)
5. T5 (Raffel et al., 2019)

---

## NEXT STEPS

To create **Literature_Papers.pdf**:

1. Download PDFs of all 30 papers
2. Compile into single PDF document
3. Add table of contents
4. Organize by category
5. Include citation information

**Status**: Reference list complete ✅  
**Ready for**: PDF compilation

