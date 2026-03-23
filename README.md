# Store Manager — GUI Blueprints

**Activity 3 | Group: Michael Krueger & Creed McFall**

Interactive GUI blueprints for the Store Manager application. All screens are designed to visually and logically represent how the application functions, how users navigate between screens, and how database information is displayed in the GUI.

---

## Design Standards

| Property | Value |
|---|---|
| Window size | 1280 × 800 (all screens) |
| Font | Segoe UI (regular / semibold for headings) |
| Primary color | `#2C3E50` dark blue-gray |
| Action color | `#3498DB` action buttons |
| Alert color | `#E74C3C` alerts / low stock |
| Background | `#F5F5F5` light gray |

---

## Repository Structure

```
/blueprints/       → GUI mockup images (PNG exports per screen)
/docs/             → Activity3_Blueprints.pdf
README.md          → this file
store_gui_blueprints_activity3.html  → interactive blueprint file
```

---

## Application Navigation Structure

```
Login
  ↓
Dashboard
 ├── Products
 │     └── Add / Edit Product
 ├── Categories
 ├── Suppliers
 ├── Inventory
 │     └── Receive Stock → Inventory Overview
 ├── Customers
 │     └── Customer Details
 ├── Orders
 │     └── New Order → Payment → Order Confirmation
 └── Returns
```

---

## Screen Index

| # | Screen | Description |
|---|---|---|
| 1 | Dashboard | Sales totals, orders today, low stock alerts, recent orders |
| 2 | Products list | SKU, name, category, price, quantity, status |
| 3 | Add / Edit product | Product form with category and supplier dropdowns |
| 4 | Categories | Category list and add/edit form |
| 5 | Suppliers | Supplier list and add/edit form |
| 6 | Inventory overview | Quantity on hand, reorder level, LOW/OK status |
| 7 | Receive stock | Log incoming stock with product, qty, and supplier |
| 8 | Customers | Customer list with order count |
| 9 | Customer details | Customer info and order history |
| 10 | Orders list | Order ID, customer, date, total, status |
| 11 | New order | Select customer, add products, review order items |
| 12 | Payment | Order summary, payment method, payment status |
| 13 | Order confirmation | Confirmation screen after payment |
| 14 | Returns | Log and track product returns |

---

## Explicit Screen Transitions

- Dashboard → Products (click Products in sidebar)
- Products list → Product Form (click Add Product)
- Product Form → Products list (save or cancel)
- Inventory → Receive Stock (click Receive Stock button)
- Receive Stock → Inventory Overview (confirm receipt)
- Customers → Customer Details (click Details)
- Orders → New Order (click New Order)
- New Order → Payment (click Proceed to Payment)
- Payment → Order Confirmation (click Confirm Payment)

---

## Database Table Mapping

| Table | Displayed in screen |
|---|---|
| Products | Products list, Add/Edit Product, New Order, Returns |
| Categories | Categories, Add/Edit Product (dropdown) |
| Suppliers | Suppliers, Add/Edit Product (dropdown), Receive Stock (dropdown) |
| Inventory | Inventory Overview, Receive Stock, Dashboard (low stock) |
| Customers | Customers, Customer Details, New Order (dropdown) |
| Orders | Orders list, New Order, Payment, Order Confirmation, Customer Details |
| Payments | Payment screen, Order Confirmation |
| Returns | Returns list and log form |

> Note: Inventory history table is restricted to admin users and is not shown in the GUI.

---

## Collaborators

- Michael Krueger
- Creed McFall
- Instructor: [@rkandru](https://github.com/rkandru)

---

## Commit Message Log (examples)

```
Initial commit: added dashboard and navigation blueprint
Added products and categories screen layouts
Added inventory and receive stock screens
Added customers, customer details screen
Added orders, new order, payment, confirmation flow
Added returns screen and finalized transitions
Finalized GUI blueprints for Activity 3 submission
```
