# Implementation Notes

**Last Updated**: 2025-11-12

> **NOTE**: This file contains examples from a reference e-commerce project (React/Vite, Redux Toolkit, Express, MongoDB, PayPal/Solana payments). These serve as templates for documenting YOUR project's implementation decisions. Replace with your actual architectural decisions, performance considerations, and lessons learned.

This document contains technical rationale, design decisions, troubleshooting guides, and lessons learned during development.

---

## Architectural Decisions

### Why Redux Toolkit Over Context API?

**Decision**: Use Redux Toolkit for all global state management

**Rationale**:
- Complex state interactions (cart, auth, products all interconnected)
- Built-in async handling with createAsyncThunk
- Redux DevTools for debugging
- Predictable state updates with reducers
- Better performance with selective subscriptions

**Trade-offs**: Slightly more boilerplate, but worth it for maintainability

### Why Vite Over Create React App?

**Decision**: Use Vite as the build tool

**Rationale**:
- Significantly faster dev server startup
- Lightning-fast HMR (Hot Module Replacement)
- Better out-of-the-box TypeScript support
- Smaller production bundles
- Modern ESM-based approach

**Migration Note**: CRA is effectively deprecated; Vite is the React team's recommended approach

### Dual Cart Storage (Redux + localStorage)

**Decision**: Persist cart state in both Redux store and localStorage

**Rationale**:
- Survives page refreshes without backend persistence
- Works offline
- Reduces database load for anonymous users
- Instant cart state on app reload

**Implementation Detail**:
- Cart loads from localStorage on app initialization
- Every cart action updates both Redux and localStorage synchronously
- Prevents race conditions by updating in single function

**Trade-off**: 5MB localStorage limit could be an issue for extreme cart sizes (unlikely in practice)

### Mongoose Deprecated Options

**Current State**: Using deprecated Mongoose connection options
```javascript
mongoose.set('useFindAndModify', false);
mongoose.set('useUnifiedTopology', true);
```

**Issue**: These options are no longer needed in Mongoose 6+

**TODO**: Upgrade Mongoose to v6+ and remove deprecated options

**Impact**: No functional issues currently, but should be addressed before production

### PayPal vs Crypto Payments

**Decision**: Support both traditional (PayPal) and crypto (Solana) payment methods

**Rationale**:
- Broader market reach (not everyone has crypto)
- Hedge against crypto volatility
- PayPal provides buyer protection (reduces disputes)
- Crypto offers lower fees and faster settlement

**Implementation Status**:
- PayPal: Fully implemented via PayPal REST SDK
- Solana: Libraries included, implementation needs verification

---

## Performance Considerations

### Frontend Bundle Size

**Current Approach**: No code splitting implemented

**Recommended Optimization**:
```typescript
// Lazy load pages
const Catalog = lazy(() => import('./pages/Catalog'));
const Product = lazy(() => import('./pages/Product'));

// Wrap routes with Suspense
<Suspense fallback={<LoadingSpinner />}>
  <RouterProvider router={router} />
</Suspense>
```

**Impact**: Initial bundle size reduction of ~30-40%

### Redux State Normalization

**Current State**: Product and cart data stored as arrays

**Potential Optimization**: Normalize data with IDs as keys
```typescript
// Instead of
products: Product[]

// Use
products: {
  byId: { [id: string]: Product },
  allIds: string[]
}
```

**Benefit**: O(1) lookups instead of O(n) array searches

**When to Implement**: When product catalog exceeds ~100 items

### Image Optimization

**Current State**: No image optimization pipeline

**Recommendation**:
- Use WebP format with fallbacks
- Implement lazy loading for product images
- Consider CDN for image hosting (Cloudinary, Imgix)
- Add responsive image sizes

**Impact**: 50-70% reduction in image transfer size

---

## Security Considerations

### Environment Variable Exposure

**CRITICAL ISSUE**: `.env` file with production credentials currently in repository

**Immediate Action Required**:
1. Remove `.env` from git history: `git filter-branch` or BFG Repo-Cleaner
2. Rotate all exposed credentials (PayPal, Printful, MongoDB)
3. Ensure `.env` is in `.gitignore`
4. Use `.env.example` with dummy values for documentation

