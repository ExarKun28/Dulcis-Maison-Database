from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import declarative_base, relationship
from datetime import datetime

Base = declarative_base()

class Barangay(Base):
    __tablename__ = 'barangay'
    
    barangay_id = Column(Integer, primary_key=True, autoincrement=True)
    barangay_name = Column(String(100))
    streets = relationship("Street", back_populates="barangay")

class Street(Base):
    __tablename__ = 'street'
    
    street_id = Column(Integer, primary_key=True, autoincrement=True)
    barangay_id = Column(Integer, ForeignKey('barangay.barangay_id'))
    street_name = Column(String(100))
    barangay = relationship("Barangay", back_populates="streets")
    addresses = relationship("Address", back_populates="street")

class Address(Base):
    __tablename__ = 'address'
    
    address_id = Column(Integer, primary_key=True, autoincrement=True)
    description = Column(String(200))
    street_id = Column(Integer, ForeignKey('street.street_id'))
    street = relationship("Street", back_populates="addresses")
    customers = relationship("Customer", back_populates="address")
    employees = relationship("Employee", back_populates="address")

class Customer(Base):
    __tablename__ = 'customer'
    
    customer_id = Column(Integer, primary_key=True, autoincrement=True)
    customer_name = Column(String(100))
    address_id = Column(Integer, ForeignKey('address.address_id'))
    address = relationship("Address", back_populates="customers")
    orders = relationship("Order", back_populates="customer")
    phone_numbers = relationship("CustomerNum", back_populates="customer")

class CustomerNum(Base):
    __tablename__ = 'customer_num'
    
    customer_num_code = Column(Integer, primary_key=True, autoincrement=True)
    contact = Column(String(20))
    customer_id = Column(Integer, ForeignKey('customer.customer_id'))
    customer = relationship("Customer", back_populates="phone_numbers")


class Employee(Base):
    __tablename__ = 'employee'
    
    employee_id = Column(Integer, primary_key=True, autoincrement=True)
    employee_name = Column(String(100))
    employee_age = Column(Integer)
    civil_status = Column(String(20))
    address_id = Column(Integer, ForeignKey('address.address_id'))
    address = relationship("Address", back_populates="employees")
    phone_numbers = relationship("EmployeeNum", back_populates="employee")
    orders = relationship("Order", back_populates="employee")
    deliveries = relationship("Delivery", back_populates="employee")
    supplies = relationship("Supply", back_populates="employee")

class EmployeeNum(Base):
    __tablename__ = 'employee_num'
    
    employee_num_code = Column(Integer, primary_key=True, autoincrement=True)
    contact_num = Column(String(20))
    employee_id = Column(Integer, ForeignKey('employee.employee_id'))
    employee = relationship("Employee", back_populates="phone_numbers")

class Order(Base):
    __tablename__ = 'order'
    
    order_id = Column(Integer, primary_key=True, autoincrement=True)
    date = Column(DateTime, default=datetime.utcnow)
    customer_id = Column(Integer, ForeignKey('customer.customer_id'))
    employee_id = Column(Integer, ForeignKey('employee.employee_id'))
    total = Column(Float)
    customer = relationship("Customer", back_populates="orders")
    employee = relationship("Employee", back_populates="orders")
    order_details = relationship("OrderDetails", back_populates="order")
    deliveries = relationship("Delivery", back_populates="order")
    packagings = relationship("Packaging", back_populates="order")

class Menu(Base):
    __tablename__ = 'menu'
    
    menu_id = Column(Integer, primary_key=True, autoincrement=True)
    menu_name = Column(String(100))
    category = Column(String(50))
    menu_details = relationship("MenuDetails", back_populates="menu")
    order_details = relationship("OrderDetails", back_populates="menu")

class MenuDetails(Base):
    __tablename__ = 'menu_details'
    
    menu_details_id = Column(Integer, primary_key=True, autoincrement=True)
    date = Column(DateTime, default=datetime.utcnow)
    menu_id = Column(Integer, ForeignKey('menu.menu_id'))
    number_of_serving = Column(Integer)
    price = Column(Float)
    menu = relationship("Menu", back_populates="menu_details")

class OrderDetails(Base):
    __tablename__ = 'order_details'
    
    order_id = Column(Integer, ForeignKey('order.order_id'), primary_key=True)
    menu_id = Column(Integer, ForeignKey('menu.menu_id'), primary_key=True)
    quantity = Column(Integer)
    price = Column(Float)
    subtotal = Column(Float)
    order = relationship("Order", back_populates="order_details")
    menu = relationship("Menu", back_populates="order_details")

class Delivery(Base):
    __tablename__ = 'delivery'
    
    delivery_id = Column(Integer, primary_key=True, autoincrement=True)
    employee_id = Column(Integer, ForeignKey('employee.employee_id'))
    order_id = Column(Integer, ForeignKey('order.order_id'))
    date = Column(DateTime, default=datetime.utcnow)
    departure = Column(DateTime)
    arrival = Column(DateTime)
    fee = Column(Float)
    employee = relationship("Employee", back_populates="deliveries")
    order = relationship("Order", back_populates="deliveries")

class Packaging(Base):
    __tablename__ = 'packaging'
    
    packaging_id = Column(Integer, primary_key=True, autoincrement=True)
    order_id = Column(Integer, ForeignKey('order.order_id'))
    quantity = Column(Integer)
    type = Column(String(50))
    size = Column(String(20))
    price = Column(Float)
    order = relationship("Order", back_populates="packagings")

class Supplier(Base):
    __tablename__ = 'supplier'
    
    supplier_id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100))
    contact = Column(String(20))
    address_id = Column(Integer, ForeignKey('address.address_id'))
    supplies = relationship("Supply", back_populates="supplier")

class Supply(Base):
    __tablename__ = 'supply'
    
    supply_id = Column(Integer, primary_key=True, autoincrement=True)
    date = Column(DateTime, default=datetime.utcnow)
    employee_id = Column(Integer, ForeignKey('employee.employee_id'))
    supplier_id = Column(Integer, ForeignKey('supplier.supplier_id'))
    employee = relationship("Employee", back_populates="supplies")
    supplier = relationship("Supplier", back_populates="supplies")
    supply_details = relationship("SupplyDetails", back_populates="supply")

class Ingredients(Base):
    __tablename__ = 'ingredients'
    
    ingredients_id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100))
    unit = Column(String(20))
    current = Column(Float)
    critical_level = Column(Float)
    supply_details = relationship("SupplyDetails", back_populates="ingredient")

class SupplyDetails(Base):
    __tablename__ = 'supply_details'
    
    supply_id = Column(Integer, ForeignKey('supply.supply_id'), primary_key=True)
    ingredients_id = Column(Integer, ForeignKey('ingredients.ingredients_id'), primary_key=True)
    quantity = Column(Float)
    price = Column(Float)
    expiration_date = Column(DateTime)
    supply = relationship("Supply", back_populates="supply_details")
    ingredient = relationship("Ingredients", back_populates="supply_details")

def create_database():
    # For MySQL connection through XAMPP
    engine = create_engine('mysql+pymysql://root:@localhost/dulcis_maison')
    
    
    Base.metadata.create_all(engine)
    print("Database and tables created successfully!")

if __name__ == "__main__":
    create_database()
