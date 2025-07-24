# Zoho FSM to Supabase Bidirectional Sync

A comprehensive Python/FastAPI solution for bidirectional synchronization between Zoho Field Service Management (FSM) and Supabase, with support for multiple Zoho apps in separate schemas.

## Project Status

This project is currently in development. The following components are implemented:

- ✅ **Zoho FSM Authentication**: OAuth2 setup with proper FSM scopes
- ✅ **Zoho FSM Client**: Working API client with correct endpoints
- ✅ **FSM Data Access**: Verified access to Work Orders and Service Appointments
- 🔄 **Supabase Integration**: Database client and schema management (next)
- 🔄 **Sync Manager**: Bidirectional sync orchestration (next)
- 🔄 **Webhook Support**: Real-time update handling (next)
- 🔄 **Monitoring**: Sync status and error tracking (next)

## Recent Progress

### ✅ Completed (Latest Session)
1. **FSM OAuth Authentication**: Successfully configured with proper scopes
2. **API Endpoint Discovery**: Found correct FSM endpoints through testing
3. **Client Development**: Built and tested working FSM client
4. **Data Verification**: Confirmed access to real FSM data

### 🔄 Next Steps
1. **Supabase Setup**: Create database schema and tables
2. **Sync Infrastructure**: Build bidirectional sync logic
3. **Webhook Integration**: Add real-time update support
4. **Monitoring**: Add sync status tracking

## Features

- 🔄 **Bidirectional Sync**: Real-time synchronization between Zoho FSM and Supabase
- 🏗️ **Schema Separation**: Each Zoho app gets its own Supabase schema
- 🚀 **FastAPI Backend**: High-performance async API with automatic documentation
- 🔒 **Conflict Resolution**: Smart conflict detection and resolution
- 📊 **Monitoring**: Real-time sync status and error tracking
- 🔐 **Security**: Secure credential management and API key handling
- 🎯 **Webhook Support**: Real-time updates via Zoho webhooks

## Architecture

### Core Components
- **FastAPI Server**: RESTful API with automatic OpenAPI documentation
- **Zoho Client**: Async client for Zoho FSM API with OAuth2 authentication
- **Supabase Client**: Async client for Supabase with schema management
- **Sync Manager**: Orchestrates bidirectional sync with error handling
- **Background Tasks**: Non-blocking sync operations

### Data Flow
1. **Zoho → Supabase**: Poll Zoho API for changes, upsert to Supabase
2. **Supabase → Zoho**: Detect local changes, sync back to Zoho
3. **Webhooks**: Real-time updates from Zoho webhooks
4. **Conflict Resolution**: Handle conflicts based on timestamps and source

## Quick Start

### Prerequisites
- Python 3.8+
- Zoho FSM account with API access
- Supabase project
- PostgreSQL database

### Installation

1. **Clone the repository**
```bash
git clone <repository-url>
cd zoho-sync-to-supabase
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Configure environment**
```bash
cp .env.example .env
# Edit .env with your credentials (see Configuration section below)
```

4. **Set up Zoho FSM Authentication** ✅ **COMPLETED**
```bash
# FSM OAuth authentication is already configured
# Working refresh token obtained with proper FSM scopes
# FSM client tested and verified
```

5. **Set up Supabase** 🔄 **IN PROGRESS**
```sql
-- Run the SQL files in supabase/migrations/
-- This creates schemas, tables, and functions
```

6. **Start the sync service**
```bash
python main.py
```

### Configuration

#### Environment Variables
```env
# Zoho Configuration (✅ CONFIGURED)
ZOHO_CLIENT_ID=1000.3W1DWDWE6VK331JVHDE4R6UCXR59QZ
ZOHO_CLIENT_SECRET=d1facfc63fe9e7f30a038a33b4f12f6c359dd37464
ZOHO_REFRESH_TOKEN=1000.46b406330c7bc61a2b5398b3f758a54f.bd5b0487f535c43f2c9cd436c2bb5f3b
ZOHO_ORG_ID=your_org_id  # Will be obtained from API response

# Supabase Configuration (🔄 TO BE CONFIGURED)
SUPABASE_URL=your_supabase_url
SUPABASE_ANON_KEY=your_anon_key
SUPABASE_SERVICE_ROLE_KEY=your_service_role_key

# Sync Configuration
SYNC_INTERVAL=300  # 5 minutes
WEBHOOK_SECRET=your_webhook_secret
MAX_RETRIES=3
BATCH_SIZE=100

