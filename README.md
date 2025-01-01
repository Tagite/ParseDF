# 🦜 ParseDF

![License](https://img.shields.io/github/license/Tagite/parseDF)
![Build Status](https://img.shields.io/github/actions/workflow/status/Tagite/parseDF/main.yml)
![Issues](https://img.shields.io/github/issues/Tagite/parseDF)

> ✨ PDF labeling tool to enhance the performance of RAG.


## 📋 Table of Contents
- [📖 Project Overview](#-project-overview)
- [✨ Features](#-features)
- [🛠️ Installation](#️-installation)
- [🚀 Usage](#-usage)
- [⚙️ Configuration](#-configuration)


## 📖 Project Overview
This project is a PDF labeling tool designed to enhance RAG performance. The tool allows users to draw bounding boxes to label elements such as tables and images. It also supports labeling all pages for items located in fixed positions and provides options for auto-labeling using APIs or custom-trained models. The labeled data is then used to generate Markdown (MD) files optimized for RAG workflows. The main features include precise manual labeling, automated labeling capabilities, and seamless integration into RAG pipelines, making it a versatile solution for various use cases.


## ✨ Features
- 1️⃣ **bbox labeling**: Easily define label types and draw precise bounding boxes for tables, images, and other elements in PDFs.

- 2️⃣ **Apply Labels Across All Pages**: Apply Labels Across All Pages

- 3️⃣ **Auto Labeling with API or Custom Models**: Leverage APIs or your trained models to perform automated and efficient labeling.


## 🛠️ Installation
1. Clone the repository:
   ```bash
   git clone -b dev https://github.com/Tagite/ParseDF.git
2. Install UV([Python package and project manager](https://github.com/astral-sh/uv))
   ```bash
   # On macOS and Linux.
   curl -LsSf https://astral.sh/uv/install.sh | sh 

   # On Windows.
   powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
   
   # (Cross platform)With pip.
   pip install uv

## 🚀 Usage
1. Run with pdf_path:
   ```python
   uv run main.py {PDF_PATH}