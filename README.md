# AWS SAM Items API ハンズオン

AWS SAMでREST API、Lambda、DynamoDBを使ったItems APIを動かすためのサンプルです。

Qiita記事「【AWS SAM】サーバーレス開発の基礎から本番運用まで、AWS SAMを一気にまとめてみた」で使うコード一式を置いています。

## 1. 必要なもの

- AWS CLI
- AWS SAM CLI
- Docker
- Python 3.12

## 2. ローカルで動かす

リポジトリを取得します。

```bash
git clone https://github.com/miruky/aws-sam-items-api-handson.git
cd aws-sam-items-api-handson
```

DynamoDB Localを起動します。

```bash
docker run -d --name dynamodb-local -p 8000:8000 amazon/dynamodb-local
```

ローカル用テーブルを作ります。

```bash
aws dynamodb create-table \
  --endpoint-url http://localhost:8000 \
  --table-name local-items \
  --attribute-definitions AttributeName=id,AttributeType=S \
  --key-schema AttributeName=id,KeyType=HASH \
  --billing-mode PAY_PER_REQUEST
```

SAMテンプレートを検証してビルドします。

```bash
sam validate --lint
sam build --cached --parallel
```

関数単体を呼び出します。

```bash
sam local invoke CreateItemFunction \
  --event events/create-item.json \
  --env-vars env-local.json

sam local invoke ListItemsFunction \
  --event events/list-items.json \
  --env-vars env-local.json
```

APIとして起動します。

```bash
sam local start-api \
  --port 3000 \
  --env-vars env-local.json
```

別ターミナルから呼び出します。

```bash
curl http://localhost:3000/items

curl -X POST http://localhost:3000/items \
  -H "Content-Type: application/json" \
  -d '{"name": "Local API Item", "description": "created by curl", "price": 500}'
```

## 3. AWSへデプロイする

AWS CLIの認証情報とリージョンを確認してから実行します。

```bash
aws sts get-caller-identity
aws configure get region

sam validate --lint
sam build --cached --parallel

sam deploy --guided \
  --stack-name sam-items-api-dev \
  --capabilities CAPABILITY_IAM \
  --parameter-overrides Stage=dev
```

## 4. 削除する

AWS上のスタックを削除します。

```bash
sam delete \
  --stack-name sam-items-api-dev
```

ローカルのDynamoDB Localを削除します。

```bash
docker rm -f dynamodb-local
```

