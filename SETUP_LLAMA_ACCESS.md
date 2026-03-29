# Setup LLaMA Access for Experiments

## Step 1: Create HuggingFace Account
1. Go to https://huggingface.co/join
2. Create a free account

## Step 2: Request LLaMA Access
1. Go to https://huggingface.co/meta-llama/Llama-2-7b-hf
2. Click "Request Access" button
3. Fill out the form (usually approved within minutes to hours)
4. Wait for approval email

## Step 3: Generate Access Token
1. Go to https://huggingface.co/settings/tokens
2. Click "New token"
3. Name it: "llama-experiments"
4. Type: "Read"
5. Click "Generate"
6. Copy the token (starts with "hf_...")

## Step 4: Login to HuggingFace CLI
Run this command and paste your token when prompted:

```bash
C:\Users\hares\AppData\Local\Programs\Python\Python313\python.exe -m pip install huggingface_hub
C:\Users\hares\AppData\Local\Programs\Python\Python313\python.exe -c "from huggingface_hub import login; login()"
```

Or use this batch file I created: `LOGIN_HUGGINGFACE.bat`

## Step 5: Verify Access
Run: `VERIFY_LLAMA_ACCESS.bat`

## Step 6: Run All 9 Experiments
Once verified, run: `RUN_EXPERIMENTS_NOW.bat`

This will run all 9 experiments including LLaMA (E25-E27).