# Logging
LOG_LEVEL=INFO
LOG_FILE=sync.log
```

#### FSM API Endpoints (✅ VERIFIED)
- **Work Orders**: `https://www.zohoapis.com/fsm/v1/Work_Orders`
- **Service Appointments**: `https://www.zohoapis.com/fsm/v1/Service_Appointments`
- **Base URL**: `https://www.zohoapis.com/fsm/v1`

#### FSM Scopes (✅ CONFIGURED)
- `ZohoFSM.modules.ALL`
- `ZohoFSM.users.CREATE`
- `ZohoFSM.modules.ServiceAppointments.UPDATE`
- `ZohoFSM.users.UPDATE`
- `ZohoFSM.users.READ`
- `ZohoFSM.files.CREATE`

## API Endpoints

### Core Endpoints
- `GET /` - API information and available endpoints
- `GET /health` - Health check
- `POST /sync/trigger` - Manual sync trigger
- `GET /sync/status` - Current sync status
- `POST /sync/start` - Start continuous sync
- `POST /sync/stop` - Stop continuous sync
- `POST /webhook/zoho` - Zoho webhook endpoint
- `GET /logs` - Sync logs

### API Documentation
Once running, visit:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## Schema Structure

Each Zoho app gets its own schema in Supabase:

```
supabase/
├── zoho_fsm/           # Field Service Management
│   ├── work_orders/    # Work orders and jobs
│   ├── customers/      # Customer information
│   ├── technicians/    # Field technicians
│   └── appointments/   # Scheduled appointments
├── zoho_crm/           # Customer Relationship Management
│   ├── leads/
│   ├── contacts/
│   └── deals/
└── zoho_inventory/     # Inventory Management
    ├── products/
    ├── warehouses/
    └── transactions/
```

## Usage Examples

### Manual Sync
```bash
curl -X POST "http://localhost:8000/sync/trigger" \
     -H "Content-Type: application/json" \
     -d '{"force": true}'
```

### Check Sync Status
```bash
curl "http://localhost:8000/sync/status"
```

### Start Continuous Sync
```bash
curl -X POST "http://localhost:8000/sync/start"
```

### Python Client Example
```python
import httpx

async with httpx.AsyncClient() as client:
    # Trigger manual sync
    response = await client.post("http://localhost:8000/sync/trigger")
    
    # Get sync status
    status = await client.get("http://localhost:8000/sync/status")
    print(status.json())
```

## Monitoring

### Sync Status Dashboard
The API provides real-time sync status for all schemas and tables:
```json
{
  "zoho_fsm": {
    "work_orders": {
      "last_sync": "2024-01-15T10:30:00Z",
      "status": "success"
    },
    "customers": {
      "last_sync": "2024-01-15T10:30:00Z",
      "status": "success"
    }
  }
}
```

### Error Tracking
- Failed syncs are logged with error messages
- Retry logic with exponential backoff
- Error status tracking in database

### Logging
- Structured logging with loguru
- Log rotation (daily) and retention (7 days)
- Different log levels (DEBUG, INFO, WARNING, ERROR)

## Security

### API Security
- CORS configuration for web access
- Input validation with Pydantic models
- Error handling without exposing sensitive data

### Credential Management
- Environment variable configuration
- Secure token refresh for Zoho OAuth2
- Service role key for Supabase admin operations

### Webhook Security
- Webhook signature verification (to be implemented)
- Rate limiting for webhook endpoints
- IP whitelisting support

## Development

### Project Structure
```
zoho-sync-to-supabase/
├── src/
│   ├── __init__.py
│   ├── config.py          # Configuration management
│   ├── zoho_client.py     # Zoho API client
│   ├── supabase_client.py # Supabase client
│   ├── sync_manager.py    # Sync orchestration
│   └── api.py            # FastAPI application
├── supabase/
│   └── migrations/       # Database migrations
├── main.py              # Application entry point
├── requirements.txt     # Python dependencies
├── env.example         # Environment template
└── README.md           # This file
```

### Adding New Zoho Apps
1. Create new schema in Supabase
2. Add schema to sync manager initialization
3. Create corresponding Zoho client methods
4. Add sync logic for new data types

### Testing
```bash
# Run tests
pytest

# Run with coverage
pytest --cov=src
```

## Troubleshooting

### Common Issues

1. **Zoho Authentication Errors**
   - Verify client ID, secret, and refresh token
   - Check token expiration and refresh logic

2. **Supabase Connection Issues**
   - Verify URL and service role key
   - Check database permissions

3. **Sync Failures**
   - Check logs for specific error messages
   - Verify data format compatibility
   - Check rate limits on both APIs

### Debug Mode
Set `LOG_LEVEL=DEBUG` in `.env` for detailed logging.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## License

MIT License - see LICENSE file for details
