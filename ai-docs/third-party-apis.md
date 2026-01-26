# Third-Party API Documentation

**Last Updated**: 2025-11-12

> **NOTE**: This file contains examples from a reference e-commerce project (PayPal, Printful, Solana blockchain, MongoDB). These serve as templates for how to document YOUR project's third-party integrations. Replace or remove sections as appropriate for your actual project.

This document contains integration details for all external APIs and services used in the project.

---

## PayPal REST SDK

**Purpose**: Payment processing for traditional fiat currency transactions

**Environment Variables**:
- `PAYPAL_MODE` - "sandbox" or "live"
- `PAYPAL_CLIENT_KEY` - OAuth client ID
- `PAYPAL_SECRET_KEY` - OAuth secret

**Implementation Location**:
- Backend: [backend/controller/paymentController.js](../backend/controller/paymentController.js)
- Routes: [backend/routes/paymentRoute.js](../backend/routes/paymentRoute.js)

**Key Endpoints Used**:
- `paypal.payment.create()` - Initialize payment
- `paypal.payment.execute()` - Complete payment after user approval

**Flow**:
1. Frontend initiates payment → Backend creates PayPal payment
2. User redirects to PayPal approval URL
3. Success: Returns to `http://localhost:5173/success` with `PayerID` and `paymentId`
4. Cancel: Returns to `http://localhost:5173/cancel`

**Rate Limits**: Standard PayPal sandbox/live limits apply

**Error Handling**:
- Check `error.response` for PayPal API errors
- Log payment failures to console (consider structured logging)

**Testing**:
- Use PayPal sandbox credentials for development
- Test with sandbox test accounts

**Documentation**: https://developer.paypal.com/docs/api/payments/v1/

---

## Printful API

**Purpose**: Print-on-demand product fulfillment and order management

**Environment Variables**:
- `PRINTFUL_API_KEY` - Bearer token for API authentication

**Implementation Location**:
- Backend: [backend/controller/printfulService.js](../backend/controller/printfulService.js)
- Routes: [backend/routes/printfulRoute.js](../backend/routes/printfulRoute.js)

**Base URL**: `https://api.printful.com`

**Key Endpoints**:
- `GET /store/products` - List all store products
- `GET /store/products/{id}` - Get single product details
- `POST /orders` - Create new order
- `GET /orders` - List all orders
- `GET /orders/{id}` - Get specific order
- `PUT /orders/{id}` - Update order
- `DELETE /orders/{id}` - Cancel order

**Authentication**: Bearer token in Authorization header

**Rate Limits**:
- Standard: 120 requests per minute
- Consider implementing request throttling for bulk operations

**Error Handling**:
- All methods wrap errors with descriptive messages
- Original error included in thrown Error message

**Documentation**: https://developers.printful.com/docs/

---

## Solana Blockchain (@solana/web3.js)

**Purpose**: Cryptocurrency payment processing via Solana network

**Package**: `@solana/web3.js` v1.95.4

**Implementation Location**:
- Frontend: Integrated in cart/payment flow
- Backend: Transaction verification (check payment controller)

**Key Concepts**:
- **Wallet Connection**: User connects Solana wallet (Phantom, Solflare, etc.)
- **Transaction Signing**: Frontend creates and signs transactions
- **Verification**: Backend verifies transaction on Solana blockchain

**Network Endpoints**:
- Mainnet: `https://api.mainnet-beta.solana.com`
- Devnet: `https://api.devnet.solana.com` (use for testing)
- Testnet: `https://api.testnet.solana.com`

**Rate Limits**:
- Public RPC nodes have rate limits
- Consider using dedicated RPC provider (QuickNode, Alchemy, etc.) for production

**Security Considerations**:
- Never store private keys in code or env variables
- Always verify transactions on backend before fulfilling orders
- Implement transaction confirmation checking (await finalization)

**Testing**:
- Use Solana devnet for development
- Request SOL from devnet faucet for testing
- Test with multiple wallet providers

**Documentation**: https://solana.com/docs

---

## Socket.io

**Purpose**: Real-time bidirectional communication (likely for order status updates)

**Package**: `socket.io-client` v4.8.1 (both frontend and backend)

**Implementation Status**: Library included, implementation details TBD

**Typical Use Cases**:
- Real-time order status updates
- Live inventory updates
- Cart synchronization across devices
- Admin dashboard live notifications

**Connection**: Backend should expose Socket.io server, frontend connects as client

**Documentation**: https://socket.io/docs/v4/

---

## MongoDB Atlas

**Purpose**: Primary database for user data, products, carts, and orders

**Environment Variables**:
- `DATABASE_URL` - MongoDB connection string (Atlas cluster)

**Connection Options**:
```javascript
{
  useNewUrlParser: true,
  useFindAndModify: false,
  useUnifiedTopology: true
}
```

**Models**:
- User - Authentication and profile data
- Product - Product catalog
- Cart - Shopping cart persistence

**Indexes**: Review and add indexes for frequently queried fields

**Backup Strategy**: Ensure Atlas automated backups are enabled

**Documentation**: https://www.mongodb.com/docs/atlas/

---

## Notes for AI Agents

- Always check environment variables are set before making API calls
- Implement proper error handling and logging for all external calls
- Consider implementing retry logic for transient failures
- Keep API response data structures documented if complex
- Update this document when adding new integrations or changing existing ones
