# PoToken Configuration Guide

## Overview
PoToken (Proof of Origin Token) is YouTube's anti-bot protection mechanism. This service supports two modes to handle PoToken for reliable YouTube access.

## Configuration Modes

### 1. AUTO Mode (Default)
Uses pytubefix's automatic PoToken generation with WEB client.

**Environment Variables:**
```bash
PO_TOKEN_MODE=AUTO
```

**Requirements:**
- Requires Node.js in the container/environment
- pytubefix automatically generates tokens using the WEB client

**Advantages:**
- No manual token extraction needed
- Automatically refreshes tokens
- Simplest setup

### 2. MANUAL Mode
Uses manually extracted PoToken and visitorData from browser.

**Environment Variables:**
```bash
PO_TOKEN_MODE=MANUAL
PO_TOKEN=your_extracted_po_token_here
VISITOR_DATA=your_visitor_data_here  # Optional but recommended
```

**How to Extract Tokens:**

1. Open YouTube in your browser
2. Open Developer Tools (F12)
3. Go to Network tab
4. Play any video
5. Look for requests to `youtubei/v1/player`
6. In the request payload, find:
   - `serviceIntegrityDimensions.poToken` - This is your PO_TOKEN
   - `context.client.visitorData` - This is your VISITOR_DATA

**Advantages:**
- Works without Node.js
- More control over token lifecycle
- Can use tokens from specific browser sessions

**Disadvantages:**
- Tokens may expire and need manual refresh
- Requires browser-based extraction

## Kubernetes Deployment

Update your `dynaforge-values.yaml`:

```yaml
env:
  - name: PO_TOKEN_MODE
    value: "AUTO"  # or "MANUAL"
  - name: PO_TOKEN
    value: ""  # Only needed for MANUAL mode
  - name: VISITOR_DATA
    value: ""  # Optional for MANUAL mode
```

## Docker Configuration

For Docker deployments:

```bash
# AUTO mode (default)
docker run -e PO_TOKEN_MODE=AUTO your-image

# MANUAL mode
docker run \
  -e PO_TOKEN_MODE=MANUAL \
  -e PO_TOKEN=your_token \
  -e VISITOR_DATA=your_visitor_data \
  your-image
```

## Status Endpoint

Check current PoToken configuration:

```bash
curl http://your-service/
```

Response:
```json
{
  "message": "YouTube to MP3 Service",
  "status": "running",
  "po_token": {
    "mode": "AUTO",
    "po_token_configured": false,
    "visitor_data_configured": false
  }
}
```

## Troubleshooting

### 403 Errors
If you get 403 errors, try:
1. Switch to MANUAL mode with fresh tokens
2. Ensure Node.js is available for AUTO mode
3. Check token expiration in MANUAL mode

### Token Extraction Issues
- Make sure you're extracting from actual player requests, not other YouTube API calls
- Tokens are base64-encoded strings, quite long
- visitorData is optional but improves success rate

## Security Notes
- Keep PoTokens secure - they're tied to your browser session
- Tokens may expire, requiring periodic refresh in MANUAL mode
- AUTO mode handles refresh automatically but needs Node.js runtime