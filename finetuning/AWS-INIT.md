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

## Monitor Training

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

