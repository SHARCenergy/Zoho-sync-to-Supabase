# Zoho-Supabase Sync Service

A Python-based service that synchronizes data between Zoho applications (FSM, CRM, Inventory) and Supabase database.

## 🎯 Current Status: ✅ WORKING

- ✅ **Supabase Connection**: Working
- ✅ **Database Schema**: Complete (schemas, tables, functions)
- ✅ **API Endpoints**: Functional
- ✅ **Data Retrieval**: Working
- ✅ **Sync Status**: Working
- 🔄 **Ready for Zoho Integration**: Database is ready for data sync

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- Supabase account
- Zoho API credentials

### Setup Instructions

#### 1. Environment Setup
```bash
# Copy environment template
cp env.example .env

# Edit .env with your credentials
# - SUPABASE_URL
# - SUPABASE_SERVICE_ROLE_KEY  
# - SUPABASE_ANON_KEY
# - ZOHO_CLIENT_ID
# - ZOHO_CLIENT_SECRET
# - ZOHO_REFRESH_TOKEN
# - ZOHO_ORG_ID
```

#### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

#### 3. Database Setup (COMPLETED)
**✅ Database is already set up and working!**

The following have been completed:
- ✅ Schemas created (`zoho_fsm`, `zoho_crm`, `zoho_inventory`)
- ✅ Tables created in all schemas
- ✅ Database functions created and working
- ✅ Permissions configured correctly

#### 4. Start the Service
```bash
python main.py
```

#### 5. Test the API
```bash
python test_api.py
```

## 📊 Database Schema

### Schemas
- `zoho_fsm` - Field Service Management data
- `zoho_crm` - Customer Relationship Management data  
- `zoho_inventory` - Inventory management data

### Tables (in each schema)
- `work_orders` - Service work orders
- `service_appointments` - Scheduled appointments
- `customers` - Customer information
- `technicians` - Technician profiles
- `sync_status` - Sync tracking (FSM schema only)

## 🔌 API Endpoints

- `GET /health` - Health check ✅
- `GET /sync/status` - Get sync status ✅
- `POST /sync/start` - Start manual sync ✅
- `GET /data/{schema}/{table}` - Get data from specific table ✅
- `GET /data/{schema}/{table}/{record_id}` - Get specific record ✅

## 🔍 Monitoring

- **Logs**: Check `sync.log` for detailed sync operations
- **API Health**: `http://localhost:8000/health`
- **Sync Status**: `http://localhost:8000/sync/status`

## 🛠️ Troubleshooting

### Common Issues

1. **"permission denied for schema"**
   - ✅ **RESOLVED**: Permissions are correctly configured

2. **"relation does not exist"**
   - ✅ **RESOLVED**: All schemas and tables exist

3. **"function not found"**
   - ✅ **RESOLVED**: All database functions are working

4. **API not responding**
   - Check if `main.py` is running
   - Verify port 8000 is available
   - Check logs for errors

### Diagnostic Commands
```bash
# Test database connection
python test_connection.py

# Test data retrieval
python test_simple_data.py

# Test API endpoints
python test_api.py

# Check sync status
curl http://localhost:8000/sync/status
```

## 📁 Project Structure

```
├── src/
│   ├── api.py              # FastAPI endpoints
│   ├── config.py           # Configuration settings
│   ├── supabase_client.py  # Supabase database client
│   ├── sync_manager.py     # Sync orchestration
│   └── zoho_client.py      # Zoho API client
├── main.py                 # Application entry point
├── test_api.py            # API testing script
├── test_connection.py     # Database connection test
├── test_simple_data.py    # Data retrieval test
├── requirements.txt       # Python dependencies
└── *.sql                 # Database setup scripts
```

## 🔄 Sync Process

1. **Initialization**: ✅ Creates schemas and validates connections
2. **Zoho → Supabase**: Ready to fetch data from Zoho APIs and store in Supabase
3. **Supabase → Zoho**: Ready to sync changes back to Zoho (if configured)
4. **Status Tracking**: ✅ Maintains sync status and error handling

## 📝 Development

### Adding New Tables
1. Add table definition to `create_schemas_and_tables.sql`
2. Update sync logic in `sync_manager.py`
3. Add API endpoints in `api.py`

### Environment Variables
See `env.example` for all required environment variables.

## 🆘 Support

If you encounter issues:
1. Check the troubleshooting section above
2. Review `sync.log` for detailed error messages
3. Run diagnostic commands to isolate the problem
4. The database setup is complete and working

## 🎉 Success!

Your Zoho-Supabase sync service is now fully functional! The database is ready to receive data from Zoho APIs, and all API endpoints are working correctly.