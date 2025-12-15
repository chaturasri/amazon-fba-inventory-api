# amazon-fba-inventory-api
Production-grade REST API for FBA inventory management - Amazon SDE project


Production-grade REST API for **Amazon SDE role** - simulates FBA inventory operations across multiple fulfillment centers.

## 🎯 Features
- ✅ Multi-fulfillment center inventory tracking (FC1, FC2)
- ✅ Real-time low-stock alerts (< safety threshold)
- ✅ ACID-compliant order processing
- ✅ Input validation & error handling
- ✅ Production-ready: Docker, tests, monitoring

 API Endpoints
| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/api/products` | Create product + stock allocation |
| `GET` | `/api/products` | List all products |
| `GET` | `/api/inventory/low-stock` | **FBA Low Stock Alerts** |
| `GET` | `/api/health` | Health check |
