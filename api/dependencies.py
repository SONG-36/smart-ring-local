from fastapi import Header, HTTPException

async def verify_vip(x_vip_token: str = Header(default="false")):
    """
    Core Auth Dependency: Mock verification of user subscription status.
    The frontend passes X-VIP-Token in headers.
    If not 'true', trigger a 403 circuit breaker to protect expensive LLM compute.
    """
    if x_vip_token.lower() != "true":
        raise HTTPException(
            status_code=403, 
            detail="HTTP 403 Forbidden: Paywall triggered. Non-VIP users cannot access the AI coach."
        )
    return True