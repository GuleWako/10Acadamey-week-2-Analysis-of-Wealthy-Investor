FROM python:3.9-slim

# Install dependencies
RUN pip install pandas scikit-learn matplotlib seaborn

# Copy your Python script
COPY .. /app/

# Set the working directory
WORKDIR /app

# Define the entry point
ENTRYPOINT ["python"]