# AWS SageMaker Setup Guide for QLoRA Fine-Tuning

## STEP 1 — Create / Log Into Your AWS Account

If you don’t already have one:

* Go to **console.aws.amazon.com**
* Sign in or create an account.
* Add a **credit card** (AWS requires this, even for free tier).

---

## STEP 2 — Create an S3 Bucket for Datasets + Model Outputs

SageMaker stores:

* Your uploaded training data
* Model artifacts from training jobs
* Checkpoints (optional)

### Create a bucket:

1. Go to **AWS Console → S3**
2. Click **Create bucket**
3. Name example:

   ```
   vips-llama3-training
   ```
4. Leave all defaults.
5. Click **Create**.

### Upload your dataset:

1. Enter your bucket → **Upload**
2. Drag in your `tiktok.json`
3. Confirm upload

Your file should end up in:

```
s3://kalpana-llama3-training/tiktok.json
```

---

## STEP 3 — Create an IAM Execution Role for SageMaker

SageMaker needs permission to:

* Read/write S3
* Access Secrets Manager (for your HF token)
* Run training jobs

### Create Role:

1. Go to **IAM → Roles → Create role**

2. **Trusted entity**: AWS Service

3. **Use case**: choose **SageMaker**

4. Attach these permissions:

   * `AmazonS3FullAccess` (or restrict to your buckets)
   * `AmazonSageMakerFullAccess`
   * `SecretsManagerReadWrite`

5. Name it:

```
SageMakerExecutionRole
```

Save the **ARN** — you’ll need it:

```
arn:aws:iam::<ACCOUNT-ID>:role/SageMakerExecutionRole
```

---

## STEP 4 — Store Your Hugging Face Token in Secrets Manager (SECURE)

This keeps your token protected.

1. Go to **AWS Console → Secrets Manager**
2. Click **Store a new secret**
3. Choose **Other type of secret**
4. Enter key/value:

| Key      | Value                     |
| -------- | ------------------------- |
| HF_TOKEN | hf_your_actual_token_here |

5. Name the secret:

```
hf-token-secret
```

Save the secret ARN:

```
arn:aws:secretsmanager:us-east-1:<ACCOUNT-ID>:secret:hf-token-secret-XXXXX
```

---

## STEP 5 — Open SageMaker Studio (Recommended)

SageMaker Studio is where you'll run your launcher script.

### Create a SageMaker Studio domain:

1. Go to **AWS Console → SageMaker → SageMaker Studio**
2. Click **Set up for single user**
3. Choose:

   * **User profile name**: `kalpana`
   * **Execution role**: `SageMakerExecutionRole`
4. Create domain (takes ~5 minutes)

### Open Studio:

* After creation, click **Open Studio**
* You’ll now be inside a Jupyter-like environment

---

## STEP 6 — Create a SageMaker Notebook to Launch Jobs

Inside Studio:

1. **File → New Notebook**
2. Choose instance:

   * `ml.t3.medium` (cheap and enough for launching jobs)

### Install dependencies:

Run in a notebook cell:

```bash
pip install sagemaker --upgrade
pip install boto3
```

---

## STEP 7 — Upload Your `qlora-sagemaker/` Project Folder

Drag your project folder into the Studio file browser:

```
qlora-sagemaker/
  code/train.py
  code/requirements.txt
  launch/run_training_job.py
```

---

## STEP 8 — Modify the Launcher: Add ROLE + S3 Paths + Secret

Open:

```
launch/run_training_job.py
```

### Set your execution role:

```python
role = "arn:aws:iam::<ACCOUNT-ID>:role/SageMakerExecutionRole"
```

### Set dataset S3 path:

```python
inputs = {
    "training": "s3://kalpana-llama3-training/tiktok.json"
}
```

### Add HF Token from Secrets Manager

Replace the insecure version:

```python
environment={"HF_TOKEN": sagemaker.get_execution_role()}
```

With the secure one:

```python
environment={
    "HF_TOKEN": "{{resolve:secretsmanager:hf-token-secret:SecretString:HF_TOKEN}}"
}
```

This securely injects your HF token during training.

---

## STEP 9 — Run the Training Job

In your SageMaker notebook, run:

```bash
!python launch/run_training_job.py
```

This will:

* Spin up an `ml.p4d.24xlarge`
* Download your dataset to `/opt/ml/input/data/training`
* Run your QLoRA training
* Save final model to `/opt/ml/model`
* Upload model artifacts to S3:

```
s3://<your-default-sagemaker-bucket>/huggingface-pytorch-training-<timestamp>/output/model.tar.gz
```

---

## STEP 10 — Monitor Training

Go to: **AWS Console → SageMaker → Training jobs**

Click your job to monitor:

* CloudWatch logs
* GPU utilization
* Job status
* Training artifacts

---

## STEP 11 — After Training: Download or Deploy

### **Option A — Download the Model**

From S3:

```
model.tar.gz
```

Extract:

```bash
tar -xvzf model.tar.gz
```

Contents:

* `adapter_model.safetensors`
* `adapter_config.json`
* `tokenizer.json`
* `tokenizer.model`

### **Option B — Deploy on SageMaker Endpoint**

You can deploy:

* LoRA adapter only
* Merged model
* Or use Hugging Face TGI container

