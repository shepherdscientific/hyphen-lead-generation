# Custom Patterns and Conventions

**Last Updated**: 2025-11-12

> **NOTE**: This file contains examples from a reference e-commerce project using React/Redux/Express/MongoDB/Solana. These patterns serve as templates for documenting YOUR project's conventions. Adapt, replace, or remove sections based on your actual tech stack and patterns.

This document describes project-specific patterns, conventions, and architectural decisions that should be followed throughout the codebase.

---

## Frontend Patterns

### State Management Architecture

**Redux Toolkit Slice Pattern**:

All Redux slices follow a consistent structure:

```typescript
// 1. Define State Interface
interface FeatureState {
  data: DataType[];
  isError: boolean;
  isSuccess: boolean;
  isLoading: boolean;
  status: string;
}

// 2. Define Async Thunks
export const fetchData = createAsyncThunk(
  "feature/fetch",
  async (params, thunkAPI) => {
    try {
      return await featureService.fetch(params);
    } catch (error) {
      return thunkAPI.rejectWithValue(error);
    }
  }
);

// 3. Create Slice with reducers
const featureSlice = createSlice({
  name: "feature",
  initialState,
  reducers: {
    // synchronous actions
  },
  extraReducers: (builder) => {
    // async thunk handlers
  }
});
```

**Current Slices**:
- `authSlice` - [frontend/src/features/auth/authSlice.ts](../frontend/src/features/auth/authSlice.ts)
- `cartSlice` - [frontend/src/features/cart/cartSlice.ts](../frontend/src/features/cart/cartSlice.ts)
- `productSlice` - [frontend/src/features/product/productSlice.ts](../frontend/src/features/product/productSlice.ts)

### Dual Storage Pattern for Cart

**Pattern**: Cart state is persisted in both Redux and localStorage for offline resilience.

```typescript
// Load from localStorage on initialization
const loadCartFromLocalStorage = (): CartState => {
  const cart = localStorage.getItem('cart');
  const totalItems = localStorage.getItem('totalQuantity');
  return {
    cartItems: cart ? JSON.parse(cart) : [],
    totalItems: totalItems ? parseInt(totalItems, 10) : 0,
    // ... other state
  };
};

// Update localStorage on every cart mutation
const updateLocalStorage = (cartItems: CartItem[]) => {
  const totalQuantity = cartItems.reduce((acc, item) => acc + item.quantity, 0);
  localStorage.setItem('cart', JSON.stringify(cartItems));
  localStorage.setItem('totalQuantity', totalQuantity.toString());
};
```

**When to Use**: Apply this pattern for any user data that should persist across sessions without requiring authentication.

### React Router v6 Pattern

**Nested Routes Structure**:

```typescript
export const router = createBrowserRouter([
  {
    path: "/",
    element: <App />,  // Layout component
    children: [
      { path: "", element: <Home /> },
      { path: "catalog", element: <Catalog /> },
      { path: "products/:id", element: <Product /> },
      { path: "cart", element: <Cart /> },
      { path: "*", element: <Navigate to="/" /> }
    ]
  }
]);
```

**Convention**: All authenticated routes should be defined as children of the App layout component, which handles common layout (header, footer, navigation).

### TypeScript Path Aliases

**Vite Config Aliases**:
```typescript
resolve: {
  alias: {
    '@': path.resolve(__dirname, 'src'),
    components: path.resolve('src/components/'),
    hooks: path.resolve('src/hooks/'),
    data: path.resolve('src/data/'),
  }
}
```

**Usage**:
```typescript
// Preferred
import { useAuth } from '@/hooks/useAuth';
import Button from 'components/Button';

// Avoid
import { useAuth } from '../../../hooks/useAuth';
```

### SCSS + Tailwind Hybrid Approach

**Pattern**: Use Tailwind for utility classes, SCSS for component-specific styling and global variables.

**Global SCSS Variables**: [frontend/src/variables.scss](../frontend/src/variables.scss)
- Automatically imported in all SCSS files via Vite config
- Define project-wide colors, spacing, breakpoints here

**Component Pattern**:
```tsx
// Use Tailwind for layout and common utilities
<div className="flex items-center justify-between p-4">
  {/* Use SCSS modules for complex component-specific styles */}
  <button className={styles.customButton}>Click me</button>
</div>
```

### Toast Notifications Pattern

**Library**: `react-toastify`

**Standard Usage**:
```typescript
import { toast } from 'react-toastify';

// Success
toast.success("Item added to cart");

// Error
toast.error("Failed to load products");

// Info
toast.info("Processing your request");
```

**When to Use**:
- User action confirmations (add to cart, update profile)
- API error feedback
- Success confirmations after async operations

---

## Backend Patterns

### MVC Architecture

**Strict Separation**:

```
routes/       → Define endpoints and middleware
controller/   → Business logic and orchestration
model/        → Mongoose schemas and validation
```

**Example Flow**:
```
GET /products → routes/product.js → controller/product.js → model/product.js
```

**Convention**: Each route file has a corresponding controller file with matching name.

### Express Route Organization

**Pattern**: Each domain has its own router file

```javascript
// routes/feature.js
const express = require('express');
const router = express.Router();
const controller = require('../controller/feature');

router.get('/', controller.list);
router.get('/:id', controller.getById);
router.post('/', controller.create);
router.put('/:id', controller.update);
router.delete('/:id', controller.delete);

module.exports = router;
```

