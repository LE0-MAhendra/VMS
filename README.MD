# Vendor Management System

This is a backend API project for a Vendor Management System. It provides APIs for managing vendors, purchase orders, and vendor performance metrics.

## Installation

1. Clone the repository:

   ```bash
   https://github.com/LE0-MAhendra/VMS.git
   ```

2. Navigate to the project directory:

   ```bash
   cd vms
   ```

3. Create and activate a virtual environment:

   ```bash
   python -m venv venv
   source venv/bin/activate   # On Windows, use `venv\Scripts\activate`
   ```

4. Install dependencies using `pip` and the `requirements.txt` file:

   ```bash
   pip install -r requirements.txt
   ```

5. check the `.env.copy` file add the required values as per your usage and change the file name to `.env.copy` to `.env.local`

## Usage

Run the following commands to set up and run the project:

```bash
python manage.py makemigrations
python manage.py migrate
python manage.py runserver
```

Visit [http://localhost:8000/](http://localhost:8000/) in your browser.

### API Endpoints

#### For Vendor

- **POST /api/vendors/:** Create a new vendor.
- **GET /api/vendors/:** List all vendors.
- **GET /api/vendors/{vendor_id}/:** Retrieve a specific vendor's details.
- **PUT /api/vendors/{vendor_id}/:** Update a vendor's details.
- **DELETE /api/vendors/{vendor_id}/:** Delete a vendor.

#### For Purchase Order

- **POST /api/purchase_orders/:** Create a purchase order.
- **GET /api/purchase_orders/:** List all purchase orders with an option to filter by vendor.
- **GET /api/purchase_orders/{po_id}/:** Retrieve details of a specific purchase order.
- **PUT /api/purchase_orders/{po_id}/:** Update a purchase order.
- **DELETE /api/purchase_orders/{po_id}/:** Delete a purchase order.

#### For Vendor Performance

- **GET /api/vendors/{vendor_id}/performance:** Retrieve a vendor's performance metrics.

#### For Update Acknowledgment

- **POST /api/purchase_orders/{po_id}/acknowledge**

## Configuration

please read through the steps to work with the api`s and if additional configuration is required please inform me through my profile.

# Thankyou
