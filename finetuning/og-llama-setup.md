
  

#  Llama 3 TikTok Script Generator (QLoRA Fine-Tuning)

  

##  Project Context and Goal

  

This project details the process of **fine-tuning** the **Meta-Llama-3-8B-Instruct** large language model (LLM) to perform a very specific, stylistic task.

  

Using the efficient **QLoRA (Quantized Low-Rank Adaptation)** technique, we are training the model to adopt a **Gen Z persona**. The ultimate goal is to create a tool that can receive a formal text input (like a news summary or press release) and instantly translate it into a concise, viral, and engaging **TikTok script**, complete with appropriate slang, emojis, and hashtags.

  

The following guide walks you through setting up the required GPU environment, installing dependencies, and preparing for the final deployment.

  

---

  

##  Hardware Requirements
Finetuning an LLM involves significant computational cost, making **GPU memory (VRAM)** the single most important hardware requirement. The necessary setup depends heavily on whether you are performing _full finetuning_ or using more efficient methods like **QLoRA** or **LoRA**. 

We are using **QLoRa** for 4-bit quantization so we can lessen some of those memory requirements. Testing this worked on a small dataset with a NVIDIA 5070Ti. 


The LlaMa-3-8B instruct has approximately 8 billion parameters, and takes up approximately 16GB of space. A consumer GPU with QLoRa quantization works well, but with better hardware we can increase the precision. 

**RAM:**  For 7B to 13B models, **64 GB to 128 GB** of high-speed DDR5 RAM is typically recommended.
**SSD**: A lot.

PEFT & QLoRa only train a few million _new_ parameters (adapter layers) while keeping the original LLM weights frozen. This dramatically reduces the VRAM requirement, allowing powerful 7B and 13B models to be finetuned on a single high-end consumer GPU (like an RTX 4090), avoiding the need for expensive data center hardware like the A100 or H100.

TLDR: With 4-bit quantization and a good GPU, we're OK. 


  
  

###  1.1 Environment Setup (Miniconda Installation)

  

Fine-tuning large models requires specific versions of deep learning libraries and NVIDIA's CUDA toolkit. To avoid conflicts with your system's global Python installation, we strongly recommend using **Miniconda** to create a dedicated, isolated environment.

  

1.  **Install Miniconda:** Download and install the appropriate version for your operating system (Windows, macOS, or Linux) from the official [Miniconda site](https://docs.conda.io/en/latest/miniconda.html).

2.  **Create Environment:** Open your terminal or command prompt and create a new environment named `llama-tiktok` with Python 3.10:

```bash

conda create -n llama-tiktok python=3.10

```

3.  **Activate Environment:** You **must** activate this environment before installing dependencies or running any Python scripts.

```bash

conda activate llama-tiktok

```
### 1.2. Hugging Face Instructions
Create an account on [Hugging Face](https://huggingface.co/). Click your PFP and navigate to the "access token" section. Create a READ access token, name it whatever you want. Use that for any instances of HF_TOKEN and if HF CLI asks you for it when you login. 

Then navigate to the [Meta LlaMa](https://huggingface.co/meta-llama/Meta-Llama-3-8B-Instruct) page, where you can **request access* to the models of Meta LlaMa as this is a gated repo. Being accepted should take somwhere between 5-10 mins. Just put in your contact information and affiliation (ie. Student or Digital Engagement Lab). 

---

  

##  2. Installs/Core Dependencies

  

Ensure the `llama-tiktok` environment is **active** before running the following installation commands. These libraries form the core of the QLoRA training stack.

  
  
  

###  2.1. Install PyTorch with CUDA

  

Install the PyTorch version that matches your NVIDIA CUDA Toolkit. The example below uses a common version (`cu121`).

  

To check your CUDA version, first ensure you have NVIDIA's CUDA Toolkit downloaded. From there, navigate to `C:\Program Files\NVIDIA GPU Computing Toolkit\CUDA\[version number]` where the folder in CUDA will show the version that you have. 

From there, install [Pytorch](https://pytorch.org/get-started/locally/) locally based off the version of CUDA you have.

  

```bash

# Install PyTorch and TorchVision (Adjust 'cu121' if your CUDA version is different)

pip  install  torch  torchvision  torchaudio  --index-url [https://download.pytorch.org/whl/cu121](https://download.pytorch.org/whl/cu121)

```
To check if everything is OK, you can run `python check.py` and the command line should say that the GPU is available and CUDA is working.
  

### **2.2. Remaining Dependencies/Installs**
```bash
pip install transformers==4.36.0 \ # hugging face

peft==0.7.0 \ # in hugging face, parameter-efficient fine-tuning

trl==0.7.4 \ # transformer reinforcement learning

bitsandbytes==0.41.0 \ # quantization

datasets==2.16.0 # handling large datasets

pip install accelerate # for multiple GPUs

  

# OPTIONAL: wandb for metrics tracking

pip install wandb

wandb login

  

# hugging face CLI 

pip install huggingface_hub

hf auth login # login for hf

# if it asks you for a token, enter the READ token you've created on your account
# to check if you're logged in run hf auth whoami
```


## 3. Data Entry
Data is assumed to be a simple JSON with one parameter: `tiktok_script` that contains the scraped transcript. 

## 4. Remaining To-Do 

 - [ ] Connect the `generate.py` script to some sort of backend (ie. w/ Flask) so it can be called by a frontend. 
 - [ ] Create a frontend that calls that backend.
 - [ ] Decide what service we want to use to SERVE the model from some cloud. Regular phones/consumer hardware cannot handle the fine-tuned model in it's entirety, so we need to host it somewhere. 
 - [ ] Connect the AI to our actual dataset and format that it uses. Clean it if needed. 