**Middleware Order** (in server.js):
1. CORS
2. Static files
3. Body parsing (urlencoded, json)
4. Route handlers

### Mongoose Schema Pattern

**Standard Schema Structure**:

```javascript
const mongoose = require('mongoose');
const Schema = mongoose.Schema;

const modelSchema = new Schema({
  // Define fields with validation
  field: {
    type: String,
    required: true,
    unique: false
  }
}, {
  timestamps: true  // Always include for createdAt/updatedAt
});

module.exports = mongoose.model('ModelName', modelSchema);
```

**Conventions**:
- Always use `timestamps: true`
- Define required fields explicitly
- Use descriptive field names
- Add indexes for frequently queried fields

### Error Handling Pattern

**Async Controller Pattern**:

```javascript
const controllerMethod = async (req, res) => {
  try {
    // Business logic
    const result = await someAsyncOperation();
    res.status(200).json(result);
  } catch (error) {
    console.log(error.message);
    res.status(500).json({ error: error.message });
  }
};
```

**TODO**: Implement centralized error handling middleware.

### Environment Configuration

**Pattern**: Use dotenv with expansion for complex configs

```javascript
const dotenv = require('dotenv');
const dotenvExpand = require('dotenv-expand');
const myEnv = dotenv.config();
dotenvExpand.expand(myEnv);
```

**Convention**: Always check for environment variables at startup, fail fast if missing critical configs.

---

## API Communication Patterns

### Axios Configuration

**Centralized Config**: [frontend/src/app/axiosConfig.ts](../frontend/src/app/axiosConfig.ts)

**Pattern**: Create configured axios instance with base URL and interceptors

```typescript
import axios from 'axios';

const api = axios.create({
  baseURL: process.env.VITE_API_URL || 'http://localhost:8765',
  withCredentials: true,
  headers: {
    'Content-Type': 'application/json'
  }
});

// Add request/response interceptors
api.interceptors.request.use(/* auth token injection */);
api.interceptors.response.use(/* error handling */);

export default api;
```

### Service Layer Pattern

**Convention**: Each feature has a service file that encapsulates all API calls

```typescript
// features/product/productService.ts
const productService = {
  getAll: async () => {
    const response = await api.get('/products');
    return response.data;
  },

  getById: async (id: string) => {
    const response = await api.get(`/products/${id}`);
    return response.data;
  }
};

export default productService;
```

**Usage in Thunks**:
```typescript
export const fetchProducts = createAsyncThunk(
  "products/fetch",
  async (_, thunkAPI) => {
    try {
      return await productService.getAll();
    } catch (error) {
      return thunkAPI.rejectWithValue(error);
    }
  }
);
```

---

## Testing Patterns

### Backend Testing (Jest + Supertest)

**File Naming**: `*.spec.js` in `__test__/` directory

**Pattern**:
```javascript
const request = require('supertest');
const app = require('../server');

describe('Feature API', () => {
  it('should return 200 on GET /', async () => {
    const response = await request(app).get('/feature');
    expect(response.status).toBe(200);
  });
});
```

**Test Location**: [backend/__test__/](../backend/__test__/)

**Run Command**: `npm test` in backend directory

---

## Code Style Conventions

### TypeScript

- **Strict Mode**: Enabled - all type errors must be resolved
- **Unused Variables**: Flagged as errors (`noUnusedLocals`, `noUnusedParameters`)
- **Interface Naming**: Use descriptive names, suffix with `State`, `Props`, or type as appropriate
- **Type vs Interface**: Prefer `interface` for object shapes, `type` for unions/aliases

### Import Order

**Preferred Order**:
1. External libraries (React, Redux, etc.)
2. Internal absolute imports (using path aliases)
3. Relative imports from parent directories
4. Relative imports from current directory
5. Style imports (CSS/SCSS)

### File Naming

**Convention**:
- React Components: PascalCase (e.g., `ProductCard.tsx`)
- Utilities/Services: camelCase (e.g., `authService.ts`)
- Redux Slices: camelCase + Slice suffix (e.g., `cartSlice.ts`)
- Test Files: Match source file + `.spec` or `.test`

---

## Crypto Payment Integration Pattern

### Solana Transaction Flow

**Frontend Responsibilities**:
1. Connect to user wallet (Phantom, Solflare, etc.)
2. Create transaction with product price in SOL
3. Request user signature
4. Submit signed transaction to blockchain
5. Send transaction signature to backend for verification

**Backend Responsibilities**:
1. Receive transaction signature from frontend
2. Verify transaction on Solana blockchain
3. Check transaction amount matches order total
4. Check recipient address matches store wallet
5. Mark order as paid only after verification

**Security Pattern**:
```javascript
// NEVER trust frontend payment confirmation
// ALWAYS verify on backend by querying blockchain

const verifyTransaction = async (signature, expectedAmount, recipientAddress) => {
  const connection = new Connection(clusterApiUrl('mainnet-beta'));
  const tx = await connection.getTransaction(signature);

  // Verify amount, recipient, and confirmation status
  // Only then mark order as paid
};
```

---

## Notes for AI Agents

When implementing new features:

1. **Follow Existing Patterns**: Match the style and structure of similar existing features
2. **Maintain Consistency**: Use the same libraries and approaches already in the codebase
3. **Update Documentation**: Add new patterns here if introducing novel approaches
4. **Check All Layers**: Ensure frontend, backend, and data model changes are coordinated
5. **TypeScript Strict**: Resolve all type errors before considering work complete