**Pattern for New Services**:
```bash
# .env.example (commit this)
PAYPAL_CLIENT_KEY=your_key_here
PAYPAL_SECRET_KEY=your_secret_here

# .env (NEVER commit this)
PAYPAL_CLIENT_KEY=actual_production_key
PAYPAL_SECRET_KEY=actual_production_secret
```

### CORS Configuration

**Current State**: Hardcoded to `http://localhost:5173`

**Production Issue**: Will block all production frontend requests

**Solution**:
```javascript
// Use environment variable for allowed origins
const allowedOrigins = process.env.CORS_ORIGINS?.split(',') || ['http://localhost:5173'];

app.use(cors({
  origin: (origin, callback) => {
    if (!origin || allowedOrigins.includes(origin)) {
      callback(null, true);
    } else {
      callback(new Error('Not allowed by CORS'));
    }
  },
  credentials: true
}));
```

### JWT Token Storage

**Current Implementation**: Details not yet verified in codebase

**Best Practices**:
- Store access tokens in memory (React state)
- Store refresh tokens in httpOnly cookies
- Never store tokens in localStorage (XSS vulnerability)
- Implement token refresh before expiration

### Crypto Payment Verification

**CRITICAL**: Always verify Solana transactions on backend

**Pattern**:
```javascript
// Backend verification is REQUIRED
const verifyPayment = async (txSignature, expectedAmount) => {
  const connection = new Connection(clusterApiUrl('mainnet-beta'));

  // Wait for confirmation
  const confirmation = await connection.confirmTransaction(txSignature);
  if (!confirmation.value) {
    throw new Error('Transaction not confirmed');
  }

  // Fetch transaction details
  const tx = await connection.getTransaction(txSignature);

  // Verify amount and recipient
  // Only mark order as paid if verification passes
};
```

**Never trust frontend**: User can manipulate any frontend code

---

## Common Issues and Solutions

### Issue: "Cannot find module" errors after npm install

**Cause**: Stale node_modules or package-lock.json

**Solution**:
```bash
rm -rf node_modules package-lock.json
npm install
```

### Issue: TypeScript errors in third-party libraries

**Cause**: Missing type definitions

**Solution**:
```bash
npm install --save-dev @types/library-name
```

If no types available:
```typescript
// Create a declaration file: src/types/library-name.d.ts
declare module 'library-name';
```

### Issue: MongoDB connection timeout

**Possible Causes**:
1. Network restrictions (firewall, VPN)
2. MongoDB Atlas IP whitelist doesn't include your IP
3. Invalid connection string

**Solution**:
- Check MongoDB Atlas network access settings
- Add your IP to whitelist (or use 0.0.0.0/0 for development)
- Verify DATABASE_URL in .env

### Issue: Vite dev server not hot reloading

**Cause**: File watcher limit exceeded (Linux/Mac)

**Solution (Linux)**:
```bash
echo fs.inotify.max_user_watches=524288 | sudo tee -a /etc/sysctl.conf
sudo sysctl -p
```

**Solution (Mac)**:
```bash
# Usually not an issue on Mac, but check:
ulimit -n 10240
```

### Issue: CORS errors in development

**Cause**: Frontend and backend on different ports

**Check**:
1. Backend CORS allows `http://localhost:5173`
2. Frontend axios config points to `http://localhost:8765`
3. Both servers are running

---

## Database Design Notes

### Product Schema

**Current Schema**:
```javascript
{
  title: String,
  price: Number,
  description: String,
  image: String,
  category: String,
  quantity: Number,
  timestamps: true
}
```

**Potential Improvements**:
- Add `sku` field for inventory tracking
- Add `variants` array for size/color options
- Add `images` array instead of single image
- Add `tags` array for better search
- Add soft delete flag instead of hard delete

### Cart Schema

**Note**: Cart schema exists but implementation details not yet reviewed

**Considerations**:
- Should cart be per-user or per-session?
- How long should abandoned carts persist?
- Should cart items link to product IDs or snapshot product data?

**Recommendation**: Snapshot product data (price, name) at add-to-cart time to handle product updates

---

## Third-Party Integration Notes

### Printful Integration

**Use Case**: Print-on-demand fulfillment

**Workflow**:
1. Customer orders product
2. Payment processed (PayPal or crypto)
3. Backend creates Printful order
4. Printful fulfills and ships
5. Tracking info sent back to backend
6. Customer notified

