"""
Anthropic Claude Integration via AWS Bedrock Component

Provides production-ready Claude API client through AWS Bedrock.
Supports Claude 3.5 Sonnet, Claude 3.5 Haiku, and Claude 3.7 Sonnet.
All credentials managed via AWS credentials system - NO HARDCODED SECRETS.

Usage:
    from components.backend.ai_integrations.anthropic_bedrock import (
        create_bedrock_client,
        invoke_claude,
        ClaudeModel
    )

    # Create client
    client = create_bedrock_client(region="us-east-1")

    # Invoke Claude
    response = invoke_claude(
        client=client,
        prompt="Explain quantum computing",
        model_type=ClaudeModel.SONNET_3_7
    )

Note:
    Requires AWS credentials configured via:
    - Environment variables (AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY)
    - AWS credentials file (~/.aws/credentials)
    - IAM role (when running on AWS infrastructure)
"""

import json
import logging
from enum import Enum
from typing import Optional, Dict, Any
from botocore.config import Config
from botocore.exceptions import ClientError

logger = logging.getLogger(__name__)


class ClaudeModel(Enum):
    """Supported Claude model versions.

    Each model has different capabilities and pricing:
    - SONNET_3_5: Balanced performance and cost
    - HAIKU_3_5: Fast and cost-effective for simpler tasks
    - SONNET_3_7: Latest model with enhanced reasoning
    """
    SONNET_3_5 = "3.5-sonnet"
    HAIKU_3_5 = "3.5-haiku"
    SONNET_3_7 = "3.7-sonnet"


# Model type to inference profile ID mapping
MODEL_MAP = {
    "3.5-sonnet": "us.anthropic.claude-3-5-sonnet-20241022-v2:0",
    "3.5-haiku": "us.anthropic.claude-3-5-haiku-20241022-v1:0",
    "3.7-sonnet": "us.anthropic.claude-3-7-sonnet-20250219-v1:0"
}


def create_bedrock_client(
    region: str = "us-east-1",
    read_timeout: int = 120
):
    """Create AWS Bedrock Runtime client for Claude models.

    Args:
        region: AWS region (default: us-east-1)
        read_timeout: Request timeout in seconds (default: 120)

    Returns:
        Boto3 Bedrock Runtime client

    Environment Variables:
        AWS_ACCESS_KEY_ID: AWS access key
        AWS_SECRET_ACCESS_KEY: AWS secret key
        AWS_SESSION_TOKEN: Optional session token
        AWS_DEFAULT_REGION: Default AWS region

    Example:
        # Use default region and AWS credentials from environment
        client = create_bedrock_client()

        # Custom region
        client = create_bedrock_client(region="us-west-2")
    """
    import boto3

    logger.info(f"Creating Bedrock Runtime client for region: {region}")

    return boto3.client(
        'bedrock-runtime',
        region_name=region,
        config=Config(read_timeout=read_timeout)
    )


def invoke_claude(
    client,
    prompt: str,
    model_type: str = "3.7-sonnet",
    max_tokens: int = 500,
    temperature: float = 0.7,
    system_prompt: Optional[str] = None
) -> Optional[str]:
    """Invoke Claude model via AWS Bedrock.

    Args:
        client: Boto3 Bedrock Runtime client
        prompt: User prompt/question
        model_type: Model version (3.5-sonnet, 3.5-haiku, 3.7-sonnet)
        max_tokens: Maximum tokens to generate (default: 500)
        temperature: Sampling temperature 0.0-1.0 (default: 0.7)
        system_prompt: Optional system message for context

    Returns:
        Generated text response, or None if error occurs

    Raises:
        ValueError: If model_type is invalid
        ClientError: If AWS API call fails

    Example:
        # Simple completion
        response = invoke_claude(
            client=client,
            prompt="Explain how LLMs work in 20 words or less",
            model_type="3.5-sonnet"
        )

        # With system prompt
        response = invoke_claude(
            client=client,
            prompt="Write a haiku about coding",
            model_type="3.7-sonnet",
            system_prompt="You are a creative poet",
            temperature=0.9
        )
    """
    # Get the correct model ID
    model_id = MODEL_MAP.get(model_type.lower())
    if not model_id:
        valid_models = ', '.join(MODEL_MAP.keys())
        raise ValueError(
            f"Invalid model type: {model_type}. "
            f"Must be one of: {valid_models}"
        )

    logger.info(f"Invoking Claude model: {model_type} ({model_id})")

    # Build messages array
    messages = [{
        "role": "user",
        "content": [{"type": "text", "text": prompt}]
    }]

    # Format request payload for Claude through Bedrock
    request_body = {
        "anthropic_version": "bedrock-2023-05-31",
        "max_tokens": max_tokens,
        "temperature": temperature,
        "messages": messages
    }

    # Add system prompt if provided
    if system_prompt:
        request_body["system"] = system_prompt

    try:
        # Invoke the model using the inference profile
        response = client.invoke_model(
            modelId=model_id,
            body=json.dumps(request_body)
        )

        # Parse and return the response
        response_body = json.loads(response['body'].read())
        return response_body['content'][0]['text']

    except ClientError as e:
        logger.error(f"Error invoking Claude model '{model_type}': {e}")
        return None


