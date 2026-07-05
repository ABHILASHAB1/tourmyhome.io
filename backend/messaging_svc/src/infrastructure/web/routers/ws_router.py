from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Depends
import json
from src.infrastructure.web.connection_manager import manager
from src.application.use_cases.send_message import SendMessageUseCase

router = APIRouter(prefix="/ws", tags=["messaging"])

@router.websocket("/{user_id}")
async def websocket_endpoint(websocket: WebSocket, user_id: str):
    await manager.connect(user_id, websocket)
    use_case = SendMessageUseCase()
    
    try:
        while True:
            # Receive raw text from the client
            data_str = await websocket.receive_text()
            
            try:
                data = json.loads(data_str)
                recipient_id = data.get("recipient_id")
                listing_id = data.get("listing_id")
                content = data.get("content")
                
                if not recipient_id or not content:
                    await websocket.send_json({"error": "Missing recipient_id or content"})
                    continue
                
                # Execute Use Case
                sent_msg = await use_case.execute(
                    sender_id=user_id,
                    recipient_id=recipient_id,
                    listing_id=listing_id,
                    content=content
                )
                
                # Acknowledge to sender
                await websocket.send_json({
                    "status": "delivered",
                    "message_id": sent_msg["id"]
                })
                
            except json.JSONDecodeError:
                await websocket.send_json({"error": "Invalid JSON format"})
            except ValueError as ve:
                await websocket.send_json({"error": str(ve)})
                
    except WebSocketDisconnect:
        manager.disconnect(user_id)
