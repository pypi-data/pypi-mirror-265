Usage Guide
===========

In this guide we'll explore how to create preprocessing pipelines for text using the different functionalities available in ``gepref_text``. This includes:

* **Preprocessor**: the preprocessor is the main class that orchestates the preprocessing. It composes several preprocessing steps and allows to generate a clean text string from a raw text string.
* **Normalization**: the ``normalization`` module contains several components for text normalization. This includes writing modification, unicode normalization, and trimming.
* **Regex substitution**: the ``regex`` module includes components for regex-based text substitution, allowing to replace special characters, numbers, duplicated spaces, URLs, among others.
* **Custom**: you can create custom components that can be directly integrated in the preprocessing pipelines.

.. toctree::
   :maxdepth: 3
   :caption: Contents:

   usage/preprocessor
   usage/normalization
   usage/regex
   usage/custom