def invoke_claude_advanced(
    client,
    messages: list,
    model_type: str = "3.7-sonnet",
    max_tokens: int = 500,
    temperature: float = 0.7,
    system_prompt: Optional[str] = None,
    top_p: Optional[float] = None,
    top_k: Optional[int] = None
) -> Optional[Dict[str, Any]]:
    """Advanced Claude invocation with multi-turn conversation support.

    Args:
        client: Boto3 Bedrock Runtime client
        messages: List of message dicts with 'role' and 'content'
        model_type: Model version (3.5-sonnet, 3.5-haiku, 3.7-sonnet)
        max_tokens: Maximum tokens to generate
        temperature: Sampling temperature 0.0-1.0
        system_prompt: Optional system message
        top_p: Nucleus sampling parameter (0.0-1.0)
        top_k: Top-k sampling parameter

    Returns:
        Dictionary with:
            - text: Response text
            - stop_reason: Why generation stopped
            - usage: Token usage statistics
        Or None if error occurs

    Example:
        # Multi-turn conversation
        messages = [
            {"role": "user", "content": "What is Python?"},
            {"role": "assistant", "content": "Python is a programming language..."},
            {"role": "user", "content": "What are its main features?"}
        ]
        response = invoke_claude_advanced(
            client=client,
            messages=messages,
            model_type="3.7-sonnet"
        )
        print(response["text"])
    """
    # Get the correct model ID
    model_id = MODEL_MAP.get(model_type.lower())
    if not model_id:
        valid_models = ', '.join(MODEL_MAP.keys())
        raise ValueError(
            f"Invalid model type: {model_type}. "
            f"Must be one of: {valid_models}"
        )

    logger.info(f"Invoking Claude model (advanced): {model_type}")

    # Format messages for Bedrock
    formatted_messages = []
    for msg in messages:
        formatted_messages.append({
            "role": msg["role"],
            "content": [{"type": "text", "text": msg["content"]}]
        })

    # Build request body
    request_body = {
        "anthropic_version": "bedrock-2023-05-31",
        "max_tokens": max_tokens,
        "temperature": temperature,
        "messages": formatted_messages
    }

    # Add optional parameters
    if system_prompt:
        request_body["system"] = system_prompt
    if top_p is not None:
        request_body["top_p"] = top_p
    if top_k is not None:
        request_body["top_k"] = top_k

    try:
        response = client.invoke_model(
            modelId=model_id,
            body=json.dumps(request_body)
        )

        response_body = json.loads(response['body'].read())

        return {
            "text": response_body['content'][0]['text'],
            "stop_reason": response_body.get('stop_reason'),
            "usage": {
                "input_tokens": response_body.get('usage', {}).get('input_tokens'),
                "output_tokens": response_body.get('usage', {}).get('output_tokens')
            }
        }

    except ClientError as e:
        logger.error(f"Error invoking Claude model '{model_type}': {e}")
        return None


def bedrock_health_check(client=None, region: str = "us-east-1") -> bool:
    """Check if Bedrock Claude client is functioning properly.

    Args:
        client: Optional existing client (creates new one if not provided)
        region: AWS region for client creation

    Returns:
        True if healthy, False otherwise

    Example:
        if bedrock_health_check():
            print("Claude via Bedrock is ready")
    """
    try:
        if client is None:
            client = create_bedrock_client(region=region)

        response = invoke_claude(
            client=client,
            prompt="Say 'OK'",
            max_tokens=10
        )
        return bool(response)
    except Exception:
        return False
