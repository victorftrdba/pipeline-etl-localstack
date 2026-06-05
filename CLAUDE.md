# CLAUDE.md - pipeline-etl-localstack

## O que é

Pipeline ETL local (sem custos) que gera dados, converte para Parquet, faz upload para S3 simulado e publica mensagem em SQS. Parte de um ecossistema de três repos: `lab-terraform-local` (infra) → este repo (ETL) → `data-validator-app` (validação).

## Stack

- Python 3.12 · boto3 · pandas · pyarrow · python-dotenv
- LocalStack (S3 + SQS simulados) · Mailpit (SMTP local)
- Docker · Kubernetes Jobs · Terraform (via repo externo)

## Estrutura

```
app.py           -- lógica ETL principal (gera dados, Parquet, S3, SQS, e-mail)
Dockerfile       -- imagem Docker da aplicação
job.yaml         -- manifesto Kubernetes Job (namespace data-science-env)
requirements.txt -- dependências Python
config/          -- settings.py com variáveis de configuração
pipeline/        -- consumer.py e producer.py
services/        -- aws_client.py, data_generator.py, email_service.py
```

## Comandos

```bash
pip install -r requirements.txt
python app.py                                        # execução local

docker build -t data-pipeline-local:v1 .
docker run --rm -e AWS_ENDPOINT_URL=... data-pipeline-local:v1

kubectl apply -f job.yaml                            # submete job no k8s
kubectl logs -n data-science-env job/data-pipeline-job
kubectl delete -f job.yaml && kubectl apply -f job.yaml   # re-executar
```

## Padrões

- Variáveis de ambiente: `AWS_ENDPOINT_URL`, `S3_BUCKET_NAME`, `SQS_QUEUE_NAME`, `AWS_DEFAULT_REGION`, `AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY`
- Namespace Kubernetes: `data-science-env`
- Formato de saída: Parquet via pyarrow
- E-mail de notificação enviado ao Mailpit (porta 1025); UI em http://localhost:8025
