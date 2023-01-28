from fastapi import FastAPI, HTTPException
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from pydantic import BaseModel


class CreateProductModel(BaseModel):
    model: str
    name: str
    info: str


class Product:
    def __init__(self, id: int, model: str, name: str, info: str):
        self.id = id
        self.model = model
        self.name = name
        self.info = info


ProductList: list[Product] = [
    # Product(0, 'Бытавая техника', 'Электрическая плита', 'поверхность - эмалированная сталь, конфорок - 2 шт'),
    # Product(1, 'Компьютерная техника', 'Ноутбук Acer', 'Full HD (1920x1080), IPS, Intel Core i5-11400H'),
    # Product(2, 'Смартфоны', 'Xioami', 'ядер - 4x(2 ГГц), 2 Гб, 2 SIM, IPS, 1600x720'),

]


def add_products(content: CreateProductModel):
    id = len(ProductList)
    ProductList.append(Product(id, content.model, content.name, content.info))
    return id


app = FastAPI()

##########
# Jaeger

from opentelemetry import trace
from opentelemetry.exporter.jaeger.thrift import JaegerExporter
from opentelemetry.sdk.resources import SERVICE_NAME, Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor

resource = Resource(attributes={
    SERVICE_NAME: "product-service"
})

jaeger_exporter = JaegerExporter(
    agent_host_name="jaeger",
    agent_port=6831,
)

provider = TracerProvider(resource=resource)
processor = BatchSpanProcessor(jaeger_exporter)
provider.add_span_processor(processor)
trace.set_tracer_provider(provider)

FastAPIInstrumentor.instrument_app(app)


#
##########

##########
# Prometheus

from prometheus_fastapi_instrumentator import Instrumentator


@app.on_event("startup")
async def startup():
    Instrumentator().instrument(app).expose(app)

#
##########


@app.get("/v1/product")
async def get_product():
    return ProductList


@app.post("/v1/product")
async def add_product(content: CreateProductModel):
    add_products(content)
    return ProductList[-1]


@app.get("/v1/product/{id}")
async def get_product_by_id(id: int):
    result = [item for item in ProductList if item.id == id]
    if len(result) > 0:
        return result[0]
    else:
        raise HTTPException(status_code=404, detail="Product not found")


@app.get("/__health")
async def check_product():
    return
