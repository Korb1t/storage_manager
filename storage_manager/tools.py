
from .models import *

villa_services_names = ['revenue',
                        'rent',
                        'slaries',
                        'commissions_to_agents',
                        'tax',
                        'commissions_to_VG',
                        'commissions_to_partner',
                        'electricity_bill',
                        'storeroom',
                        'repairs',
                        'petrol_DG',
                        'ac_repairs',
                        'TV',
                        'laundry',
                        'bfast_food',
                        'transfres',
                        'others'
                        ]
preaty_services_names = ["Revenue",
                         "Rent",
                         "Salaries",
                         "Commissions to agent",
                         "Tax",
                         "Commissions to VG",
                         "Commissions to partner",
                         "Electricity bill",
                         "Storeroom",
                         "Repairs",
                         "Petrol_DG",
                         "AC Repairs",
                         "TV",
                         "Laundry",
                         "Fast food",
                         "Transfers",
                         "Others"
                         ]


class ServiceDetail:
    def __init__(self, service_name, preaty_service_name, villa):
        self.service_name = service_name
        self.preaty_service_name = preaty_service_name
        self.service_details = Service.objects.filter(storage=villa, type=service_name)