from sqlalchemy import create_engine, Column, Integer, String, Date, ForeignKey, Float
from sqlalchemy.orm import sessionmaker, declarative_base
from faker import Faker
import random

# Define Snowflake schema structure
Base = declarative_base()

class DimCustomers(Base):
    __tablename__ = 'dim_customers'
    __table_args__ = {'schema': 'dw_schema'}  # Specify the schema
    customer_id = Column(Integer, primary_key=True)
    customer_name = Column(String)

class DimProducts(Base):
    __tablename__ = 'dim_products'
    __table_args__ = {'schema': 'dw_schema'}  # Specify the schema
    product_id = Column(Integer, primary_key=True)
    product_name = Column(String)

class DimTime(Base):
    __tablename__ = 'dim_time'
    __table_args__ = {'schema': 'dw_schema'}  # Specify the schema
    time_id = Column(Integer, primary_key=True)
    sale_date = Column(Date)

class DimLocation(Base):
    __tablename__ = 'dim_location'
    __table_args__ = {'schema': 'dw_schema'}  # Specify the schema
    location_id = Column(Integer, primary_key=True)
    location_name = Column(String)

class FactSales(Base):
    __tablename__ = 'fact_sales'
    __table_args__ = {'schema': 'dw_schema'}  # Specify the schema
    sale_id = Column(Integer, primary_key=True)
    customer_id = Column(Integer, ForeignKey('dw_schema.dim_customers.customer_id'))
    product_id = Column(Integer, ForeignKey('dw_schema.dim_products.product_id'))
    time_id = Column(Integer, ForeignKey('dw_schema.dim_time.time_id'))
    location_id = Column(Integer, ForeignKey('dw_schema.dim_location.location_id'))
    quantity_sold = Column(Integer)
    total_amount = Column(Float)  # New column for total amount

# Function to generate random data
def generate_random_data(session, num_rows):
    fake = Faker()
    
    # Generate customers
    customers = [DimCustomers(customer_name=fake.name()) for _ in range(num_rows)]
    session.bulk_save_objects(customers)
    session.commit()

    # Generate products
    products = [DimProducts(product_name=fake.word()) for _ in range(num_rows)]
    session.bulk_save_objects(products)
    session.commit()

    # Generate time dimension
    time_dimension = [DimTime(sale_date=fake.date_between(start_date='-365d', end_date='today')) for _ in range(num_rows)]
    session.bulk_save_objects(time_dimension)
    session.commit()

    # Generate location dimension
    locations = [DimLocation(location_name=fake.city()) for _ in range(num_rows)]
    session.bulk_save_objects(locations)
    session.commit()

    # Retrieve dimensions from the database
    saved_customers = session.query(DimCustomers).all()
    saved_products = session.query(DimProducts).all()
    saved_time_dimension = session.query(DimTime).all()
    saved_locations = session.query(DimLocation).all()

    # Generate sales using retrieved dimensions
    sales = [
        FactSales(
            customer_id=random.choice(saved_customers).customer_id,
            product_id=random.choice(saved_products).product_id,
            time_id=random.choice(saved_time_dimension).time_id,
            location_id=random.choice(saved_locations).location_id,
            quantity_sold=random.randint(1, 100),
            total_amount=random.uniform(10, 1000),  # Adjust as per your scenario
        ) for _ in range(num_rows)
    ]
    session.bulk_save_objects(sales)
    session.commit()

if __name__ == '__main__':
    # Set up database connection
    engine = create_engine('postgresql+psycopg2://admin:admin@127.0.0.1:5432/dw')
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()

    # Generate random data (e.g., 100 rows)
    generate_random_data(session, num_rows=100000)
