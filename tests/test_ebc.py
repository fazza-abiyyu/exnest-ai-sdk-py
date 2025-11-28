import pytest
from unittest.mock import Mock, AsyncMock, patch
from exnestai.client import ExnestAI
from exnestai.models import ExnestMessage, EBCDecisionContext, ExnestChatResponse

@pytest.fixture
def client():
    return ExnestAI(api_key="test-key")

@pytest.mark.asyncio
async def test_deep_think(client):
    mock_response = {
        "id": "chatcmpl-123",
        "object": "chat.completion",
        "created": 1677652288,
        "model": "gpt-4",
        "choices": [{
            "index": 0,
            "message": {
                "role": "assistant",
                "content": "Deep thought result"
            },
            "finish_reason": "stop"
        }],
        "usage": {
            "prompt_tokens": 9,
            "completion_tokens": 12,
            "total_tokens": 21
        }
    }
    
    with patch.object(client, '_execute_request', new_callable=AsyncMock) as mock_request:
        mock_request.return_value = mock_response
        
        messages = [ExnestMessage(role="user", content="Think deeply")]
        response = await client.deep_think(messages)
        
        assert isinstance(response, ExnestChatResponse)
        assert response.choices[0]['message']['content'] == "Deep thought result"
        mock_request.assert_called_once()
        args, kwargs = mock_request.call_args
        assert args[1] == "/ebc/deep-think"
        assert args[2]['messages'][0]['content'] == "Think deeply"

@pytest.mark.asyncio
async def test_structured_decision(client):
    mock_response = {
        "id": "chatcmpl-124",
        "object": "chat.completion",
        "choices": [{
            "index": 0,
            "message": {
                "role": "assistant",
                "content": "Decision result"
            },
            "finish_reason": "stop"
        }]
    }
    
    with patch.object(client, '_execute_request', new_callable=AsyncMock) as mock_request:
        mock_request.return_value = mock_response
        
        messages = [ExnestMessage(role="user", content="Make a decision")]
        context = EBCDecisionContext(
            decisionType="hiring",
            criteria=["experience", "skills"],
            constraints=["budget"],
            preferences={"remote": True}
        )
        
        response = await client.structured_decision(messages, context)
        
        assert isinstance(response, ExnestChatResponse)
        assert response.choices[0]['message']['content'] == "Decision result"
        mock_request.assert_called_once()
        args, kwargs = mock_request.call_args
        assert args[1] == "/decision-making/session"
        assert args[2]['context']['decisionType'] == "hiring"

@pytest.mark.asyncio
async def test_delegate(client):
    mock_response = {
        "id": "chatcmpl-125",
        "object": "chat.completion",
        "choices": [{
            "index": 0,
            "message": {
                "role": "assistant",
                "content": "Delegation result"
            },
            "finish_reason": "stop"
        }]
    }
    
    with patch.object(client, '_execute_request', new_callable=AsyncMock) as mock_request:
        mock_request.return_value = mock_response
        
        messages = [ExnestMessage(role="user", content="Delegate this")]
        response = await client.delegate(messages)
        
        assert isinstance(response, ExnestChatResponse)
        assert response.choices[0]['message']['content'] == "Delegation result"
        mock_request.assert_called_once()
        args, kwargs = mock_request.call_args
        assert args[1] == "/ebc/delegate"
