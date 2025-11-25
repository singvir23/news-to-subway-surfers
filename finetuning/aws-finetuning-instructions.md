# Fine-Tuning LLaMA 3.1 on TikTok Transcripts with QLoRA in SageMaker

This guide walks you through running QLoRA fine-tuning for LLaMA 3.1 in AWS SageMaker Studio using a GPU instance.

---

## 1. Set up SageMaker Studio

1. Open **SageMaker Studio** in your AWS console
2. Launch a **Accelerated Compute** instance (may need money)
3. Access the **terminal** in the notebook interface

---

## 2. Copy project files from your local `qlora-sagemaker` folder

Use `boto3` or the terminal to download/copy your project folder (with `train.py`, `data/`, etc.) into SageMaker Studio.

```bash
aws s3 cp s3://subway-surfers-llama3/qlora-sagemaker ./ --recursive
```

**Verify that your folder contains:**

- `train.py`
- `data/reddit_transcripts.csv` 
- Any other scripts or config files

---

## 3. Install required packages

Run the following in the terminal or a notebook cell:

```bash
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121
pip install transformers==4.44.2
pip install datasets
pip install peft
pip install trl
pip install bitsandbytes
pip install accelerate
pip install evaluate
```

> ⚠️ **Important:** Install `bitsandbytes` after PyTorch to avoid version conflicts.

---

## 4. Add your Hugging Face token

Open `train.py` with nano or any text editor:

```bash
nano train.py
```

Find the `HF_TOKEN` placeholder and set your Hugging Face token:

```python
HF_TOKEN = "YOUR_HF_READ_TOKEN"
```

Save and exit (`Ctrl+O`, `Enter`, `Ctrl+X`).

> 💡 This token allows the script to download LLaMA 3.1 from Hugging Face.

---

## 5. Log into Hugging Fcae

Login to Hugging Face using: 

```bash
hf auth login
```

Paste in the HF access token to log in, you can say no to making it a git instance. 

---

## 6. Run the training script

In the terminal:

```bash
python train.py
```

**The script will:**

- Load LLaMA 3.1 with 4-bit QLoRA quantization
- Load your CSV dataset (`transcript` column) and format it into the instruction template
- Fine-tune using LoRA
- Save the adapter weights and tokenizer to `OUTPUT_DIR`

---

## 7. Check outputs

After training:

- `./llama_tiktok/pytorch_model.bin` – LoRA adapter weights
- `./llama_tiktok/tokenizer/` – tokenizer files

**Upload to S3 (optional):**

```bash
aws s3 cp ./llama_tiktok s3://your-bucket/llama_tiktok/ --recursive
```

---

## 8. Tips

- If using a smaller GPU or limited memory, reduce `BATCH_SIZE` or `GRAD_ACCUM`
- Always test your data preprocessing before training to avoid tokenization errors
- Make sure your HF token has read access to the LLaMA 3.1 model

---

**Happy fine-tuning! 🚀**
