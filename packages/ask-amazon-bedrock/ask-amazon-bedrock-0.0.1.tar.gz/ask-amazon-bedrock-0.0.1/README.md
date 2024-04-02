## Tool Execution

`python askamzbr.py -b <bedrock_region> -m <bedrock_model> -q "query to ask Amazon Bedrock"`

The tool invokes the Bedrock Claude3 model by default to get the query from user and return results.


## Tool arguments

| Argument                    | Description                                                         | Required | Default                                             | Usage                                             |
|-----------------------------|---------------------------------------------------------------------|----------|-----------------------------------------------------|---------------------------------------------------|
| `--bedrock-region`, `-b`    | Region where Bedrock Model will be invoked.                         | NO       | "us-west-2"                                         | `--bedrock-region "us-west-2"`                    |
| `--bedrock-model`, `-m`     | Bedrock Model used to get insights.                                 | NO       | "anthropic.claude-3-sonnet-20240229-v1:0"           | `--bedrock-model "model_name"`                    |
| `--query`, `-q`             | Query to ask Bedrock.                                               | YES      | N/A                                                 | `--query "tell me a joke"`                              |
