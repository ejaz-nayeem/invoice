1. login API
method: POST
 
API: http://localhost:8000/api/tpken/

input:
{
"username": "e",
"password":"e"
}

output: 

{
    "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTc2MTY3Njk4OSwiaWF0IjoxNzYxNTkwNTg5LCJqdGkiOiIxZTk3MzNmYmYwMzM0ZjdjYWJjZjUxMzcyODk1ZTFiOSIsInVzZXJfaWQiOiIxIn0.Jgs82ovczAwhxQXN6rb5ZPFEWzfT0Xd_2a0KI_X9TEM",
    "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzYxNjc2OTg5LCJpYXQiOjE3NjE1OTA1ODksImp0aSI6IjJhOWVlNTZmYmZkMzQ0ODFhZWRhOGIwZDVlYTYyODAyIiwidXNlcl9pZCI6IjEifQ.u8cQndHZSaMSVPyg-OoLO2SJCKJQytFg0CZc2QH5VSQ"
}

Description: simple JWT Authentication login


2. Fetch all invoices API

method:GET.

API:http://localhost:8000/invoices/

3. Fetch all invoices API
method:GET

API: http://localhost:8000/transactions/

input: N/A


output:

[
    {
        "id": 2,
        "customer_name": "John Doe",
        "status": "Pending",
        "sub_total": "190.00",
        "created_at": "2025-10-27T16:24:21.076060Z",
        "items": [
            {
                "product_name": "Product A"
            },
            {
                "product_name": "Product B"
            },
            {
                "product_name": "Product C"
            }
        ]
    },
    {
        "id": 1,
        "customer_name": "John Doe Updated",
        "status": "Paid",
        "sub_total": "250.00",
        "created_at": "2025-10-27T16:16:12.090873Z",
        "items": [
            {
                "product_name": "Product A Updated"
            },
            {
                "product_name": "Product B also updated"
            },
            {
                "product_name": "Product C"
            },
            {
                "product_name": "New Product D"
            }
        ]
    }
]

description: both API do the same work. returns all created invoices

4. specific fetch invoice API

method:GET

API: http://localhost:8000/invoices/<int:pk>/

input:N/A


output:
{
    "id": 1,
    "customer_name": "John Doe Updated",
    "customer_phone": "0987654321",
    "created_at": "2025-10-27T16:16:12.090873Z",
    "is_paid": true,
    "status": "Paid",
    "sub_total": "250.00",
    "items": [
        {
            "id": 13,
            "product_name": "Product A Updated",
            "quantity": 3,
            "amount": "50.00",
            "total_amount": "150.00"
        },
        {
            "id": 14,
            "product_name": "Product B also updated",
            "quantity": 1,
            "amount": "30.00",
            "total_amount": "30.00"
        },
        {
            "id": 15,
            "product_name": "Product C",
            "quantity": 3,
            "amount": "20.00",
            "total_amount": "60.00"
        },
        {
            "id": 16,
            "product_name": "New Product D",
            "quantity": 1,
            "amount": "10.00",
            "total_amount": "10.00"
        }
    ]
}



description: returns specified invoice with details. http://localhost:8000/invoices/1/(take int:pk=1 for example)

5. update invoice API

method:PUT
API:http://localhost:8000/invoices/<int:pk>/


input:
http://localhost:8000/invoices/5/

{
  "customer_name": "ejaz",
  "customer_phone": "00000",
  "items": [
    {
      "product_name": "Product A Updated",
      "quantity": 3,
      "amount": 50.00
    },
    {
      "product_name": "Product B",
      "quantity": 1,
      "amount": 30.00
    },
    {
      "product_name": "Product C",
      "quantity": 3,
      "amount": 20.00
    },
    {
      "product_name": "New Product D",
      "quantity": 1,
      "amount": 10.00
    }
  ]
}

output:method:GET-http://localhost:8000/invoices/5/

{
    "id": 5,
    "customer_name": "updated ejaz",
    "customer_phone": "00000",
    "created_at": "2025-10-27T19:52:25.705559Z",
    "is_paid": false,
    "status": "Pending",
    "sub_total": "250.00",
    "items": [
        {
            "id": 23,
            "product_name": "Product A Updated",
            "quantity": 3,
            "amount": "50.00",
            "total_amount": "150.00"
        },
        {
            "id": 24,
            "product_name": "Product B",
            "quantity": 1,
            "amount": "30.00",
            "total_amount": "30.00"
        },
        {
            "id": 25,
            "product_name": "Product C",
            "quantity": 3,
            "amount": "20.00",
            "total_amount": "60.00"
        },
        {
            "id": 26,
            "product_name": "New Product D",
            "quantity": 1,
            "amount": "10.00",
            "total_amount": "10.00"
        }
    ]
}

Description: updates specified invoice.

6. DELETE invoice API

method:DELETE 

API:http://localhost:8000/invoices/<int:pk>/



input:N/A.

output: N/A

Description: for validation check GET-http://localhost:8000/invoices/5/.
returns {
    "detail": "Invoice not found"
}



7. field update API.

method:PATCH. 

API: http://localhost:8000/invoices/<int:pk>/pay/

input: N/A
output: N/A


Description: 

to change the is_paid=Pending status to Paid using primary key of invoice. in this case pk=1.
http://localhost:8000/invoices/1/pay/.


8. listing API

method:GET, 
API:http://localhost:8000/paid-invoices/

input;N/A


output:
[
    {
        "id": 1,
        "customer_name": "John Doe Updated",
        "status": "Paid",
        "sub_total": "250.00",
        "created_at": "2025-10-27T16:16:12.090873Z",
        "items": [
            {
                "product_name": "Product A Updated"
            },
            {
                "product_name": "Product B also updated"
            },
            {
                "product_name": "Product C"
            },
            {
                "product_name": "New Product D"
            }
        ]
    }
]

description: list all Paid invoices only.


9. specified paid API
method:GET, 
API:http://localhost:8000/paid-invoices/<int:pk>/

input:N/A


output:
{
    "id": 1,
    "customer_name": "John Doe Updated",
    "customer_phone": "0987654321",
    "created_at": "2025-10-27T16:16:12.090873Z",
    "is_paid": true,
    "status": "Paid",
    "sub_total": "250.00",
    "items": [
        {
            "id": 13,
            "product_name": "Product A Updated",
            "quantity": 3,
            "amount": "50.00",
            "total_amount": "150.00"
        },
        {
            "id": 14,
            "product_name": "Product B also updated",
            "quantity": 1,
            "amount": "30.00",
            "total_amount": "30.00"
        },
        {
            "id": 15,
            "product_name": "Product C",
            "quantity": 3,
            "amount": "20.00",
            "total_amount": "60.00"
        },
        {
            "id": 16,
            "product_name": "New Product D",
            "quantity": 1,
            "amount": "10.00",
            "total_amount": "10.00"
        }
    ]
}

description: list specified Paid invoice only with details.in this case int:pk=1.http://localhost:8000/paid-invoices/1/


10. Create invoice API.

Method:POST

API:http://localhost:8000/invoices/

input:

{
  "customer_name": "nayeem",
  "customer_phone": "0000980",
  "items": [
    {
      "product_name": "Product b",
      "quantity": 3,
      "amount": 50.00
    },
    {
      "product_name": "Product B",
      "quantity": 1,
      "amount": 30.00
    },
    {
      "product_name": "Product C",
      "quantity": 3,
      "amount": 20.00
    },
    {
      "product_name": "New Product D",
      "quantity": 1,
      "amount": 10.00
    }
  ]
}

output: 
N/A

Description: creates invoice.
