[![Build Status](https://runbot.odoo.com/runbot/badge/flat/1/master.svg)](https://runbot.odoo.com/runbot)
[![Tech Doc](https://img.shields.io/badge/master-docs-875A7B.svg?style=flat&colorA=8F8F8F)](https://www.odoo.com/documentation/master)
[![Help](https://img.shields.io/badge/master-help-875A7B.svg?style=flat&colorA=8F8F8F)](https://www.odoo.com/forum/help-1)
[![Nightly Builds](https://img.shields.io/badge/master-nightly-875A7B.svg?style=flat&colorA=8F8F8F)](https://nightly.odoo.com/)

# odoo_property_management

Module to manage Property AND Maintenance.


<h1>Problem Statement</h1>

One of the largest challenges in
maintaining operating as a landlord or property manager is balancing the various
dynamics that occur daily regarding new residents, requests for repairs, and
balancing payments and invoices. A professional system that integrates the
important information like lease obligations, resident details, work requests,
payments from tenants and to suppliers is a requirement in order to maintain the
property, operate efficiently, and ensure resident's satisfaction. Our company,
Pro-Manage Consulting, Inc. has designed a system that can help a property
manager maintain their community in a centralized system.

<h1>Organizational Description</h1>

<h3>Company Overview</h3>
Al Taaluq, Contracting And Maintenance :


<h3>Client Overview</h3>
In this example, the client, University Village Apartments, located on the campus
of the University of Texas at Dallas has installed the Pro-Manage Apartment
Management System. With this system, the property management team will be
able to insert new resident information, create leases for apartments, accept
payments for rent and track payments to suppliers.

<h3>Units</h3>
In this example, University Village has 25 units, ranging in size square footage size,
from 650 sqft. to 1090 sqft. and number of bedrooms and bathrooms, with
between 1 and 2 bedrooms, and 1 or 2 bathrooms, depending on the unit size.

<h3>Tenants</h3>
Although most apartment complexes would prefer to have a very high occupancy
rate, due to operating without a comprehensive management system, University
Village has suffered a significant move-out rate, resulting in only 20 residents
currently holding leases within the complex.

<h3>Claims</h3>
One of the advantages to tenants in an apartment is that they can call the
apartment's management office and place Claim requests with the staff of
the apartment complex to have repairs made. One of the most important
functions that this system performs is to allow the complex to track the status,
estimated times to complete and estimated and actual costs related the
requested task.

<h3>Suppliers</h3>
In order to resolve the Claim that might be placed with the apartment staff,
the complex must have specific suppliers in order to provide the needed
replacement items that meet their needs, either in quality, style, or cost, such as
light bulbs or patches of carpet.



### Explanation:

- **GitHub Actions Workflow**:
- The workflow triggers on a `push` event.
- It checks out the code and sets up a Python environment.
- It runs the `comment_lines.py` script to process the files.
- It commits and pushes the changes back to the repository.

- **Python Script**:
- The script walks through the repository directory.
- It checks each `.py` file and comments out lines containing 
- `#should not be in production`.

By following these steps, you can automate the process of commenting
out specific lines during a push to GitHub. If you need further 
assistance or have any questions, feel free to ask! 😊
