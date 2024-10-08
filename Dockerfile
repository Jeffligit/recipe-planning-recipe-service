# 
FROM python:3.11

# 
WORKDIR /code

# 
COPY ./requirements.txt /code/requirements.txt

# 
RUN pip install --no-cache-dir -r /code/requirements.txt

# 
COPY ./src /code/src

# 
CMD ["fastapi", "dev", "src/main.py", "--host", "0.0.0.0", "--port", "8000"]