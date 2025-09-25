FROM public.ecr.aws/lambda/python:3.12 as eagleai-basketball-model
COPY . .
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
CMD [ "main.handler" ]