**Consideration**: Printful requires product setup in their dashboard first

**API Wrapper**: [backend/controller/printfulService.js](../backend/controller/printfulService.js) provides clean interface

### Socket.io Implementation

**Current Status**: Library installed but implementation incomplete

**Recommended Use Cases**:
- Real-time order status updates
- Admin notifications for new orders
- Inventory level warnings
- Cart synchronization across devices (same user, multiple tabs)

**Implementation Pattern**:
```javascript
// Backend
const io = require('socket.io')(server, {
  cors: { origin: 'http://localhost:5173' }
});

io.on('connection', (socket) => {
  socket.on('order:update', (data) => {
    io.to(data.userId).emit('order:status', data);
  });
});

// Frontend
import io from 'socket.io-client';
const socket = io('http://localhost:8765');

socket.on('order:status', (data) => {
  // Update UI with real-time order status
});
```

---

## Testing Strategy

### Current Test Coverage

**Backend**: Basic tests exist in `__test__/` directory
- user.spec.js
- product.spec.js
- cart.spec.js

**Frontend**: No tests currently implemented

**Gap Analysis**:
- No integration tests
- No E2E tests
- No payment flow tests
- No crypto transaction tests

### Recommended Testing Additions

**Frontend Unit Tests** (Jest + React Testing Library):
```bash
npm install --save-dev @testing-library/react @testing-library/jest-dom
```

**E2E Tests** (Playwright or Cypress):
- Full checkout flow
- Payment processing (use test credentials)
- User registration and login

**Backend Integration Tests**:
- Test external API integrations with mocked responses
- Test database operations with test database

---

## Deployment Considerations

### Environment-Specific Configs

**Development**:
- Frontend: http://localhost:5173 (Vite dev server)
- Backend: http://localhost:8765 (Express with nodemon)
- Database: MongoDB Atlas (development cluster)

**Production TODO**:
- [ ] Set up production MongoDB cluster
- [ ] Configure production PayPal credentials
- [ ] Set up production Solana RPC endpoint
- [ ] Configure CDN for static assets
- [ ] Set up proper logging (not console.log)
- [ ] Implement rate limiting
- [ ] Set up health check endpoints
- [ ] Configure SSL/TLS certificates

### Docker Configuration

**Status**: No Dockerfile or docker-compose.yml found

**Recommendation**: Create containerized deployment
```dockerfile
# Example structure needed
FROM node:18-alpine
WORKDIR /app
COPY package*.json ./
RUN npm ci --only=production
COPY . .
EXPOSE 8765
CMD ["npm", "start"]
```

### Build Process

**Frontend**:
```bash
cd frontend
npm run build  # Outputs to frontend/dist
```

**Backend**:
- No build step needed (Node.js runtime)
- Ensure all dependencies are production-ready

---

## Future Enhancements

### Short Term
- Implement Socket.io for real-time features
- Complete Solana payment integration with verification
- Add comprehensive error logging (Winston, Pino)
- Implement request rate limiting
- Add frontend loading skeletons
- Improve mobile responsiveness

### Medium Term
- Add product search and filtering
- Implement user reviews and ratings
- Add wishlist functionality (page exists, needs backend)
- Implement order tracking
- Add email notifications (SendGrid, Mailgun)

### Long Term
- Multi-language support (i18n)
- Multiple cryptocurrency support (Bitcoin, Ethereum)
- Advanced analytics dashboard
- Social media integration
- Referral program
- Loyalty points system

---

## Notes for AI Agents

When troubleshooting issues:

1. **Check Logs First**: Look at console output for both frontend and backend
2. **Verify Environment**: Ensure all .env variables are set correctly
3. **Network Tab**: Use browser DevTools Network tab for API issues
4. **Redux DevTools**: Use Redux DevTools extension to inspect state
5. **Database State**: Verify MongoDB data directly if issues persist
6. **Version Compatibility**: Check package versions match requirements

When adding new features:

1. **Update This Document**: Add new patterns, decisions, and gotchas
2. **Consider Security**: Review security implications of new code
3. **Test Thoroughly**: Test both happy path and error cases
4. **Document APIs**: Update api-docs if adding new endpoints
5. **Consider Performance**: Think about scale and optimization
