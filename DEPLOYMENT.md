# ☁️ Google Cloud Run Deployment Guide

To deploy this platform to the cloud, we use a modern microservices approach: hosting the **FastAPI Backend** and the **React Frontend** as two separate, highly scalable Google Cloud Run services.

We have included `Dockerfile.backend` and `Dockerfile.frontend` in the project root to handle the containerization.

You can deploy using either the **gcloud CLI** or the **Google Cloud Console (UI)**.

---

## Method 1: Using the gcloud CLI

### Prerequisites
1. Ensure you have the [Google Cloud CLI (gcloud)](https://cloud.google.com/sdk/docs/install) installed and authenticated (`gcloud auth login`).
2. Ensure you have a GCP Project created with Billing enabled.
3. Set your project ID:
   ```bash
   gcloud config set project YOUR_PROJECT_ID
   ```
4. Enable the Cloud Run API:
   ```bash
   gcloud services enable run.googleapis.com
   ```

---

## Step 1: Deploy the FastAPI Backend

We deploy the Python backend first so we can obtain its live public URL, which the frontend will need to route API calls.

> **Important**: You must pass your LLM API keys and your Supabase `DATABASE_URL` securely into the Cloud Run environment.

Run the following command from the root directory of your project:

```bash
gcloud run deploy retail-ai-backend \
  --source . \
  --dockerfile Dockerfile.backend \
  --region us-central1 \
  --allow-unauthenticated \
  --set-env-vars="LLM_PROVIDER=openai" \
  --set-env-vars="OPENAI_API_KEY=your-openai-api-key" \
  --set-env-vars="ANTHROPIC_API_KEY=your-anthropic-api-key" \
  --set-env-vars="SUPABASE_URL=your-supabase-url" \
  --set-env-vars="SUPABASE_KEY=your-supabase-key" \
  --set-env-vars="DATABASE_URL=your-postgres-url"
```
*Note: Wait for this deployment to finish. Once done, `gcloud` will output a Service URL (e.g., `https://retail-ai-backend-xxxxxx-uc.a.run.app`). Copy this URL!*

---

## Step 2: Deploy the React Frontend

Now we will deploy the React application. We need to pass the Backend URL we just generated as an environment variable (`VITE_API_URL`) so the frontend knows where to send requests in production.

Run this command from the root directory:

```bash
gcloud run deploy retail-ai-frontend \
  --source . \
  --dockerfile Dockerfile.frontend \
  --region us-central1 \
  --allow-unauthenticated \
  --set-build-env-vars="VITE_API_URL=https://retail-ai-backend-xxxxxx-uc.a.run.app"
```

> **Tip**: Notice we use `--set-build-env-vars` instead of `--set-env-vars`. This is because Vite is a static build tool, so it must bake the API URL into the HTML/JS assets during the Docker build stage!

---

## Method 2: Google Cloud Console (UI)

If you prefer using the graphical web interface instead of the terminal, you can deploy both services directly from your GitHub repository using the Cloud Run Console.

### Step 1: Deploy the Backend
1. Push this project code to a repository on GitHub, Bitbucket, or Cloud Source Repositories.
2. Go to the [Google Cloud Run Console](https://console.cloud.google.com/run).
3. Click **Create Service**.
4. Select **Continuously deploy new revisions from a source repository** and click **Set up with Cloud Build**.
5. Select your Repository and Branch, then click **Next**.
6. Under **Build Configuration**:
   - Build Type: Select **Dockerfile**.
   - Source Location: Type `/Dockerfile.backend` and click Save.
7. Scroll down to **Authentication** and select **Allow unauthenticated invocations**.
8. Expand the **Container(s), Volumes, Networking, Security** panel at the bottom.
9. Click the **Variables & Secrets** tab and add the following Environment Variables:
   - `LLM_PROVIDER`: `openai` (or `anthropic`)
   - `OPENAI_API_KEY`: `your-api-key`
   - `SUPABASE_URL`: `your-supabase-url`
   - `SUPABASE_KEY`: `your-supabase-key`
   - `DATABASE_URL`: `your-postgres-url`
10. Click **Create** and wait for the deployment to finish. Copy the generated URL!

### Step 2: Deploy the Frontend
1. Click **Create Service** again.
2. Select the same repository and branch.
3. Under **Build Configuration**:
   - Build Type: Select **Dockerfile**.
   - Source Location: Type `/Dockerfile.frontend` and click Save.
4. Select **Allow unauthenticated invocations**.
5. Expand the **Container(s), Volumes, Networking, Security** panel.
6. Click the **Variables & Secrets** tab. Since Vite needs variables at *build time*, you must add them as **Build Environment Variables** (not standard Environment Variables). Add:
   - Name: `VITE_API_URL`
   - Value: `[Paste your backend URL here]`
7. Click **Create**. 

Once finished, click the public URL provided by Cloud Run to access your live React application!
