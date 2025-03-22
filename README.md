# Langchain RAG Application
# Deployed to AWS using asynchronous Lambda worker function to handle background AI/RAG processing.

## Getting Started

### AWSRequirements

- AWS account
- AWS CLI set up
- AWS Bedrock enabled on AWS (and granted AImodel access for whichever AI model being used)

- Update .env File with AWS Credentials

Create a file named `.env` in `image/`. The .gitignore excludes this file, so it will not be committed to the repo. The file should have content like this:

```
AWS_ACCESS_KEY_ID=XXXXX
AWS_SECRET_ACCESS_KEY=XXXXX
AWS_DEFAULT_REGION=us-east-1
TABLE_NAME=YourTableName
```

These credentials are used by Docker locally to access Bedrock and DynamoDB to read/write data.

You will also need to set the TABLE_NAME for the DynamoDB table.

### Installation Requirements

```sh
pip install -r image/requirements.txt
```

### Building the Chroma Vector DB

Put all the PDF source files you want into `image/src/data/source/`. Then go `image` and run:

```sh
# Use "--reset" if you want to overwrite an existing DB.
python populate_database.py --reset
```

### Running the Application

```sh
# Execute from image/src directory
cd image/src
python rag_app/query_rag.py "How many energy types are there in pokemon tcg?"
```

Example output:

```text
Answer the question based on the above context: What are the parts of a pokemon card in pokemon TCG?

Response:  Based on the context provided, the parts of a Pokémon card in the Pokémon Trading Card Game are:

1. Card Name
2. Stage (Basic, Stage 1, Stage 2)
3. Card Type (Pokémon, Energy, Trainer)
4. Collector Card Number
5. Expansion Code
6. Evolves From (if applicable)
7. Pokémon Type
8. HP (Hit Points)
9. Text Box (containing Abilities, Attacks, and Retreat Cost)

The context mentions that Pokémon cards can be Basic, Stage 1, or Stage 2, and that Stage 1 and Stage 2 Pokémon are also called Evolution cards. It also explains that Energy cards are needed for Pokémon to attack, and that the text box on a Pokémon card contains the card's Abilities, Attacks, and Retreat Cost.
```

### Starting FastAPI Server

```sh
# From image/src directory.
python api_handler.py
```

Navigate to `http://0.0.0.0:8000/docs` to try it out.

## Using Docker Image

### Build and Test the Image Locally

These commands can be run from `image/` directory to build, test, and serve the app locally.

```sh
docker build --platform linux/amd64 -t langchain-rag-aws .
```

```sh
# Run the container using command `python app_work_handler.main`
docker run --rm -it \
    --entrypoint python \
    --env-file .env \
    langchain-rag-aws work_handler.py
```

This will test the image, seeing if it can run the RAG/AI component with a hard-coded question (see ` work_handler.py`).

## Running Locally as a Server

Once the image is built from the previous step.

```sh
docker run --rm -p 8000:8000 \
    --entrypoint python \
    --env-file .env \
    langchain-rag-aws api_handler.py
```

## Testing Locally

After running the Docker container on localhost, you can access an interactive API page locally to test it: `http://0.0.0.0:8000/docs`.

```sh
curl -X 'POST' \
  'http://0.0.0.0:8000/submit_query' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "query_text": "How many energy types are there in pokemon tcg?"
}'
```

## Deploy to AWS

The AWS Cloud Development Framework files are located in `rag-cdk-infra/`. 

Install the Node dependencies.

```sh
npm install
```

You can then deploy the application using CDK. CDK uses CloudFormation to assign the resources and deploy the application.

```sh
cdk deploy
```

## Accessing the API

Once deployed, you can access the API at the URL provided by the CDK deployment.

Outputs:

```
RagCdkInfraStack.FunctionUrl = https://xxxxxxxx.lambda-url.us-east-1.on.aws/
```

The API is available if you postpend the URL with `/docs`.
