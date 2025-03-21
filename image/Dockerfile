FROM public.ecr.aws/lambda/python:3.12

# Install build tools and dependencies
RUN dnf install -y gcc gcc-c++ make cmake openblas-devel lapack-devel python3-devel

# Copy requirements.txt
COPY requirements.txt ${LAMBDA_TASK_ROOT}

# Install setuptools first
RUN pip install --upgrade pip setuptools wheel

# Install requirements
RUN pip install -r requirements.txt --upgrade

# For local testing.
EXPOSE 8000

# Set IS_USING_IMAGE_RUNTIME Environment Variable
ENV IS_USING_IMAGE_RUNTIME=True

# Copy all files in ./src
COPY src/* ${LAMBDA_TASK_ROOT}
COPY src/rag_app ${LAMBDA_TASK_ROOT}/rag_app
COPY src/data/chroma ${LAMBDA_TASK_ROOT}/data/chroma