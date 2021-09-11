import json
import urllib
import uuid
from json.decoder import JSONDecodeError

import uvicorn
from fastapi import FastAPI, Request, status, Query
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse, Response
from pydantic import BaseModel

from src.payment import get_transaction_data


def create_response(data, additional_info=None):
    if additional_info:
        response = {"status": "failure"}
        response.update(additional_info)
        return response
    return {"status": "success"}


class CardRequestModel(BaseModel):
    """
    This is a Card request model.
    """
    number: str = Query("0000000000000000", max_length=16, min_length=16)
    expirationMonth: str = Query("00", max_length=2)
    expirationYear: str = Query("0000", max_length=4)
    cvv: str = Query("000", max_length=3)


tags_metadata = [
    {
        "name": "Initiate payment",
        "description": "These APIs will be used to initiate payment with debit or credit card.",
    }
]

app = FastAPI(
    title="Payment Gateway API Server",
    description="Payment Gateway server to accept payment requests.",
    openapi_tags=tags_metadata
)


@app.exception_handler(RequestValidationError)
def validation_exception_handler(request: Request, exc: RequestValidationError):
    """
    @param request:
    @param exc:
    @return:
    """
    err_resp = create_response(data=False, additional_info={
        "desc": "One or more args missing"})
    err_resp.update({"detail": exc.errors()})
    print(err_resp)
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content=jsonable_encoder(err_resp))


@app.middleware("http")
async def log_requests(request: Request, call_next):
    try:
        print("ip address: {}, request path: {}, parameters: {}"
              .format(request.client.host, request.url.path,
                      urllib.parse.unquote(request.url.query).replace("+", " ")))
        response = await call_next(request)
        body = b""
        async for chunk in response.body_iterator:
            body += chunk
        if request.url.path not in ['/docs', '/openapi.json']:
            try:
                print("ip address: {}, request path: {}, parameters: {}, response: \n{}"
                      .format(request.client.host, request.url.path,
                              urllib.parse.unquote(request.url.query).replace("+", " "),
                              json.dumps(json.loads(str(body.decode())), indent=4)))
            except JSONDecodeError:
                print("ip address: {}, request path: {}, parameters: {}, response: \n{}"
                      .format(request.client.host, request.url.path,
                              urllib.parse.unquote(request.url.query).replace("+", " "),
                              str(body.decode()), indent=4))
            except Exception:
                print("Exception in {} response : ".format(request.url.path))

        return Response(
            content=body,
            status_code=response.status_code,
            headers=dict(response.headers),
            media_type=response.media_type
        )
    except Exception:
        print("Exception in ")
    return None


@app.post("/payment_request", tags=["Initiate payment"])
def create_payment_request(amount: int, card: CardRequestModel,
                           currency: str = Query("USD", enum=("USD", "EUR", "BTC", "INR")),
                           type: str = Query("CreditCard", enum=("CreditCard", "DebitCard"))):
    txn_id = uuid.uuid1().hex  # just to generate a unique id
    transaction_data = get_transaction_data(amount=amount, 
                                            currency=currency, 
                                            txn_id=txn_id, 
                                            card=card, 
                                            type=type)
    return transaction_data


@app.get("/transactions")
def get_transaction_data():
    """
    This function is used to get the transaction data
    """
    pass


if __name__ == '__main__':
    uvicorn.run(app, host="0.0.0.0", port=5000)
